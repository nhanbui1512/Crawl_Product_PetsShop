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
with open('./links/vat_dung_an_uong.txt', 'r', encoding='utf-8') as file:
    # Đọc toàn bộ nội dung của file vào biến content
    content = file.read()


links = content.split('\n')


names = []
prices = []
descriptions = []
link_images = []
doms = []
product_options = []
file_urls = []


def crawl(link, driver):
    driver.get(link)
    time.sleep(2)

    product_name_tag = driver.find_element(By.CSS_SELECTOR, '.product-name')
    product_name = product_name_tag.find_element(
        By.CSS_SELECTOR, 'h1')  # product name = product_name.text

    price_tag = driver.find_element(By.CSS_SELECTOR, '.special-price')
    price = price_tag.text

    description_tag = driver.find_element(By.CLASS_NAME, 'short-description')

    image_container_tag = driver.find_element(By.CLASS_NAME, 'large-image')
    image = image_container_tag.find_element(By.CSS_SELECTOR, 'img')
    link_image = image.get_attribute('src')

    names.append(product_name.text)
    prices.append(price)
    descriptions.append(description_tag.text)
    link_images.append(link_image)

    dom = driver.find_element(By.CLASS_NAME, 'std')
    dom_string = dom.get_attribute('outerHTML')
    doms.append(dom_string)
    option_texts = ''
    try:
        selector = driver.find_element(By.CLASS_NAME, 'single-option-selector')
        options = selector.find_elements(By.CSS_SELECTOR, 'option')
        for option in options:
            option_texts += option.text + "--"
        product_options.append(option_texts)
    except:
        product_options.append('No option')
    print('-------------------------------------------------------------------------------------------------')

    product_images = ''
    try:
        slide = driver.find_element(By.CLASS_NAME, 'previews-list')
        a_tags = slide.find_elements(By.CSS_SELECTOR, 'a')
        for tag in a_tags:
            link_file = tag.get_attribute('href')
            product_images += link_file + "--"
        file_urls.append(product_images)
    except:
        file_urls.append(product_images)
    print('Name: ', product_name.text)
    print('Price :', price)
    print('description :', description_tag.text)
    print('link image: ', link_image)
    print('options:', option_texts)
    print('images', product_images)


for link in links:
    try:
        crawl(link, driver)
    except Exception as e:
        print(e)
        continue


print('nameLength: ', len(names))
print('priceLength: ', len(prices))
print('descriptionLenght: ', len(descriptions))
print('linkLength: ', len(link_images))
print('options: ', len(product_options))
print('file_urls: ', len(file_urls))

data = pd.DataFrame({
    'name': names,
    'price': prices,
    'description': descriptions,
    'link_image': link_images,
    'dom': doms,
    'product_option': product_options,
    'file_url': file_urls,
})

data.to_csv('./data/vat_dung_an_uong(2).csv',
            index=False, encoding='utf-8-sig')

# Đóng trình duyệt sau khi đã hoàn thành crawl
driver.quit()
