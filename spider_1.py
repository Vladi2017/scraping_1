import scrapy
import scrapy.http.response.html
from scrapy.selector import Selector
from scrapy.selector import SelectorList

# reference file: my:rpr:C:\Users\mvman\projects2\Jobs\Gates_com\Vld1.txt#1 , 23:08 6/9/2023
class Spyder1Spider(scrapy.Spider):
    name = 'spider_1'
    # allowed_domains = [r'C:\Users\mvman\projects2\Jobs\Gates_com']
    # start_urls = [r"file:///C:\Users\mvman\projects2\Jobs\Gates_com\result_1.html"]
    allowed_domains = ['www.gates.com']
    start_urls = [r"https://www.gates.com/us/en/ymm/search/vehicle/result.html?equipment-clazz=Buses&vehicle-type=School+Buses&year=2017&make=International%2FNavistar&model=CE&engine=Cummins+ISB6.7+Diesel"]

    def parse(self, response: scrapy.http.response.html.HtmlResponse):
        """ yield {
            'URL': response.url,
            "me": "Vladi"
        } """
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
                    yield {
                        "Category" : categN,
                        "Subcategory" : scn,
                        "Application" : app,
                        "Product Type" : prType,
                        "Part#" : part,
                        "Comments" : comments
                    }