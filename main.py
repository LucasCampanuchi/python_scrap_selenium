import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By
import http.client

DRIVER_PATH = '/usr/local/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('disable-infobars')
options.add_argument('--remote-debugging-port=9222')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-notifications")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


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
            'link': children[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'),
            'font': {
                'name': 'Mercado Livre',
                'slug': 'mercado_livre'
            }
        })

    return products    

def apiShopee(search): 
    conn = http.client.HTTPSConnection("shopee.com.br")
    payload = ''
    headers = {
    'Cookie': 'REC_T_ID=d383782e-48fd-11ed-b3a3-005056bd1ef9; SPC_EC=Q2o4UGRXaElFZUVURjNOd3nt7yvzlxWS1odrgid7HOmigvA3BPfpVNdt/0D6r0juZYl2Kx8Xh6BAE0Xhpe3KYePmLgAYjWs4CANmQeTusiHyTKLDPG3uszDmQQ35Q7kag3S14yTTdUUYbmprErWGAXZE50BBgkT/aNdJdPE1U03SIXPzrFLbwLTKaLlzWEr0; SPC_F=YJ9dnyanXrRih3Y2rHBfwI3E4B77qz9I; SPC_R_T_ID=lxWJIAW6mNg+9NFf262Nq8Kzlli1BTO/ANLF76a62zPw9HVIrVxSiAMDy9teQ7CBAR5EjuU8vQDw5tj55kipTSdLWWOVsjk9o7JE32cSdEY=; SPC_R_T_IV=1n3VTz9xl2q+A7UZjdrx8A==; SPC_SI=mall.O5bXQ38bFgtfAUtAZWHFEkrQI9S0KNwA; SPC_ST=.UnM0czdmQkw4NUI5Q1I4RZT8rmIc3OOs3MaAkYncswCZ5t+uK3Mf8fl6yiAKymgMnj+TSvY5P7KuHGhWbbRNSdUikr8dx/w6QfnG8fR/zOfOleIvduV+FP1hHi4+U5tIe8Oza0iH+HjKDC51ucMe4JhzTxR02Gfz1QXagFJ/jBrQedPWknoqjRTfhNQ2hqk3mM10mMiiJ7U8TH7NuZ0sEw==; SPC_T_ID=lxWJIAW6mNg+9NFf262Nq8Kzlli1BTO/ANLF76a62zPw9HVIrVxSiAMDy9teQ7CBAR5EjuU8vQDw5tj55kipTSdLWWOVsjk9o7JE32cSdEY=; SPC_T_IV=1n3VTz9xl2q+A7UZjdrx8A==; SPC_U=223551221'
    }
    conn.request("GET", f"/api/v4/search/search_items?by=relevancy&keyword={search.replace(' ', '%20')}&limit=10&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = json.loads(data.decode("utf-8"))

    products = []

    for product in response['items']:
        products.append({
            'title': product['item_basic']['name'],
            'price': product['item_basic']['price'],
            'link': f"https://shopee.com.br/{product['item_basic']['name'].replace(' ', '-')}-i.{product['item_basic']['shopid']}.{product['item_basic']['itemid']}",            
            'font': {
                'name': 'Shopee',
                'slug': 'shopee'
            }
        })

    return products

def scrapAmazon(search):
    driver.get('https://www.amazon.com.br/s?k='+search)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "s-result-item"))
    )

    products = []
    productsElements = driver.find_elements(By.CLASS_NAME, 's-result-item')

    for product in productsElements:
        children = product.find_elements(By.CLASS_NAME, 'a-link-normal')        

        if len(children) > 0:
            if len(children) > 1:
                price = product.find_elements(By.CLASS_NAME, 'a-price-whole')
                if len(price) > 0:
                    products.append({
                        'title': children[1].text,
                        'price': price[0].text,
                        'link': children[0].get_attribute('href'),
                        'font': {
                            'name': 'Amazon',
                            'slug': 'amazon'
                        }
                    }) 
    
    return (lambda product: product['title'] != '', products)
            
def search(search):
    products = []

    products += scrapMercadoLivre(search)
    products += scrapAmazon(search)
    products += apiShopee(search)    

    return products
     


if __name__ == '__main__':
    print(search('placa de video'))
    driver.quit()



    

    






