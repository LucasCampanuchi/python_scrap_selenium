from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By

DRIVER_PATH = '/usr/local/bin/chromedriver'

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

def scrapTerabyte(search):
    driver.get('https://www.terabyteshop.com.br/busca?str='+search)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pbox"))
    )


    products = []
    productsElements = driver.find_elements(By.CLASS_NAME, 'pbox')

    for product in productsElements:
        children = product.find_elements(By.TAG_NAME, '*')
        
        def getPrice(e):
            try:
                return e.find_elements(By.CLASS_NAME, 'prod-new-price')[0].find_elements(By.TAG_NAME, 'span')[0].text
            finally:
                return '0'

        products.append({
            'title': children[0].get_attribute('title'),
            'price': getPrice(children[1]),
            'link': children[0].get_attribute('href')
        })


    return products

def scrapMercadoLivre(search):
    driver.get('https://lista.mercadolivre.com.br/'+search)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shops__result-wrapper"))
    )

    products = []
    productsElements = driver.find_elements(By.CLASS_NAME, 'shops__result-wrapper')

    for product in productsElements:
        children = product.find_elements(By.TAG_NAME, '*')

        products.append({
            'title': product.find_elements(By.TAG_NAME, 'h2')[0].text,
            'price': children[0].find_elements(By.CLASS_NAME, 'price-tag-fraction')[0].text,
            'link': children[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
        })

    return products      


if __name__ == '__main__':
    print(scrapTerabyte('placa de video'))
    print(scrapMercadoLivre('rtx 3080'))
    driver.quit()



    

    






