import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
import pandas as pd
from itertools import chain


class EuroncapSpider(scrapy.Spider):

	# Spider name
	name = "Euroncap"

	# Extracting from local file
	# start_urls = ["file:///home/ganesh/scrapy_learning/leaf_node_html.html"]
	
	# Extracting from website
	start_urls = ["https://www.euroncap.com/en/results/toyota/yaris-cross/43819"]

	

	# Parse functon to extract the features needed
	def parse(self, response):

		# Extracting images from desired location
		# having data and data-src as per the outline of the page

		# raw_image_urls_data = response.xpath('//*[@class="reward-images"]//img/@data-src').getall()
		# raw_image_urls = response.xpath('//*[@class="reward-images"]//img/@src').getall()

		# raw_image_urls_data = raw_image_urls_data + response.xpath('//*[@class="frame-content"]//img/@data-src').getall()
		# raw_image_urls = raw_image_urls + response.xpath('//*[@class="frame-content"]//img/@src').getall()

		# Extracting all possible images from the links
		raw_image_urls_data = response.xpath('//img/@data-src').getall()
		raw_image_urls = response.xpath('//img/@src').getall()


		clean_image_urls = []
		for img_url in raw_image_urls_data:
			clean_image_urls.append(response.urljoin(img_url))

		for img_url in raw_image_urls:
			clean_image_urls.append(response.urljoin(img_url))

		
		#Concentrating only table
		specification_table = response.css("div.tab_container")
		
		col1_data = [specs.css("span.tcol1::text").getall() for specs in specification_table]
		col2_data = [specs.css("span.tcol2::text").getall() for specs in specification_table]

		
		yield {

               'rating-title' : response.xpath('//div[@class="rating-title"]/p/text()').getall(),
	       'value'        : response.css('div.value::text').getall(),
               'col1' : col1_data,
               'col2' : col2_data,
               'image_urls' : clean_image_urls

		}

 



