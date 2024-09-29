
# Google Scholar Author Scraper

This repository contains a Python script that scrapes author profiles from Google Scholar using Selenium WebDriver. It extracts author IDs based on a given research category, navigates through author profiles, and saves the last page of the author's publication list in HTML format.

## Project Collaborators
- **Omar Abdelrazik**  
- **Mohamed Khalid**

## Prerequisites

Before running the script, ensure that you have the following installed on your machine:

1. **Python 3.6+**  
2. **Selenium**  
   Install Selenium via pip:
   ```bash
   pip install selenium
   ```
3. **ChromeDriver**  
   Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), and ensure it's available in your system's PATH or update the `DRIVER_PATH` in the script accordingly.

4. **pandas**  
   Install pandas for saving scraped data to CSV:
   ```bash
   pip install pandas
   ```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Adjust the `DRIVER_PATH` in the script to point to the location of your ChromeDriver executable:
   ```python
   DRIVER_PATH = '/path/to/your/chromedriver'
   ```

## Usage

The script works in two phases:

1. **Scraping Author IDs**  
   The function `scrape_google_scholar_authors` scrapes author IDs from Google Scholar based on a specified research category (e.g., "nanotoxicology") and number of pages.

2. **Scraping Author Publications**  
   For each author ID, the function `browse_profile` extracts and saves the last page of their publication list to a file in HTML format.

To run the script, simply execute the following command:

```bash
python scholar_scraper.py
```

### Example:

In the script:
```python
num_pages = 1  # Number of pages to scrape for authors
author_ids = scrape_google_scholar_authors(driver, num_pages, 'nanotoxicology')

for author_id in author_ids:
    last_page_html = browse_profile(driver, author_id)
    with open(f'user_{author_id}_last_page.html', 'w', encoding='utf-8') as file:
        file.write(last_page_html)
```

### Output:

- A CSV file named `scholar_author_ids.csv` will contain all scraped author IDs.
- HTML files will be generated, named `user_<author_id>_last_page.html`, containing the last page of publications for each author.

## Notes

- The script introduces random delays to avoid being blocked by Google Scholar.
- The "Show more" button is used to navigate through the author’s list of publications until all papers are loaded.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

