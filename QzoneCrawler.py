# -*- coding: utf-8 -*-

#  author   :    chenweiyu
#  time     :    2018.08.01
#  version  :    1.0
#  e-mail   :    weiyuchens@sina.com

from selenium import webdriver
import time
import re
import requests
import json


# 获取g_tk的计算方法
def getGTK(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff


# 获取g_tk的值
def getGTKValue(driver):
    cookies = {}
    for elem in driver.get_cookies():
        cookies[elem['name']] = elem['value']
    g_tk = getGTK(cookies)
    return g_tk


# 获得qzonetoken的值
def getQzoneToken(driver):
    driver.switch_to_default_content()
    page = driver.page_source
    g_qzonetoken = re.search('window\.g_qzonetoken = \(function\(\){ try\{return (.*?);\} catch\(e\)', page).group()
    qzonetoken = g_qzonetoken.split('"')[1]
    return qzonetoken


# 获得param的值
def getParam(qq_count):
    param = '3_' + qq_count + '_0|8_8_' + qq_count + '_1_1_0_1_1|16'
    return param


# 获得最后需要的requestURL
def getReqURL(qq_count, param, g_tk, qzonetoken):
    reqUrl = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/main_page_cgi?uin=' + str(
        qq_count) + '&param=' + str(param) + '&g_tk=' + str(g_tk) + '&qzonetoken=' + qzonetoken + '&g_tk=' + str(g_tk)
    return reqUrl


def main():
    # QQ账号和密码
    qq_count = ''
    qq_pw = ''

    # 模拟登陆
    driver = webdriver.Firefox()
    driver.set_window_position(20, 40)
    driver.set_window_size(1100, 700)

    driver.get('https://qzone.qq.com')

    driver.switch_to_frame('login_frame')

    driver.find_element_by_id('switcher_plogin').click()
    time.sleep(1)
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(qq_count)
    time.sleep(2)
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(qq_pw)
    time.sleep(2)
    driver.find_element_by_id('login_button').click()

    uin = qq_count
    print('uin:' + uin)

    g_tk = getGTKValue(driver)
    print('g_tk:' + str(g_tk))

    qzonetoken = getQzoneToken(driver)
    print('qzonetoken:' + qzonetoken)

    param = getParam(qq_count)
    print('param:' + param)

    reqURL = getReqURL(qq_count, param, g_tk, qzonetoken)
    print(reqURL)

    cookie = ""

    for elem in driver.get_cookies():
        cookie += elem["name"] + "=" + elem["value"] + ";"

    print(cookie)

    headers = {'host': 'user.qzone.qq.com',
               'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9',
               'referer': 'https://user.qzone.qq.com/726344827/main',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    headers['cookie'] = cookie

    print(headers)

    page = requests.session().get(reqURL, headers=headers)

    pagedata = page.text.encode('utf-8')
    # print(pagedata)

    pagestr1 = pagedata[10:]
    pagestr = pagestr1[0:-2]

    pagejson = json.loads(pagestr)

    list = pagejson["data"]["module_3"]["data"]["items"]

    dataList = []

    print("爬下来的数据：")

    for i in list:
        print("qq:" + str(i['uin']) + "  name:" + i['name'] + "  img:" + i['img'])
        uin = str(i['uin'])
        name = i['name']
        img = i['img']
        dataList.append([uin, name, img])

    print("存储后的数据：")

    for n in dataList:
        print("qq:" + n.__getitem__(0) + "  name:" + n.__getitem__(1) + "  img:" + n.__getitem__(2))


main()
