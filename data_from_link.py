import selenium
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("disable-infobars")
options.add_argument("start-maximised")
options.add_argument("disable-dev-shm-usage")
options.add_argument("disable-blink-features=AutomationControlled")
options.add_argument("no-sandbox")

cService = webdriver.ChromeService(executable_path= '/home/sohlost/Projects/beatprints_engine/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=cService)
driver.get("https://genius.com/The-weeknd-blinding-lights-lyrics")
element = driver.find_element("xpath", '//*[@id="application"]/main/div[1]/div[3]/div[1]/div[1]/h1/span').get_attribute("innerText")

print(element)

driver.quit()
