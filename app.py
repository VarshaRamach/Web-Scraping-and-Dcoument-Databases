from flask import Flask, jsonify, render_template
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_info_db


def overwrite_db(document):
    collection.delete()
    collection.insert_one(document)


@app.route('/')
def show_homepage():
    mars_data = scrape_mars.sample_data
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def return_scrape():
    mars_data = scrape_mars.scrape()
    # overwrite_db(mars_data)
    # collection.find()
    # return render_template('index.html')
    return render_template('index.html', mars_data=mars_data)

@app.route('/test')
def return_test():
    mars_data = scrape_mars.scrape()
    return jsonify(mars_data)


if __name__ == '__main__':
    app.run(debug=True)
