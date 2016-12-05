#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
引入自定义模块的两种方式
from getSources import myPrint
import getSources -> getSources.myPrint()
'''

import requests
from bs4 import BeautifulSoup as bs
import json
import subprocess
import time
import os
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

captchaFile = os.path.join(sys.path[0], "captcha.jpg")
cookieFile = os.path.join(sys.path[0], "cookie")
session = requests.session()
headers = {
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'Accept-Language: zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'www.zhihu.com',
}

login_data = {'phone_num': '18681821674',
             'password': 'north456123789',
             'Referer': 'https://www.zhihu.com/',
             'remember_me': 'true',
              }

def zhihuOpen(url,headers,delay=0,timeout=10):
    """打开网页，返回Response对象"""
    if delay:
        time.sleep(delay)
    return session.get(url, headers = headers,timeout=timeout, verify=False)

def get_captcha():
    t = str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    captcha = input("please input the captcha:")
    os.remove(captchaFile)
    return captcha

def loadCookie():
    """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
    if os.path.exists(cookieFile):
        print("=" * 100)
        with open(cookieFile, "r") as f:
            cookie = json.load(f)
            return cookie
    return None

def saveCookie():
    """cookies 序列化到文件
    即把dict对象转化成字符串保存
    """
    #global session
    with open(cookieFile, "w") as output:
        cookies = session.cookies.get_dict()
        json.dump(cookies, output)
        print("=" * 100)
        print("已在同目录下生成cookie文件：", cookieFile)

cookie = loadCookie()

if cookie:
    print("检测到cookie文件，直接使用cookie登录")
    session.cookies.update(cookie)
    soup = bs(zhihuOpen(r"http://www.zhihu.com/",headers).text, "html.parser")
    print("已登陆账号： %s" % soup.find("span", class_="name").getText())
else:
    print("没有找到cookie文件，将调用login方法登录一次！")
    zhihuLogin()

def zhihuLogin():
    response = session.get('http://www.zhihu.com', headers=headers, verify=False).text
    print(response)
    soup = bs(response, "html.parser")
    xsrf = soup.find('input', {'name': '_xsrf'})['value']
    print(xsrf)
    login_data['_xsrf'] = xsrf
    login_data['captcha'] = get_captcha()
    responed = session.post('https://www.zhihu.com/login/phone_num', headers=headers, data=login_data)
    if 0 == responed.json()['r']:
        saveCookie()
        print(responed.text)
    else:
        print("login failed!")



#print(responed)


startData = zhihuOpen("https://www.zhihu.com",headers)
print(startData.text)
with open("zhihu.html","w",encoding='utf-8') as f:
    f.write(startData.text)
    f.close()