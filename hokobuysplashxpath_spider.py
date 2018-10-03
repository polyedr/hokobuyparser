#!/usr/bin/python
import scrapy
from scrapy_splash import SplashRequest


class AuthorSpider(scrapy.Spider):
    name = 'hokobuysplash'

    start_urls = [
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=1',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=2',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=3',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=4',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=5',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=6',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=7',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=8',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=9',
        'https://www.hokobuy.com/search?q=%3Ahokobuy-landingSequence-sort%3Acategory%3AAA30050000000%3A&page=10',
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 6,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 3.0},)

    def parse(self, response):
        for href in response.css('#product-container a::attr(href)'):
            print(href)
            yield response.follow(href, self.parse_item)

        for href in response.css('ul#pagination-container.pagination li.next a::attr(href)'):
            yield SplashRequest(href, self.parse)

    def parse_item(self, response):
        def extract_with_xpath(query):
            try:
                return response.xpath(query).extract_first().strip()
            except:
                return ("0")
        yield{
            'title': extract_with_xpath('//div[@class="merchant_website"]/div[@class="title"]/span/text()'),
            'map-address': extract_with_xpath('//div[@class="merchant_redeem_address"]/ul/li/p/text()'),
            'website_link': extract_with_xpath('//div[@id="merchantInfo_section"]//div[@class="merchant_website"]//div[@class="website_section"]//div[@class="website"]/a/@href'),
            'instances-phones': extract_with_xpath('//div[@id="fineprint_section"]/div[@class="Content"]'),
            'facebook_link': extract_with_xpath('//div[@class="deals_main_section"]//div[@class="detail_section"]//div[@id="description_section"]//div[@class="Content"]//a[contains(@href, "facebook")]/@href'),
        }
