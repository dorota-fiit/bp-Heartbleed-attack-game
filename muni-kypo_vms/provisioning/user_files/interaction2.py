from multiprocessing.context import ForkContext
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


firefoxOptions = Options()
firefoxOptions.add_argument("-headless")

driver = webdriver.Firefox(options=firefoxOptions)
driver.get('https://www.heartbleedlabelgg.com')


#login
driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]/div/div[2]/form/fieldset/div[1]/input').send_keys('admin')
driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]/div/div[2]/form/fieldset/div[2]/input').send_keys('seedelgg')
driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]/div/div[2]/form/fieldset/div[3]/input').click()

#add a security exception
#driver.find_element_by_xpath('//*[@id="dadvancedButton"]').click()
#driver.find_element_by_xpath('//*[@id="exceptionDialogButton"]').click()

#search for friend
more=driver.find_element_by_xpath('/html/body/div/div[3]/div/ul/li[6]/a')
members=driver.find_element_by_xpath('/html/body/div/div[3]/div/ul/li[6]/ul/li[1]/a')
Hover=ActionChains(driver).move_to_element(more).move_to_element(members)
Hover.click().perform()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="elgg-user-40"]/div/div[2]/h3/a'))).click()

#send message
driver.find_element_by_xpath('/html/body/div/div[4]/div/div/div/div[3]/div/div[1]/ul[1]/li[3]/a').click()
driver.find_element_by_xpath('/html/body/div/div[4]/div/div/div[2]/form/fieldset/div[2]/input').send_keys('Re:news')
driver.find_element_by_xpath('/html/body/div/div[4]/div/div/div[2]/form/fieldset/div[3]/textarea').send_keys('Would you like to meet?')
driver.find_element_by_xpath('/html/body/div/div[4]/div/div/div[2]/form/fieldset/div[4]/input').click()

#logout and login again
driver.find_element_by_xpath('/html/body/div/div[2]/div/ul[1]/li[3]/a').click()
driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]/div/div[2]/form/fieldset/div[1]/input').send_keys('admin')
driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]/div/div[2]/form/fieldset/div[2]/input').send_keys('seedelgg')
driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[1]/div/div[2]/form/fieldset/div[3]/input').click()

driver.quit()