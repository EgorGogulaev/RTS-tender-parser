import datetime
import os
import time
import json
import sqlite3

try:
    from bs4 import BeautifulSoup
    import lxml
    from selenium.webdriver import ChromeOptions, Chrome
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    import selenium.common
    from sqlalchemy.orm import declarative_base
    from sqlalchemy import Column, VARCHAR, Integer, BigInteger
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

except:
    os.system("pip install selenium")
    os.system("pip install bs4")
    os.system("pip install lxml")
    os.system("pip install undetected_chromedriver")
    os.system("pip install sqlalchemy")

    from bs4 import BeautifulSoup
    import lxml
    from selenium.webdriver import ChromeOptions, Chrome
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    import selenium.common
    from sqlalchemy import Column, VARCHAR, Integer, BigInteger
    from sqlalchemy.orm import declarative_base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

with sqlite3.connect('RTS_SQLite.db') as conn:
    pass

engine = create_engine('sqlite:///RTS_SQLite.db')

# todo data class for SQLAlchemy
Base = declarative_base()


class RTS_info(Base):
    __tablename__ = "rts_info"

    rts_info_id = Column(Integer, primary_key=True)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    тип_закупки = Column(VARCHAR)
    номер_закупки = Column(VARCHAR)

    заказ = Column(VARCHAR)

    начальная_цена = Column(BigInteger)
    обеспечение_заявки = Column(BigInteger)
    статус = Column(VARCHAR)

    организатор = Column(VARCHAR)

    заказчик = Column(VARCHAR)

    регион = Column(VARCHAR)
    адрес_поставки = Column(VARCHAR)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


Base.metadata.create_all(engine)
# ______________________________


options = uc.ChromeOptions()
options.add_argument("--start-maximize")



with uc.Chrome(options=options) as browser:
    try:
        with sessionmaker(bind=engine)() as session:
            wait = WebDriverWait(browser, 10)
            for page_number in range(93, 1051):
                browser.get(f"https://www.rts-tender.ru/poisk/etps/rts-tender/?page={page_number}")

                try:
                    wait.until(EC.visibility_of_element_located((By.ID, 'content')))
                except:
                    pass
                card_elements = browser.find_elements(By.CSS_SELECTOR, 'div[class="card-item"]')

                for card_element in card_elements:

                    try:тип_закупки = card_element.find_elements(By.CSS_SELECTOR, 'span[class="plate__item"]')[0].text.strip()
                    except:тип_закупки = None

                    try:номер_закупки = card_element.find_element(By.CSS_SELECTOR, 'div[class="card-item__about"] a[href][target="_blank"]').text.lower().replace("закупка", "").replace("в еис", "").strip()
                    except:номер_закупки = None

                    try: заказ = card_element.find_element(By.CSS_SELECTOR, 'div[class="card-item__title"]').text.strip()
                    except: заказ = None

                    try: начальная_цена = int(float(card_element.find_element(By.CSS_SELECTOR, 'div[class="card-item__properties-desc"][itemprop="price"]').get_attribute('content')))
                    except: начальная_цена = None

                    try: обеспечение_заявки = int(float(card_element.find_elements(By.CSS_SELECTOR, 'div[class="card-item__properties-cell"]')[1].find_element(By.CSS_SELECTOR, 'div[class="card-item__properties-desc"]').text.strip().split()[0].replace("&nbsp;", '').replace(",", '.')))
                    except: обеспечение_заявки = None

                    try: статус = card_element.find_elements(By.CSS_SELECTOR, 'div[class="card-item__properties-cell"]')[3].find_element(By.CSS_SELECTOR, 'div[class="card-item__properties-desc"]').text.strip()
                    except: статус = None

                    try: организатор = card_element.find_element(By.CSS_SELECTOR, 'div[class="card-item__organization-main"] a[class="text--bold"]').text.strip()
                    except: организатор = None

                    try: заказчик = card_element.find_element(By.XPATH, '//div//div/p[1]/span').text.strip()
                    except: заказчик = None

                    try: регион = card_element.find_element(By.XPATH, '//div/div//div/div[2]/div/p/a').text.strip()
                    except: регион = None

                    try: адрес_поставки = card_element.find_element(By.CSS_SELECTOR, 'span[itemprop="areaServed"]').text.strip()
                    except: адрес_поставки = None

                    RTS_info_object = RTS_info(
                        тип_закупки=тип_закупки,
                        номер_закупки=номер_закупки,
                        заказ=заказ,
                        начальная_цена=начальная_цена,
                        обеспечение_заявки=обеспечение_заявки,
                        статус=статус,
                        организатор=организатор,
                        заказчик=заказчик,
                        регион=регион,
                        адрес_поставки=адрес_поставки,
                    )

                    session.add(RTS_info_object)
                    session.commit()

                print(f"Page {page_number} of 1000.")
    except Exception as ex:
        os.system('git add .')
        os.system('git commit -m "Updated database with new data"')
        os.system('git push')

os.system('git add .')
os.system('git commit -m "Updated database with new data"')
os.system('git push')

print('Done!')
