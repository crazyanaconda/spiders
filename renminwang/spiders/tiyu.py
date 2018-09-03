# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import RenminwangItem
from ..settings import SPIDER_NAME,ALLOWED_DOMAINS,START_URLS

class TiyuSpider(CrawlSpider):
    name = SPIDER_NAME
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    rules = (
        Rule(LinkExtractor(allow=()), follow=True,callback='parse_item'),
    )

    def parse_item(self, response):
        item = RenminwangItem()
        # 标题
        title = response.xpath("//h1/div/text() | //h1/text()").extract()
        self.check(item, title, 'title')
        # 正常文章的内容
        content_ls = response.xpath("//p[@style='text-indent: 2em;']/text() | //p[@style='text-indent: 2em']/text() | //p[@style='text-indent: 2em']/text() | //div[@class='box_con']//p/text() | //div[@id='p_content']/p[not(@style)]/text() | //p[@style='text-indent: 2em;']/text() | //div[@id='p_content'][./text() and ./a//text()]").extract()
        content = ''.join(content_ls)
        # 文章里的插图链接
        inset_ls = response.xpath("//div[@class='text w1000 clearfix']//div[@class='box_pic']//img/@src | //div[@class='box_pic']/following-sibling::p/img/@src | //*[@align='center']/img/@src").extract()
        inset = '+++'.join(inset_ls)



        # self.check(item,content_ls,'content')
        # self.check(item,inset_ls,'inset')

        item['content'] = content
        item['inset'] = inset
        item['url'] = str(response.url)

        return item

    def check(self,item,type,name):
        if len(type) == 0:
            item[name] = 'kong_{}'.format(name)
        else:
            item[name] = ''.join(type)







