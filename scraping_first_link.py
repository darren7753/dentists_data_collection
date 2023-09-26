import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

data_folder = "Data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Set up the driver
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1920x1080")

driver = webdriver.Chrome(options=options)

url = "https://yankes.kemkes.go.id/praktekmandiri/cari/index/?propinsi=&kabkota=&kategori=5&nama=Gigi"
driver.get(url)

# Create an empty dataframe
df = pd.DataFrame(columns=['Name', 'Address', 'Phone Number'])

# Function to scrape data from the opened detail tab
def scrape_data():
    name = driver.find_element(By.CSS_SELECTOR, 'h4.mb-0').text
    address_elements = driver.find_elements(By.XPATH, '//font[@class="text-info"]')
    address = address_elements[1].text
    phone = address_elements[2].text
    
    return {
        'Name': name,
        'Address': address,
        'Phone Number': phone
    }

page = 1
while True:
    print(f"Page {page}")

    # Get the number of "Lihat" links on the page
    lihat_links_count = len(driver.find_elements(By.XPATH, '//a[contains(text(), "Lihat")]'))

    # Iterate using the count
    for i in range(lihat_links_count):
        # Get a fresh set of "Lihat" links on the current page
        lihat_link = driver.find_elements(By.XPATH, '//a[contains(text(), "Lihat")]')[i]
        lihat_link.click()
        time.sleep(2)  # Wait for the detailed page to load
        
        data = scrape_data()
        print(data)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        
        # Return to the main page
        driver.back()
        time.sleep(2)
        
    # Check if the 'Next' button is available
    try:
        next_button = driver.find_element(By.XPATH, '//a[text()="Next"]')
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    except NoSuchElementException:
        # If 'Next' button is not found, exit the loop
        break

    page += 1

    if page > 1:
        break

driver.quit()

df.to_excel("Data/data_first_link.xlsx", index=False)