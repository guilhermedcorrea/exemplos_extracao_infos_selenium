from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import Literal, List, Generator
import pandas as pd


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")

driver.get('https://tarkett.com.br/')

def scroll() -> None:
    
    driver.implicitly_wait(7)
        
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
        
    while(match==False):
        lastCount = lenOfPage

        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def confere_skus() -> Generator[list, None, None]:
    lista_dicts: list = []
    driver.implicitly_wait(7)
    data = pd.read_excel('D:\\produtoshausz\\tarkett\\excelfile\\tarkett.xlsx')
    skus = data.loc[:,'SKU'].to_list()
    for sku in skus:
        busca = driver.find_element(By.CSS_SELECTOR,'#searchText')
        busca.clear()
        busca.send_keys(sku)

        time.sleep(1)

        dict_produtos: dict = {}

        try:
            pesquisa = driver.find_element(By.CSS_SELECTOR, '#btBuscaSite').click()
        except:
            print("error")
        try:
            imagem = driver.find_elements(By.XPATH,'//*[@id="produtos"]/div/div/figure/img')
            for img in imagem:
                try:
                    dict_produtos['imagem'] = img.get_attribute('src')
                except:
                    dict_produtos['imagem'] = 'valor nao encontrado'
        except:
            print("erro imagem")
        
        try:
            formato = driver.find_elements(By.XPATH, '//*[@id="produtos"]/div/div/article/p')[0].text
            dict_produtos['formato'] = formato.split(": ")[-1].capitalize()
        except:
            print('erro')

        try:
            referencias = driver.find_elements(By.XPATH,'//*[@id="produtos"]/div/div/article/div')
            for referencia in referencias:
                skus = referencia.text.split("\n")
                for sku in skus:
                    if re.search('\d+',sku, re.IGNORECASE):
                        try:
                            dict_produtos['codigoprodutoo'] = sku
                            dict_produtos['ulrbusca'] = 'https://tarkett.com.br/busca/' + sku
                        except:
                            dict_produtos['codigoprodutoo'] = 'valor nao encontrado'

                    if re.search('x|mm',sku, re.IGNORECASE):
                        try:
                            dict_produtos['dimensoes'] = sku
                        except:
                            dict_produtos['dimensoes'] = 'valor nao encontrado'
         
        except:
            print("erro referencias")
        print(dict_produtos)
        lista_dicts.append(dict_produtos)

        data = pd.DataFrame(lista_dicts)
        data.to_excel(r'D:\produtoshausz\tarkett\excelfile\tarkett_skus.xlsx')

 

listas = confere_skus()
