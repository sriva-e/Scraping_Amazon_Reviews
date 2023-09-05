# Amazon Web Scraping Project

## Overview

This project consists of Python scripts for web scraping Amazon product reviews and collecting product ASINs from search results. The objective of this project is to extract valuable information from Amazon's website for various purposes, such as market research or data analysis.

## Prerequisites
Before running the scripts, make sure you have Python and the required libraries installed. You can install the necessary libraries using the following command:

```bash
pip install -r requirements.txt
```


## Usage

### Web Scraping Amazon Product Reviews

1. Open the `amazon_review_scraper.py` script.

2. Customize the list of proxies, the target Amazon product URL, and other parameters as needed. For example:

```python
proxies = [
    'us-ca.proxymesh.com:31280',
    # Add more proxies as needed
]
```
url = 'https://www.amazon.com/s?k=camera&ref=nb_sb_noss'

3. Run the script to scrape product reviews and save the data in an Excel file.

## Scraping Amazon Product ASINs
1. Open the amazon_asin_scraper.py script.
2. Customize the search URL and other parameters as needed.
3. Run the script to scrape ASINs from Amazon search results and save them in an Excel file
## File Descriptions
1. amazon_review_scraper.py: Python script for scraping Amazon product reviews.
2. amazon_asin_scraper.py: Python script for scraping Amazon product ASINs from search results.
3. requirements.txt: A list of required Python libraries and their versions.
## Contributing
If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request. Your contributions are welcome.
