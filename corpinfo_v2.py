# Created by Ziji Zhang
# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import pymongo
import uuid
import time

myClient = pymongo.MongoClient('mongodb://localhost:27017')
myDB = myClient['河北高速公路阳光工程企业信息']
myCol = myDB['企业信息']
myCol.delete_many({})     # 清空数据库

tmpDict = {}    # 用来储存每一家公司的信息

sourceURL = 'http://120.211.63.97:8213/forUI/corpInfo/showCorpList.aspx'
BaseInfoPrefix = 'http://120.211.63.97:8213/forUI/corpInfo/CorpBaseInfo.aspx?CorpCode='
AptitudeInfoPrefix = 'http://120.211.63.97:8213/forUI/corpInfo/CorpAptitudeInfo.aspx?CorpCode='
sourcePageHTML = requests.get(sourceURL)
sourcePageEtree = etree.HTML(sourcePageHTML.text)
totalPage = sourcePageEtree.xpath('//*[@id="SqlPager1"]/font[2]')
companyCode = sourcePageEtree.xpath('//*[@id="datagrid"]/tr/td[2]')
nextPageRes = sourcePageHTML

index = 0
lastIndex = int(totalPage[0].text) + 1
for index in range(1, lastIndex):
    if index == 1:  # 第一页
        print('当前页码为：1')
        for i in range(0, len(companyCode)):
            if i != 0:
                companyCodeFinal = companyCode[i].text.strip()  # get rid of the space and newline

                # 企业基本信息页面抓取
                BaseInfoURL = BaseInfoPrefix + companyCodeFinal    # get URL of every company
                targetPageHTML = requests.get(BaseInfoURL)
                targetPageEtree = etree.HTML(targetPageHTML.text)
                companyCode1 = targetPageEtree.xpath('//*[@id="LblCorporationCode"]')
                companyName = targetPageEtree.xpath('//*[@id="LblCorporationName"]')
                regProvince = targetPageEtree.xpath('//*[@id="LblRegProvince"]')
                regCity = targetPageEtree.xpath('//*[@id="LblRegCity"]')
                regAddress = targetPageEtree.xpath('//*[@id="LblRegAddress"]')
                regZipCode = targetPageEtree.xpath('//*[@id="LblRegCityPost"]')
                companyKind = targetPageEtree.xpath('//*[@id="LblCorporationKind"]')
                companyType = targetPageEtree.xpath('//*[@id="LblCorporationType"]')
                bizLicense = targetPageEtree.xpath('//*[@id="LblBusinessLicence"]')
                regTime = targetPageEtree.xpath('//*[@id="LblRegTime"]')
                regFund = targetPageEtree.xpath('//*[@id="LblRegFund"]')
                buildOnTime = targetPageEtree.xpath('//*[@id="LblBuildOnTime"]')
                issueDepart = targetPageEtree.xpath('//*[@id="txtIssueDepartment"]')
                bizRange = targetPageEtree.xpath('//*[@id="LblBusinessRange"]')
                companyResume = targetPageEtree.xpath('//*[@id="LblCorpResume"]')
                remark = targetPageEtree.xpath('//*[@id="txtRemark"]')

                # 资质信息页面抓取
                AptitudeInfoURL = AptitudeInfoPrefix + companyCodeFinal
                targetPageHTML = requests.get(AptitudeInfoURL)
                targetPageEtree = etree.HTML(targetPageHTML.text)
                CACode = targetPageEtree.xpath('//*[@id="txtCACode"]')
                approvalCode = targetPageEtree.xpath('//*[@id="txtSealCode"]')
                issueDepartment = targetPageEtree.xpath('//*[@id="txtIssueDepartment"]')
                assessTime = targetPageEtree.xpath('//*[@id="txtAssessTime"]')
                carryRange = targetPageEtree.xpath('//*[@id="txtCarryRange"]')

                # 打印以上所有信息
                # print('组织机构代码：', companyCode1[0].text)
                # print('企业名称：', companyName[0].text)
                # print('注册省份：', regProvince[0].text)
                # print('注册城市：', regCity[0].text)
                # print('注册地址：', regAddress[0].text)
                # print('注册城市邮编：', regZipCode[0].text)
                # print('企业性质：', companyKind[0].text)
                # print('企业类型：', companyType[0].text)
                # print('营业执照注册号：', bizLicense[0].text)
                # print('营业执照注册时间：', regTime[0].text)
                # print('注册资金（万元）：', regFund[0].text)
                # print('成立时间：', buildOnTime[0].text)
                # print('发照机关：', issueDepart[0].text)
                # print('经营范围：', bizRange[0].text)
                # print('资产构成情况及投资参股的关联企业情况：', companyResume[0].text)
                # print('备注：', remark[0].text)
                # print('资质证书编号：', CACode[0].text)
                # print('批准文号：', approvalCode[0].text)
                # print('发证机关：', issueDepartment[0].text)
                # print('发证日期：', assessTime[0].text)
                # print('业务承接范围：', carryRange[0].text)

                # 将信息存入字典，以备输入数据库
                tmpDict['_id'] = uuid.uuid4()
                tmpDict['组织机构代码'] = companyCode1[0].text
                tmpDict['企业名称'] = companyName[0].text
                tmpDict['注册省份'] = regProvince[0].text
                tmpDict['注册城市'] = regCity[0].text
                tmpDict['注册地址'] = regAddress[0].text
                tmpDict['注册城市邮编'] = regZipCode[0].text
                tmpDict['企业性质'] = companyKind[0].text
                tmpDict['企业类型'] = companyType[0].text
                tmpDict['营业执照注册号'] = bizLicense[0].text
                tmpDict['营业执照注册时间'] = regTime[0].text
                tmpDict['注册资金（万元）'] = regFund[0].text
                tmpDict['成立时间'] = buildOnTime[0].text
                tmpDict['发照机关'] = issueDepart[0].text
                tmpDict['经营范围'] = bizRange[0].text
                tmpDict['资产构成情况及投资参股的关联企业情况'] = companyResume[0].text
                tmpDict['备注'] = remark[0].text
                tmpDict['资质证书编号'] = CACode[0].text
                tmpDict['批准文号'] = approvalCode[0].text
                tmpDict['发证机关'] = issueDepartment[0].text
                tmpDict['发证日期'] = assessTime[0].text
                tmpDict['业务承接范围'] = carryRange[0].text

                myCol.insert_one(tmpDict)
                ii = 0
                for z in myCol.find({}, {'_id': 0}):
                    ii = ii + 1
                    print(z)
                print('当前共有', ii, '条数据。')
                print()
    else:   # 不是第一页
        nextPageEtree = etree.HTML(nextPageRes.text)
        currentPage = nextPageEtree.xpath('//*[@id="SqlPager1"]/font[1]')
        print('******************************************')
        print('******************************************')
        print("************ 当前页码为：", int(currentPage[0].text)+1, ' *************')
        print('******************************************')
        print('******************************************')
        viewState = nextPageEtree.xpath('//*[@id="__VIEWSTATE"]//@value')
        randomData = nextPageEtree.xpath('//*[@id="Login1_RandomData"]//@value')
        # sqlPager = nextPageEtree.xpath('//*[@id="SqlPager1_ToPage"]/option[' + currentPage[0].text + ']')
        requestHeader = {
            'Host': '120.211.63.97:8213',
            'Connection': 'keep-alive',
            'Content-Length': '3990',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://120.211.63.97:8213',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'http://120.211.63.97:8213/forUI/corpInfo/showCorpList.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        formData = {
            '__EVENTTARGET': 'SqlPager1$NextPage',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewState[0],
            'Login1$txtUserName': '',
            'Login1$txtPassword': '',
            'Login1$Digest': '',
            'Login1$UserID': '',
            'Login1$epassSN': '',
            'Login1$RandomData': randomData[0],
            'txtCorpCode': '',
            'txtCorpName': '',
            'ddlCorpType': '',
            'SqlPager1$ToPag': currentPage[0].text,
        }
        nextPageRes = requests.post(sourceURL, formData, requestHeader)
        nextPageEtree = etree.HTML(nextPageRes.text)
        companyCode = nextPageEtree.xpath('//*[@id="datagrid"]/tr/td[2]')
        for i in range(0, len(companyCode)):
            if i != 0:
                companyCodeFinal = companyCode[i].text.strip()  # get rid of the space and newline

                # 企业基本信息页面抓取
                BaseInfoURL = BaseInfoPrefix + companyCodeFinal    # get URL of every company
                targetPageHTML = requests.get(BaseInfoURL)
                targetPageEtree = etree.HTML(targetPageHTML.text)
                companyCode1 = targetPageEtree.xpath('//*[@id="LblCorporationCode"]')
                companyName = targetPageEtree.xpath('//*[@id="LblCorporationName"]')
                regProvince = targetPageEtree.xpath('//*[@id="LblRegProvince"]')
                regCity = targetPageEtree.xpath('//*[@id="LblRegCity"]')
                regAddress = targetPageEtree.xpath('//*[@id="LblRegAddress"]')
                regZipCode = targetPageEtree.xpath('//*[@id="LblRegCityPost"]')
                companyKind = targetPageEtree.xpath('//*[@id="LblCorporationKind"]')
                companyType = targetPageEtree.xpath('//*[@id="LblCorporationType"]')
                bizLicense = targetPageEtree.xpath('//*[@id="LblBusinessLicence"]')
                regTime = targetPageEtree.xpath('//*[@id="LblRegTime"]')
                regFund = targetPageEtree.xpath('//*[@id="LblRegFund"]')
                buildOnTime = targetPageEtree.xpath('//*[@id="LblBuildOnTime"]')
                issueDepart = targetPageEtree.xpath('//*[@id="txtIssueDepartment"]')
                bizRange = targetPageEtree.xpath('//*[@id="LblBusinessRange"]')
                companyResume = targetPageEtree.xpath('//*[@id="LblCorpResume"]')
                remark = targetPageEtree.xpath('//*[@id="txtRemark"]')

                # 资质信息页面抓取
                AptitudeInfoURL = AptitudeInfoPrefix + companyCodeFinal
                targetPageHTML = requests.get(AptitudeInfoURL)
                targetPageEtree = etree.HTML(targetPageHTML.text)
                CACode = targetPageEtree.xpath('//*[@id="txtCACode"]')
                approvalCode = targetPageEtree.xpath('//*[@id="txtSealCode"]')
                issueDepartment = targetPageEtree.xpath('//*[@id="txtIssueDepartment"]')
                assessTime = targetPageEtree.xpath('//*[@id="txtAssessTime"]')
                carryRange = targetPageEtree.xpath('//*[@id="txtCarryRange"]')

                # 打印以上所有信息
                # print('组织机构代码：', companyCode1[0].text)
                # print('企业名称：', companyName[0].text)
                # print('注册省份：', regProvince[0].text)
                # print('注册城市：', regCity[0].text)
                # print('注册地址：', regAddress[0].text)
                # print('注册城市邮编：', regZipCode[0].text)
                # print('企业性质：', companyKind[0].text)
                # print('企业类型：', companyType[0].text)
                # print('营业执照注册号：', bizLicense[0].text)
                # print('营业执照注册时间：', regTime[0].text)
                # print('注册资金（万元）：', regFund[0].text)
                # print('成立时间：', buildOnTime[0].text)
                # print('发照机关：', issueDepart[0].text)
                # print('经营范围：', bizRange[0].text)
                # print('资产构成情况及投资参股的关联企业情况：', companyResume[0].text)
                # print('备注：', remark[0].text)
                # print('资质证书编号：', CACode[0].text)
                # print('批准文号：', approvalCode[0].text)
                # print('发证机关：', issueDepartment[0].text)
                # print('发证日期：', assessTime[0].text)
                # print('业务承接范围：', carryRange[0].text)

                # 将信息存入字典，以备输入数据库
                tmpDict['_id'] = uuid.uuid4()
                tmpDict['组织机构代码'] = companyCode1[0].text
                tmpDict['企业名称'] = companyName[0].text
                tmpDict['注册省份'] = regProvince[0].text
                tmpDict['注册城市'] = regCity[0].text
                tmpDict['注册地址'] = regAddress[0].text
                tmpDict['注册城市邮编'] = regZipCode[0].text
                tmpDict['企业性质'] = companyKind[0].text
                tmpDict['企业类型'] = companyType[0].text
                tmpDict['营业执照注册号'] = bizLicense[0].text
                tmpDict['营业执照注册时间'] = regTime[0].text
                tmpDict['注册资金（万元）'] = regFund[0].text
                tmpDict['成立时间'] = buildOnTime[0].text
                tmpDict['发照机关'] = issueDepart[0].text
                tmpDict['经营范围'] = bizRange[0].text
                tmpDict['资产构成情况及投资参股的关联企业情况'] = companyResume[0].text
                tmpDict['备注'] = remark[0].text
                tmpDict['资质证书编号'] = CACode[0].text
                tmpDict['批准文号'] = approvalCode[0].text
                tmpDict['发证机关'] = issueDepartment[0].text
                tmpDict['发证日期'] = assessTime[0].text
                tmpDict['业务承接范围'] = carryRange[0].text

                myCol.insert_one(tmpDict)
                for z in myCol.find({}, {'_id': 0}):
                    print(z)

                print()
