import scrapy
import json
from ..items import GetirspiderItem


class GetirSpider(scrapy.Spider):
    name = "getir"

    def start_requests(self):
        yield scrapy.Request("https://getir.com", callback=self.get_categories)

    def get_categories(self, response):
        category_json = json.loads(response.xpath("//script[@id='__NEXT_DATA__']/text()").get())
        categories = category_json["props"]["pageProps"]["initialState"]["getirListing"]["categories"]["data"]
        build_id = category_json["buildId"]

        for category in categories:
            category_slug = category["slug"]
            category_url = f"https://getir.com/_next/data/{build_id}/tr/categoryPage/{category_slug}.json?slug={category_slug}"
            yield scrapy.Request(category_url, callback=self.category_parser)

    def category_parser(self, response):
        data = response.json()
        main_category = data["pageProps"]["initialPageTitle"]

        for products in data["pageProps"]["initialState"]["getirListing"]["products"]["data"]:
            for product in products["products"]:
                item = GetirspiderItem()
                item["main_category"] = main_category
                item["name"] = product["name"]
                item["short_name"] = product["shortName"]
                item["brand"] = product["brand"]["name"]
                item["short_description"] = product["shortDescription"]
                item["price"] = product["price"]
                item["currency"] = product["currency"]["codeAlpha"]
                yield item