# -*- coding: utf-8 -*-


#from bs4 import BeautifulSoup
import urllib.request

import xml.etree.ElementTree as ET
import configparser

import requests
from bs4 import BeautifulSoup
#from datetime import datetime
import json

def get_news_pool(root):
    news_pool = []
    print(root)
    response = urllib.request.urlopen(root)
    #esponse = requests(root)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    # td = soup.find('a', {'class':'feed-card-item'})
    td = soup.findAll('a')
    for i in td:
        if (i.get('href') != None and i.get('href').find('https://news.sina.com.cn/c/') == 0):
            news_pool.append(i.get('href'))
    return news_pool

def crawl_news(news_pool, doc_dir_path, doc_encoding):
    i = 1
    for news in news_pool:
        res = requests.get(news)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            title = soup.select('.main-title')[0].text
            # timesource1=soup.select('.date-source')[0].text.split('\n')[1]    #获取时间
            timesource = soup.select('.date-source span')[0].text  # 获取时间
            # dt = datetime.strptime(timesource, '%Y年%m月%d日 %H:%M')
            # dt.strftime('%Y-%m-%d')
            # place = soup.select('.date-source a')[0].text  # 获取新闻来源
            article = []  # 获取文章内容
            for p in soup.select('#article p')[:-1]:
                article.append(p.text.strip())
            articleall = ' '.join(article)
            # editor = soup.select('#article p')[-1].text.strip('责任编辑：')  # 获取作者姓名
            comments = requests.get(
                'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-hcscwxa1809510&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1')
            # print(comments.text)
            jd = json.loads(comments.text)  # 用jason解析器
            # comment_num = jd['result']['count']['total']

            doc = ET.Element("doc")
            ET.SubElement(doc, "id").text = "%d" % (i)
            ET.SubElement(doc, "url").text = news
            ET.SubElement(doc, "title").text = title
            ET.SubElement(doc, "datetime").text = timesource
            ET.SubElement(doc, "body").text = articleall
            tree = ET.ElementTree(doc)
            tree.write(doc_dir_path + "%d.xml" % (i), encoding=doc_encoding, xml_declaration=True)
            i += 1
        except IndexError:
            pass
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')
    root = 'https://news.sina.com.cn/china/'
    news_pool = get_news_pool(root)
    crawl_news(news_pool, config['DEFAULT']['doc_dir_path'], config['DEFAULT']['doc_encoding'])
    print('done!')