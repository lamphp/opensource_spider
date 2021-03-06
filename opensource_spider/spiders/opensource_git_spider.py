#!/usr/bin/python
#coding=utf-8
# @hequan

from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.spiders import CrawlSpider
from scrapy.http import Request

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from opensource_spider.items import OpensourceSpiderItem

class opensource_git_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "git_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    # https://www.kernel.org/pub/software/scm/git/
    allowed_domains = ["www.kernel.org"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        'https://www.kernel.org/pub/software/scm/git/'
    ]

    def parse_item(self, rsp):
        item = rsp.meta['item']
        path_tmp = item['downurl'][43:]
        item['orginname'] = path_tmp
        return item


    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse(self, response):
        #print "text = " , response.text
        #sel = Selector(response)
        pt1 = re.compile(r'<a\shref="(.*?)">(.*?)</a>([\s]*)([\d\w-]*)\s([\d:]*)([\s]*)([-\d\w]*)([\s]*)')
        ret1 = re.findall(pt1, response.text)
        for v in ret1:
            if v[6] == '-':
                new_url = response.url + v[0]
                yield Request(new_url, callback = self.parse)
            elif v[6] == '':
                continue
            else:
                item = OpensourceSpiderItem()
                item['orginname']   = v[0]
                item['downurl']     =  response.url + v[0]
                item['filesize']    = 0
                yield Request(item['downurl'], meta = {'item' : item}, callback = self.parse_item)
        

