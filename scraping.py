import sys
import time
import re
import datetime
import calendar
import os
import glob
import requests
import warnings
import configparser
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Initial Variables
sleep_time=2


# Relevant links
website_link = "https://www.empa.ch/web/simbiosys/publications"
file_path = "/Users/divinefavourodion/Documents/TLNP_Project/data"
driver_path = "/Users/divinefavourodion/Documents/TLNP_Project/chromedriver"


# Setting up Selenium Chrome webdriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {
    'download.default_directory': file_path,
    'download.prompt_for_download': False}  # Specify the file system for default downloads by the webdriver
chrome_options.add_experimental_option('prefs', prefs)
# service = Service(driver_path)
browser = webdriver.Chrome(driver_path, options=chrome_options)

# Scraping section
browser.get(website_link)
time.sleep(sleep_time)
link_list = []
links = browser.find_elements(By.XPATH, "//a")
time.sleep(sleep_time)

for link in links:
    link_list.append(str(link.get_attribute("href")))

article_link_pattern = re.compile('|'.join(['sciencedirect', 'springer', 'oxford', 'lib4ri', 'islandora', 'engrxiv', 'kuleuven',
                               'dora', 'nature', 'documents/', 'frontiersin', 'arxiv', 'tandfonline', 'medrxiv',
                               'preprint']))
filtered_links = [link for link in link_list if article_link_pattern.search(link)]


for link in filtered_links:
    browser.get(link)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    sub_links = soup.find_all('a', href=True)

    for sub_link in sub_links:
        print(sub_link)
        if sub_link['href'].endswith('.pdf'):
            base_url= link
            full_url = urljoin(base_url, sub_link['href'])
            try:
                response = requests.get(full_url['href'])
                with open(f"/Users/divinefavourodion/Documents/TLNP_Project/data/{sub_link.text.pdf}", 'wb') as f:
                    f.write(response.content)
                    print(f"Saved the {sub_link.text} pdf file")
                    print("continuing...")
            except:
                print("Link skipped ")

browser.quit()




