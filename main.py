import time
from helpful import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
browser.get('https://www.thuiswinkel.org/leden')

links = []
while True:
    check = browser.find_elements(By.XPATH, '//ul[@class="flex flex-wrap space-x-2"]/li/a')[2].text
    if check != '60':
        ledens = browser.find_elements(By.CSS_SELECTOR, '#results > ul > li')
        for leden in ledens:
            link = leden.find_element(By.TAG_NAME, 'a').get_attribute('href')
            links.append(link)
        browser.find_elements(By.XPATH, '//ul[@class="flex flex-wrap space-x-2"]/li/a')[-1].click()
    else:
        break

needed = {}
for link in links:
    browser.get(link)
    name = browser.find_element(By.XPATH, '//h1[@class="h1 order-2"]').text
    infos = browser.find_elements(By.XPATH, '//div[@class="flex-1"]')
    domain = domain = infos[0].text
    location = 'No address found.'
    try:
        location = infos[4].text
    except IndexError:
        pass

    needed.update({
        "Company's Name": name,
        "Domain": domain,
        "Location": location,
    })

    write_json(needed, 'results/thuiswinkel.json')
write_csv('results/thuiswinkel.json')

time.sleep(2)