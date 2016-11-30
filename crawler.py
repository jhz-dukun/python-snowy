#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
引入自定义模块的两种方式
from getSources import myPrint
import getSources -> getSources.myPrint()
'''

from getSources import GetSource
import re
import requests
import testDemo

def requestTest():
    params = {'firstname': 'Du', 'lastname' : 'Kun'}
    r = requests.post("http://pythonscraping.com/files/processing.php",data=params)
    print(r.text)

print("hello, world!")

#requestTest()

url = "http://www.zhihu.com/"

news = GetSource(url)

client = testDemo.ZhiHuClient()
client.login("18681821674","north456123789")








