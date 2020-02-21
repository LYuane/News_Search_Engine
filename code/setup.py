# -*- coding: utf-8 -*-


from code.spider import get_news_pool
from code.spider import crawl_news
from code.index_module import IndexModule
from code.recommendation_module import RecommendationModule
from datetime import *
import urllib.request
import configparser

def get_max_page(root):
    response = urllib.request.urlopen(root)
    html = str(response.read())
    html = html[html.find('var maxPage =') : ]
    html = html[:html.find(';')]
    max_page = int(html[html.find('=') + 1 : ])
    #print(max_page)
    return(max_page)

def crawling():
    print('-----start crawling time: %s-----'%(datetime.today()))
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')
    root = 'https://news.sina.com.cn/china/'
    #max_page = get_max_page(root+'.shtml')
    news_pool = get_news_pool(root)
    crawl_news(news_pool, config['DEFAULT']['doc_dir_path'], config['DEFAULT']['doc_encoding'])
    
if __name__ == "__main__":
    print('-----start time: %s-----'%(datetime.today()))
    
    #抓取新闻数据
    crawling()
    
    #构建索引
    print('-----start indexing time: %s-----'%(datetime.today()))
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()
    
    #推荐阅读
    print('-----start recommending time: %s-----'%(datetime.today()))
    rm = RecommendationModule('../config.ini', 'utf-8')
    rm.find_k_nearest(5, 25)
    print('-----finish time: %s-----'%(datetime.today()))