# -*- coding: utf-8 -*-
from hitwhnews.items import HitwhnewsItem
import scrapy
import MySQLdb.cursors

from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors
class xinwenspider(scrapy.Spider):
    name = "hitwhnews"

    start_urls = ["http://news.hitwh.edu.cn/",urls]



    def parse1(self, response):
        for sel in response.xpath("body/div/div[5]/div[2]/div/ul/li"):
            item = HitwhnewsItem()

            item['link'] = sel.xpath('a/@href').extract()

            yield item

    con = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='hitwh'

    )

    # con = mdb.connect('localhost', 'root', 'root', 'xw')
    global urls
    urls = []
    # global opq
    # opq=[]
    # for i in range(30):
    #    opq.append('link')
    # global ppp
    # ppp=dict(zip(opq,urls))


    with con:
        # 仍然是，第一步要获取连接的cursor对象，用于执行查询
        cur = con.cursor()
        # 类似于其他语言的query函数，execute是python中的执行查询函数
        cur.execute("SELECT link FROM urls")
        # 使用fetchall函数，将结果集（多维元组）存入rows里面
        rows = cur.fetchall()

        for row in rows:
            url = "http://news.hitwh.edu.cn/" + (str(row))[2:-3]
            urls.append(url)



    def parse2(self, response):

        item = HitwhnewsItem()
        item['title'] = response.xpath(".//*[@id='show_left_news']/div[1]/text()").extract()

        item['content'] = response.xpath(".//*[@id='newsContnet']//span/text()").extract()

        yield item
