# -*- coding: utf-8 -*-
import scrapy
#import requests
from scrapy import Request
from scrapy.spiders import CrawlSpider
import time
import re
import json
from ZhihuSpider.items import QuesInfoItem

class ZhSpider(CrawlSpider):
    name = 'ZH'
    allowed_domains = ['zhihu.com']
    # start_urls是Spider在启动时进行爬取的入口URL列表。第一个被获取到的页面的URL将是其中一个，
    # 后续的URL从初始的URL的响应中获取
    start_urls = ['https://www.zhihu.com/r/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0',
    'https://www.zhihu.com/r/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&correction=1&type=content&offset=30',
    ]

    i = 0
    # parse是Spider的一个方法。被调用时，每个初始的URL响应后返回的response对象，将会作为唯一的参数返回给该方法
    # 该方法负责解析返回的数据（respose data）、提取数据（item）以及生成需要进一步处理的URL的Response对象

    def parse(self, response):

        # print('***********************\n',response.body,'***********************\n\n')
        print('*************开始下载json文件:*********************')
        # 1、实现网页的解析，生成item
        # 首先打开js路径，获取'htmls'KEY下面的内容，是一个整体的str文件，没有标KEY，所以用re去解析它
        try:
            # print(type(response.body))
            # print(type(response.text))
            jsDict = json.loads(response.body)
            # print(type(jsDict))
            print('*************开始解析页面*********************')
            questions = jsDict['htmls']
    
            # 抽取所有的问题和对应的follwer_num, answer_num和answer_abstract
            for q in questions:
                item = QuesInfoItem()
                # 删去源代码中关键词“<em>机器学习</em>”的标签
                q = q.replace('<em>','').replace('</em>','')
                # 问题信息在标签 class=\"js-title-link\">和</a>当中
                question = re.findall('class=\"js-title-link\">(.*?)</a>',q)[0]
                print(question)
                item['question'] = question

                time.sleep(2)
        
                # 作者姓名在标签 data-author-name=\"和\" data-entry-url=\"当中
                try:
                    author_name = re.findall('data-author-name=\"(.*?)\" data-entry-url=\"',q)[0]
                    print('作者姓名:',author_name)
                except:
                    author_name = None
                item['author_name'] = author_name
    
                # 作者简介在标签 <span title=\"和\" class=\"bio\">当中
                try:
                    author_bio = re.findall('<span title=\"(.*?)\" class=\"bio\">',q)
                    print('作者简介:',author_bio)
                except:
                    author_bio = None
                item['author_bio'] = author_bio

                time.sleep(2)

                # 回答内容信息在标签 <script type=\"text\" class=\"content\">和</script>当中
                try:
                    answer_content = re.findall('<script type=\"text\" class=\"content\">(.*?)</script>', q)[0]
                    print(answer_content[:100]) #内容太多只打印一部分出来看一下
                except:
                    answer_content = None
                item['answer_content'] = answer_content

                time.sleep(2)

                yield item

            # 2、构造下一页的链接并回调给parse方法
            first_url = 'https://www.zhihu.com/r/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0'
            # 下一页链接信息在js文件的['paging']标签下的['next']KEY中
            nexturl = jsDict['paging']['next']
            last_url = re.findall('&(.*)', nexturl)[0]
            url = first_url + '&' +last_url
            print(url)
            yield Request(url, callback=self.parse) 

        except json.decoder.JSONDecodeError as e: #这个报错开始是因为找错了url一直报错加的，现在应该没关系可以去掉了
            print('JSONDecodeError')

