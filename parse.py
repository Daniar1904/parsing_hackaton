import csv
from bs4 import BeautifulSoup
import requests
count = 0

def get_html(url: str) ->str:
    response = requests.get(url)
    return response.text

def get_data(html: str) -> bool:

    soup = BeautifulSoup(html, 'html.parser')

    catalog = soup.find('div', class_='list-view')
    if not catalog:
        return False

    phones = catalog.find_all('div', class_ = 'item product_listbox oh')

    for phone in phones:
        title = phone.find('div', class_='listbox_title oh').text.strip()

        price = phone.find('div', class_='listbox_price text-center').text

        try:
            image = phone.find('img').get('src')
        except:
            image = 'Нет картинки'
        
        data = {
            'title': title,
            'price': price,
            'img': image
        }
        write_to_csv(data)
    return True

def write_to_csv(data: dict) -> None:
    '''Функция для записи данных в csv файл'''
    global count
    with open('phones.csv', 'a') as file:
        fieldnames = ['№', 'Модель', 'Цена', 'Фото']
        writer = csv.DictWriter(file, fieldnames)
        count += 1
        writer.writerow({
            '№': count,
            'Модель': data.get('title'),
            'Цена': data.get('price'),
            'Фото': data.get('img')
        })
        
def prepare_csv() -> None:
    '''Подготавливает csv файл'''
    with open('phones.csv', 'w') as file:
        fieldnames = ['№', 'Модель', 'Цена', 'Фото']
        writer = csv.DictWriter(file, fieldnames)
        writer.writerow({
            '№': '№',
            'Модель': 'Модель',
            'Цена': 'Цена',
            'Фото': 'Фото'
        })

def main():
    i = 1
    prepare_csv()
    while True:
        BASE_URL = f'https://www.kivano.kg/mobilnye-telefony?page={i}'
        html = get_html(BASE_URL)
        is_res = get_data(html)
        if not is_res:
            break
        print(f'Страница: {i}')
        i += 1

main()