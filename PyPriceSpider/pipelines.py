# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class PyPriceSpiderPipeline():

    CurrentData = []

    def __init__(self):
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                self.CurrentData = json.load(file)
        except:
            self.CurrentData = []
    
    def close_spider(self, spider):
        self.process_items(spider)
    
    def process_items(self, spider):
        for item in spider.items:
            jsonObj = dict(Name = item.get("name"), Prices = [item.get("price")])

            if "Name" in jsonObj and jsonObj["Prices"][0]:
                for x in self.CurrentData:
                    if x["Name"] == jsonObj["Name"]:
                        x["Prices"].append(jsonObj["Prices"][0])
                        break
                else:
                    self.CurrentData.append(jsonObj)

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(
                self.CurrentData,
                file,
                sort_keys = True,
                indent = 4,
                ensure_ascii = False)

    # def process_item(self, item, spider):
    #     jsonObj = dict(Name = item.get("name"), Prices = [item.get("price")])

    #     if "Name" in jsonObj and jsonObj["Prices"][0]:
    #         for x in self.CurrentData:
    #             if x["Name"] == jsonObj["Name"]:
    #                 x["Prices"].append(jsonObj["Prices"][0])
    #                 break
    #         else:
    #             self.CurrentData.append(jsonObj)

    #         with open('data.json', 'w') as file:
    #             json.dump(
    #                 self.CurrentData,
    #                 file,
    #                 sort_keys = True,
    #                 indent = 4,
    #                 ensure_ascii = False)
    #     yield item
