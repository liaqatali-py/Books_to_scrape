from DrissionPage import ChromiumPage
from time import sleep
import csv, os

class JoemachensnissanScraper:
    def __init__(self):
        self.output_file = 'Joemachensnissan.csv'

    def open_browser(self):
        return ChromiumPage()


    def get_boxes(self, driver):
        sleep(3)
        boxes = driver.eles('xpath://a[contains(@class,"vehicle-card-link") or contains(@href,"new-vehicles")]')
        all_urls = [box.attr('href') for box in boxes]
        return all_urls

    def get_all_boxes(self, driver):
        boxes = self.get_boxes(driver)
        for url in boxes:
            driver.get(url)
            sleep(2)

            title_tag = driver.ele('xpath://h1', timeout=0)
            title = title_tag.text.strip() if title_tag else ''
            price_tag = driver.ele('xpath=//span[contains(@class,"primary-price") or contains(text(),"$")]', timeout=2)
            price = price_tag.text.strip() if price_tag else ''
            stock_tag = driver.ele('xpath://div[contains(text(),"Stock") or contains(@class,"stock-number")]', timeout=0)
            stock = stock_tag.text.strip() if stock_tag else ''
            img_tag = driver.ele('xpath://img[contains(@src,".jpg") or contains(@src,"cdn")]', timeout=0)
            img = img_tag.attr('src') if img_tag else ''
            row = [title, price, stock, img]
            print('Saving Data:-', row)
            self.save_data(row)
    def save_data(self, row):
        with open(self.output_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def csv_header(self):
        self.csv_headers = ['Title', 'Price', 'Stock', 'Img']
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.csv_headers)

    def run(self):
        if self.output_file not in os.listdir():
            self.csv_header()

        driver = self.open_browser()
        web_url = 'https://www.joemachensnissan.com/new-vehicles/'
        sleep(3)

        while True:
            print(f'\n[INFO] - Getting Page URL:- {web_url}\n')
            driver.get(web_url)
            sleep(1)

            self.get_all_boxes(driver)

            next_btn = driver.ele('xpath://a[contains(@class,"next page-numbers")] | //a[@aria-label="Next Page"]')
            if next_btn and next_btn.attr('href'):
                 sleep(1)
            else:
                break
        driver.close()
        print("\n[INFO] - Data saved to Joemachensnissan.csv")

if __name__ == '__main__':
    scraper = JoemachensnissanScraper()
    scraper.run()
