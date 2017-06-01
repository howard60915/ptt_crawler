# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    comment = scrapy.Field()
    content = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    # pass
