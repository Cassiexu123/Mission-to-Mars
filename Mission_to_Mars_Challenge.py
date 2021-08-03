# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


# %%
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# %%
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# %%
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# %%
slide_elem.find('div', class_='content_title')


# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# %% [markdown]
# # Featured Images

# %%
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# %%
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# %%
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# %%
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# %%
df.to_html()


# %%
browser.quit()

# %% [markdown]
# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# %% [markdown]
# ### Hemispheres

# %%
URL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
page = requests.get(URL)

b_soup = soup(page.content, 'html.parser')
b_soup
s_request = b_soup.findAll('div', class_='item')


list_ancor = []

for i in s_request:
    for j in i.findAll('a'):
        list_ancor.append('https://astrogeology.usgs.gov' + j['href'])
hemisphere_image_urls= []   
for uri in list_ancor:
    url = uri
    page = requests.get(url)
    b_soup = soup(page.content, 'html.parser')
    title = b_soup.findAll('h2', class_='title')[0].text
    img_href = b_soup.findAll('img', class_='wide-image')[0]['src']
    hemispheres = {'img_url': ('https://astrogeology.usgs.gov' + img_href), 'title': title}
    hemisphere_image_urls.append(hemispheres)
hemisphere_image_urls


