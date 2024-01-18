import os 
import logging
import pickle
import scrapy
from scrapy.crawler import CrawlerProcess

with open ('urls.pkl', 'rb') as fp:
    url_list = pickle.load(fp)

class BookingSpider(scrapy.Spider):

    name = "booking"

    start_urls = url_list

    def parse(self, response):
        city = response.xpath("substring-before(/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/h1/text(), ':')").get()
        hotels = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div")
        for hotel in hotels:
            name = hotel.xpath("div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a/div[@data-testid='title']/text()").get()
            url = hotel.xpath("div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a[@data-testid='title-link']/@href").get()
            score = hotel.xpath("div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/a/span/div/div[1]/text()").get()                  
            yield scrapy.Request(response.urljoin(url), cb_kwargs={'name': name, 'score': score, 'city' : city}, callback=self.parse_hotel)

    def parse_hotel(self, response, name, score, city):

        coord = response.xpath('//*[@id="hotel_sidebar_static_map"]/@data-atlas-latlng').get()
        desc = response.xpath("//div[@id='property_description_content']/div/p/text()").get()
        yield {'city' : city,
               'name': name,
               'coord' : coord,
               'score' : score, 
               'desc' : desc,
               'url' : response.url}

filename = "Hotels.json"


if filename in os.listdir('./'):
        os.remove('./' + filename)


process = CrawlerProcess(settings = {
    'USER_AGENT': 'Firefox/117.0.1',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        './' + filename : {"format": "json"},
    },
    'DOWNLOAD_DELAY': 5,
    "AUTOTHROTTLE_ENABLED": True,
    "COOKIES_ENABLED": False
}) 

# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()
