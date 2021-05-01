import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class QuotesSpider(scrapy.Spider):

    name = 'quotes_spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']
    
    def __init__(self, *args, **kwargs):
        
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path='./chromedriver', options=option)
        
        super(QuotesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        
        self.driver.get(response.url)
        for quote in self.driver.find_elements_by_css_selector('div.quote'):
            yield {
                'quote': quote.find_element_by_css_selector("span.text").text,
                'author': quote.find_element_by_css_selector("small.author").text,
                'tags': [e.text for e in quote.find_elements_by_class_name('tag')],
            }
            
        
        next_page = response.css("li.next > a::attr(href)").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
