# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from scrapy import signals
import json
import codecs
import sys
from scrapy import log

from scrapy.exporters import JsonItemExporter

reload(sys)
sys.setdefaultencoding('utf-8')

data = None


class JsonPipline(object):
    def open_spider(self, spider):
        self.file = codecs.open('data.json', 'wb', encoding='utf-8')
        pass

    def process_item(self, item, spider):
        print 'process_item'
        if item is not None:
            print type(item)
            if item['links'] is not None:
                print type(item['links'])
                for link in item['links']:
                    if link.find('http://aims.fao.org/aos/agrovoc/c') != 0:
                        log.msg("link = " + link, level=logging.INFO)
                        item['links'].remove(link)
                line = json.dumps(dict(item)) + "\n"
                print 'line = ' + line
                self.file.write(line)
        else:
            print 'item is None'
        return item

    def close_spider(self, spider):
        self.file.close()
        print 'close_spider'
