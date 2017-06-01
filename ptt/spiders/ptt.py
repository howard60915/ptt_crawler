from datetime import datetime
import logging
import scrapy
from scrapy.http import FormRequest
from ptt.items import PostItem

class PTTSpider(scrapy.Spider):
  name = 'ptt'
  allowed_domains = ['ptt.cc']
  start_urls = ('https://www.ptt.cc/bbs/Gossiping/index.html', )
  _retry  = 0
  MAX_RETRY = 1
  _pages = 0
  MAX_PAGE = 2

  def parse(self, response):
    if len(response.xpath('//div[@class="over18-notice"]')) > 0:
      if self._retry < PTTSpider.MAX_RETRY:
        self._retry += 1
        logging.warning('retry {} times...'.format(self._retry))
        yield FormRequest.from_response( response,
                                          formdata={ 'yes': 'yes' },
                                          callback=self.parse )
    else:
      self._pages += 1
      for href in response.css('.r-ent > div.title > a::attr(href)'):
        url = response.urljoin( href.extract() )
        yield scrapy.Request(url, callback=self.post_parse)

      if self._pages < PTTSpider.MAX_PAGE:
        next_page = response.xpath('//div[@class=""]//a[contains(text(), "上頁")/@href]')
        if next_page:
          url = response.urljoin(next_page[0].extract())
          logging.warning('follow {}'.format(url))
          yield scrapy.Request( url, callback=sel.parse )
        else:
          logging.warning("there is no next page")
      else:
        logging.warning("MAX PAGE reached")


  def post_parse(self, response):
    print('==================Shit Rocks+++++++++++++++++++++++++++')
    item = PostItem()
    item['title'] = response.xpath('//meta[@property="og:title"]/@content')[0].extract()
    item['author'] = response.xpath('//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span/text()')[0].extract()
    date_str = response.xpath('//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span/text()')[0].extract()
    item['date'] = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
    item['content'] = response.xpath('//meta[@name="description"]/@content')[0].extract()
    item['url'] = response.url

    comments = []
    total_score = 0

    for comment in response.xpath('//div[@class="push"]'):
      push_tag = comment.css('.push-tag::text')[0].extract()
      push_user = comment.css('.push-userid::text')[0].extract()
      push_content = comment.css('.push-content::text')[0].extract()

      if '推' in push_tag:
        score = 1
      elif '噓' in push_tag:
        score = 1
      else:
        score = 0

      total_score += score
      comments.append({
          'user': push_user,
          'content': push_content,
          'score': score
        })
    item['comment'] = comments
    item['score'] = total_score

    yield item














