from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import random

# Path to your WebDriver executable
DRIVER_PATH = '/opt/homebrew/bin/chromedriver'

# Function to create a WebDriver instance
def create_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to scrape author IDs
def scrape_google_scholar_authors(num_pages, categoryName):
    all_author_ids = []

    driver = create_driver()
    try:
        # Open the Google Scholar Author Search page
        driver.get('https://scholar.google.com/citations?view_op=search_authors')

        # Search for "computer science"
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'mauthors'))
        )
        search_box.send_keys(f"{categoryName}")
        search_box.submit()
        
        for page in range(num_pages):
            time.sleep(random.uniform(2, 12))  # Random wait time to avoid blocking

            # Extract author user IDs
            author_elements = driver.find_elements(By.CSS_SELECTOR, 'h3.gs_ai_name a')

            for author in author_elements:
                href = author.get_attribute('href')  # Now we get the href from the <a> tag
                if 'user=' in href:
                    user_id = href.split('user=')[1].split('&')[0]
                    print(user_id)
                    all_author_ids.append(user_id)

            # Try to click on the 'Next' button for pagination
            try:
                # Wait for the 'Next' button to be present and clickable
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.gs_btnPL.gsc_pgn_pnx'))
                )
                next_button.click()  # Click the 'Next' button
            except Exception as e:
                print(f"No more pages or error navigating to next page: {e}")
                break
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

    return all_author_ids

# Example usage
num_pages = 3  # Number of pages you want to scrape
author_ids = scrape_google_scholar_authors(num_pages,'physics')

# Convert to DataFrame
df = pd.DataFrame(author_ids, columns=['Author_ID'])
print(df)

# Save to CSV
df.to_csv('scholar_author_ids.csv', index=False)
