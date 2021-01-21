import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    categories = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
