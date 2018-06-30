# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json_file_util


url = 'https://www.okzy.co/?m=vod-type-id-1.html'

wb_data = requests.get(url)  # 获取页面html
wb_data.encoding = 'utf-8'
soup = BeautifulSoup(wb_data.text, 'html.parser')  # 对页面进行解析
link_label = soup.select('.xing_vb4')  # 找class=xing_vb4

# 链接
links = []
names = []
for i in link_label:
    # data.append(url + i.get('href'))
    for j in i.children:
        links.append(url + j.get('href'))
        names.append(j.get_text())


# 分类
cat_label = soup.select('.xing_vb5')
cats = []
for i in cat_label:
    cats.append(i.get_text())

# 时间
date_label = soup.select('.xing_vb6')
dates = []
for i in date_label:
    dates.append(i.get_text())

# 写入json

list = []

for i in range(links.__len__()):
    data = {}
    data['name'] = names[i]
    data['link'] = links[i]
    data['cat'] = cats[i]
    data['date'] = dates[i]
    list.append(data)
    # print('片名: ' + names[i] + '\n' + '链接: ' + links[i] + '\n' + '分类: ' + cats[i] + '\n' + '时间: ' + dates[i] + '\n')

print(list)

json = {}
json['data'] = list
json_file_util.write('data',json)