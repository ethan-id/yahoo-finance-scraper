from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import csv

# if there are no CLI parameters
if len(sys.argv) <= 1:
    print('Ticker symbol CLI argument missing!')
    sys.exit(2)

# read the ticker from the CLI argument
ticker_symbol = sys.argv[1]
           
# initialize the dictionary
def scrape_stock(driver, ticker_symbol):
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}'
    driver.get(url)
    stock = {'ticker': ticker_symbol}

    # scraping logic...
    stock['regular_market_price'] = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPrice"]').text
    stock['regular_market_change'] = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketChange"]').text
    stock['regular_market_change_percent'] = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketChangePercent"]').text.replace('(', '').replace(')', '')
    
    stock['post_market_price'] = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="postMarketPrice"]').text
    stock['post_market_change'] = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="postMarketChange"]').text
    stock['post_market_change_percent'] = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="postMarketChangePercent"]').text.replace('(', '').replace(')', '')

    stock['previous_close'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="PREV_CLOSE-value"]').text
    stock['open_value'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="OPEN-value"]').text
    stock['bid'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="BID-value"]').text
    stock['ask'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="ASK-value"]').text
    stock['days_range'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="DAYS_RANGE-value"]').text
    stock['week_range'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="FIFTY_TWO_WK_RANGE-value"]').text
    stock['volume'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="TD_VOLUME-value"]').text
    stock['avg_volume'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="AVERAGE_VOLUME_3MONTH-value"]').text
    stock['market_cap'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="MARKET_CAP-value"]').text
    stock['beta'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="BETA_5Y-value"]').text
    stock['pe_ratio'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="PE_RATIO-value"]').text
    stock['eps'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="EPS_RATIO-value"]').text
    stock['earnings_date'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="EARNINGS_DATE-value"]').text
    stock['dividend_yield'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="DIVIDEND_AND_YIELD-value"]').text
    stock['ex_dividend_date'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="EX_DIVIDEND_DATE-value"]').text
    stock['year_target_est'] = driver.find_element(By.CSS_SELECTOR, '#quote-summary [data-test="ONE_YEAR_TARGET_PRICE-value"]').text

    return stock

# initialize a Chrome instance with the right
# configs
options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
driver.set_window_size(1150, 1000)

# the array containing all scraped data
stocks = []

# scraping all market securities
for ticker_symbol in sys.argv[1:]:
    stocks.append(scrape_stock(driver, ticker_symbol))

# close the browser and free up the resources
driver.quit()

# extract the name of the dictionary fields
# to use it as the header of the output CSV file
csv_header = stocks[0].keys()

# export the scraped data to CSV
with open('stocks.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, csv_header)
    dict_writer.writeheader()
    dict_writer.writerows(stocks)