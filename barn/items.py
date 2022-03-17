# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BarnItem(scrapy.Item):
    
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    category3 = scrapy.Field()
    id = scrapy.Field()
    product_code = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    product_url = scrapy.Field()
    price = scrapy.Field()

