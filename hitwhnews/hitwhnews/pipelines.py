# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors


class HitwhnewsPipeline(object):
    def __init__(self):
        self.file = codecs.open('hitwhnews.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySQLPipeline1(object):
    @classmethod
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='localhost',
                                            db='hitwh',
                                            user='root',
                                            passwd='root',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True
                                            )

    def process_item(self, item, spider):
        print(spider)
        # run db query in thread pool
        self.dbpool.runInteraction(self.insert_into_table, item)

        return item

    def insert_into_table(self, conn, item):
        conn.execute('insert into urls(link) values(%s)', (

            item['link']
        ))

class MySQLPipeline2(object):
        @classmethod
        def __init__(self):
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                                host='localhost',
                                                db='hitwh',
                                                user='root',
                                                passwd='root',
                                                cursorclass=MySQLdb.cursors.DictCursor,
                                                charset='utf8',
                                                use_unicode=True
                                                )

        def process_item(self, item, spider):
            print(spider)
            # run db query in thread pool
            self.dbpool.runInteraction(self.insert_into_table, item)

            return item

        def insert_into_table(self, conn, item):
            conn.execute('insert into news(title,link,content) values(%s,%s,%s)', (

                item['title'], item['link'], item['content']
            ))
