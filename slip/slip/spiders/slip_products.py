from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SlipItem
from scrapy.loader import ItemLoader


class SlipProductsSpider(CrawlSpider):
    name = "slip-products"
    allowed_domains = ["slip.com"]
    start_urls = ["https://www.slip.com/collections/shop-all"]
    rules = (
        Rule(LinkExtractor(allow=(r"page="))),
        Rule(
            LinkExtractor(allow=(r"products")),
            callback="parse_item",
        ),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=SlipItem(), response=response)
        loader.add_css("product_name", "h1[class='h3 product__title']")
        loader.add_css("price", "strong.product__price")

        return loader.load_item()
