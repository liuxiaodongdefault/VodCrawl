# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json_file_util
import threading


# 获取视频封面
def get_vod_img(soup):

    try:

        img_label = soup.select('.lazy')

        if img_label.__len__() > 0:
            img_url = img_label[0].get('src')
        else:
            img_url = None

    except Exception:
        return None

    return img_url

# 获取视频信息
def get_vod_info(soup):

    info_json = {}


    name_label = soup.select('.vodh h2')
    info_json['vod_name'] = name_label[0].get_text()

    sub_label = soup.select('.vodh span')
    info_json['sub_title'] = sub_label[0].get_text()


    info_label = soup.select('.vodinfobox li span')

    info_json['director'] = info_label[1].get_text()
    info_json['actor'] = info_label[2].get_text()
    info_json['type'] = info_label[3].get_text()
    info_json['area'] = info_label[4].get_text()
    info_json['language'] = info_label[5].get_text()
    info_json['release_date'] = info_label[6].get_text()
    info_json['duration'] = info_label[7].get_text()
    info_json['update_date'] = info_label[8].get_text()

    return info_json.__str__()

# 获取剧情介绍
def get_vod_des(soup):

    des_label = soup.select('.vodplayinfo')
    vod_des = des_label[1].get_text()
    return vod_des

# 获取播放链接
def get_vod_play_link(soup):
    vod_play_data = soup.select('.vodplayinfo div #1 ul li')

    # return vod_play_data[0].get_text()

    links = []
    for i in vod_play_data:
        vod_episode = {}
        episode = i.get_text().split('$')
        vod_episode['episode_name'] = episode[0]
        vod_episode['episode_link'] = episode[1]
        links.append(vod_episode)


    return links.__str__()

# 循环爬取页面 并将数据写入json
def loop_request(start_count, end_count, file_name):

    print('loop request start--------------------------------------------------------')

    vod_list = []

    for i in range(start_count, end_count + 1):

        try:

            url = 'https://www.okzy.co/?m=vod-detail-id-' + str(i) + '.html'

            print('\n' + 'loop count == ' + str(i) + '\n' + 'url == ' + url + '\n')

            wb_data = requests.get(url)  # 获取页面html

            if wb_data == None :
                continue

            wb_data.encoding = 'utf-8'
            soup = BeautifulSoup(wb_data.text, 'html.parser')  # 对页面进行解析

            vod_img = get_vod_img(soup)
            print('vod_img == ' + str(vod_img))

            if vod_img == None:

                continue

            vod_info = get_vod_info(soup)
            print('vod_info ==' + vod_info)

            vod_des = get_vod_des(soup)
            print('vod_des == ' + vod_des)

            vod_play_link = get_vod_play_link(soup)
            print('vod_link == ' + vod_play_link)

            vod_json = {}

            vod_json['img'] = vod_img

            vod_json['info'] = vod_info

            vod_json['des'] = vod_des

            vod_json['link'] = vod_play_link

            vod_list.append(vod_json)

        except Exception:
            pass
        continue

    json = {}
    json['data'] = vod_list
    print(json)
    json_file_util.write('data_' + file_name, json)



if __name__ == '__main__':

    # 起始页码
    page_start = 1

    # 结束页码
    page_end = 35

    # 每集合页数
    page_count = 10

    # 每集合(page_count条数据)开启一条线程

    # 创建线程
    threads = []
    times = int((page_end - page_start)/page_count) + 1
    print('times == ' + str(times))
    for i in range(times):
        s = page_start + page_count * i
        if page_end <= page_count:
            e = page_end
            print('s == ' + str(s) + ' e== ' + str(e))
        else:
            if i == times-1:
                e = page_end % page_count + page_count * i
                print('s == ' + str(s) + ' e == ' + str(e))
            else:
                e = page_count * (i + 1)
                print('s == ' + str(s) + ' e == ' + str(e))

        t = threading.Thread(target=loop_request,args=(s,e,str(s) + '_' + str(e)))
        threads.append(t)

    for i in range(times):
        threads[i].start()
    for i in range(times):
        threads[i].join()
    print('Main thread end---------------------------------------------')

