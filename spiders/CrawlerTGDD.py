import scrapy
from PIL import Image


class AliexpressTabletsSpider(scrapy.Spider):
    name = 'Name'
   # allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.thegioididong.com/laptop']
    def parse(self, response):

        print("procesing:"+response.url)

        price = response.xpath("//div[@class='price']/strong/text()").extract()
        product_name = response.xpath("//h3/text()").extract()
        product_ram = response.xpath("//div[@class='props']/span/text()").extract()
        product_gift = response.xpath("//div[@class='promo']/p/text()[1]").extract()
        product_gift1 = response.xpath("//div[@class='promo']/p/b/text()").extract()

        images = response.css('.laptop img::attr(src)').extract()
        print("hello")
        print(len(images))
        name = []
        for i in range(1,len(product_name)):
            name.append(product_name[i])
        row_data=zip(price,name,product_ram,product_gift,product_gift1,images)

        #Making extracted data row wise
        for item in row_data:
            scraped_info = {
                #key:value
                'page':response.url,
                'price' : item[0],
                'product_name' : item[1],
                'config' : item[2] ,
                'gift' : item[3] + item[4] ,
                'image_urls': [item[5]]
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
