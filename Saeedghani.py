from DrissionPage import ChromiumPage
import csv, time, os


class SaeedGhaniScrapper:
    def __init__(self):
        self.output_file = 'saeedghani_data.csv'

    def open_browser(self):
        driver = ChromiumPage()
        return driver
    
    def get_boxes(self, driver):
        boxes = driver.eles('xpath://div[@class="product-collection products-grid row"]//div[contains(@class,"grid-item")]',timeout=10)
        return boxes
    
    def extract_data(self, boxes):
        for box in boxes:
            product_url_tag = box.ele('xpath:.//a[@class="product-title cstm-url"]',timeout=0)
            product_url = product_url_tag.attr('href') if product_url_tag else ''
            product_img_tag = box.ele("xpath:.//div[contains(@class, 'product-image')]/a/img",timeout=0)
            product_img_check = product_img_tag.attr('src') if product_img_tag else ''
            product_img = product_img_check if product_img_check else 'https:' + product_img_tag.attr('data-src')
            product_title = product_img_tag.attr('alt') if product_img_tag else ''
            price_box_tag = box.ele('xpath:.//div[@class="price-box"]',timeout=0)
            price_box_text = price_box_tag.text.replace('from','').strip() if price_box_tag else '' 
            all_prices = [tag for tag in price_box_text.split('Rs.') if tag]
            new_price_tag = ''
            old_price_tag = ''
            dicount_price = ''
            dicount_percentage = ''
            if len(all_prices) > 1:
                old_price_tag = all_prices[0].replace(',','')
                new_price_tag = all_prices[1].replace(',','')
                dicount_price = f'Rs. {int(old_price_tag) - int(new_price_tag)}'
                subtraction = int(old_price_tag) - int(new_price_tag) 
                division = subtraction / int(old_price_tag)
                dicount_percentage = f'-{str(division * 100).split('.')[0]}%'
            else:
                new_price_tag = all_prices[0]

            old_price = f'Rs. {old_price_tag}' if old_price_tag else ''
            new_price = f'Rs. {new_price_tag}' if new_price_tag else ''
            row = [product_title,product_url,product_img,old_price,new_price,dicount_price,dicount_percentage]
            print(row)
            self.save_to_csv(row)

    
    def csv_header(self):
        header = ['Product Title','Product URL','Product Image','Old Price','New Price','Discount Price','Discount Percentage']
        with open(self.output_file, 'w', encoding='utf-8',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    
    def save_to_csv(self, data):
        with open(self.output_file, 'a', encoding='utf-8',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    
    def scrolling_page(self,driver):
        for x in range(4):
            driver.scroll.to_bottom()
            time.sleep(4)
    
    def run(self):
        if self.output_file not in os.listdir(): self.csv_header()
        driver = self.open_browser()
        web_url = 'https://saeedghani.pk/collections/skin-care'
        print(f'[INFO] Opening {web_url}')
        driver.get(web_url)
        time.sleep(3)
        self.scrolling_page(driver)
        boxes = self.get_boxes(driver)
        if not boxes:
            print('[ERROR] No product boxes found.')
            return
        self.extract_data(boxes)
        print(f'\n[INFO] - All Product Finished!\n')
        driver.close()
    
if __name__ == '__main__':
    scrapper = SaeedGhaniScrapper()
    scrapper.run()        
