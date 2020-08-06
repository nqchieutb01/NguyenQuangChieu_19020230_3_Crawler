import scrapy
import json
from datetime import datetime

OUTPUT_FILE = 'C:/Users/ADMIN/PycharmProjects/Hamy/tutorial/tutorial/Output/vnexpress3_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
class VnexpressSpider(scrapy.Spider):
    name = 'run'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net']
    cnt = 0
    def parse(self, response):
      #  print("111")
        if response.status == 200 and response.css('meta[name="tt_page_type"]::attr("content")').get() == 'article' :
            #print("222")
            print('Crawling from: ',response.url)

            data ={
                'link': response.url,
                'title': response.css('h1.title-detail::text').get(),
                'content': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('article.fck_detail p.Normal')
                ]),
                'author' : response.css('strong::text').get() ,
                'time' : response.xpath("//div[@class='header-content width_common']/span[@class='date']/text()").extract()
            }
            with open(OUTPUT_FILE, 'a',encoding='utf8') as f:
                f.write(json.dumps(data,ensure_ascii=False))
                f.write('\n')
        yield from response.follow_all(css='a[href^="https://vnexpress.net"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)

