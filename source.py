#!/usr/bin/env python
# encoding=utf-8

"""
爬取豆瓣电影TOP250 - 完整示例代码
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

    with codecs.open('source', 'wb', encoding='utf-8') as file_open:
        _s = [title, thumb, source_url, createTime]
        raw_string = ','.join(_s)
        content = str(raw_string) + '\n'
        file_open.write(content)


def main():
    url = DOWNLOAD_URL
    html = []
    a_href_list = []
    next_page_url = ''
    #with codecs.open('detail_urls', 'wb', encoding='utf-8') as fp:
        # 当前资源网的伦理片页数为48
        # for page in range(1, 49):
        #     url = BASE_URL + "/?m=vod-type-id-17-pg-" + str(page) + ".html"
        #     print(url)
        #     html = download_page(url)
        #     a_href_list = parse_html(html)
        #     # 将a_href_list数组拆分成字符串并且用|隔开保存到detail_urls文件中
        #     fp.write(u'{a_href_list}\n'.format(a_href_list='\n'.join(a_href_list)))


        # fp2 = open("D:\phpStudy\WWW\pyCharm\\navcmssource\detail_urls", 'r')
        # print('111')
        # contents = fp2.read()
        # chapters = filter(lambda x: x != '', contents.split('\n'))
        # fp2.close()
        # return (chapter.split('|') for chapter in chapters)



    html2 = download_page("http://zuidazy.com/?m=vod-detail-id-33099.html")
    html_obj = detail_html(html2)


if __name__ == '__main__':
    main()