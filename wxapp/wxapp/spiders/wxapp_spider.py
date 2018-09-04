# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem


class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),  # 所有页面url
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback="parse_detail", follow=False),  # 每个文章的url
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='ph']/text()").get()  # 标题
        author_p = response.xpath("//p[@class='authors']")  # 作者的p标签
        author = author_p.xpath(".//a/text()").get()  # 作者
        pub_time = author_p.xpath(".//span/text()").get()  # 发布时间
        content = response.xpath("//td[@id='article_content']//text()").getall()
        content = "".join(content).strip()  # 文章内容

        item = WxappItem(title=title, author=author, pub_time=pub_time, content=content)
        yield item


