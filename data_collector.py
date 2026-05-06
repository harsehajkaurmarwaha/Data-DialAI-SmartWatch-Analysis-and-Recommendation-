import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import random

class ProductDataCollector:
    def __init__(self):
        self.products = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_amazon_watches(self):
        # watch data from amazon
        base_urls = [
            "https://www.amazon.in/s?k=watches&i=watches&ref=nb_sb_noss",
            "https://www.amazon.in/s?k=smart+watches&i=watches&ref=nb_sb_noss",
            "https://www.amazon.in/s?k=luxury+watches&i=watches&ref=nb_sb_noss",
            "https://www.amazon.in/b?node=207171479031&ref_=AF_WIN_bub_w_cml_t_1&pf_rd_r=Q1NBEMWMAV4ARAY4FTTV&pf_rd_p=95c202ee-0e23-4ae7-b9c1-bde187ea867c&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-2&pf_rd_t=&pf_rd_i=1350387031","https://www.amazon.in/s?k=premium+watches&i=watches&crid=7GBNPE8H3ZMX&sprefix=premiumwatches%2Cwatches%2C203&ref=nb_sb_noss_2",
            "https://www.amazon.in/s?k=apple+watches"
        ]
        
        for url in base_urls:
            try:
                print(f"Scraping: {url}")
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                products = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for product in products:
                    try:
                        # Extract product name
                        name_elem = product.find('h2')
                        product_name = name_elem.text.strip() if name_elem else "Unknown Product"
                        
                        # Extract price
                        price_elem = product.find('span', {'class': 'a-price-whole'})
                        price = int(price_elem.text.replace(',', '').strip()) if price_elem else 0
                        
                        # Extract rating
                        rating_elem = product.find('span', {'class': 'a-icon-alt'})
                        rating_text = rating_elem.text if rating_elem else "0 out of 5 stars"
                        rating = float(rating_text.split(' ')[0]) if rating_elem else 0.0
                        
                        # Extract reviews count
                        reviews_elem = product.find('span', {'class': 'a-size-base'})
                        reviews_text = reviews_elem.text if reviews_elem else "0"
                        reviews = int(reviews_text.replace(',', '')) if reviews_elem else 0
                        
                        # category based on product name
                        category = self.categorize_watch(product_name)
                        
                        # brand from product name
                        brand = self.extract_brand(product_name)
                        
                        if product_name != "Unknown Product" and price > 0:
                            self.products.append({
                                'product_id': len(self.products) + 1,
                                'product_name': product_name,
                                'brand': brand,
                                'category': category,
                                'price': price,
                                'rating': rating,
                                'reviews': reviews
                            })
                            
                    except Exception as e:
                        print(f"Error parsing product: {e}")
                        continue
                
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"Error scraping URL {url}: {e}")
                continue
    
    def categorize_watch(self, product_name):
        # watch category based on keywords
        name_lower = product_name.lower()
        
        if any(word in name_lower for word in ['smart', 'fitness', 'tracker', 'activity']):
            return 'Smartwatch'
        elif any(word in name_lower for word in ['luxury', 'premium', 'gold', 'diamond']):
            return 'Luxury'
        elif any(word in name_lower for word in ['sport', 'fitness', 'running', 'gym']):
            return 'Sports'
        elif any(word in name_lower for word in ['digital', 'led', 'display']):
            return 'Digital'
        elif any(word in name_lower for word in ['fashion', 'style', 'designer']):
            return 'Fashion'
        else:
            return 'Analog'
    
    def extract_brand(self, product_name):
        # brand name from product name
        common_brands = ['Titan', 'Casio', 'Fastrack', 'Sonata', 'Fossil', 'Samsung', 
                        'Apple', 'Noise', 'Boat', 'Fitbit', 'Garmin', 'Timex', 'HMT']
        
        for brand in common_brands:
            if brand.lower() in product_name.lower():
                return brand
        return 'Other'
    
    def generate_fallback_data(self):
        # if scraping fails , sample data
        print("Generating fallback sample data...")
        
        categories = {
            'Smartwatch': {
                'brands': ['Apple', 'Samsung', 'Noise', 'Boat', 'Fitbit', 'Garmin'],
                'products': ['Smart Watch', 'Fitness Tracker', 'Health Monitor', 'GPS Watch']
            },
            'Luxury': {
                'brands': ['Titan', 'Fastrack', 'Fossil', 'Casio', 'Timex'],
                'products': ['Chronograph', 'Automatic', 'Quartz', 'Dress Watch']
            },
            'Sports': {
                'brands': ['Casio', 'Fastrack', 'Titan', 'Timex', 'G-Shock'],
                'products': ['Sports Watch', 'Digital Watch', 'Fitness Tracker']
            },
            'Fashion': {
                'brands': ['Sonata', 'Maxima', 'Esprit', 'Swiss Military'],
                'products': ['Fashion Watch', 'Designer Watch', 'Trendy Edition']
            },
            'Digital': {
                'brands': ['Casio', 'Timex', 'Fastrack', 'Sonata'],
                'products': ['Digital Watch', 'LED Display', 'Calculator Watch']
            },
            'Analog': {
                'brands': ['Titan', 'HMT', 'Timex', 'Casio'],
                'products': ['Analog Watch', 'Classic Dial', 'Vintage Series']
            }
        }
        
        for i in range(200):
            category = random.choice(list(categories.keys()))
            brand = random.choice(categories[category]['brands'])
            product_type = random.choice(categories[category]['products'])
            
            product_name = f"{brand} {product_type} {random.randint(1, 999)}"
            
            base_prices = {
                'Smartwatch': (1500, 45000),
                'Luxury': (2000, 35000),
                'Sports': (800, 15000),
                'Fashion': (1000, 12000),
                'Digital': (500, 8000),
                'Analog': (1200, 25000)
            }
            
            min_price, max_price = base_prices[category]
            price = random.randint(min_price, max_price)
            rating = round(random.uniform(3.8, 4.8), 1)
            reviews = random.randint(50, 10000)
            
            self.products.append({
                'product_id': i + 1,
                'product_name': product_name,
                'brand': brand,
                'category': category,
                'price': price,
                'rating': rating,
                'reviews': reviews
            })
    
    def save_data(self):
        df = pd.DataFrame(self.products)

        df.to_csv('products.csv', index=False)

        conn = sqlite3.connect('products.db')
        df.to_sql('products', conn, if_exists='replace', index=False)
        conn.close()
        
        print("-> Product data collected successfully!")
        print(f"-> Total products: {len(self.products)}")
        print(f"-> Data saved to: products.csv & products.db")

def main():
    collector = ProductDataCollector()
    
    print("🕒 Starting web scraping from Amazon...")
    collector.scrape_amazon_watches()
    
    # If no data was scraped
    if len(collector.products) < 50:
        print("⚠️  Not enough data scraped, using sample data...")
        collector.generate_fallback_data()
    
    collector.save_data()
    
    # Display sample data
    df = pd.read_csv('products.csv')
    print("\n✅ Sample of collected data:")
    print(df.head(8))

if __name__ == "__main__":
    main()