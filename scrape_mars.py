
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template
from flask_pymongo import PyMongo
import pandas as pd



def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    mars_dict={}

def scrape():

    browser= init_browser()

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html= browser.html
    soup= bs(html, 'html.parser')


    # In[22]:



    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text
    print(news_title)
    print("-----------------------------------")
    print(news_p)


    # In[23]:


    #JPL Mars Space Images

    image_url = 'https://spaceimages-mars.com/'

    browser.visit(image_url)

    html= browser.html
    soup= bs(html, 'html.parser')


    # In[24]:


    image_path = soup.find('img', class_='headerimage fade-in')['src']

    featured_image_url = image_url + image_path
    print(featured_image_url)


    # In[25]:


    #Mars Facts

    mars_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_facts_url)
    html= browser.html
    soup= bs(html, 'html.parser')


    # In[26]:


    tables = pd.read_html(mars_facts_url)
    tables


    # In[39]:


    # Find in lists of dataframes

    mars = tables[1]
    mars.columns = ["Description","Value"]
    mars_facts = mars.set_index("Description")
    mars_facts


    # In[40]:


    mars_facts = mars_facts.to_html()
    print(mars_facts)


    # In[ ]:





    # In[41]:


    #Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html= browser.html
    soup= bs(html, 'html.parser')


    # In[42]:


    items = soup.find_all('div', class_='item')
    #print(items)


    # In[43]:


    urls = []
    img_urls= []

    for i in items: 
        
        title = i.find('h3').text
        
        
        img_url = i.find('a', class_='itemLink product-item')['href']
        
    
        browser.visit(url + img_url)
        
        
        img_html = browser.html
        
        
        soup = bs(img_html, 'html.parser')
        
        
        img_url = url + soup.find('img', class_='wide-image')['src']
        
        
        img_urls.append({"title" : title, "img_url" : img_url})
        



    mars_dict={
            "news_title":news_title,
            "news_p":news_p,
            "featured_image_url":featured_image_url,
            "fact_table":mars_facts,
            "hemisphere_images":img_urls
        }
       
    browser.quit()


    return mars_dict



