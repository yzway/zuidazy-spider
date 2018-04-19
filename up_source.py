#!/usr/bin/env python
# encoding=utf-8

"""
爬取最大资源网-伦理片 - 完整示例代码
上次抓取截至时间 2018-01-29
2017/11/22  builded by dchaster
"""

import codecs
import urllib
import datetime
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://zuidazy.com'
DOWNLOAD_URL = 'http://www.zuidazy.com/?m=vod-type-id-17.html'
PARSE_URL = 'http://zuida-jiexi.com/m3u8/m3u8.php?url='

def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content


# 分析列表页
def parse_html(html):
    soup = BeautifulSoup(html,'lxml')
    list_soup = soup.find('div', attrs={'class': 'xing_vb'})

    a_href_list = []

    for item in list_soup.find_all('ul'):
        li_detail = item.find('li')
        span_detail = li_detail.find('span',attrs={'class':'xing_vb4'})

        if span_detail:
            a_detail = span_detail.find('a',attrs={'target':'_blank'})
            str_up_datetime = li_detail.find('span',attrs={'class':'xing_vb6'}).text

            upTimeStamp = int(time.mktime(time.strptime(str_up_datetime, "%Y-%m-%d")))
            # 更新开始日期
            nowTimeStamp = int(time.mktime(time.strptime('2018-01-29', "%Y-%m-%d")))
            # 从截至上次的时间开始遍历
            if nowTimeStamp < upTimeStamp and a_detail:
                a_href_list.append(BASE_URL + a_detail.attrs['href'])

    return a_href_list

# 分析详情页
def detail_html(html):
    # 标题titile   缩略图thumb   上传时间createTime  点播地址source_url
    soup = BeautifulSoup(html, 'lxml')
    warp_dom = soup.find('div', attrs={'class':'warp'})
    title = warp_dom.find('div', attrs={'class':'vodh'}).find('h2').text
    thumb = warp_dom.find('div', attrs={'class':'vodImg'}).find('img').attrs['src']
    source_url = warp_dom.find('div', attrs={'id':'play_1'}).find('input', attrs={'name':'copy_sel'}).attrs['value']
    createTime = warp_dom.find('div', attrs={'class':'vodinfobox'}).find('ul').contents[17].find('span').text
    area = warp_dom.find('div', attrs={'class':'vodinfobox'}).find('ul').contents[9].find('span').text
    language = warp_dom.find('div', attrs={'class': 'vodinfobox'}).find('ul').contents[11].find('span').text
    release = warp_dom.find('div', attrs={'class': 'vodinfobox'}).find('ul').contents[13].find('span').text
    # 过滤图片可成功下载的资源
    if thumb.find("http://tupian.tupianzy.com/pic/upload/vod/201") != -1 and title.strip() and source_url.strip() and createTime.strip():
        _s = ["'mytitle" + title + "'", "'" + thumb + "'", "'" + source_url + "'", "'" + area + "'",
              "'" + language + "'", "'" + release + "'", "'" + createTime + "mytime'"]
        return _s

# 分析详情页的缩略图
def parse_detail_pic(html):
    soup = BeautifulSoup(html, 'lxml')
    warp_dom = soup.find('div', attrs={'class': 'warp'})
    thumb = warp_dom.find('div', attrs={'class': 'vodImg'}).find('img').attrs['src']
    # 过滤图片可成功下载的链接
    if thumb.find("http://tupian.tupianzy.com/pic/upload/vod/201") != -1:
        _s = [thumb]
        return _s

def main():
    url = DOWNLOAD_URL
    html = []
    a_href_list = []

    #获取所有详情页的链接并写入到detail_urls文件中
    with codecs.open('detail_urls.txt', 'wb', encoding='utf-8') as fp:

        #当前资源网的伦理片页数为57
        for page in range(1, 58):
            url = BASE_URL + "/?m=vod-type-id-17-pg-" + str(page) + ".html"
            html = download_page(url)
            a_href_list = parse_html(html)
            # 将a_href_list数组拆分成字符串并且用|隔开保存到detail_urls文件中
            fp.write(u'{a_href_list}\n'.format(a_href_list='\n'.join(a_href_list)))
            print('write detail url : ' + str(page))

    # 解析所有页面并写入到source文件中
    items = []
    contents = []
    with codecs.open('detail_urls.txt', 'r', encoding='utf-8') as fp:
        contents = fp.read()
        items = contents.split('\n')

    r_content = ''
    with codecs.open('source.txt', 'wb', encoding='utf-8') as fp_source:
        if items:
            for index, item in enumerate(items):
                if item:
                    html2 = download_page(item)
                    if html2:
                        source = detail_html(html2)
                        raw_string = ','.join(source)  # list拆分成字符串并以逗号连接\
                        r_content = str(raw_string) + '\n'
                        fp_source.write(r_content)
                        print('write source : '+str(index+1))

    # 解析图片下载地址列表写入pics文件中
    with codecs.open('pics.txt', 'wb', encoding='utf-8') as fp_pic:
        if items:
            for index, item in enumerate(items):
                x = 1
                if item:
                    html3 = download_page(item)
                    if html3:
                        source = parse_detail_pic(html3)
                        raw_string = ','.join(source)
                        r_content = str(raw_string) + '\n'
                        fp_pic.write(r_content)
                        print('write pic : '+str(index + 1))


if __name__ == '__main__':
    main()