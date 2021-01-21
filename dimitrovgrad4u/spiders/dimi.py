import scrapy
from scrapy.loader import ItemLoader
from dimitrovgrad4u.items import Article
from datetime import datetime
from itemloaders.processors import TakeFirst


class DimiSpider(scrapy.Spider):
    name = 'dimi'
    allowed_domains = ['dimitrovgrad4u.com']
    start_urls = ['https://dimitrovgrad4u.com/']

    def parse(self, response):
        titles = response.xpath("//div[@id='content']//article//h4/a/@href").getall()
        yield from response.follow_all(titles, self.parse_article)

        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article(), response)
        item.default_output_processor = TakeFirst()
        title = response.xpath("//h1[@class='title single']/a/text()").get().strip()
        categories = response.xpath("(//div[@class='mg-blog-category'])[1]/a/text()").getall()
        categories = [cat.strip() for cat in categories]
        categories = ", ".join(categories)
        author = response.xpath("//h4[@class='media-heading']/a/text()").get()
        date = response.xpath("(//span[@class='mg-blog-date'])[1]/text()").get().strip()
        date = format_date(date)
        content = response.xpath("//article//text()").getall()
        content = [text for text in content if text.strip() and text != 'Contents' and text != 'hide']
        content = " ".join(content)

        item.add_value('title', title)
        item.add_value('categories', categories)
        item.add_value('author', author)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()


def format_date(date):
    date_dict = {
        "яну.": "January",
        "фев.": "February",
        "мар.": "March",
        "апр.": "April",
        "май": "May",
        "юни": "June",
        "юли": "July",
        "авг.": "August",
        "сеп.": "September",
        "окт.": "October",
        "ное.": "November",
        "дек.": "December",
    }
    date = date.split()
    for key in date_dict.keys():
        if date[0] == key:
            date[0] = date_dict[key]

    date = " ".join(date)
    date_time_obj = datetime.strptime(date, '%B %d, %Y')
    date = date_time_obj.strftime("%Y/%m/%d")
    return date
