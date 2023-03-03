
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.http import FormRequest
import re
from itemadapter import ItemAdapter
import asyncio
from twisted.internet import asyncioreactor
scrapy.utils.reactor.install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
from twisted.internet import reactor
from scrapy_playwright.page import PageMethod
# import pyppeteer
# import schedule
# import time

# import openpyxl

# SCRAPER_API_KEY = "52b9c2fa3e4a3a0af3b7c4af3706115b" #ef991d16e237a6680f215c650206cf8e
SCRAPER_API_KEY = "ef991d16e237a6680f215c650206cf8e" #ef991d16e237a6680f215c650206cf8e
PROXY = f"http://scraperapi.country_code=us.device_type=desktop:{SCRAPER_API_KEY}.render=true@proxy-server.scraperapi.com:8001 "
URL = "https://ec.europa.eu/eures/portal/jv-se/search?page=1&resultsPerPage=50&orderBy=MOST_RECENT&lang=en"


SELECTORS = {
	"player_name" : '//div[@id="player-general-info"]/div[1]/span[1]/text()',
    "team_name" : '//div[@id="player-general-info"]/div[1]/span/a/text()',
}
class TestScrapy(scrapy.Spider):
	name="TEST"
	custom_settings=dict(
		# "ITEM_PIPELINES": {
		# 	'__main__.XLSXPipeline': 100
		# 	},
		# "DOWNLOADER_MIDDLEWARES" : {
		# 	'__main__.CustomProxyMiddleware': 350,
		# 	'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
		# },
		# "DOWNLOAD_HANDLERS" : {
		#     "http": "scrapy_pyppeteer.handler.ScrapyPyppeteerDownloadHandler",
		#     "https": "scrapy_pyppeteer.handler.ScrapyPyppeteerDownloadHandler",
		# },
		DOWNLOAD_HANDLERS = {
		    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
		    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
		},
		PLAYWRIGHT_BROWSER_TYPE = "chromium",
		PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True},
		TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
		CONCURRENT_REQUESTS =32
	)

	def start_requests(self):
		# yield scrapy.Request(url=URL,callback=self.parse, meta={"pyppeteer": True})
		yield scrapy.Request(url=URL,callback=self.parse, meta=dict(
			playwright = True,
			playwright_include_page = True,
			 playwright_page_methods =[PageMethod('wait_for_selector', 'role=complementary')],
			))
	
	async def parse(self,response):
		page = response.meta["playwright_page"]
		html = await page.content()
		with open('source.html', 'w') as f:
			f.write(html)
			f.close()
		print(html)
	# def parse(self,response,page: pyppeteer.page.Page):
		# print(response.text)
		await page.close()

	# def clean(self,value):
	# 	new_str = re.sub(r'[\t\n\r]',"",value)
	# 	return new_str

	# def remainAlpabet(self, value):

	# 	value_1 = re.sub(r'[^a-zA-Z]',"",value)
	# 	return value_1

	# def remainAlpabetNumeric(self, value):

	# 	value_1 = re.sub(r'[^a-zA-Z0-9]',"",value)
	# 	return value_1

# class Item(scrapy.Item):
#     player_link = scrapy.Field()

# class CustomProxyMiddleware:
#     def process_request(self, request, spider):
#         request.meta["proxy"] = PROXY


# class XLSXPipeline(object):
#     wb = None
#     ws = None

#     def open_spider(self, spider):
#         self.wb = openpyxl.Workbook()
#         self.ws = self.wb.active

#         self.ws.append(FIELDNAMES)
    
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         self.ws.append([
#         	adapter.get("player_link"),
#         	])

#         return item

#     def close_spider(self, spider):
#         self.wb.save('output.xlsx')



def start_crawl():
	print("Start Crawling...")
	configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
	runner = CrawlerRunner()
	# install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
	d = runner.crawl(TestScrapy)
	d.addBoth(lambda _: reactor.stop())
	reactor.run()

start_crawl()