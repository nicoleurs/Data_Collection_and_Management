
# Import os => Library used to easily manipulate operating systems
## More info => https://docs.python.org/3/library/os.html
import os 

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess

class OneweekSpider(scrapy.Spider):

    name = "booking"

    start_urls = [
        'https://one-week-in.com/35-cities-to-visit-in-france/',
    ]

    def parse(self, response):

        cities = response.xpath("/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/article/div/div[2]/ol/li")
        for city in cities:
            yield {
                'city' : city.xpath("a/text()").get()
            }

filename = "Best_cities.json"


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
process.crawl(OneweekSpider)
process.start()
