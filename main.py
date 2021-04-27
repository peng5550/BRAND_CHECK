import requests
from lxml import etree
import re
import pymysql


class BrandCheck:

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="mydata",
                                    charset="utf8")
        self.db = self.conn.cursor()

    def insert_data(self, item_info, table_name="brand_check"):
        keys = ', '.join(list(item_info.keys()))
        values = ', '.join(['%s'] * len(item_info))
        insert_sql = "insert into `{}`({})values({});".format(table_name, keys, values)
        try:
            self.db.execute(insert_sql, tuple(item_info.values()))
            self.conn.commit()
        except Exception as e:
            print(e.args)
            self.conn.rollback()

    def create_session(self):
        sess = requests.session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "trademarks.ipo.gov.uk",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        sess.headers = headers
        return sess

    def get_csrf_token(self, sess):
        url = "https://trademarks.ipo.gov.uk/ipo-tmtext"
        resp = sess.get(url, timeout=180).text
        respHtml = etree.HTML(resp)
        csrf_token = respHtml.xpath("//input[@name='csrfToken']/@value")[0]
        return csrf_token

    def check_brand(self, sess, brand, csrf_token):
        post_data = {
            "csrfToken": csrf_token,
            "sectionIndex": "0",
            "searchType": "WORD",
            "wordSearchType": "SIMILAR",
            "wordSearchPhrase": brand,
            "wordSearchMatchType": "ALLWORDS",
            "ViennaClassesCategoriesDropDownOne": "",
            "ViennaClassesDivisionsDropDownOne": "",
            "ViennaClassesSectionsDropDownOne": "",
            "firstOperator": "NO",
            "ViennaClassesCategoriesDropDownTwo": "",
            "ViennaClassesDivisionsDropDownTwo": "",
            "ViennaClassesSectionsDropDownTwo": "",
            "secondOperator": "NO",
            "ViennaClassesCategoriesDropDownThree": "",
            "ViennaClassesDivisionsDropDownThree": "",
            "ViennaClassesSectionsDropDownThree": "",
            "filedFrom.month": "1",
            "filedFrom.day": "1",
            "filedFrom": "1876",
            "filedTo.day": "27",
            "filedTo.month": "4",
            "filedTo": "2021",
            "legalStatus": "ALLLEGALSTATUSES",
            "pageSize": "10",
        }
        post_url = "https://trademarks.ipo.gov.uk/ipo-tmtext"
        post_headers = {
            "Host": "trademarks.ipo.gov.uk",
            "Connection": "keep-alive",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://trademarks.ipo.gov.uk",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://trademarks.ipo.gov.uk/ipo-tmtext",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        sess.headers = post_headers
        resp = sess.post(post_url, data=post_data, timeout=180)
        if resp.status_code == 200:
            respHtml = etree.HTML(resp.text)
            result = respHtml.xpath("//p[@class='bold-medium']/a/@id")
            resultStr = "".join(result)
            if re.findall(r"uk", resultStr, re.I):
                item = {"brand": brand, "result": "有"}
            else:
                item = {"brand": brand, "result": "无"}

            self.insert_data(item)
        else:
            item = {"brand": brand, "result": f"请求失败:状态码为{resp.status_code}"}
            self.insert_data(item)
        print(f"【{item}】,存储成功")

    def start(self):
        brandStr = '''
Log-Barn
Method
lofuanna
Lifewit
Ikea
Craft Planet
Bloo
sodastream
NUTRiBULLET
Johnstone's
Finish
De'Longhi
Pangton Villa
Bosch Home and Garden
Blue Spot Tools
Vileda
Nutley's
Plasti-Kote
Culinare
Adoric
Stardrops
Munchkin
Clearwater
Eco Bag
Zoflora
Utopia Home
Spares2go
HG
DYLON
KEPLIN
ANSIO
EK Supplies
Zero In
Bakery Direct Ltd
Toastabags
Luigi's
Krcher
Jumkeet
Breville
Mr Muscle
Roundup
Febreze
Bemis
Plantworks Ltd
BEEWAY
WOTEK
Hario
IKEA..
Home Care
Meowoo
'''
        for brand in brandStr.split("\n"):
            brand = brand.strip()
            if brand:
                try:
                    sess = self.create_session()
                    csrf_token = self.get_csrf_token(sess)
                    self.check_brand(sess, brand, csrf_token)
                except Exception as e:
                    item = {"brand": brand, "result": f"请求失败：{e}"}
                    self.insert_data(item)
                    print(f"【{item}】,存储成功")

if __name__ == '__main__':
    app = BrandCheck()
    app.start()

