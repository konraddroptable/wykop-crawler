import scrapy
import re
from Wykop.items import WykopItem, Comment, Subcomment, Author
import datetime


class WykopSpider(scrapy.Spider):
    name = "Wykop"
    allowed_domains = ["wykop.pl"]
    start_urls = ["http://www.wykop.pl/strona/" + str(i) + "/" for i in range(1, 2794)]
    xpath_url = "//div[@class='grid-main grid-main m-reset-margin']//ul[@id='itemsStream']/li[@class='link iC ']//div[@class='media-content m-reset-float']/a/@href"
    
    def parse(self, response):
        for href in response.xpath(self.xpath_url):
            url = "http://www.wykop.pl" + href.extract()
            yield scrapy.Request(url, callback=self.parse_content)
            
    def parse_content(self, response):
        item = WykopItem()
        
        item["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        item["date"] = response.xpath("//div[@class='space information bdivider']/div[position()=1]//time/@title").extract()[0]
        item["title"] = response.xpath("//div[@class='lcontrast m-reset-float m-reset-margin']/h2/a/text()").extract()[0]
        item["desc"] = response.xpath("//div[@class='lcontrast m-reset-float m-reset-margin']/div[last()]/p/a/text()").extract()[0]
        item["tags"] = response.xpath("//div[@class='lcontrast m-reset-float m-reset-margin']/div[@class='fix-tagline']/a[position()>1]/text()").extract()
        item["likes"] = response.xpath("//a[@href='#voters']/b/text()").extract()[0]
        item["dislikes"] = response.xpath("//a[@href='#votersBury']/b/text()").extract()[0]
        item["views"] = response.xpath("//a[@class='donttouch']//b/text()").extract()[0]
        
        item["author"] = self.parse_author(response)
        item["comments"] = self.parse_comments(response)
        
        yield item
    
    def parse_author(self, response):
        author = Author()
        
        author["username"] = response.xpath("//div[@class='usercard']//b/text()").extract()[0]
        author["signup_date"] = response.xpath("//div[@class='usercard']//span[@class='info']/time/@title").extract()[0]
        author["nick_color"] = response.xpath("//div[@class='usercard']//a[last()]/span/@class").extract()[0]
        
        return author
    
    def merge_text(self, s_list):
        return str.join('', s_list)
    
    def parse_comments(self, response):
        comments = []     
        
        for iter_comment in range(1, len(response.xpath("//ul[@class='comments-stream']/li[@class='iC']")) + 1):
            comments.append(self.parse_single_comment(response, str(iter_comment)))
        
        return comments
    
    def parse_single_comment(self, response, i):
        comment = Comment()
        single_comment = Subcomment()
                
        single_comment["username"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/div[1]/div/div[@class='author ellipsis']/a[1]/b/text()").extract()[0]
        single_comment["text"] = self.merge_text(response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/div[1]//div[@class='text']/p/text()").extract())
        single_comment["tags"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/div[1]//div[@class='text']//a[@class='showTagSummary']/text()").extract()
        single_comment["shouts"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/div[1]//div[@class='text']/p/a[@class='showProfileSummary']/text()").extract()        
        single_comment["score"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/div[1]//div[@class='author ellipsis']/p/@data-vcp").extract()[0]
        single_comment["date"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/div[1]//div[@class='author ellipsis']//small/time/@title").extract()[0]
        
        comment["comment"] = dict(single_comment)
        comment["subcomments"] = self.parse_subcomments_per_comment(response, i)
        
        return comment    
    
    def parse_subcomments_per_comment(self, response, i):
        subcomments = []
        
        for iter_subcomment in range(1, len(response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/ul[@class='sub']/li")) + 1):
            subcomments.append(self.parse_single_subcomment(response, i, str(iter_subcomment)))
        
        return subcomments    
    
    def parse_single_subcomment(self, response, i, j):
        subcomment = Subcomment()
        
        subcomment["username"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC']["+ i + "]/ul[@class='sub']/li[" + j + "]//div[@class='author ellipsis']/a//b/text()").extract()[0]
        subcomment["text"] = self.merge_text(response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/ul[@class='sub']/li[" + j + "]//div[@class='text']/p/text()").extract())
        subcomment["tags"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/ul[@class='sub']/li[" + j + "]//div[@class='text']//a[@class='showTagSummary']/text()").extract()
        subcomment["shouts"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/ul[@class='sub']/li[" + j + "]//div[@class='text']/p/a[@class='showProfileSummary']/text()").extract()        
        subcomment["score"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/ul[@class='sub']/li[" + j + "]//div[@class='author ellipsis']/p/@data-vcp").extract()[0]
        subcomment["date"] = response.xpath("//ul[@class='comments-stream']/li[@class='iC'][" + i + "]/ul[@class='sub']/li[" + j + "]//div[@class='author ellipsis']//small/time/@title").extract()[0]
        
        return dict(subcomment)
            
