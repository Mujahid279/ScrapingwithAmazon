import scrapy
from ..items import AmazonItem


class AmzSpider(scrapy.Spider):
    name = 'amz'
    start_urls = [
        'https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A1292115011&ref=nav_em__nav_desktop_sa_intl_monitors_0_2_6_8']

    def parse(self, response):
        all_quotes = response.css('.s-latency-cf-section')
        items = AmazonItem()
        for q in all_quotes:

            title = q.css('.a-color-base.a-text-normal::text').extract()
            price = q.css('.a-price span span::text').extract()
            rank = q.css('span.a-icon-alt::text').extract()
            if not (title and price):
                print("empty")
            else:
                if len(title) > 1:
                    print(" found")
                else:
                    items['title'] = title
                    items['price'] = price
                    items['rank'] = rank
                    yield items
        nex_page = response.css('li.a-last a::attr(href)').get()
        if nex_page is not None:
            yield response.follow(nex_page, callback=self.parse)
