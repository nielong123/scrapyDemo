# -*-coding: utf-8
import logging

from scrapy import Request
from scrapy.spiders import Spider
import sys, os
from scrapy import log

reload(sys)
sys.setdefaultencoding("utf-8")

from BotanyClassify.items import DmozItem

base = "d:/dataset/"


class DmozSplider(Spider):
    name = 'dmoz'
    # allowed_domains = ['aims.fao.org']
    start_urls = [
        'http://aims.fao.org/standards/agrovoc/linked-data',
        # 'http://aims.fao.org/aos/agrovoc/c_130.html',
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            link = sel.xpath('a/@href').extract()
            for url in link:
                if url.find('http://aims.fao.org/aos/agrovoc/c') == 0:
                    url += '.html'
                    print 'url = ' + url
                    yield Request(url, callback=self.parse_child_1_content)

    def parse_child_1_content(self, response):
        dmozItem = DmozItem()
        info = response.xpath("//div[@id='header']").extract()
        if len(info) != 0:
            kind = info[0].encode('utf-8').lstrip().rstrip().strip().replace('\r', '').replace('\n', '').replace('\t',
                                                                                                                 '')
            if kind.strip != '':
                if kind.find('<br>') != -1:
                    start = kind.index('<br>') + 4
                    end = kind.index('</div>')
                    dmozItem['info'] = info[0][start:end]
                    print dmozItem['info']

                    dmozItem['links'] = response.xpath(
                        '//*[@id="left"]//table[@class="customTable"][1]//tbody//tr[@class="customTableEvenRow"][2]/td').xpath(
                        'a/@href').extract()
                    yield dmozItem

                    if len(dmozItem['links']) != 0:
                        for link in dmozItem['links']:
                            if link.find('http://aims.fao.org/aos/agrovoc/c') == 0:
                                print 'child link _1 = ' + link
                                link += '.html'
                                log.msg("child item...", level=logging.INFO)
                                yield Request(link, callback=self.parse_child_1_content)
                log.msg("this level done.", level=logging.INFO)
            else:
                print 'not find <br>'
