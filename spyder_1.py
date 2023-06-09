import scrapy


class Spyder1Spider(scrapy.Spider):
    name = 'spyder_1'
    allowed_domains = [r'C:\Users\mvman\projects2\Jobs\Gates_com']
    start_urls = [r"file:///C:\Users\mvman\projects2\Jobs\Gates_com\result_1.html"]

    def parse(self, response):
        yield {
            'URL': response.url,
            "Vladi": "me"
        }
