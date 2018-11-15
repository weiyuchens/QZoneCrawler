# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import re
import requests


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
    # 账号密码
    qq_count = ''
    qq_pw = ''

    # 模拟登陆
    driver = webdriver.Firefox()
    # driver.set_window_position(20, 40)
    # driver.set_window_size(1100, 700)

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

    req = requests.session()
    headers = {}


def getMethod():

    url = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/main_page_cgi?uin=726344827&param=3_726344827_0%7C8_8_726344827_1_1_0_1_1%7C16&g_tk=2059051196&qzonetoken=46fb3ee25c3fde95b8a93ee2d450e21e92bb589803d3ae1b9991032e526e2230b392bea1aab8&g_tk=2059051196'

    headers ={'host' :'user.qzone.qq.com',
              'accept' : '*/*',
              'accept-encoding' : 'gzip, deflate, br',
              'accept-language': 'zh-CN,zh;q=0.9',
              'cookie':'pgv_pvi=3497795584;RK=6NpIz0QgZy;ptcz=e27dcb585adc4ef88a74f88ea7eef2703a126b7734f9d8b6b717d7b7cd328d24;qz_screen=1920x1080;pgv_pvid=3786048277;QZ_FE_WEBP_SUPPORT=1; cpu_performance_v8=0; __Q_w_s__QZN_TodoMsgCnt=1; zzpaneluin=; zzpanelkey=;pgv_si=s8697273344;_qpsvr_localtk=0.9498334307209215;pt2gguin=o0726344827; uin=o0726344827; skey=@otp6wSogK; ptisp=ctc; p_uin=o0726344827; pt4_token=-ENXaOPhK4QA9d9rNwXR8P950hGmFNoh4mVliM*KE4g_;p_skey=iQnjVRX3MLwgx9au0CpoBJmZ4Kp31hiWkpIZ*Rz2p8g_; Loading=Yes; pgv_info=ssid=s5722514815',
              'referer': 'https://user.qzone.qq.com/726344827/main',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    page = requests.session().get(url,headers=headers)
    print(page.text)

# main()
getMethod()