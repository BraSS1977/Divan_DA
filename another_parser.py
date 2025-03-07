from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd
import matplotlib.pyplot as plt
import re

# Опции для Firefox
options = Options()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.36')  # Подмена User-Agent

# Запуск браузера Firefox
driver = webdriver.Firefox(options=options)
url = 'https://skdesign.ru/product-category/sofas?utm_source=yandex&utm_medium=cpc&utm_campaign=rf_konkurenti_divani_poisk&utm_content=16656615084&utm_term=---autotargeting&calltouch_tm=yd_c%3A115929218_gb%3A5512824776_ad%3A16656615084_ph%3A53677718962_st%3Asearch_pt%3Apremium_p%3A2_s%3Anone_dt%3Adesktop_reg%3A213_ret%3A53677718962_apt%3Anone&yclid=10471959217663639551'

try:
    driver.get(url)

    # Ожидание загрузки элементов с ценами
    prices = WebDriverWait(driver, 120).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='CardPricesc__CardPriceContainer-sc-1mqsou5-0 fBumnl']"))
    )

    if not prices:
        raise ValueError("Не удалось найти элементы с ценами на странице.")

    # Открытие CSV файла для записи
    with open('divan_prices.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Price'])

        # Запись цены в CSV файл
        for price in prices:
            writer.writerow([price.text.strip('"')])  # Записываем цену в CSV

    print("Цены успешно записаны в файл 'divan_prices.csv'.")

###

    def clean_price(price):
        # Удаление всех символов, кроме цифр
        digits_only = re.sub('[^0-9]', '', price)
        return int(digits_only) if digits_only else 0  # Возврат 0, если строка пустая


    # Чтение данных из исходного CSV файла и их обработка
    input_file = 'divan_prices.csv'
    output_file = 'cleaned_prices.csv'

    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='',
                                                                      encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Чтение заголовка и запись его в новый файл
        header = next(reader)
        writer.writerow(header)

        # Обработка и запись данных в строках
        for row in reader:
            for price in row[0].split('\n'):  # Разделяем строку по символу новой строки
                clean_row = [clean_price(price.strip())]  # Чистим каждую часть и записываем в новый ряд
                writer.writerow(clean_row)

    print(f"Обработанные данные сохранены в файл {output_file}")
###



except Exception as e:
    print(f"Ошибка: {e}")


# Чтение очищенных данных из CSV файла
cleaned_prices_df = pd.read_csv('cleaned_prices.csv')

# Расчет средней цены
average_price = cleaned_prices_df['Price'].mean()
print(f'Средняя цена на диваны составляет: {average_price:.0f} рублей')

# Построение гистограммы цен
plt.figure(figsize=(10, 6))
plt.hist(cleaned_prices_df['Price'], bins=20, color='skyblue', edgecolor='black')
plt.title('Распределение цен на диваны')
plt.xlabel('Цена (руб.)')
plt.ylabel('Количество')
plt.grid(axis='y', alpha=0.75)


plt.show()

# Закрытие браузера
driver.quit()