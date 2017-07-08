# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class BetexplorerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Odds(Item):
    id = Field()
    datetime = Field()
    #area_id = Field()
    area_name = Field()
    #competition_id = Field()
    competition_name = Field()
    #home_team_id = Field()
    home_team = Field()
    #away_team_id = Field()
    away_team = Field()
    kick_off = Field()
    #score = Field()
    #fts = Field()
    home = Field()
    draw = Field()
    away = Field()
    updated = Field()


class Match(Item):
    id = Field()
    datetime = Field()
    #area_id = Field()
    area_name = Field()
    #competition_id = Field()
    competition_name = Field()
    #home_team_id = Field()
    home_team = Field()
    #away_team_id = Field()
    away_team = Field()
    kick_off = Field()
    score = Field()
    fts = Field()
    odd1 = Field()
    oddX = Field()
    odd2 = Field()
    updated = Field()


