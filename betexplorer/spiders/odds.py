# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from betexplorer.items import Odds
#from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, date

class OddsSpider(Spider):
    name = "odds"
    allowed_domains = ["https://www.betexplorer.com"]
    start_urls = ['https://www.betexplorer.com/next/soccer/']
    params = {
        "sport": "soccer",
        "page": "match",
        "id" : "2255155",
        "localization_id": "www"
    }
    def start_requests(self):
        start_url = 'https://www.betexplorer.com/odds-filter/soccer/?rangeFrom=1&rangeTo=999&days=14'
        request = Request(url=start_url, callback=self.parse)
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        yield request

    def parse(self, response):
        #items = []
        competitions = response.xpath('//table[@class="table-matches js-tablebanner-t"]//tbody')
        for c in competitions:
            kick_off_date = c.xpath('.//th[@class="table-matches__date"]/text()').extract_first()
            if not kick_off_date:
                kick_off_date = date.today().isoformat()
            area_comp = c.xpath('.//th[@class="h-text-left"]//text()').extract_first().split(':')
            kick_offs = c.xpath('.//td[@class="table-matches__tt"]//span/text()').extract()
            teams = c.xpath('.//td[@class="table-matches__tt"]//a/text()').extract()
            odds_ha = c.xpath('.//td[@class="table-matches__odds fav-odd"]//a/@data-odd').extract()
            odds_d = c.xpath('.//td[@class="table-matches__odds"]//a/@data-odd').extract()
            for i in range(len(teams)):
                item = Odds()
                item['id'] = 0
                item['area_name'], item['competition_name'] = area_comp
                #hh, mm = map(int, ick_offs[i].split(':')))
                #hh = hh -2
                item['kick_off'] = ':'.join((kick_offs[i],'00'))
                item['datetime'] = ' '.join((kick_off_date, item['kick_off']))
                item['home_team'], item['away_team'] = teams[i].split(' - ')
                item['home'] = odds_ha[i*2]
                item['draw'] = odds_d[i]
                item['away'] = odds_ha[i*2+1]

                item['updated'] = datetime.utcnow().isoformat(' ')
                yield item
                #items.append(item)
        #return items
        #self.log('URL: {}'.format(response.url))

    """
    def parse(self, response):
        venue = Venue()
        venue['country'], venue['city'], venue['name'] = response.css('title::text')[0].extract().split(',')
        res = response.xpath('//td//b/text()')
        if len(res) > 0:
            venue['opened'] = res[0].extract()
        res = response.xpath('//td//b/text()')
        if len(res) > 1:
            venue['capacity'] = res[1].extract()
        venue['lat'], venue['lng'] = response.xpath('//script/text()')[1].re(r'\((.*)\)')[1].split(',')
        return venue
    """

