import scrapy

class StandardStockPick(scrapy.Item):
	investor_name = scrapy.Field()
	website_title = scrapy.Field()
	stockchase_date= scrapy.Field()
	investor_title = scrapy.Field()
	signal_value = scrapy.Field()
	company_name = scrapy.Field()
	company_ticker = scrapy.Field()
	opinion_date = scrapy.Field()
	stock_comments = scrapy.Field()
	stock_sector = scrapy.Field()
	href_link = scrapy.Field()
	occupation_title = scrapy.Field()
	current_price_to_buy = scrapy.Field()


#Left to fill
	investor_name = scrapy.Field()
	stockchase_date= scrapy.Field()
	investor_title = scrapy.Field()
	current_price_to_buy = scrapy.Field()

class stockchaseSpider(scrapy.Spider):
	name = "stockchase_expert_spider"

	start_urls = [
	'https://stockchase.com/expert/view/1421'
	]

	def parse(self, response):
		#How to get an individual expert's profile
		expert_profile = response.xpath('//*[@id="expert-profile"]')
		fourth_value = expert_profile.xpath('.//div')[4]

		#Specific information with name, date and title
		specific_values = fourth_value.xpath('.//text()').extract()
		
		#Specific table of values
		table_of_values = response.xpath('.//*[@id="experts"]/tbody[2]')

		for x in range(1, 16):
			new_pick = StandardStockPick()
			#Fill in common values from above
			new_pick['website_title'] = response.css('title').extract_first()

			current_row_value = '"row'+str(x)+'"'
			current_row = table_of_values.xpath('.//*[@id='+current_row_value+']')
			#Fill Values from the current row
			new_pick['signal_value'] = current_row.xpath(('.//div[contains(@class, "-border")]/text()')).extract()
			opinion_section = current_row.xpath(('.//td[contains(@data-label, "Opinion")]'))
			new_pick['company_name'] = opinion_section.xpath('.//span[contains(@class, "opinion-company-name")]/text()').extract_first()
			new_pick['company_ticker'] = opinion_section.xpath('.//span[contains(@style, "color")]/text()').extract_first()
			new_pick['opinion_date'] = opinion_section.xpath('.//p[contains(@class, "opinion-date")]/text()').extract_first() #conversion function from word date to number date needed
			new_pick['stock_comments'] = opinion_section.xpath('.//div[contains(@id, "opinion-content-")]//p//text()').extract_first()
			new_pick['stock_sector'] = opinion_section.xpath('.//span[contains(@class, "opinion-sector-tag")]//text()').extract_first()

			expert_section = firstRow.xpath(('.//td[contains(@data-label, "Expert")]'))
			new_pick['href_link'] = expert_section.xpath('.//a[contains(@class, "anchor-link")]/@href').extract_first()
			new_pick['occupation_title'] = expert_section.xpath('normalize-space(.//p[contains(@class, "expert-title-company")]/text())').extract_first()
			
			#Get the list, find price and go up two
			expertSection.xpath('.//text()').extract()
			currentPriceToBuy = expertSection.xpath('.//text()')[22].extract()

			#Return the new item and move onto the next one in the list
			yield new_pick



	#Across sectors who is right and companies in that sector
