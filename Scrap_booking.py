import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class BookingSpider(scrapy.Spider):

    name = "booking"

    start_urls = [
                    'https://www.booking.com/searchresults.fr.html?ss=Mont+Saint+Michel',
                    'https://www.booking.com/searchresults.fr.html?ss=St+Malo',
                    'https://www.booking.com/searchresults.fr.html?ss=Bayeux',
                    'https://www.booking.com/searchresults.fr.html?ss=Le+Havre',
                    'https://www.booking.com/searchresults.fr.html?ss=Rouen',
                    'https://www.booking.com/searchresults.fr.html?ss=Paris',
                    'https://www.booking.com/searchresults.fr.html?ss=Amiens',
                    'https://www.booking.com/searchresults.fr.html?ss=Lille',
                    'https://www.booking.com/searchresults.fr.html?ss=Strasbourg',
                    'https://www.booking.com/searchresults.fr.html?ss=Chateau+du+Haut+Koenigsbourg',
                    'https://www.booking.com/searchresults.fr.html?ss=Colmar',
                    'https://www.booking.com/searchresults.fr.html?ss=Eguisheim',
                    'https://www.booking.com/searchresults.fr.html?ss=Besancon',
                    'https://www.booking.com/searchresults.fr.html?ss=Dijon',
                    'https://www.booking.com/searchresults.fr.html?ss=Annecy',
                    'https://www.booking.com/searchresults.fr.html?ss=Grenoble',
                    'https://www.booking.com/searchresults.fr.html?ss=Lyon',
                    'https://www.booking.com/searchresults.fr.html?ss=Verdon+Gorge',
                    'https://www.booking.com/searchresults.fr.html?ss=Bormes+les+Mimosas',
                    'https://www.booking.com/searchresults.fr.html?ss=Cassis',
                    'https://www.booking.com/searchresults.fr.html?ss=Marseille',
                    'https://www.booking.com/searchresults.fr.html?ss=Aix+en+Provence',
                    'https://www.booking.com/searchresults.fr.html?ss=Avignon',
                    'https://www.booking.com/searchresults.fr.html?ss=Uzès',
                    'https://www.booking.com/searchresults.fr.html?ss=Nímes',
                    'https://www.booking.com/searchresults.fr.html?ss=Aigues+Mortes',
                    'https://www.booking.com/searchresults.fr.html?ss=Saintes+Maries+de+la+mer',
                    'https://www.booking.com/searchresults.fr.html?ss=Collioure',
                    'https://www.booking.com/searchresults.fr.html?ss=Carcassonne',
                    'https://www.booking.com/searchresults.fr.html?ss=Ariege',
                    'https://www.booking.com/searchresults.fr.html?ss=Toulouse',
                    'https://www.booking.com/searchresults.fr.html?ss=Montauban',
                    'https://www.booking.com/searchresults.fr.html?ss=Biarritz',
                    'https://www.booking.com/searchresults.fr.html?ss=Bayonne',
                    'https://www.booking.com/searchresults.fr.html?ss=La+Rochelle',]

    def parse(self, response):

        city = response.xpath("substring-before(/html/body/div[5]/div/div[4]/div[1]/div[1]/div[1]/div/div/h1/text(), ':')").get()
        hotels = response.xpath("/html/body/div[5]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]/div")
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
