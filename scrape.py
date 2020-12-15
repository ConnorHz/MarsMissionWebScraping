from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd

def scrape_data():

    # Get Featured Article
    executable_path = {'executable_path': 'C:\chromedriver_win32\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://mars.nasa.gov/news"

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')

    articles = soup.find_all("li", class_="slide")

    browser.quit()

    article_title = articles[0].find("div", class_="content_title").text
    article_teaser = articles[0].find("div", class_="article_teaser_body").text

    # Get Featured Image
    url_start = 'https://www.jpl.nasa.gov'
    url_end = '/spaceimages/?search=&category=Mars'

    url = url_start + url_end

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')

    browser.quit()

    image_id = soup.find("div", class_="carousel_items").find("article")["style"].split("/")[-1].split("-")[0]
    featured_image_url = f'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/{image_id}_ip.jpg'

    # Get Mars Info
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    soup = bs(tables[0].to_html(index=False), 'lxml')

    table = soup.find('table')

    # Remove table head
    for thead in table.find_all('thead'):
        thead.replace_with('')

    table_html = str(table.encode())

    # Get Mars Hemisphere Info
    hemisphere_image_urls = []

    url_start = 'https://astrogeology.usgs.gov'
    url_end = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    url = url_start + url_end

    source = req.get(url).text
    soup = bs(source, 'lxml')

    links = soup.find("div", id='product-section').find_all("a")

    for x in links:
        if x.text != "":
            url = url_start + x['href']
            title = x.find("h3").text
            source = req.get(url_start+x['href']).text
            mars_page = bs(source, 'lxml')
            hemisphere_image_urls.append({"title": title.rsplit(" ", 1)[0], "img_url": mars_page.find("div", class_="downloads").find("li").find("a")["href"]})


    return article_title, article_teaser, featured_image_url, table_html, hemisphere_image_urls