# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名称
    name = 'douban_spider'
    # 设置允许爬取的域(可以指定多个)
    allowed_domains = ['movie.douban.com']
    # 设置起始url(设置多个) 扔到调度器里面
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
       movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
       # 循环电影信息
       for i_item in movie_list:
           douban_item = DoubanItem()
           #xpath数据解析
           douban_item['serial_number'] =i_item.xpath(".//div[@class='item']//em/text()").extract_first()
           douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
           content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
           for i_content in content:
               contents = "".join(i_content.split())
               douban_item['introduce'] = contents
           douban_item['star'] = i_item.xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[2]/text()").extract_first()
           douban_item['evaluate'] = i_item.xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[4]/text()").extract_first()
           douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
           print(douban_item)
           #第一页数据yeild到管道
           yield douban_item
       #解析下一页
       next_link = response.xpath("//span[@class='next']/link/@href").extract()
       if next_link:
           next_link = next_link[0]
           yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)



