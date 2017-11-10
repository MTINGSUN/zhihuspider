# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os,sys
import sqlite3
from ZhihuSpider.items import QuesInfoItem

class ZhihuSpiderWriteToCSVPipeline(object):

    def open_spider(self, spider):
        # print("abs path is %s" %(os.path.abspath(sys.argv[0])))
        
        self.csvFile = open(os.path.abspath('C:/Users/Administrator/Desktop/ZhihuSpider/test.csv'), "w+",newline='')
        try:
            self.write = csv.writer(self.csvFile)
            self.write.writerow(('question', 'author_name', 'author_bio', 'answer_content'))
        except Exception as e:
            pass 

    def close_spider(self, spider):
        self.csvFile.close()

    def process_item(self, item, spider):
        try:
            self.write.writerow((item["question"], item["author_name"], item["author_bio"], item["answer_content"]))
        except BaseException as e:
            pass
            
        return item

class ZhihuSpiderWriteToDBPipeline(object):

    def open_spider(self, spider):
        try:
            self.conn = sqlite3.connect(os.path.abspath('C:/Users/Administrator/Desktop/ZhihuSpider/test.db'))
            self.cursor = self.conn.cursor()
        except BaseException as e:
            pass
            

    def close_spider(self, spider):
        try:
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except BaseException as e:
            pass

    def process_item(self, item, spider):
        try:
            if isinstance(item, QuesInfoItem):
                self.cursor.execute('insert into question (question, author_name, author_bio, answer_content) values (?, ?, ?, ?)', (item["question"], item["author_name"], item["author_bio"], item["answer_content"]))
        except BaseException as e:
            print(e)
            pass
            
        return item
