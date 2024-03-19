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
with open('./links/do_choi_cho_meo_links.txt', 'r',encoding='utf-8') as file:  
    # Đọc toàn bộ nội dung của file vào biến content
    content = file.read()


links = content.split('\n')

def writeFile(contents,nameFile):
  path = "./news/Car/"+nameFile+".txt"
  if not os.path.isfile(path):
    with open(path, 'w') as file:
      pass
  for content in contents: 
    text = content.text
    with open(path, 'a', encoding="utf-8") as file:
      file.write(text + "\n")



names = []
prices = []
descriptions = []
link_images = []

def crawl (link, driver) :
  driver.get(link)
  time.sleep(2)
  
  product_name_tag = driver.find_element(By.CSS_SELECTOR, '.product-name')
  product_name = product_name_tag.find_element(By.CSS_SELECTOR, 'h1') # product name = product_name.text

  price_tag = driver.find_element(By.CSS_SELECTOR, '.special-price')
  price = price_tag.text 

  description_tag = driver.find_element(By.CLASS_NAME, 'std')

  image_container_tag = driver.find_element(By.CLASS_NAME, 'large-image')
  image = image_container_tag.find_element(By.CSS_SELECTOR,'img')
  link_image = image.get_attribute('src')

  names.append(product_name.text )
  prices.append(price )
  descriptions.append(description_tag.text )
  link_images.append(link_image)

  print('-------------------------------------------------------------------------------------------------')
  print('Name: ', product_name.text)
  print('Price :', price)
  print('description :', description_tag.text)
  print('link image: ' , link_image)



   


for link in links:
  try:
    crawl(link,driver)      
  except Exception as e:
    print(e)
    continue
      
import pandas as pd 

data = pd.DataFrame({
  'name': names,
  'price': prices,
  'description': descriptions,
  'link_image': link_images
})

data.to_csv('./data/do_choi_cho_meo.csv', index=False, encoding='utf-8-sig')

# Đóng trình duyệt sau khi đã hoàn thành crawl
driver.quit()


