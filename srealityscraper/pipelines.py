# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os


class SrealityscraperPipeline:
	
	def __init__(self):
	 ## Connection Details
		hostname = os.getenv('POSTGRES_HOSTNAME', 'localhost')
		username = os.getenv('POSTGRES_USER', 'user')
		password = os.getenv('POSTGRES_PASSWORD', 'pass')
		database = os.getenv('POSTGRES_DATABASE', 'database')

		## Create/Connect to database
		self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

		## Create cursor, used to execute commands
		self.cur = self.connection.cursor()
		
		## Create table if none exists
		self.cur.execute("""
		CREATE TABLE IF NOT EXISTS sreality_items(
			id serial PRIMARY KEY, 
			title text,
			image_url VARCHAR(255)
		);
		TRUNCATE sreality_items;
		""")
	def process_item(self, item, spider):
		## Define insert statement
		self.cur.execute(""" insert into sreality_items (title, image_url) values (%s,%s)""", (
			item["title"],
			item['image_url']
		))

		## Execute insert of data into database
		self.connection.commit()
		return item

	def close_spider(self, spider):
		## Close cursor & connection to database 
		self.cur.close()
		self.connection.close()        
