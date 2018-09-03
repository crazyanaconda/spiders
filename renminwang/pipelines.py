# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os,io

import requests
import pymysql

from renminwang import settings
from renminwang.settings import BASE_DIR,BASE_URL
# 下载插图
class DownLoadInsetPipeline(object):
    def process_item(self, item, spider):
        inset_list = item['inset'].split('+++')
        if inset_list[0] != '':
            for inset_url in inset_list:
                if inset_url.startswith('http://'):
                    # 图片的链接是完整的
                    dir_name = (item['url'].split('/')[-1]).replace('.html','')
                    #dir_path = 'E:\img\{}'.format(dir_name)
                    dir_path = BASE_DIR + dir_name
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    self.down_img(dir_path,inset_url)
                else:
                    img_url = BASE_URL + inset_url
                    html_name = (item['url'].split('/')[-1]).split('-')
                    if len(html_name) == 2:
                        dir_name = ''.join(html_name).replace('.html','')
                    else:
                        dir_name = ''.join(html_name[:-1])
                    #dir_path = 'E:\img\{}'.format(dir_name)
                    dir_path = BASE_DIR + dir_name
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)
                    self.down_img(dir_path,img_url)
        return item
    def down_img(self,dir_path,img_url):
        file_name = dir_path + '\\' + img_url.split('/')[-1]
        resp = requests.get(img_url,timeout=30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        with io.open(file_name,'wb') as f:
            f.write(resp.content)



class RenminwangPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            # 下面两个属性要记得添加上，不然会报编码错误
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        if dict(item)['title'] == 'kong_title':
            self.insert_url(item,'kong_title')
        # if dict(item)['content'] == 'kong_content':
        #     self.insert_url(item,'kong_content')
        # if dict(item)['inset'] == 'kong_inset':
        #     self.insert_url(item,'kong_inset')
        # if dict(item)['title'] != 'KONG_TITLE' and dict(item)['content'] != 'KONG_CONTENT':
        else:
            title = pymysql.escape_string(item['title'])
            content = pymysql.escape_string(item['content'])
            inset = pymysql.escape_string(item['inset'])
            url = pymysql.escape_string(item['url'])

            try:
                self.cursor.execute(
                    """insert into tiyu(title,content,inset,url) values ('%s','%s','%s','%s')""" % (title,content,inset,url)
                )
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()

        return item

    def insert_url(self,item,type):
        url = pymysql.escape_string(item['url'])
        cc = re.compile(r'index\d*?.html')
        res = cc.search(url[-15:])
        if res is None:
            try:
                self.cursor.execute(
                    """insert into kong(%s) values ('%s')""" % (type,url)
                )
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()