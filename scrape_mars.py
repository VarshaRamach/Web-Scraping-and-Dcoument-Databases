from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
import time
import numpy as np
import os

def init_browser():
    
   
    return Browser("chrome",executable_path=r'C:/Users/Varsha/Desktop/mission_to_Mars/Chromedriver.exe', headless=False)

def get_requests_html(url):
    html = requests.get(url)
    return BeautifulSoup(html.text, 'html.parser')


def get_mars_news(url, verbose=False):
    soup = get_requests_html(url)
    news_title = soup.find_all(class_='content_title')
    news_p = soup.find_all(class_='article_teaser_body')

    mars_news = []
    for title in news_title:
        print(title.get_text().strip())
        mars_news.append({'title': title.get_text().strip()})

    if verbose:
        for title, teaser in zip(news_title, news_p):
            print(news_title)
            print(news_p)

    return mars_news


def get_mars_featured_img(url):
    soup = get_requests_html(url)
    base_url = 'https://www.jpl.nasa.gov/'
    img_url = soup.find('a', class_='button fancybox').get('data-fancybox-href')
    return base_url + img_url


def get_mars_weather(url, verbose=False):
    soup = get_requests_html(url)
    div_class = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'
    weather = soup.find('p', class_=div_class)

    if verbose:
        print(weather.text)
    return weather.text


def get_mars_facts(url, verbose=False):
    mars_facts_table = pd.read_html(url, index_col=0)[0]

    if verbose:
        print(mars_facts_table.to_html())
    return mars_facts_table.to_html(header=False, classes='table table-striped table-hover table-sm')


def get_hemi_imgs(verbose=False):
    base_url = 'https://astrogeology.usgs.gov'
    mars_hemis_url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    soup = get_requests_html(mars_hemis_url)
    titles = soup.find_all('h3')

    mars_hemis_list = []
    mars_hemis_imgs = soup.find_all('img', class_='thumb')
    for img in mars_hemis_imgs:
        mars_hemis_local_href = img.parent.get('href')
        hemis_full_url = base_url + mars_hemis_local_href
        mars_hemis_list.append(hemis_full_url)

    image_urls = []
    for hemi_url in mars_hemis_list:
        html = requests.get(hemi_url).text
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('div', class_='downloads'):
            image_urls.append(link.find_all('a')[0].get('href'))

    hemisphere_img_urls = []
    for title, img_url in zip(titles, image_urls):
        hemisphere_img_urls.append({'title': title.text,
                                    'img_url': img_url})

    if verbose:
        print(hemisphere_img_urls)
    return hemisphere_img_urls


def scrape(verbose=False):
    '''
    Returns a python dict with various facts about the planet Mars.
    `verbose = True` prints the returned output to the terminal.
    '''
    mars_news = get_mars_news('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest',
                              verbose=verbose)
    featured_image_url = get_mars_featured_img('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    mars_weather = get_mars_weather('https://twitter.com/marswxreport?lang=en',
                                    verbose=verbose)
    mars_facts_table = get_mars_facts('https://space-facts.com/mars/',
                                      verbose=verbose)
    hemisphere_img_urls = get_hemi_imgs(verbose=verbose)

    # OUTPUT
    mars_dict = {'mars_news': mars_news,
                 'featured_image_url': featured_image_url,
                 'mars_weather': mars_weather,
                 'mars_facts_table': mars_facts_table,
                 'hemisphere_image_urls': hemisphere_img_urls
                 }

    if verbose:
        print(mars_dict)
    return mars_dict




sample_data = {
  "featured_image_url": "/spaceimages/images/mediumsize/PIA19036_ip.jpg",
  "hemisphere_image_urls": [
    {
      "img_url": "",
      "title": "Cerberus Hemisphere Enhanced"
    },
    {
      "img_url": "",
      "title": "Schiaparelli Hemisphere Enhanced"
    },
    {
      "img_url": "",
      "title": "Syrtis Major Hemisphere Enhanced"
    },
    {
      "img_url": "",
      "title": "Valles Marineris Hemisphere Enhanced"
    }
  ],
  "mars_facts_table": "",
  "mars_news": [
    {
      "title": "Click the Refresh Mars data at the top Right"
    }
  ],
  "mars_weather": "Current Mars Climate is super cold"
}