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
            lat_lng = re.findall(r'",\[(-?\d+\.?\d*),(-?\d+\.?\d*)\]\]', latlong, re.I)
            venue_latitude, venue_longitude = lat_lng[0] if lat_lng else ('', '')
            print venue_latitude, venue_longitude
            if not venue_latitude or not venue_longitude:
                with open('missing_lat_lng.txt', 'a+') as d:
                    print "*** DROPPED ZIP - %s"%(zip_item)
                    d.write(zip_item+'\n')
                print "NO LATITUDE OR LONGITUDE"
            else:
                fetch_url = 'http://api.invisalign.com/svc/rd?pc=%s&cl=CA&lat=%s&lng=%s&it=us'%(zip_item, venue_latitude, venue_longitude)
                meta_data = {'venue_latitude': venue_latitude,
                             'venue_longitude': venue_longitude,
                             'zip_code': zip_item}
                yield Request(url = fetch_url, dont_filter=True, callback=self.parse_result, meta=meta_data)

    def parse_result(self, response):
        sel = Selector(response)
        meta_data = response.meta
        zip_item = meta_data['zip_code']

        json_data = json.loads(response.body)
        responseData = json_data.get('responseData', {})
        if responseData:
            results = responseData.get('results', [])
            if results:
                for result in results:
                    item = self.create_item(result, zip_item)
                    try:
                        self.item_check(item)
                        yield item
                    except Exception as e:
                        with open('dropped.txt', 'a+') as d:
                            print "*** DROPPED item - %s"%(str(e))
                            d.write(zip_item+'\n')

            else:
                with open('invalid_json_zip.txt', 'a+') as d:
                    print "*** INVALID JSON ZIP - %s"%(zip_item)
                    d.write(zip_item+'\n')
        else:
            with open('invalid_json_zip.txt', 'a+') as d:
                print "*** INVALID JSON ZIP - %s"%(zip_item)
                d.write(zip_item+'\n')

    def create_item(self, result, zip_item):
        name = result.get('FullName', '')
        address = '. '.join(filter(None, [result.get('Line1', ''), result.get('Line2', ''), result.get('City', ''), result.get('State', ''), result.get('PostalCode', '')]))
        phone = result.get('OfficePhone', '')
        type = result.get('DoctorType', '')
        if type == 'D':
            type = 'General Dentist'
        elif type == 'C':
            type = 'Orthodontist'
        category = result.get('SegmentCode', '')
        if category == 1:
            category = 'Top 1%'
        elif category == 2:
            category = 'Elite'
        elif category == 3:
            category = 'Premier'
        elif category == 4:
            category = 'Preferred'
        item = InvisalignScrapyItem(name = name,
                                    address = address,
                                    phone = phone,
                                    type = type,
                                    category = category,
                                    zip = zip_item)
        return item

    def item_check(self, item):
        if not item['name']:
            raise AssertionError('Name missing')
        if not item['address']:
            raise AssertionError('address missing')
        if not item['phone']:
            raise AssertionError('phone missing')
        if not item['type']:
            raise AssertionError('type missing')
        if not item['category']:
            raise AssertionError('category missing')
        if not item['zip']:
            raise AssertionError('zip missing')


