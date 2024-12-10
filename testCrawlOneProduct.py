import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# driver = webdriver.Chrome()

chrome_options = Options()

# Thêm tùy chọn --ignore-certificate-errors vào đối tượng tùy chọn
chrome_options.add_argument("--disable-notifications")

# Khởi tạo trình điều khiển Chrome với các tùy chọn đã cấu hình
driver = webdriver.Chrome(options=chrome_options)

# Mở file để đọc
with open('./links/dem_long_van_chuyen.txt', 'r', encoding='utf-8') as file:
    # Đọc toàn bộ nội dung của file vào biến content
    content = file.read()


links = content.split('\n')


names = []
prices = []
descriptions = []
link_images = []
doms = []
images = []


def crawl(link, driver):
    driver.get(link)
    time.sleep(2)

    product_name_tag = driver.find_element(By.CSS_SELECTOR, '.product-name')
    product_name = product_name_tag.find_element(
        By.CSS_SELECTOR, 'h1')  # product name = product_name.text

    price_tag = driver.find_element(By.CSS_SELECTOR, '.special-price')
    price = price_tag.text

    description_tag = driver.find_element(By.CLASS_NAME, 'short-description')
    p_description_tag = description_tag.find_element(By.CSS_SELECTOR, 'p')
    short_description = ''
    if (p_description_tag is not None):
        short_description = p_description_tag.text

    image_container_tag = driver.find_element(By.CLASS_NAME, 'large-image')
    image = image_container_tag.find_element(By.CSS_SELECTOR, 'img')
    link_image = image.get_attribute('src')

    names.append(product_name.text)
    prices.append(price)
    descriptions.append(short_description)
    link_images.append(link_image)

    dom = driver.find_element(By.CLASS_NAME, 'std')
    dom_string = dom.get_attribute('outerHTML')
    doms.append(dom_string)

    list_image_container = driver.find_element(By.CLASS_NAME, 'previews-list')
    li_tags = list_image_container.find_elements(By.CSS_SELECTOR, 'li')
    images_of_product = []
    for li in li_tags:
        image_tag = li.find_element(By.CSS_SELECTOR, 'a')
        href = image_tag.get_attribute('href')
        images_of_product.append(href)

    print('-------------------------------------------------------------------------------------------------')
    print('Name: ', product_name.text)
    print('Price :', price)
    print('description :', description_tag.text)
    # print('link image: ', link_image)
    print(images_of_product)


link = 'https://kunmiu.com/bat-chong-gu-mat-gau'
crawl(link, driver)
