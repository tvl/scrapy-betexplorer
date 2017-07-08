# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from betexplorer.items import Match
#from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime

class OddsSpider(Spider):
    name = "odds"
    allowed_domains = ["http://www.betexplorer.com"]
    start_urls = ['http://www.betexplorer.com/next/soccer/']
    params = {
        "sport": "soccer",
        "page": "match",
        "id" : "2255155",
        "localization_id": "www"
    }
    def start_requests(self):
        start_url = 'http://www.betexplorer.com/odds-filter/soccer/?rangeFrom=1&rangeTo=999&days=2'
        request = Request(url=start_url, callback=self.parse)
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        yield request

    def parse(self, response):
        items = []
        competitions = response.xpath('//table[@class="table-matches js-tablebanner-t"]//tbody')
        for c in competitions:
            item = Match()
            item['area_name'], item['competition_name'] = \
                    c.xpath('.//th[@class="h-text-left"]//text()').extract_first().split(':')
            matches = c.xpath('.//tr[@data-def="0"]')
            for m in matches:
                item['id'] = 0
                dd, mm, yy, hh, mmm = list(map(int, m.xpath('.//@data-dt').extract_first().split(',')))
                item['datetime'] = datetime(yy, mm, dd, hh, mmm, 0).isoformat(' ')
                item['kick_off'], item['home_team'], item['away_team'] = \
                        m.xpath('.//td[@class="table-matches__tt"]//span//text()').extract()
                item['score'] = m.xpath('.//td[@class="table-matches__result"]//text()').extract_first()
                item['fts'] = m.xpath('.//td[@class="table-matches__partial"]//text()').extract_first()

                odds1x2 =  m.xpath('.//td[@class="table-matches__odds"]//a//@data-odd').extract()
                if odds1x2:
                    item['odd1'], item['oddX'],item['odd2'] = odds1x2
            item['updated'] = datetime.utcnow().isoformat(' ')
            yield item
            items.append(item)
        return items
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

