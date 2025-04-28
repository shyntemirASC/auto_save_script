from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import os
import time
import pandas as pd
from config import EMAIL, PASSWORD
from datetime import datetime

def collect_numbers():
    # Подключение драйвера
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 15)

    driver.get("https://app.jaicp.kz/login")

    # Вход в аккаунт
    time.sleep(2)
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)


    time.sleep(5)
    driver.get("https://app.jaicp.kz/inara_transkaz_prepr-1000013-yGI/statistic/dialogs")
    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ReactSelectPrefix__control")))

    # Скроллим к элементу, чтобы он был виден
    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    time.sleep(0.5)  # Немного подождать после скролла
    dropdown.click()

    input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ReactSelectPrefix__input input")))
    input_field.send_keys("100")
    input_field.send_keys(Keys.ENTER)

    time.sleep(5)  

    all_numbers = set()  # Используем множество для хранения уникальных номеров
    attempts = 0
    max_attempts = 3  # Максимальное количество попыток сбора номеров

    # Тут мы берем 100 последних уникальных номеров, если нужно то можно поменять значения
    clients = 100
    while len(all_numbers) < clients and attempts < max_attempts:
        rows = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "td[data-test-id='dialogUserID'] span:first-child")
        ))
            
        # Добавляем только уникальные номера
        new_numbers = {row.text.strip() for row in rows if row.text.strip()}
        all_numbers.update(new_numbers)
            
        # Если номеров все еще недостаточно, переходим на следующую страницу
        if len(all_numbers) < clients:
            next_page_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.AnalyticActionPanel_next-link")))
            driver.execute_script("arguments[0].click();", next_page_btn) 
            time.sleep(3)  
            attempts += 1

    client_ids = list(all_numbers)[:clients]

    # Создаем папку и файл
    os.makedirs("excel", exist_ok=True)
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"excel/numbers_{current_date}.xlsx"
    
    df = pd.DataFrame({
        "client_id": client_ids,
        "GMT_ZONE": ["+05:00"] * len(client_ids)
        })

    df.to_excel(file_name, index=False)

    print("Успешно сохранено!")

    # Переходим к добавлению нашего списка в список клиентов
    driver.get("https://app.jaicp.kz/calllists")
    time.sleep(3)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Создать список клиентов')]")))
    button.click()
    time.sleep(2)

    # Находим и загружаем созданный файл
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_path = os.path.abspath(file_name)
    file_input.send_keys(file_path)
    print(f"Загружаем файл {file_name}...")
    time.sleep(5)

    # Добавление нового списка клиентов
    list_name = f"Список от {current_date}"
    name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='listName']")))
    name_input.clear()
    name_input.send_keys(list_name)
    time.sleep(2)

    # Подтверждение
    checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.custom-control-label[for='isAgreed']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    time.sleep(1)
    checkbox.click()

    # Нажатие кнопки Создать
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='MailingList.CreateModal.Submit']")))
    time.sleep(1)
    driver.execute_script("arguments[0].click();", save_btn)

    print("Список успешно загружен!")


if __name__ == "__main__":
    excel = "excel/"
    os.makedirs(excel, exist_ok=True)
    collect_numbers()
