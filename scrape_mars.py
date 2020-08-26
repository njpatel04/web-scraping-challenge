from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import pymongo
import requests

def init_browser():
    #Navigating to page
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    #Parsing thorugh HTML
    html = browser.html
    soup = bs(html, 'html.parser')


    # NASA Mars News
    #----------------------------------------------------------------------------------
    artical_list = soup.find('li', class_='slide')
    
    #Ponting variable to the correct session
    title = artical_list.find('div', class_="content_title")
    paragraph = artical_list.find('div', class_="article_teaser_body")

    #assign variables to the latest artical title and paragraph
    latest_title = title.a.text
    latest_paragraph = paragraph.text
    #print(latest_paragraph)

    # JPL Mars Space Images - Featured Image
    #----------------------------------------------------------------------------------
    #getting URL
    url = 'https://www.jpl.nasa.gov/spaceimages'
    browser.visit(url)

    #Parsing thorugh HTML
    html = browser.html
    soup = bs(html, 'html.parser')

    first_step = soup.find("div", class_= "carousel_items")
    image_url = first_step.a['data-fancybox-href']
    
    featured_image_url = "https://www.jpl.nasa.gov" + image_url
    

    # Mars Facts
    #----------------------------------------------------------------------------------

    url = 'https://space-facts.com/mars/'
    raw_table = pd.read_html(url)
    
    fact_table_df = raw_table[0]
    fact_table_df.columns=["Description", "Values"]
    fact_table_df.set_index("Description", inplace=True)

    #fact_table_df.to_html('datahtml.html', index=True)
    data_html = fact_table_df.to_html()


    # Mars Hemispheres
    #----------------------------------------------------------------------------------
    #getting URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #Parsing thorugh HTML
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for result in results:
    
        title_loc = result.find("h3")
        title = title_loc.text
    
        page1_img_url_text = result.a["href"] # location of the image link text on the main page
    
        page2_img_url = "https://astrogeology.usgs.gov" + page1_img_url_text # URL for the location of the full image
   
        response = requests.get(page2_img_url)
        response = response.text
        soup = bs(response, "html.parser")
    
        page3_img_url = soup.find("img", class_="wide-image")["src"]
    
        final_img_url = "https://astrogeology.usgs.gov" + page3_img_url
    
        hemisphere_image_urls.append({"title": title, "img_url": final_img_url})
    
    data_dic = {"news_title": latest_title,
                "news_paragraph": latest_paragraph,
                "featured_image_url": featured_image_url,
                "data_table": data_html,
                "hemisphere_data": hemisphere_image_urls}
    
    browser.quit()

    # Return results
    return data_dic
