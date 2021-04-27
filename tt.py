import requests
from lxml import etree

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

url = "https://trademarks.ipo.gov.uk/ipo-tmtext"
resp = sess.get(url, headers=headers).text
# print(resp.text)
respHtml = etree.HTML(resp)
csrf_token = respHtml.xpath("//input[@name='csrfToken']/@value")[0]
print(csrf_token)

post_data = {
    "csrfToken": csrf_token,
    "sectionIndex": "0",
    "searchType": "WORD",
    "wordSearchType": "SIMILAR",
    "wordSearchPhrase": "GROHE",
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
resp = sess.post(post_url, data=post_data)
print(resp.status_code)
print(resp.url)
print(resp.text)
print('-'*100)
# resp2 = sess.get("https://trademarks.ipo.gov.uk/ipo-tmtext/page/Results")
# print(resp2.text)

