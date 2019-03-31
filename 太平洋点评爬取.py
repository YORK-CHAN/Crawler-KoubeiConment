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

def getdata(url):#找到口碑，并且获取文字数据。
    result = []
    try:
        r = urllib.urlopen(url)
    except:
        print '出错。跳过。'
        return result
    #将网页以utf-8格式解析然后转换为系统默认格式
    a = r.read().decode('GBK',errors='ignore').encode('utf-8')
    soup = BeautifulSoup(a,"html.parser",from_encoding="utf-8")
    view_score = soup.find_all('td', class_='leftTD')
    view = soup.find_all('td', class_='rightTD')

    for (i1, i2) in zip(view_score,view):
       temp = i1.get_text().replace("\n","7").replace("77","-").replace("7","")

       print temp
       temp0 = temp.split('-')[9]
       temp1 =temp.split('-')[10]
       temp2 = temp.split('-')[11]
       temp3 = temp.split('-')[12]
       temp = (temp0+temp1+temp2+temp3).encode('utf-8')
       list1 = ['外观','内饰','空间','配置','动力','油耗','舒适']
       if '操控' in temp:
           list1.append('操控')
       if '越野' in temp:
           list1.append('越野')

       lists = re.split("外观|内饰|空间|配置|动力|操控|油耗|舒适|越野", temp)

       dict_map = dict(zip(list1,lists[1:]))
       print json.dumps(dict_map, encoding="UTF-8", ensure_ascii=False)


       temp = i2.get_text()

       temp = temp.split('\n')
       temp = filter(None, temp)

       for index,i in enumerate(temp):
           if '外观：'in i and '外观' in dict_map.keys():
               result.append(['外观',i.split('：')[1],dict_map['外观']])

           if '内饰：'in i and '内饰' in dict_map.keys():
               result.append(['内饰', i.split('：')[1], dict_map['内饰']])

           if '空间：'in i and i!='QQ空间' and '空间' in dict_map.keys():
               result.append(['空间', i.split('：')[1], dict_map['空间']])

           if '配置：'in i and '配置' in dict_map.keys():
               result.append(['配置', i.split('：')[1], dict_map['配置']])
           if '动力：'in i and '动力' in dict_map.keys():
               result.append(['动力', i.split('：')[1], dict_map['动力']])
           if '操控：'in i and '操控' in dict_map.keys():
               result.append(['操控', temp[index+1], dict_map['操控']])
           if '油耗：'in i and '油耗' in dict_map.keys():
               result.append(['油耗', i.split('：')[1], dict_map['油耗']])
           if '舒适：'in i and '舒适' in dict_map.keys():
               result.append(['舒适', i.split('：')[1], dict_map['舒适']])

    return result


def main():
    data=[]
    old_url_1 = 'https://price.pcauto.com.cn/comment/sg'
    for i in range(1000,9999):
        # print '睡眠1s。。'
        # time.sleep(1)
        print '遍历至：',i
        old_url_2 = old_url_1+str(i)+'/'
        for j in range(1,3000):

            url = old_url_2+'p'+str(j)+'.html'
            print url
            col = getdata(url)#结果会保存在data.txt
            if len(col)>0:
                print col
                data.extend(col)
            else:
                break


    data = DataFrame(data, columns=['subject','content','score'])
    data.to_csv('TPY_data_2.csv', index=None)
    print data

    # print '睡眠30s。。'
    # time.sleep(30)
    # new_data = pd.DataFrame(col, columns=['content', 'subject', 'sentiment_value'])
    # new_data.to_csv('data_new.csv', index=None)
    # print new_data
main()
# getdata('http://newcar.xcar.com.cn/auto/index.php?r=reputation/reputation/GetAjaxKbList3&page=3&pserid=1093&jh=0&wd=0')
# print getPagesUrl('http://newcar.xcar.com.cn/1093/review.htm')