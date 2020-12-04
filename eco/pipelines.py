# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import scrapy
from scrapy.exceptions import DropItem
from scrapy.http.request import Request
import csv
import requests
from eco.items import DdItem
#Пайплайн для генерации 1 файла
class Csv1_Writer():
    def __init__(self):
        self.directory = 'data/'#путь(можно изменять), должен быть в папке с проектом, иначе выведет ошибку
        self.fieldnames = ['page','name','price','manufacturer','artikul_code','sort_leather','age','sostav','opisanie','photo1','photo2','photo3','photo4','photo5']
    def process_item(self,item,spider):
        with open(self.directory + 'data1.csv','a') as csvfile:
            writer = csv.DictWriter(csvfile,delimiter = ';',fieldnames=self.fieldnames)
            writer.writerow(item)
        return item
#Пайплайн для генерации 2 файла        
class Csv2_Writer():
    def __init__(self):
        self.directory = 'data/'#путь(можно изменять), должен быть в папке с проектом, иначе выведет ошибку
        self.fieldnames = ['page','name','price','manufacturer','artikul_code','sort_leather','age','sostav','opisanie','photo']
    def process_item(self,item,spider):
        with open(self.directory + 'data.csv','a') as csvfile:
            writer = csv.DictWriter(csvfile,delimiter = ';',fieldnames=self.fieldnames)
            data = dict()
            for i in range(5):
                if item['photo{}'.format(i+1)]:
                    for keys in self.fieldnames:
                        data[keys] = item[keys] if keys !='photo' else item['photo{}'.format(i+1)]
                    writer.writerow(data)
        return item
#Пайплайн для сохранения картинок  
class Image_Downl():
    def __init__(self):
        #путь(можно изменять), должен быть в папке с проектом, иначе выведет ошибку
        self.directory = 'Img/'
    def process_item(self,item,spider):
        for i in range(5):
            if item['photo{}'.format(i+1)]:
                #в данном месте возможно появление ошибок, связанных с некорректным именем файла, если name содержит запрещенные для названия символы (/,\,| и т.д.)
                #поэтому необходимо удалить такие символы
                with open(self.directory+str(item['name']) +str(i)+'.jpg', 'wb') as ph:
                    ph.write(requests.get(spider.domain+item['photo{}'.format(i+1)]).content)
        return item
    