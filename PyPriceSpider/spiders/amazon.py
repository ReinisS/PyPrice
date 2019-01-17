import scrapy
from .helper import *
from ..items import *

class AmazonSpider(scrapy.Spider):
    name = 'amazon-xpath'
    allowed_domains = ['amazon.com']

    items = []

    nameXpath = '//*[@id="productTitle"]/text()'
    priceXpath = '//*[@id="priceblock_ourprice"]/text()'

    # def __init__(self):
        # #super(AmazonSpider, self).__init__() 
        # #self.start_urls = start_urls

    def parse(self, response):
        item = PyPriceSpiderItem(
            name = parseString(response.xpath(self.nameXpath)),
            price = parseString(response.xpath(self.priceXpath))
            #rating = parseString(response.xpath(self.ratingXpath))
            #asin = parseString(response.xpath(self.asinXpath))
        )
        self.items.append(item)
        yield item
