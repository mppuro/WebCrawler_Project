import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# WebCrawler class which is responsible for handling all the scraping
class WebCrawler:
    #Constructor definition which initializes all the data.
    def __init__(self, target_url, depth, limit):
        self.start_url = target_url
        self.depth = depth
        self.visited_urls = set()
        self.limit = limit
        self.data = []

    # To check whether or not - we have reached the limit of scraping the records
    def check_limit_reached(self):
        return len(self.data) >= self.limit

    # This method will crawl through all the pages of a website.
    def crawl(self, url, current_depth):
        if current_depth > self.depth or url in self.visited_urls or self.check_limit_reached():
            return

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/91.0.4472.124 Safari/537.36 "
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.visited_urls.add(url)
                self.parse_content(response.text, url)
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    next_url = link['href']
                    if next_url and not next_url.startswith('#'):
                        next_url = urljoin(self.start_url, next_url)
                        self.crawl(next_url, current_depth + 1)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    # Responsible for scraping the content from the website. 
    def parse_content(self, html_content, url):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_containers = soup.find_all('a', {'class': 'plp-card-wrapper'})
    
        if product_containers:
            for container in product_containers:
                product_url = "https://www.jiomart.com" + container.get("href") or ""
                
                # Check if the product name element is found
                product_name_element = container.find('div', {'class': 'plp-card-details-name'})
                product_name = product_name_element.get_text(strip=True) if product_name_element else ""

                # Check if the product price element is found
                product_price_element = container.find('div', {'class': 'plp-card-details-price'})
                product_price = product_price_element.find('span', {'class': 'jm-heading-xxs'}).get_text(strip=True) if product_price_element else ""

                # Check if the product image element is found
                product_image_element = container.find('div', {'class': 'plp-card-image'})
                product_image = product_image_element.find('img').get('src') if product_image_element else ""

                product_page_response = requests.get(product_url).text
                product_soup = BeautifulSoup(product_page_response, 'html.parser')

                # Check if the product description element is found
                product_description_element = product_soup.find('div', {'id': 'pdp_description'})
                product_description = product_description_element.find('div').get_text(strip=True) if product_description_element else ""

                self.limit -= 1

                product_data = {
                    'url': product_url,
                    'name': product_name,
                    'price': product_price,
                    'image': product_image,
                    'description': product_description,
                }
                print("Scraped", product_name)
                self.data.append(product_data)
        else:
            print("Page has been ignored, since it did not contain any product in it - ", url)


    # Once the JSON dump is ready, we are saving this as JSON file.
    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(self.data, file, indent=2)
        except Exception as e:
            print(f"Error saving data to file {filename}: {str(e)}")


if __name__ == "__main__":
    start_url = "https://www.jiomart.com/"
    crawler = WebCrawler(start_url, 3, 50)
    crawler.crawl(start_url, current_depth=1)
    crawler.save_to_file('product_data.json')
