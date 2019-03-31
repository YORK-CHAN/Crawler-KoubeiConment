# -*- coding: utf-8 -*-
import bs4
import re
from bs4 import BeautifulSoup
import cookielib
import urllib2
import urllib
import time
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8') # 设置默认编码格式为'utf-8'

import json
from pandas import Series,DataFrame
import scrapy

def getdata(url,col):#找到口碑，并且获取文字数据。
    r = urllib.urlopen(url)
    #将网页以utf-8格式解析然后转换为系统默认格式
    a = r.read().decode('GBK',errors='ignore').encode('utf-8')

    soup = BeautifulSoup(a,"html.parser",from_encoding="utf-8")
    links = soup.find_all('a')
    print "口碑"
    link_koubei=''
    for link in links:
        href = link['href']
        name = link.get_text().encode('utf-8')
        if name=='口碑':
            link_koubei = 'http://newcar.xcar.com.cn'+str(href)
            break
    print link_koubei
    if 'javascript' not in link_koubei:#若不为空链接。则获取数据
        view_url_list = getPagesUrl(link_koubei)#获取这个车的所有评论分页链接
        pag = 1

        for link_koubei in view_url_list:
            print '第',pag,'页'
            pag=pag+1
            r = urllib.urlopen(link_koubei)
            #将网页以utf-8格式解析然后转换为系统默认格式
            a = r.read().decode('GBK',errors='ignore').encode('utf-8')

            #创建一个BeautifulSoup解析对象
            soup = BeautifulSoup(a,"html.parser",from_encoding="utf-8")
            print "获取段落的文字"
            view_score = soup.find_all('div', class_='score')
            view = soup.find_all('div', class_='review_post')

            for (i1, i2) in zip(view_score,view):
               item_score = i1.get_text().replace("\n",":")
               item_score=re.findall(r"[\w']+", item_score)
               item_score = [int(x) for x in item_score[2:11]]#外观，内饰，空间，舒适，油耗，动力，操控，性价比
               item_subject = ['外观','内饰','空间','舒适','油耗','动力','操控','性价比']
               dictionary = dict(zip(item_subject, item_score),encoding = 'utf-8')
               # dictionary = json.dumps(dict(zip(item_subject, item_score)), ensure_ascii=False,indent=2)
               # print dictionary
               # print dictionary['外观']
               # print i2.get_text().replace("\n","")
               i2 = i2.get_text().replace("\n","").encode('utf-8')
               line = i2.split('[')
               for item in line:
                   if '外观]' in item:
                       if len(item.split('外观]')[1]) > 5:
                           col.append([item.split('外观]')[1],'外观',dictionary['外观']])
                   if '内饰]' in item:
                       if len(item.split('内饰]')[1]) > 5:
                           col.append([item.split('内饰]')[1], '内饰', dictionary['内饰']])
                   if '空间]' in item:
                       if len(item.split('空间]')[1]) > 5:
                           col.append([item.split('空间]')[1], '空间', dictionary['空间']])
                   if '舒适]' in item:
                       if len(item.split('舒适]')[1]) > 5:
                           col.append([item.split('舒适]')[1], '舒适', dictionary['舒适']])
                   if '油耗]' in item:
                       if len(item.split('油耗]')[1]) > 5:
                           col.append([item.split('油耗]')[1], '油耗', dictionary['油耗']])
                   if '动力]' in item:
                       if len(item.split('动力]')[1]) > 5:
                           col.append([item.split('动力]')[1], '动力', dictionary['动力']])
                   if '操控]' in item:
                       if len(item.split('操控]')[1]) > 5:
                           col.append([item.split('操控]')[1], '操控', dictionary['操控']])
                   if '性价比]' in item:
                       if len(item.split('性价比]')[1]) > 5:
                           col.append([item.split('性价比]')[1], '性价比', dictionary['性价比']])

            # print col

               # exit(1)
               # if not os.path.exists('data_all.txt'):
               #     with open('data_all.txt', "w") as f:
               #         print(f)
               # with open('data_all.txt', "a") as f:
               #     f.write(item.get_text().replace("\n",""))
               #     f.write('\n')
    else:
        print link_koubei,'绕过！'
    return col

def getCAR(url):#获取一页所有的车型
    r = urllib.urlopen(url)
    #将网页以utf-8格式解析然后转换为系统默认格式
    a = r.read().decode('GBK',errors='ignore').encode('utf-8')
    # print a
    soup = BeautifulSoup(a,"html.parser",from_encoding="utf-8")
    links = soup.find_all('a',class_='list_img car_search_ps_list_a')
    result = []
    for i in links:
        print i['href']
        result.append(i['href'])
    return result

def generatorURL():#按规律产生页面url，用于找到所有车型，共66页
    url = 'http://newcar.xcar.com.cn/car/0-0-0-0-0-0-0-0-0-0-0-'
    result = []
    for i in range(1,67):
        result.append(url+str(i))
    return result

def getPagesUrl(url):#获取一个口碑页下的所有可选的分页链接
    url_split = url.split('/')
    car_id = url_split[3]
    print '车id：' ,car_id
    r = urllib.urlopen(url)
    # 将网页以utf-8格式解析然后转换为系统默认格式
    a = r.read().decode('GBK', errors='ignore').encode('utf-8')
    soup = BeautifulSoup(a, "html.parser", from_encoding="utf-8")
    links = soup.find_all('a', class_='page')
    results = []
    temp=[]
    for i in links:
        temp.append(int(i.get_text()))
        maxpage = max(temp)
        result = [i for i in range(1,(maxpage+1))]
        for j in result:
            results.append('http://newcar.xcar.com.cn/auto/index.php?r=reputation/reputation/GetAjaxKbList3&page='+str(j)+'&pserid='+str(car_id)+'&jh=0&wd=0')
    return results


def main():
    url_set = generatorURL()
    car_set = []
    for i in url_set:
        print i
        temp = getCAR(i)
        car_set.extend(temp)
    number=1
    col =[]
    for i in car_set:
        print '第%s辆车'%number
        number = number+1
        url = 'http://newcar.xcar.com.cn'+i
        print url
        col = getdata(url,col)#结果会保存在data.txt
        print '睡眠30s。。'
        time.sleep(30)
    new_data = pd.DataFrame(col, columns=['content', 'subject', 'sentiment_value'])
    new_data.to_csv('data_new.csv', index=None)
    print new_data
main()
# getdata('http://newcar.xcar.com.cn/auto/index.php?r=reputation/reputation/GetAjaxKbList3&page=3&pserid=1093&jh=0&wd=0')
# print getPagesUrl('http://newcar.xcar.com.cn/1093/review.htm')