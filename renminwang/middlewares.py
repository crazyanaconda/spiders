# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

from renminwang.settings import USER_AGENTS


class RandomUserAgent(object):
    def process_request(self,request,spider):
        useragnet = random.choice(USER_AGENTS)
        request.headers.setdefault('UserAgent',useragnet)

