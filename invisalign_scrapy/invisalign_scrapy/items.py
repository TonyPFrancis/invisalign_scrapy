# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field,Item


class InvisalignScrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    address = Field()
    phone = Field()
    type = Field()
    category = Field()