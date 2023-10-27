# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StackoverflowScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class StackoverflowQTItems(scrapy.Item):

    title = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    score = scrapy.Field()
    answer_count = scrapy.Field()
    views = scrapy.Field()
    creation_date = scrapy.Field()
    first_answer_date = scrapy.Field()


