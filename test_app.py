import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Docker network ke liye sahi URL
APP_URL = os.environ.get('APP_URL', 'http://todo-app-container:5000')

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def test_page_loads():
    print(f"Running Test 1: Page Load Test on {APP_URL}...")
    driver = get_driver()
    try:
        driver.get(APP_URL)
        # Title check (case insensitive)
        assert "todo" in driver.title.lower(), f"Title mismatch: {driver.title}"
        print("✅ Test 1 PASSED")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        raise
    finally:
        driver.quit()

def test_add_task():
    print("Running Test 2: Add Task Test...")
    driver = get_driver()
    try:
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 10)
        
        # 1. Input field dhoondo (ID content ya task-input dono try karega)
        input_field = None
        for selector in ["content", "task-input", "task_content"]:
            try:
                input_field = driver.find_element(By.ID, selector)
                break
            except:
                continue
        
        if not input_field:
            input_field = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))

        input_field.send_keys("Selenium Final Task")
        
        # 2. Add Button dhoondo
        try:
            add_btn = driver.find_element(By.ID, "add-btn")
        except:
            # Agar ID nahi mili toh 'submit' type wala button dhoondo
            add_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
            
        add_btn.click()
        time.sleep(2)
        
        # 3. Verification
        assert "Selenium Final Task" in driver.page_source
        print("✅ Test 2 PASSED")
        
    except Exception as e:
        print(f"❌ Test 2 FAILED: Element nahi mila. Error: {e}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    time.sleep(5)
    test_page_loads()
    test_add_task()