# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class DdItem(scrapy.Item):
    page = Field()
    name = Field()
    price = Field()
    manufacturer = Field()
    artikul_code = Field()
    sort_leather = Field()
    age = Field()
    sostav = Field()
    opisanie = Field()
    photo1 = Field()
    photo2 = Field()
    photo3 = Field()
    photo4 = Field()
    photo5 = Field()