import os

from datetime import datetime

import requests

from bs4 import BeautifulSoup

import openpyxl



# Автогенерация уникального имени файла на основе даты и времени

time_str = datetime.now().strftime("%Y%m%d_%H%M%S")

FILENAME = f"books_{time_str}.xlsx"



# Маппинг рейтинга

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}



headers = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

}



wb = openpyxl.Workbook()

ws = wb.active

ws.title = "Книги"

ws.append(["Название", "Цена", "Рейтинг"])



for page in range(1, 4):

    url = f"http://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Парсим страницу {page}...")

   

    try:

        response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status() # Вызовет исключение для кодов 4xx/5xx

    except requests.RequestException as e:

        print(f"Ошибка сети или некорректный статус-код на странице {page}: {e}")

        continue



    # Фикс кодировки

    response.encoding = "utf-8"

   

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")



    for book in books:

        h3_tag = book.find("h3")

        a_tag = h3_tag.find("a") if h3_tag else None

       

        price_tag = book.find("p", class_="price_color")

        rating_tag = book.find("p", class_="star-rating")



        # Парсим даже если чего-то не хватает, защищаясь от AttributeError

        title = a_tag.get("title", "").strip() if a_tag else "Без названия"

       

        # Безопасное приведение цены к числу

        price = 0.0

        if price_tag:

            price_text = price_tag.get_text().replace("£", "").strip()

            try:

                price = float(price_text)

            except ValueError:

                print(f"Не удалось конвертировать цену для книги '{title}': {price_text}")

       

        # Вытаскиваем рейтинг

        rating = 0

        if rating_tag:

            classes = rating_tag.get("class", [])

            rating_word = classes[1] if len(classes) > 1 else ""

            rating = RATING_MAP.get(rating_word, 0)

           

        ws.append([title, price, rating])



# Безопасное определение директории (работает и в скриптах, и в консоли)

try:

    current_dir = os.path.dirname(os.path.abspath(__file__))

except NameError:

    current_dir = os.getcwd()



full_path = os.path.join(current_dir, FILENAME)



wb.save(full_path)

print(f"\nГотово! Данные успешно сохранены в файл:\n{full_path}") 

