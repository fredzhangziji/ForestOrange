# Created by Ziji Zhang

import requests
from lxml import etree

post_url = 'http://120.211.63.97:8213/forUI/Credit/showCreditList.aspx' # get the url

for x in range(0, 3):
    if x == 0:
        response1 = requests.get(post_url)  # get method to scrape the whole html
        web_data = response1.text
        html = etree.HTML(web_data)
        html_data = html.xpath('//*[@id="datagrid"]/tr/td')  # xpath to locate the position
        for i in html_data:
            print(i.text)
        print('x is: ', x)

    else:
        post_headers = {
            'Host': '120.211.63.97:8213',
            'Connection': 'keep-alive',
            'Content-Length': '1168',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://120.211.63.97:8213',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://120.211.63.97:8213/forUI/Credit/showCreditList.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6'
        }
        viewState = html.xpath('//*[@id="__VIEWSTATE"]/@value')
        currentPage = html.xpath('//*[@id="SqlPager1_ToPage"]/option/@value')
        loginRandomData = html.xpath('//*[@id="Login1_RandomData"]/@value')
        ddlPeriod = html.xpath('//*[@id="ddlPeriod"]/option[1]/@value')
        ddlCorpType = html.xpath('//*[@id="ddlCorpType"]/option[1]/@value')
        post_data = {
            '__EVENTTARGET': 'SqlPager1$NextPage',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewState[0],  # fix me
            'Login1$txtUserName': '',
            'Login1$txtPassword': '',
            'Login1$Digest': '',
            'Login1$UserID': '',
            'Login1$epassSN': '',
            'Login1$RandomData': loginRandomData[0],
            'ddlCorpType': ddlCorpType[0],
            'ddlPeriod': ddlPeriod[0],
            'ddlGrade': '',
            'txtCorpCode': '',
            'txtCorpName': '',
            'SqlPager1$ToPage': currentPage[x-1],  # fix me
        }
        response_nextPage = requests.post(url=post_url, data=post_data, headers=post_headers)
        html = etree.HTML(response_nextPage.text)
        # result2 = etree.tostring(html)
        html_data = html.xpath('//*[@id="datagrid"]/tr/td')
        for j in html_data:
            print(j.text)
        print('x is: ', x)
