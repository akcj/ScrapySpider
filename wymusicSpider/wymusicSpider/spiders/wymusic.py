# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from wymusicSpider.items import WymusicItem
import sys
import lxml

reload(sys)
sys.setdefaultencoding('utf-8')

#html DOM tree to lxml 格式
def parse_from_unicode(unicode_str):  
        utf8_parser = lxml.etree.HTMLParser(encoding='utf-8')
        s = unicode_str.encode('utf-8')
        return lxml.etree.fromstring(s, parser=utf8_parser)

class WymusicSpider(scrapy.Spider):
    name = 'wymusic'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/#/discover/toplist']

    def parse(self, response):
        items = []
        dom = parse_from_unicode(response.body)
        
        lists = dom.xpath('//tbody/tr')
        for row in lists:
            td = row.xpath("td")
            rank = td[0].xpath("div/span[@class='num']/text()")[0]
            title = td[1].xpath("div/div/div/span/a/b//@title")[0]
            duration = td[2].xpath("span/text()")[0]
            author = td[3].xpath("div//@title")[0]
            
            item = WymusicItem()

            item['rank']  = rank
            item['title']  = title
            item['duration']  = duration
            item['author']  = author

            if item not in items:
                items.append(item)

        return items
       