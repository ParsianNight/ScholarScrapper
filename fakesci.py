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
def scrape_google_scholar_authors(driver, num_pages, categoryName):
    all_author_ids = []

    try:
        # Open the Google Scholar Author Search page
        driver.get('https://scholar.google.com/citations?view_op=search_authors')

        # Search for the category (e.g., "computer science" or "physics")
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
                href = author.get_attribute('href')  # Get the href from the <a> tag
                if 'user=' in href:
                    user_id = href.split('user=')[1].split('&')[0]
                    print(user_id)
                    all_author_ids.append(user_id)

            # Try to click on the 'Next' button for pagination
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.gs_btnPL.gsc_pgn_pnx'))
                )
                next_button.click()  # Click the 'Next' button
            except Exception as e:
                print(f"No more pages or error navigating to next page: {e}")
                break
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    return all_author_ids


# Function to browse the user's profile and extract all paper data using the same WebDriver session
def browse_profile(driver, user_id):
    all_results = []
    base_url = f'https://scholar.google.com/citations?hl=en&user={user_id}&cstart={{}}&pagesize=100'

    # Initial URL to load the profile
    url = base_url.format(0)
    driver.get(url)

    # Wait for the profile page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div#gsc_bdy'))
    )

    last_page_html = None  # Placeholder for the last page

    while True:
        # Get the current page's HTML content
        page_html = driver.page_source

        # Store the current page HTML as the last one (will keep replacing until the end)
        last_page_html = page_html

        # Introduce a random delay to avoid being blocked
        time.sleep(random.uniform(2, 5))

        # Try to find and click the "Show more" button to load additional papers
        try:
            # Wait for the "Show more" button to be clickable
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'gsc_bpf_more'))
            )

            # If the button is disabled, we've reached the last page
            if show_more_button.get_attribute('disabled'):
                print(f"Reached the last page for user {user_id}")
                break

            # Click the "Show more" button to load more papers
            show_more_button.click()
            
            # Introduce a delay after clicking
            time.sleep(random.uniform(2, 5))

        except Exception as e:
            print(f"No more papers to load or error for user {user_id}: {e}")
            break

    return last_page_html


# Example usage
driver = create_driver()  # Create a WebDriver session

# Scrape author IDs
num_pages = 1  # Number of pages you want to scrape
author_ids = scrape_google_scholar_authors(driver, num_pages, 'nanotoxicology')

# Browse each author's profile and extract papers
for author_id in author_ids:
    print(f"Processing author: {author_id}")
    last_page_html = browse_profile(driver, author_id)

    # Save only the last page's HTML content to a file
    with open(f'user_{author_id}_last_page.html', 'w', encoding='utf-8') as file:
        file.write(last_page_html)
    print(f"Saved last page for user {author_id}")


# Close the WebDriver after finishing
driver.quit()
print('kokos')
# Convert to DataFrame
df = pd.DataFrame(author_ids, columns=['Author_ID'])

print(df)

# Save to CSV
df.to_csv('scholar_author_ids.csv', index=False)
