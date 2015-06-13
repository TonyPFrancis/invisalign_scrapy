from scrapy import Spider, Selector, log
from scrapy.http import Request
from scrapy.log import ScrapyFileLogObserver
import requests, json, re, urllib
from time import sleep
from invisalign_scrapy.items import InvisalignScrapyItem



class InvisalignSpider(Spider):
    name = 'invisalign'
    start_urls = ['http://www.invisalign.com/find-a-doctor', ]
    allowed_domains = ['invisalign.com']
    TIMEZONE = ''
    BASE_URL = 'http://www.invisalign.com'

    def __init__(self, name=None, **kwargs):
        ScrapyFileLogObserver(open("spider.log", 'w'), level=log.INFO).start()
        ScrapyFileLogObserver(open("spider_error.log", 'w'), level=log.ERROR).start()
        super(InvisalignSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        zip_file = open('CANADA_ZIPCODES.txt', 'r+')
        zip_list = filter(None, zip_file.read().split('\n'))
        for zip_item in zip_list:
            print "*** zip_item"
            print zip_item
            geo_url = 'https://maps.google.com/?q=%s canada'%(zip_item)
            map_url_content = requests.get(geo_url).content
            sleep(3)
            sell = Selector(text=map_url_content)
            map_error_1 = sell.xpath(
                '//div[@class="sp-error-msg"]|//div[@class="noprint res"]/div//div[contains(@id,"marker_B")]')
            latlong = ' '.join(sell.xpath('//script').extract()) if not map_error_1 else ''

