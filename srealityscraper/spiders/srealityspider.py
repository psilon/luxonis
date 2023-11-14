import scrapy
import json
import urllib.parse as urlparse
from scrapy.exceptions import CloseSpider
import os

class SrealityspiderSpider(scrapy.Spider):
	name = "srealityspider"
	allowed_domains = ["sreality.cz"]
	start_urls = ["https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20"]
	counter = 0
	limit = int(os.getenv('LIMIT_ITEMS', 10))

	def start_requests(self): 
		url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20"
		yield scrapy.Request(url, self.parse) 
  
	def parse(self, response): 
		domain = "https://www.sreality.cz/api"
		data = json.loads(response.text) 
  
		if "_embedded" in data:
			estates = data["_embedded"]["estates"] 
			current_link = data["_links"]["self"]["href"]
			for estate in estates:
				title = estate["name"]
				image_url = estate["_links"]["images"][0]['href']
				
				self.counter = self.counter+1
				if self.counter > self.limit:
					raise CloseSpider("Limit reached!")
				
				print(self.counter,'/',self.limit,title, flush=True)

				yield {"title": title, "image_url": image_url} 


			parsed_current_link = urlparse.urlparse(current_link)
			query = dict(urlparse.parse_qsl(parsed_current_link.query))
			query.update({"page":int(query["page"])+1})
			new_url = domain+parsed_current_link._replace(query=urlparse.urlencode(query)).geturl()
			
			yield response.follow(new_url, callback=self.parse)
			
