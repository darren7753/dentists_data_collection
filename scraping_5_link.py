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

url = "https://www.ikorti-iao.com/direktori"

driver = webdriver.Chrome(options=options)  # Add any required driver options here
driver.maximize_window()
driver.get(url)

# Create an empty dataframe
df = pd.DataFrame(columns=['Name', 'Address', 'Phone Number'])

# Function to scrape phone number from Google Maps    
def scrape_phone():
    # Identify all containers having class 'AeaXub'
    phone_containers = driver.find_elements(By.CSS_SELECTOR, ".AeaXub")
    
    for phone_container in phone_containers:
        try:
            # Check if the container has the phone icon based on the src attribute
            phone_icon = phone_container.find_element(By.XPATH, ".//img[contains(@src, 'system_gm/2x/phone_gm_blue_24dp.png')]")
            
            if phone_icon:
                # Fetch the phone number from within this container
                phone_elem = phone_container.find_element(By.CSS_SELECTOR, ".Io6YTe.fontBodyMedium.kR99db")
                return phone_elem.text
        except NoSuchElementException:
            continue

    return ""

page = 1
while True:
    print(f"Page {page}")

    rows = driver.find_elements(By.XPATH, "//tr[@role='row'][contains(@class, 'odd') or contains(@class, 'even')]")

    for row in rows:
        name = row.find_element(By.XPATH, "./td[2]").text
        address_links = row.find_elements(By.XPATH, "./td[4]/a")
        
        # Get all address lines
        address_list = [link.text for link in address_links]

        # Navigate to Google Maps to get the phone number for each address
        phone_numbers = []

        for link in address_links:
            # Save the main window handle before clicking the link
            main_window = driver.current_window_handle
            
            link.click()
            time.sleep(2)  # Wait for the new tab to open
            
            # Switch to the new tab
            driver.switch_to.window([window for window in driver.window_handles if window != main_window][0])
            
            phone_numbers.append(scrape_phone())
            
            # Close the new tab
            driver.close()
            
            # Switch back to the main window
            driver.switch_to.window(main_window)
            time.sleep(2)  # Wait to ensure you're back to the main page

        # Combine all addresses and phone numbers
        address = "\n".join(address_list).replace("\n", ", ")
        phone = ", ".join(filter(None, phone_numbers))  # Join non-empty phone numbers with comma
        
        data = {
            'Name': name,
            'Address': address,
            'Phone Number': phone
        }
        print(data)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Check if the 'Next' button is available
    try:
        next_button = driver.find_element(By.XPATH, "//a[@class='paginate_button next']")
        next_button.click()
        time.sleep(2)  # Wait for the next page to load

        # Scroll to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    except NoSuchElementException:
        # If 'Next' button is not found, exit the loop
        break

    page += 1

driver.quit()

df.to_excel("Data/data_5_link.xlsx", index=False)