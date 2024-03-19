from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=chrome_options)

unique_links = set()    

def writeLinkToFile(link): 
  with open("./links/links.txt", 'a', encoding="utf-8") as file:
    file.write(link + "\n")


def getLinks(page): 
  driver.get("https://kunmiu.vn/cat-ve-sinh-dung-cu-ve-sinh?page="+str(page))
  time.sleep(2)
  links = driver.find_elements(By.CSS_SELECTOR, ".item-title")
  for link in links:
    a_tag = link.find_element(By.CSS_SELECTOR, 'a')
    href = a_tag.get_attribute('href')
    unique_links.add(href)

for i in range(1,3):
  getLinks(i)

driver.quit()
result = list(unique_links)

with open('./links/dung_cu_ve_sinh_links.txt','w',encoding='utf-8') as file: 
  for link in result :
      file.write(link + "\n")


