import scrapy
from PIL import Image
from collections import OrderedDict

arr = OrderedDict()
class AliexpressTabletsSpider(scrapy.Spider):
    name = 'vnn'
    start_urls = ['https://baotintuc.vn/thoi-su/thu-tuong-nguyen-xuan-phuc-chu-tri-phien-hop-chinh-phu-thuong-ky-thang-7-20200803091032205.htm']
    begin = "https://baotintuc.vn/thoi-su/thu-tuong-nguyen-xuan-phuc-chu-tri-phien-hop-chinh-phu-thuong-ky-thang-7-20200803091032205.htm"
    arr.update({begin:1})
    def parse(self, response):

        title = response.css('.detail-title::text').extract()
        time = response.css('.date .txt').css('::text').extract()
        row_data=zip(title,time)

        for item in row_data:
            scraped_info = {
                #key:value
                'title' : item[0].strip() ,
                'time' : item[1].strip()
            }
            yield scraped_info
        next_page =  response.xpath(".//a/@href").extract()
        for link_nxt in next_page :
            if link_nxt and not link_nxt in arr.keys():
                 arr.update({link_nxt:1})
                 yield scrapy.Request(
                    response.urljoin(link_nxt),
                    callback=self.parse)

