import scrapy
import json


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
                yield {
                    "main_category": main_category,
                    "name": product["name"],
                    "short_name": product["shortName"],
                    "brand": product["brand"]["name"],
                    "short_description": product["shortDescription"],
                    "price": product["price"],
                    "currency": product["currency"]["codeAlpha"],
                }
