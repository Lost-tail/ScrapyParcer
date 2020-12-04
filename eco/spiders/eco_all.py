# -*- coding: utf-8 -*-
#скрапим каталог
import scrapy
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url
import w3lib.html
import re
from eco.items import DdItem#Импорт класса, прописанного в items

#инициализируем робота из коробки - сканировать карту сайта
class Dd1Spider(SitemapSpider):
    name = "eco_all"
    sitemap_urls = ['https://ecobiolife.ru/sitemap.xml']
    domain = 'https://ecobiolife.ru'
    def parse(self, response):
        print("procesing:" + response.url)

        # Извлечение данных с использованием CSS
        if len(response.css('.e-product-info__title::text').extract()) != 0 :
            name = (response.css('.e-product-info__title::text').extract())
        else: 
            name = (response.css('h1.category-name::text').extract())
        
        if len(response.xpath('(//*[@class="price nowrap"])/text()').extract()) != 0 :
            price = (response.xpath('(//*[@class="price nowrap"])/text()').extract())
        else: 
            price = (response.css('.e-product-prices__general.price::text').extract())
        
        """if len(response.xpath('(//td[text()="Бренд  "])/following-sibling::*/text()').extract()) != 0 :
            manufacturer = (response.xpath('(//td[text()="Бренд  "])/following-sibling::*/text()').extract())
        else: 
            manufacturer = (response.xpath('(//*[text()="Бренд  "])/../following-sibling::*[1]/span/text()').extract())
        
        if len(response.xpath('(//*[@class="articul"])/span/text()').extract()) != 0 :
            artikul_code = (response.xpath('(//*[@class="articul"])/span/text()').extract())
        else: 
            artikul_code = (response.xpath('(//*[@class="e-product-sku"])/span/following-sibling::*[1]/text()').extract())
        
        if len(response.xpath('(//td[text()="Тип кожи"])/following-sibling::*/text()').extract()) != 0:
            sort_leather = (response.xpath('(//td[text()="Тип кожи"])/following-sibling::*/text()').extract())
        else: 
            sort_leather = (response.xpath('(//*[text()="Тип кожи"])/../following-sibling::*[1]/span/text()').extract())
       
        if len(response.xpath('(//td[text()="Возраст"])/following-sibling::*/text()').extract()) != 0:
            age = (response.xpath('(//td[text()="Возраст"])/following-sibling::*/text()').extract())
        else: 
            age = (response.xpath('(//*[text()="Возраст"])/../following-sibling::*[1]/span/text()').extract())

        if len(response.xpath('//*[text()="Состав:"]/following::*/text()').extract()) != 0:
            sostav = (response.xpath('//*[text()="Состав:"]/following::*/text()').extract())
        else:
            sostav = (response.xpath('//*[text()="Состав:"]/following::*/text()').extract())"""

        if len(response.css('.panel-body').extract()) != 0:
            opisanie = (response.css('.panel-body').extract())
        else:
            opisanie = (response.css('.e-product-description__content').extract())
            
        photos = [None]*5
        """
        Создаю список для хранения урл изображений
        Для первого типа карточек, главное фото хранится отдельно, поэтому сперва пытаюсь получить его, если не получается, значит второй тип карточки
        """
        try:
            photos[0] = response.xpath('//div[contains(@id,"product-core-image")]/a[@href]/@href')[0].get()
            for i,x in enumerate(response.xpath('//*[@id="product-gallery"]/div[contains(@class, "push-to-fancybox image")]/a[@href]/@href')):
                photos[i] = x.get()
        except:
            for i,x in enumerate(response.xpath('//div[contains(@class,"e-product-image__list js-product-image-list owl-carousel")]/div/a[@href]/@href')):
                photos[i] = x.get()
        
        
        Item = DdItem()
        Item['page'] = response.url
        Item['name'] = name
        Item['price'] = 20#(re.sub(r'от', ' ', re.sub(r'\s', '',(re.sub(r'руб.', ' ', price)))))
        Item['manufacturer'] = None#re.sub(r'\s', '', manufacturer)
        Item['artikul_code'] = None#re.sub(r'\s', '',  artikul_code)
        Item['sort_leather'] =  None#re.sub(r'\s+', ' ', sort_leather)
        Item['age'] = None#re.sub(r'\s+', ' ', age)
        Item['sostav'] = None#re.sub(r'\s+', ' ', w3lib.html.remove_tags(sostav))
        Item['opisanie'] = None#re.sub(r'<div class="e-product-description__content" itemprop="description">', ' ', re.sub(r'<div class="panel-body">', ' ',opisanie.split("<p><strong>Страна производства")[0]))
        Item['photo1'] = photos[0]
        Item['photo2'] = photos[1]
        Item['photo3'] = photos[2]
        Item['photo4'] = photos[3]
        Item['photo5'] = photos[4] 
        yield Item
    