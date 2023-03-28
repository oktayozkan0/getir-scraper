# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetirspiderItem(scrapy.Item):
    main_category = scrapy.Field()
    name = scrapy.Field()
    short_name = scrapy.Field()
    brand = scrapy.Field()
    short_description = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
