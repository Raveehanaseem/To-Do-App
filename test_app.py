import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_URL = os.environ.get('APP_URL', 'http://todo-app-container:5000')

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

# ─── Test Case 1: Page loads and title is correct ────────────────────────────
def test_page_loads():
    print(f"Running Test 1: Page Load Test on {APP_URL}...")
    driver = get_driver()
    try:
        driver.get(APP_URL)
        assert "To-Do" in driver.title, f"Expected 'To-Do' in title, got: {driver.title}"
        print("✅ Test 1 PASSED: Page loaded successfully.")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        raise
    finally:
        driver.quit()

# ─── Test Case 2: Add a new task ─────────────────────────────────────────────
def test_add_task():
    print("Running Test 2: Add Task Test...")
    driver = get_driver()
    try:
        driver.get(APP_URL)
        wait = WebDriverWait(driver, 10)
        # Check if IDs match your app's HTML
        input_box = wait.until(EC.presence_of_element_located((By.ID, "content"))) 
        input_box.send_keys("Test Task from Selenium")
        
        # 'submit' button check karein
        add_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        add_btn.click()
        
        time.sleep(2)
        page_source = driver.page_source
        assert "Test Task from Selenium" in page_source, "Task not found in page!"
        print("✅ Test 2 PASSED: Task added successfully.")
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Waiting for app to be ready...")
    time.sleep(5)  
    try:
        test_page_loads()
        test_add_task()
        print("\n🎉 All tests passed!")
    except Exception:
        exit(1)