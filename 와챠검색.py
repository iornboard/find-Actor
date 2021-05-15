
from  selenium import webdriver
from bs4 import BeautifulSoup
import time, os
from datetime import datetime

from selenium.webdriver.common.keys import Keys

def main_search(name = '박서준') :
    link = 'https://watcha.com/ko-KR'

    driver = webdriver.Chrome('./chromedriver')
    driver.get(link)

    time.sleep(2)

    #검색어 창을 찾아 search 변수에 저장
    search = driver.find_element_by_xpath('//*[@id="search_bar_in_home"]')
    #search 변수에 저장된 곳에 값을 전송
    search.send_keys(name)
    time.sleep(1)
    #search 변수에 저장된 곳에 엔터를 입력
    search.send_keys(Keys.ENTER)
