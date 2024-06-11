import requests
import bs4
import lxml
import fake_headers
import json

URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def get_headers():
    return fake_headers.Headers(browser='chrome', os='win').generate()


def proverka(url_href):
    response = requests.get(url_href, headers=get_headers())
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        tag1 = soup.find('div', class_='vacancy-title')
        tag2 = tag1.find('div', {'data-qa': 'vacancy-salary'})
        tag3 = tag2.find('span')
        вилка_зп = tag3.text
        if '$' in вилка_зп or 'usd' in вилка_зп.lower():
            tag1 = soup.find('div', class_='vacancy-section')
            if 'django' in tag1.text.lower() or 'flask' in tag1.text.lower():
                tag1 = soup.find('span', class_='vacancy-company-name')
                tag2 = tag1.find('a')
                tag3 = tag2.find('span')
                название_компании = tag3.text
                tag1 = soup.find(
                    'div', class_='magritte-text___pbpft_3-0-4 magritte-text_style-primary___AQ7MW_3-0-4 magritte-text_typography-paragraph-2-regular___VO638_3-0-4')
                город = tag1.text
                return {'ссылка': url_href, 'вилка зп': вилка_зп, 'название компании': название_компании, 'город': город}


data_all = []
n = 0
while True:
    response = requests.get(f'{URL}&page={n}', headers=get_headers())
    n += 1
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        tag1 = soup.find('div', id='a11y-main-content')
        for tag2 in tag1.find_all('h2'):
            tag3 = tag2.find('a')
            url_href = tag3['href']
            try:
                data = proverka(url_href)
            except:
                data = None
            if data:
                data_all.append(data)
    else:
        break

with open("data.json", "w") as f:
    json.dump(data_all, f, indent=4, ensure_ascii=False)
