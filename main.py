from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

ACCOUNT_EMAIL = os.environ.get("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.environ.get("ACCOUNT_PASSWORD")

s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=s)

driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3335362171&f_AL=true&keywords=python%20developer&refresh=true"
)
driver.find_element(By.LINK_TEXT, 'Sign in').click()
time.sleep(1)

driver.find_element(By.NAME, 'session_key').send_keys(ACCOUNT_EMAIL)
driver.find_element(By.NAME, 'session_password').send_keys(ACCOUNT_PASSWORD)
driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()
time.sleep(3)

jobs = driver.find_elements(By.CSS_SELECTOR, '.job-card-container--clickable')

for job in jobs:
    job.click()
    job_description = driver.find_element(By.ID, 'job-details').get_attribute('innerHTML')
    job_title = driver.find_element(By.CSS_SELECTOR, '.jobs-unified-top-card__job-title').get_attribute('innerHTML')
    print(job_title)
    if 'Applied' not in driver.find_element(By.CLASS_NAME, 'jobs-unified-top-card').get_attribute('innerHTML'):
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button').click()
        driver.find_element(By.CSS_SELECTOR, 'footer button').click()
        time.sleep(1)
        try:
            driver.find_element(By.LINK_TEXT, 'Submit application').click()
        except NoSuchElementException:
            try:
                driver.find_element(By.CSS_SELECTOR, 'footer button [aria-label="Review your application"]').click()
            except NoSuchElementException:
                print('Complicated application\n')
                driver.find_element(By.CSS_SELECTOR, '.artdeco-modal__dismiss').click()
                driver.find_element(By.CSS_SELECTOR, '.artdeco-modal__confirm-dialog-btn').click()
            else:
                print('Application submitted\n')
                driver.find_element(By.LINK_TEXT, 'Submit application').click()
                driver.find_element(By.CSS_SELECTOR, '.artdeco-modal__dismiss').click()
                continue
        else:
            print('Application submitted\n')
            driver.find_element(By.LINK_TEXT, 'Done').click()
            continue
    else:
        print('Applied\n')

driver.quit()
