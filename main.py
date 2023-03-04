import requests
import time
import random
from datetime import date
from bs4 import BeautifulSoup
from database import insert


class Divar:
    def __init__(self, url=None):
        self.element = None
        self.advertise_details = None
        self.url = url
        self.request = None
        self.content = None
        self.date_time()
        self.added_in_db = []

    def send_request(self):
        s = requests.Session()
        self.request = s.get(self.url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"})

    def send_to_db(self):
        for adv in self.added_in_db:
            insert(adv)
            self.added_in_db.remove(adv)
        print(f'\033[96m {len(self.added_in_db)} inserted in db')

    def html_content(self):
        self.content = self.request.text
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def find_home_page_elements(self):
        self.old_href = []
        self.hrefs = []
        class_attr = 'post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46'
        self.elements = self.soup.find_all('div', {'class': class_attr})
        for elm in self.elements:
            url = 'https://divar.ir'
            href = url + elm.find('a')['href']
            self.hrefs.append(href)

    def find_advertise_details(self):
        try:
            self.advertise_details = {}

            class_attr = 'container--has-footer-d86a9 kt-container'
            self.element = self.soup.find('div', {'class': class_attr})
            advertise_detail = self.element.find('div', {'class': 'kt-col-5'})
            title = advertise_detail.find('div', class_='kt-page-title__title kt-page-title__title--responsive-sized').text
            kilometer, production_year, color = advertise_detail.find_all('span', class_='kt-group-row-item__value')
            kilometer, production_year, color = kilometer.text, production_year.text, color.text
            specifications = advertise_detail.find_all('p', class_="kt-base-row__title kt-unexpandable-row__title")[1:]
            values = advertise_detail.find_all('p', class_="kt-unexpandable-row__value")

            self.advertise_details['title'] = title
            self.advertise_details['kilometer'] = kilometer
            self.advertise_details['production_year'] = production_year
            self.advertise_details['color'] = color

            for i in range(len(specifications)):
                specification = specifications[i].text
                value = values[i].text
                self.advertise_details[specification] = value

            self.advertise_details['year'] = self.year
            self.advertise_details['month'] = self.month
            self.advertise_details['day'] = self.day
            self.added_in_db.append(self.advertise_details)

        except:
            pass

    def extract_advertise_details(self):
        for href in self.hrefs:
            if href not in self.old_href:
                self.url = href
                print(f'\033[93m url: ----> {self.url}')
                self.send_request()
                time.sleep(5)
                self.html_content()
                time.sleep(5)
                self.find_advertise_details()
                self.old_href.append(href)
            else:
                continue

    def date_time(self):
        now_date = date.today()
        self.year, self.month, self.day = now_date.year, now_date.month, now_date.day


batch = 1
while True:
    time_ = random.randint(350, 900)
    divar = Divar('https://divar.ir/s/tehran/car')
    print(f'\033[92m start crawling for batch {batch}...')
    divar.send_request()
    print('\033[95m sent request ...')
    divar.html_content()
    divar.find_home_page_elements()
    divar.extract_advertise_details()
    divar.send_to_db()
    time.sleep(time_)
    batch += 1
