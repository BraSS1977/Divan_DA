from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import csv

# Опции для Firefox
options = Options()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/58.0.3029.110 Safari/537.36')  # Подмена User-Agent

# Запуск браузера Firefox
driver = webdriver.Firefox(options=options)
url = 'https://www.divan.ru/category/pramye-divany'

try:
    driver.get(url)

    # Ожидание загрузки элементов с ценами
    prices = WebDriverWait(driver, 120).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='ui-LD-ZU KIkOH' or @data-testid='price']"))
    )

    if not prices:
        raise ValueError("Не удалось найти элементы с ценами на странице.")

    # Открытие CSV файла для записи
    with open('divan_prices.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Price'])

        # Запись цены в CSV файл
        for price in prices:
            writer.writerow([price.text.strip()])  # Записываем цену в CSV

    print("Цены успешно записаны в файл 'divan_prices.csv'.")



    def clean_price(price):
        # Удаление "руб." и преобразование в число
        return int(price.replace('руб.', '').replace(' ', ''))


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
            clean_row = [clean_price(row[0])]
            writer.writerow(clean_row)

    print(f"Обработанные данные сохранены в файл {output_file}")


except Exception as e:
    print(f"Ошибка: {e}")
finally:
    driver.quit()
