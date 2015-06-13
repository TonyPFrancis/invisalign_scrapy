from scrapy import Spider
from scrapy.log import ScrapyFileLogObserver
from scrapy import log

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