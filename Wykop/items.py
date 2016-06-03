# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Author(scrapy.Item):
    username = scrapy.Field()
    signup_date = scrapy.Field()
    nick_color = scrapy.Field()

class Subcomment(scrapy.Item):
    username = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    shouts = scrapy.Field()
    score = scrapy.Field()
    date = scrapy.Field()

class Comment(scrapy.Item):
    comment = scrapy.Field()
    subcomments = scrapy.Field()

class WykopItem(scrapy.Item):
    # Article:    
    timestamp = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    tags = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    views = scrapy.Field()
    # Author:
    author = scrapy.Field()
    # Comments:
    comments = scrapy.Field()