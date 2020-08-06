import scrapy
from collections import OrderedDict

arr = OrderedDict()
class Comment(scrapy.Spider):
    name = 'hic'
    start_urls = ['https://www.amazon.com/Roku-Express-Streaming-Media-Player/dp/B07WVFCVJN/ref=lp_16225007011_1_1?s=computers-intl-ship&ie=UTF8&qid=1596440209&sr=1-1']
    begin_url = "https://www.amazon.com/Roku-Express-Streaming-Media-Player/dp/B07WVFCVJN/ref=lp_16225007011_1_1?s=computers-intl-ship&ie=UTF8&qid=1596440209&sr=1-1"
    arr.update({begin_url:1})
    def parse(self, response):
        print("procesing:" + response.url)
        title = response.css('#productTitle::text').extract()
        rating = response.css('#acrCustomerReviewText::text').extract()
        price = response.css('#priceblock_ourprice::text').extract()
        comment = response.xpath("//div[@data-hook = 'review-collapsed']/span/text()").extract()

        sc = zip(comment)
        for item in sc:
            cmt = {
                'comment': item[0].strip()
            }
            yield cmt
        row_data = zip(title,rating,price)
        for item in row_data:
            scraped_info = {
                'title': item[0].strip(),
                'rating':item[1].strip(),
                'price' : item[2].strip()
            }
            yield scraped_info
        next_page =  response.xpath(".//a[@class='a-link-normal']/@href").extract()
        for link_nxt in next_page :
            if link_nxt and not link_nxt in arr.keys():
                 arr.update({link_nxt:1})
                 yield scrapy.Request(
                    response.urljoin(link_nxt),
                    callback=self.parse)
# scrapy crawl hic -o test.json
