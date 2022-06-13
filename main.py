from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time


driver = webdriver.Chrome()
info = {
    'Location': [],
    'Business Name': [],
    'Business Type': [],
    'Phone Number': []
}
searches = ['Fresno California', 'Kernersville NC', 'Yosemite']
for i in searches:
    store = [f'convenience stores in {i}', f'grocery stores in {i}']
    sub_total = 0
    total = 0
    for keyw in store:
        url = 'https://search.yahoo.com/'
        driver.get(url)
        search = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="yschsp"]')))
        search.send_keys(keyw)
        search.send_keys(Keys.ENTER)
        more = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="web"]/ol/li[1]/div/div[2]/p/a')))
        more.click()
        time.sleep(5)
        counter = 1
        pages = 1
        while counter <= 15:
            try:
                bn_path = f'/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div/div/div/ol/li/div/ul/li[{counter}]/' \
                          f'div[1]/div[1]/div/a'
                bt_path = f'/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div/div/div/ol/li/div/ul/li[{counter}]/' \
                          f'div[1]/div[2]/span[1]/span'
                p_path = f'/html/body/div[1]/div[3]/div/div[1]/div[1]/div/div/div/div/ol/li/div/ul/li[{counter}]/' \
                         f'div[1]/div[3]/span[2]/span[2]'
                business_name = WebDriverWait(driver, 15).until(ec.presence_of_element_located(
                    (By.XPATH, bn_path))).text
                business_type = WebDriverWait(driver, 15).until(ec.presence_of_element_located(
                    (By.XPATH, bt_path))).text
                phone = driver.find_element(By.XPATH, p_path).text
                if business_name not in info['Business Name'] and \
                        'Convenience Store' in business_type or 'Grocery Store' in business_type:
                    info['Business Name'].append(business_name)
                    info['Business Type'].append(business_type)
                    info['Phone Number'].append(phone)
                    info['Location'].append(i)
                    sub_total += 1
                    total += 1
            except:
                pass
            counter += 1
            if counter > 15:
                time.sleep(2)
                next_items = driver.find_element(By.XPATH, '//a[text()="Next"]')
                next_items.click()
                counter = 1
            print(sub_total)
            if sub_total == 155:
                driver.close()
                break
        if total == 335:
            break
print(info)
print(len(info['Business Name']))
