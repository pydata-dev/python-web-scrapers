import requests
from bs4 import BeautifulSoup
import openpyxl
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

url = "https://news.ycombinator.com"

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Ошибка при запросе: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")
titles = soup.find_all("span", class_="titleline")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Новости"
ws.append(["№", "Заголовок", "Источник", "Ссылка"])

for i, title in enumerate(titles[:30], 1):
    a_tag = title.find("a")
    headline = a_tag.get_text(strip=True) if a_tag else title.get_text(strip=True)
    link = a_tag["href"] if a_tag else ""
    site_tag = title.find("span", class_="sitestr")
    source = site_tag.get_text(strip=True) if site_tag else ""
    ws.append([i, headline, source, link])

desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Рабочий стол")
filepath = os.path.join(desktop, "static1.xlsx")
wb.save(filepath)
print(f"Готово! Файл сохранён: {filepath}")