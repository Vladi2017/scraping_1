from time import ctime
import scrapy
import scrapy.http.response.html
from scrapy.selector import Selector
from scrapy.selector import SelectorList
import urllib3

# reference file: my:rpr:C:\Users\mvman\projects2\Jobs\Gates_com\Vld1.txt#1 , 23:08 6/9/2023
class Spyder1Spider(scrapy.Spider):
    name = 'spider_1'
    # allowed_domains = [r'C:\Users\mvman\projects2\Jobs\Gates_com']
    start_urls = [r"file:///C:\Users\mvman\projects2\Jobs\Gates_com\test1\equipment-clazz=Buses&vehicle-type=School+Buses&year=2017&make=International%2FNavistar&model=CE&engine=Cummins+ISB6.7+Diesel", r"file:///C:\Users\mvman\projects2\Jobs\Gates_com\test1\equipment-clazz=Passenger+Cars+%26+Light+Trucks&vehicle-type=Light+Trucks&year=2022&make=BMW&model=X3&engine=6-Cyl.+3.0+L+Electric+Assist"]
    custom_settings = {
        "DOWNLOAD_DELAY" : "5",
        "CONCURRENT_REQUESTS_PER_DOMAIN" : "1",
        "ROBOTSTXT_OBEY" : "False",
        "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    # allowed_domains = ['www.gates.com']
    # start_urls = [r"https://www.gates.com/us/en/ymm/search/vehicle/result.html?equipment-clazz=Buses&vehicle-type=School+Buses&year=2017&make=International%2FNavistar&model=CE&engine=Cummins+ISB6.7+Diesel"]
    # base_url = r"https://www.gates.com/us/en/ymm/search/vehicle/result.html?"
    base_url = "C:\\Users\\mvman\\projects2\\Jobs\\Gates_com\\test1\\"  # dont support raw string bexause of last backslash..

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        print(f"{ctime()}: tag._1: received response.!")
        url = response.url
        queryStr = url.replace(self.base_url, "")
        fcd: dict = urllib3.parse.parse_qs(queryStr) #1stColumsDictionay
        for k in fcd.keys(): fcd[k] = fcd[k][0]
        apc = response.xpath('//ul[contains(@class, "gor-accordion nested-accordion")]') #{apc=AllProductsContainer (in the current page)}
        categs: SelectorList = apc[0].xpath("child::li") #{axis, works also without mo."[0]". categs = (the) categoriesList}
        categ: Selector = None  # for VSC hints.
        for categ in categs:
            categN = categ.xpath("./a/h2/text()").get().strip("\xa0 \t\n")  # categoryName
            subCategs = categ.xpath("./div/ul/li")
            subCateg: Selector
            for subCateg in subCategs:
                scn = subCateg.xpath("./a/text()").get().strip("\xa0 \t\n")  # subCategName.
                products = subCateg.xpath(".//tbody/tr")
                product: Selector = None
                for product in products:
                    app = product.xpath("./td[1]/text()").get().strip("\xa0 \t\n")
                    prType = product.xpath("./td[2]/text()").get().strip("\xa0 \t\n")
                    part = product.xpath("./td[3]/a/text()").get().strip("\xa0 \t\n")
                    comments = ""
                    sL = list(map(lambda s: s.strip("\xa0 \t\n"), product.xpath("./td[4]//text()").getall()))
                    for s in sL:
                        if s:
                            comments = s
                            break
                    lcd = { #lastColumsDictionay
                        "Category" : categN,
                        "Subcategory" : scn,
                        "Application" : app,
                        "Product Type" : prType,
                        "Part#" : part,
                        "Comments" : comments,
                        "Link" : url}
                    url = ""
                    yield fcd.update(lcd)
