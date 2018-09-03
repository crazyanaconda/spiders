# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenminwangItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 文章内容
    content = scrapy.Field()
    # 文章插图
    inset = scrapy.Field()
