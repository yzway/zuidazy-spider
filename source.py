#!/usr/bin/env python
# encoding=utf-8

"""
爬取最大资源网-伦理片 - 完整示例代码
抓取截至时间2018-01-24
2018/11/22  builded by dchaster
"""

import codecs

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://zuidazy.com'
DOWNLOAD_URL = 'http://zuidazy.com/?m=vod-type-id-17-pg-1.html'
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
            if a_detail:
                a_href_list.append(BASE_URL + a_detail.attrs['href'])


    next_page = soup.find('div', attrs={'class': 'pages'}).find('a',attrs={'class':'pagelink_a'})
    if next_page.contents[0] == '下一页':
        next_page_url = next_page.attrs['href']

    return a_href_list

# 分析详情页
def detail_html(html):
    # 标题titile   缩略图thumb   上传时间createTime  点播地址source_url
    soup = BeautifulSoup(html, 'lxml')
    warp_dom = soup.find('div', attrs={'class':'warp'})
    title = warp_dom.find('div', attrs={'class':'vodh'}).find('h2').text
    thumb = warp_dom.find('div', attrs={'class':'vodImg'}).find('img').attrs['src']
    source_url = PARSE_URL + warp_dom.find('div', attrs={'id':'play_1'}).find('input', attrs={'name':'copy_sel'}).attrs['value']
    createTime = warp_dom.find('div', attrs={'class':'vodinfobox'}).find('ul').contents[17].find('span').text
    _s = ["'" + title + "'", "'" + thumb + "'", "'" + source_url + "'", "'" + createTime + "'"]
    return _s



def main():
    url = DOWNLOAD_URL
    html = []
    a_href_list = []
    next_page_url = ''
    # 获取所有详情页的链接并写入到detail_urls文件中
    # with codecs.open('detail_urls', 'wb', encoding='utf-8') as fp:
    #     #当前资源网的伦理片页数为48
    #     for page in range(1, 49):
    #         url = BASE_URL + "/?m=vod-type-id-17-pg-" + str(page) + ".html"
    #         print(url)
    #         html = download_page(url)
    #         a_href_list = parse_html(html)
    #         # 将a_href_list数组拆分成字符串并且用|隔开保存到detail_urls文件中
    #         fp.write(u'{a_href_list}\n'.format(a_href_list='\n'.join(a_href_list)))




    # 解析所有页面并写入到source文件中
    fp = open('detail_urls', 'r')
    contents = fp.read()

    items = contents.split('\n')
    r_content = ''

    with codecs.open('source', 'wb', encoding='utf-8') as fp_source:
        if items:
            i= 0
            for index, item in enumerate(items):
                if item:
                    html2 = download_page(item)
                    if html2:
                        source = detail_html(html2)
                        raw_string = ','.join(source)  # list拆分成字符串并以逗号连接\
                        r_content = str(raw_string) + '\n'
                        fp_source.write(r_content)
                        i = i + 1
                        print(i)

    fp.close()
    fp_source.close()

if __name__ == '__main__':
    main()