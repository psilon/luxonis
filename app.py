from flask import Flask, render_template
import psycopg2
import os

os.system("scrapy runspider srealityscraper/spiders/srealityspider.py")

app = Flask(__name__)


class Sreality:
        def __init__(self):
            try:
                self.db_connection = psycopg2.connect(host = os.getenv('POSTGRES_HOSTNAME', 'localhost'),
                                database = os.getenv('POSTGRES_DATABASE', 'database'),
                                user = os.getenv('POSTGRES_USER', 'user'),
                                password = os.getenv('POSTGRES_PASSWORD', 'pass'))
                self.db_cursor = self.db_connection.cursor()
            except Exception as e:
                raise e


        def get_all_items(self):
            self.db_cursor.execute("SELECT * FROM sreality_items;")
            columns = list(self.db_cursor.description)
            result = self.db_cursor.fetchall()

            # make dict
            items = []
            for row in result:
                row_dict = {}
                for index, column in enumerate(columns):
                    row_dict[column.name] = row[index]
                items.append(row_dict)
            
            return items
        
        def __del__(self):
            self.db_cursor.close()
            self.db_connection.close()




                

@app.route('/')
def index():
    sreality = Sreality()
    items = sreality.get_all_items()
    return render_template("template.html", items=items)


