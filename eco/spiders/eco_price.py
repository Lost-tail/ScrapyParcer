# -*- coding: utf-8 -*-
#скрапим каталог
import scrapy
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url
import w3lib.html
import re

#инициализируем робота из коробки - сканировать карту сайта
class Dd1Spider(SitemapSpider):
    name = "eco_price"
    sitemap_urls = ['https://ecobiolife.ru/sitemap.xml']

    def parse(self, response):
        print("procesing:" + response.url)

        # Извлечение данных с использованием CSS
        if len(response.xpath('(//*[@class="price nowrap"])/text()').extract()) != 0 :
            price = (response.xpath('(//*[@class="price nowrap"])/text()').extract())
        else: 
            price = (response.css('.e-product-prices__general.price::text').extract())

        if len(response.xpath('(//*[@class="articul"])/span/text()').extract()) != 0 :
            artikul_code = (response.xpath('(//*[@class="articul"])/span/text()').extract())
        else: 
            artikul_code = (response.xpath('(//*[@class="e-product-sku"])/span/following-sibling::*[1]/text()').extract())

        
        row_data = zip(price,artikul_code)
        
        #извлечение данных строки
        for item in row_data:
            # создать словарь для хранения извлеченной информации
            scraped_info = {
                'page': response.url,
                'price': (re.sub(r'от', ' ', re.sub(r'\s', '',(re.sub(r'руб.', ' ', item[0]))))),
                'artikul_code': re.sub(r'\s', '', item[1]),
                
            }

            # генерируем очищенную информацию для скрапа
            yield scraped_info
    