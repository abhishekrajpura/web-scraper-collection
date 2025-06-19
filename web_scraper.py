#!/usr/bin/env python3
"""
Multi-Site Web Scraper
A comprehensive web scraping tool that demonstrates scraping different types of websites.
Includes rate limiting, error handling, and data export functionality.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import List, Dict, Any
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScrapedData:
    """Data class to store scraped information"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    timestamp: str

class WebScraper:
    def __init__(self, delay_range=(1, 3)):
        """
        Initialize the web scraper with rate limiting
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay_range = delay_range
        self.scraped_data = []
    
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
    
    def _get_page(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse a web page
        
        Args:
            url: URL to scrape
            
        Returns:
            BeautifulSoup object of the parsed page
        """
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def scrape_news_site(self, url: str = "https://httpbin.org/html") -> Dict[str, Any]:
        """
        Scrape a news-style website (using httpbin.org for demo)
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary containing scraped data
        """
        logger.info(f"Scraping news site: {url}")
        soup = self._get_page(url)
        
        if not soup:
            return {}
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title found"
        
        # Extract headings
        headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
        
        # Extract paragraphs
        paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            links.append({
                'text': link.get_text().strip(),
                'url': full_url
            })
        
        return {
            'url': url,
            'title': title_text,
            'headings': headings,
            'paragraphs': paragraphs,
            'links': links[:10],  # Limit to first 10 links
            'type': 'news_site'
        }
    
    def scrape_quotes_site(self, url: str = "http://quotes.toscrape.com/") -> Dict[str, Any]:
        """
        Scrape quotes from quotes.toscrape.com
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary containing quotes data
        """
        logger.info(f"Scraping quotes site: {url}")
        soup = self._get_page(url)
        
        if not soup:
            return {}
        
        quotes = []
        for quote_div in soup.find_all('div', class_='quote'):
            quote_text = quote_div.find('span', class_='text')
            author = quote_div.find('small', class_='author')
            tags = quote_div.find_all('a', class_='tag')
            
            if quote_text and author:
                quotes.append({
                    'text': quote_text.get_text().strip(),
                    'author': author.get_text().strip(),
                    'tags': [tag.get_text().strip() for tag in tags]
                })
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Quotes to Scrape"
        
        return {
            'url': url,
            'title': title_text,
            'quotes': quotes,
            'total_quotes': len(quotes),
            'type': 'quotes_site'
        }
    
    def scrape_books_site(self, url: str = "http://books.toscrape.com/") -> Dict[str, Any]:
        """
        Scrape books from books.toscrape.com
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary containing books data
        """
        logger.info(f"Scraping books site: {url}")
        soup = self._get_page(url)
        
        if not soup:
            return {}
        
        books = []
        for book_article in soup.find_all('article', class_='product_pod'):
            title_elem = book_article.find('h3').find('a') if book_article.find('h3') else None
            price_elem = book_article.find('p', class_='price_color')
            rating_elem = book_article.find('p', class_='star-rating')
            availability_elem = book_article.find('p', class_='instock availability')
            
            if title_elem and price_elem:
                # Extract rating from class name
                rating = 'Unknown'
                if rating_elem:
                    rating_classes = rating_elem.get('class', [])
                    for cls in rating_classes:
                        if cls in ['One', 'Two', 'Three', 'Four', 'Five']:
                            rating = cls
                            break
                
                books.append({
                    'title': title_elem.get('title', '').strip(),
                    'price': price_elem.get_text().strip(),
                    'rating': rating,
                    'availability': availability_elem.get_text().strip() if availability_elem else 'Unknown'
                })
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "Books to Scrape"
        
        return {
            'url': url,
            'title': title_text,
            'books': books,
            'total_books': len(books),
            'type': 'books_site'
        }
    
    def scrape_json_api(self, url: str = "https://jsonplaceholder.typicode.com/posts") -> Dict[str, Any]:
        """
        Scrape JSON API data
        
        Args:
            url: API endpoint URL
            
        Returns:
            Dictionary containing API data
        """
        logger.info(f"Scraping JSON API: {url}")
        
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Limit to first 10 posts for demo
            if isinstance(data, list):
                data = data[:10]
            
            return {
                'url': url,
                'title': 'JSON API Data',
                'api_data': data,
                'total_items': len(data) if isinstance(data, list) else 1,
                'type': 'json_api'
            }
        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.error(f"Error fetching JSON API {url}: {e}")
            return {}
    
    def run_all_scrapers(self) -> List[Dict[str, Any]]:
        """
        Run all scrapers and collect data
        
        Returns:
            List of all scraped data
        """
        scrapers = [
            self.scrape_news_site,
            self.scrape_quotes_site,
            self.scrape_books_site,
            self.scrape_json_api
        ]
        
        all_data = []
        for scraper in scrapers:
            try:
                data = scraper()
                if data:
                    all_data.append(data)
                    logger.info(f"Successfully scraped {data.get('type', 'unknown')} from {data.get('url', 'unknown')}")
            except Exception as e:
                logger.error(f"Error running scraper {scraper.__name__}: {e}")
        
        self.scraped_data = all_data
        return all_data
    
    def save_to_json(self, filename: str = "scraped_data.json"):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {filename}")
    
    def save_to_csv(self, filename: str = "scraped_summary.csv"):
        """Save a summary of scraped data to CSV file"""
        if not self.scraped_data:
            logger.warning("No data to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Title', 'Type', 'Items Count'])
            
            for data in self.scraped_data:
                items_count = 0
                if 'quotes' in data:
                    items_count = data.get('total_quotes', 0)
                elif 'books' in data:
                    items_count = data.get('total_books', 0)
                elif 'api_data' in data:
                    items_count = data.get('total_items', 0)
                elif 'paragraphs' in data:
                    items_count = len(data.get('paragraphs', []))
                
                writer.writerow([
                    data.get('url', ''),
                    data.get('title', ''),
                    data.get('type', ''),
                    items_count
                ])
        
        logger.info(f"Summary saved to {filename}")

def main():
    """Main function to run the web scraper"""
    logger.info("Starting web scraping session...")
    
    scraper = WebScraper(delay_range=(1, 2))
    
    # Run all scrapers
    data = scraper.run_all_scrapers()
    
    if data:
        # Save results
        scraper.save_to_json()
        scraper.save_to_csv()
        
        logger.info(f"Scraping completed! Collected data from {len(data)} sites")
        
        # Print summary
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        for item in data:
            print(f"Site: {item.get('title', 'Unknown')}")
            print(f"URL: {item.get('url', 'Unknown')}")
            print(f"Type: {item.get('type', 'Unknown')}")
            if 'quotes' in item:
                print(f"Quotes found: {item.get('total_quotes', 0)}")
            elif 'books' in item:
                print(f"Books found: {item.get('total_books', 0)}")
            elif 'api_data' in item:
                print(f"API items: {item.get('total_items', 0)}")
            elif 'paragraphs' in item:
                print(f"Paragraphs found: {len(item.get('paragraphs', []))}")
            print("-" * 30)
    else:
        logger.warning("No data was scraped successfully")

if __name__ == "__main__":
    main()
