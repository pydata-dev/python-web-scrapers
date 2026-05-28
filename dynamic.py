import os
import platform
import subprocess
import time
from datetime import datetime
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 1. Настройка Selenium (Headless)
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

URL = "https://quotes.toscrape.com/js"
scraped_data = []

try:
    print(f"Запуск парсинга. Целевой URL: {URL}")
    driver.get(URL)

    page_number = 1
    while True:
        print(f"Обработка страницы {page_number}...")

        # Ожидаем загрузки контента
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        quote_elements = soup.find_all("div", class_="quote")

        for element in quote_elements:
            text = element.find("span", class_="text").text.strip().strip("“”")
            author = element.find("small", class_="author").text.strip()

            tags_elements = element.find("div", class_="tags").find_all("a", class_="tag")
            tags_str = ", ".join([t.text.strip() for t in tags_elements])
            tags_count = len(tags_elements)

            scraped_data.append(
                {
                    "Quote": text,
                    "Author": author,
                    "Tags": tags_str,
                    "Tags Count": tags_count,
                }
            )

        # Динамическая пагинация через клик по кнопке Next
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
            next_button.click()
            page_number += 1
            time.sleep(1.5)  # Пауза для прогрузки JS
        except NoSuchElementException:
            print("Все страницы успешно обработаны.")
            break
        except TimeoutException:
            print("Ошибка ожидания кнопки пагинации.")
            break

finally:
    driver.quit()

# 2. Запись в Excel и умное определение пути для сохранения
if scraped_data:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()

    # Проверяем наличие папки "парсеры" рядом со скриптом
    local_parsers_folder = os.path.join(current_dir, "парсеры")

    if os.path.exists(local_parsers_folder) and os.path.isdir(local_parsers_folder):
        target_dir = local_parsers_folder
    else:
        # Если папки "парсеры" нет — ищем Рабочий стол (с учетом OneDrive)
        home_dir = os.path.expanduser("~")
        onedrive_desktop = os.path.join(home_dir, "OneDrive", "Desktop")
        standard_desktop = os.path.join(home_dir, "Desktop")

        if os.path.exists(onedrive_desktop):
            target_dir = onedrive_desktop
        else:
            target_dir = standard_desktop

    # Генерация имени файла ОДНОВРЕМЕННО с сохранением
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quotes_{timestamp}.xlsx"
    full_path = os.path.join(target_dir, filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Quotes Data"

    headers = ["Текст цитаты", "Автор", "Теги", "Количество тегов (int)"]
    ws.append(headers)

    for item in scraped_data:
        ws.append([item["Quote"], item["Author"], item["Tags"], item["Tags Count"]])

    wb.save(full_path)
    print(f"\n[УСПЕХ] Файл создан: {filename}")
    print(f"Путь сохранения: {full_path}")

    # Кроссплатформенный автоматический запуск проводника/папки
    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.startfile(target_dir)
        elif current_os == "Darwin":  # macOS
            subprocess.Popen(["open", target_dir])
        else:  # Linux
            subprocess.Popen(["xdg-open", target_dir])
    except Exception as e:
        print(f"[ИНФО] Не удалось автоматически открыть папку: {e}")

else:
    print("\n[ОШИБКА] Массив данных пуст. Файл не создавался.")