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
import pandas as pd
from typing import Literal, List
import json
from itertools import chain
from openpyxl.workbook import Workbook
from datetime import datetime

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")




def scroll() -> None:
    driver.implicitly_wait(7)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage

        time.sleep(3)
            
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def criar_template(keys):

    lista1 = []
    lista2 = []
    for dic in keys:

        th = f'<th scope="col">{dic}</th>'
        tr = f'<td>{keys[dic]}</td>'
        lista1.append(th)
        lista2.append(tr)


    template = """<table class="table">
            <caption>List of users</caption>
            <thead>
            <tr>
                {}
            </tr>
            </thead>
            <tbody>
            <tr>
                {}
            </tr>
            </tbody>
            </table>""".format([x.split("\n") for x in lista1], [x.split("\n") for x in lista2])


    body = template.replace("[","").replace("]","").replace("'","").replace(",","\n")

    return body



def get_url_produto():
    
    urls = ["https://www.celite.com.br/produtos/piso-box?page=1"
        ,"https://www.celite.com.br/produtos/mecanismo-original-stylus-excellence-CE96911281?sku=CE1969110010100",
        "https://www.celite.com.br/produtos/bide-3furos-apontados-metal-ducha-central-CE164000?sku=CE1124000010300",
        "https://www.celite.com.br/produtos/gabinete-03gavetas-02portas-cuba-apoio-CEM27G240?sku=CEB60004"]

    for url in urls:
        driver.get(url)
    
        dict_item = {}

        try:
            nomeproduto = driver.find_elements(By.XPATH,'//*[@id="prod-name"]')[0].text
            dict_item['NomeProduto'] = nomeproduto
        except:
                pass    
                        
        try:
            codigo  = driver.find_elements(By.XPATH,'//*[@id="prod-ref"]')[0].text
            dict_item['CodigoProduto'] = codigo
        except:
            pass

        try:
            dim_val1 = driver.find_elements(By.XPATH,'//*[@id="anclaProductDetail"]/div[2]/div/div[2]/div/div/div/form/div[1]/div[1]/div')
            cont = 0
            for x in dim_val1:
                attr = x.text.split("\n")
                for att in attr:
                    dict_item['Atributo'+str(cont)] = att
                    cont +=1

        except:
            pass

        imagens = driver.find_elements(By.XPATH,'/html/body/div[1]/section/div[1]/div/div/div/div[3]/section/div/div[2]/div/section/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div/img')
        cont = 0
        for imagem in imagens:
            dict_item['imagem'+str(cont)] = imagem.get_attribute('src')
            cont+=1

        yield dict_item

strs = get_url_produto()
for st in strs:
    st.get('CodigoProduto')
 
    templates = criar_template(st)
 
    print(templates)

