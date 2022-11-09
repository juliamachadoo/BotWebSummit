import pandas as pd
import pyperclip
import pyautogui
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys


driver = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
driver.maximize_window()
action = ActionChains(driver)
dicionarioStartups = dict()
listaAux = list()


# driver.get('https://websummit.com/startups/featured-startups')
# time.sleep(3)

driver.get('https://websummit.com/startups/featured-startups?q=eyJwYWdlIjozNSwiY29uZmlndXJlIjp7ImhpdHNQZXJQYWdlIjo0OCwidGFnRmlsdGVycyI6WyJ3czIyIl19fQ==')
time.sleep(3)

acceptCookies = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div/div[2]/div[2]')
acceptCookies.click()
time.sleep(1)

pontoScroll01 = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div[1]/div/div[1]')
driver.execute_script("arguments[0].scrollIntoView();", pontoScroll01)
time.sleep(0.5)

pageNumberText = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div[2]/nav/ul/li[8]').text
pageNumber = int(pageNumberText)

for paginas in range(1, pageNumber + 1):
    logo = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div[2]/div/div')
    logo.click()
    time.sleep(1)

    nextPage = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/button[2]')

    div_principal = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div/div')
    divs = div_principal.find_elements(By.XPATH, './ul/div')

    i = 1

    for div in range(1, len(divs)):
        companyName = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/div/div/div/ul/div[{i}]/div/div/div[2]/div[1]').text
        print(companyName)
        time.sleep(1)
        dicionarioStartups['Nome'] = companyName

        description = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/div/div/div/ul/div[{i}]/div/div/div[2]/div[2]/div[1]').text
        dicionarioStartups['Descrição'] = description
        # print(description)
        time.sleep(0.3)

        try:
            location = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/div/div/div/ul/div[{i}]/div/div/div[2]/div[2]/div[3]/div/span/span').text
            dicionarioStartups['País'] = location
        # print(location)
            time.sleep(0.3)
        except NoSuchElementException:
            dicionarioStartups['País'] = " - "

        webSiteButton = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/div/div/div/ul/div[{i}]/div/div/div[2]/div[2]/div[2]/a[1]')
        time.sleep(0.1)
        action.context_click(webSiteButton).perform()
        time.sleep(0.3)
        for down in range(0, 5):
            pyautogui.press('down')
            time.sleep(0.11)
        urlCopiado = pyautogui.press('enter')
        urlColado = pyperclip.paste()
        websiteURL = urlColado
        time.sleep(0.3)
        # print(websiteURL)
        dicionarioStartups['Website'] = websiteURL

        divLinks = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/div/div/div/ul/div[{i}]/div/div/div[2]/div[2]/div[2]')
        try:
            linkedInButton = divLinks.find_element(By.XPATH, './a[contains(@href, "linkedin")]')
            if linkedInButton.is_enabled():
                time.sleep(0.3)
                action.context_click(linkedInButton).perform()
                time.sleep(0.5)
                for down in range(0, 5):
                    pyautogui.press('down')
                    time.sleep(0.1)
                linkedINurlCopiado = pyautogui.press('enter')
                linkedINurlColado = pyperclip.paste()
                linkedINurl = linkedINurlColado
                time.sleep(.5)
                # print(linkedINurl)
                dicionarioStartups['LinkedIN'] = linkedINurl
        except NoSuchElementException:
            dicionarioStartups['LinkedIN'] = "None"
        i += 1

        listaAux.append(dicionarioStartups.copy())
        time.sleep(0.3)
        dataframe = pd.DataFrame(listaAux)
        time.sleep(0.3)
        dataframe.to_excel('Planilha Startups Summit 2022.xlsx', index=False)
        time.sleep(1)

        try:
            if nextPage.is_enabled():
                time.sleep(1)
                nextPage.click()
                time.sleep(1)
        except:
            pass

    else:
        time.sleep(0.5)
        pyautogui.press('esc')
        time.sleep(1)
        pontoScroll02 = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div[2]/nav/ul/li[9]')
        driver.execute_script("arguments[0].scrollIntoView();", pontoScroll02)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div[2]/nav/ul/li[9]').click()
        time.sleep(5)




