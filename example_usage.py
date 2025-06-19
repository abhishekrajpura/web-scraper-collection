#!/usr/bin/env python3
"""
Example usage of the Web Scraper Collection
This script demonstrates different ways to use the web scraper.
"""

from web_scraper import WebScraper
import json

def example_basic_usage():
    """Example of basic usage - scrape all sites"""
    print("=== Basic Usage Example ===")
    
    # Initialize scraper
    scraper = WebScraper(delay_range=(1, 2))
    
    # Run all scrapers
    print("Running all scrapers...")
    data = scraper.run_all_scrapers()
    
    # Save results
    scraper.save_to_json("example_output.json")
    scraper.save_to_csv("example_summary.csv")
    
    print(f"Successfully scraped {len(data)} sites")
    return data

def example_individual_scrapers():
    """Example of using individual scrapers"""
    print("\n=== Individual Scrapers Example ===")
    
    scraper = WebScraper()
    
    # Scrape quotes site only
    print("Scraping quotes...")
    quotes_data = scraper.scrape_quotes_site()
    if quotes_data:
        print(f"Found {quotes_data.get('total_quotes', 0)} quotes")
        # Print first quote as example
        if quotes_data.get('quotes'):
            first_quote = quotes_data['quotes'][0]
            print(f"First quote: \"{first_quote['text']}\" - {first_quote['author']}")
    
    # Scrape books site only
    print("\nScraping books...")
    books_data = scraper.scrape_books_site()
    if books_data:
        print(f"Found {books_data.get('total_books', 0)} books")
        # Print first book as example
        if books_data.get('books'):
            first_book = books_data['books'][0]
            print(f"First book: \"{first_book['title']}\" - {first_book['price']}")

def example_custom_configuration():
    """Example of custom configuration"""
    print("\n=== Custom Configuration Example ===")
    
    # Create scraper with longer delays (more respectful)
    scraper = WebScraper(delay_range=(2, 4))
    
    # Scrape with custom URLs
    custom_data = []
    
    # Scrape different page of quotes site
    quotes_page2 = scraper.scrape_quotes_site("http://quotes.toscrape.com/page/2/")
    if quotes_page2:
        custom_data.append(quotes_page2)
        print(f"Page 2 quotes: {quotes_page2.get('total_quotes', 0)}")
    
    # Scrape different API endpoint
    api_data = scraper.scrape_json_api("https://jsonplaceholder.typicode.com/users")
    if api_data:
        custom_data.append(api_data)
        print(f"API users: {api_data.get('total_items', 0)}")
    
    return custom_data

def display_summary(data):
    """Display a nice summary of scraped data"""
    print("\n=== SCRAPING SUMMARY ===")
    print("-" * 40)
    
    for item in data:
        print(f"Site: {item.get('title', 'Unknown')}")
        print(f"URL: {item.get('url', 'Unknown')}")
        print(f"Type: {item.get('type', 'Unknown')}")
        
        if 'quotes' in item:
            print(f"Data: {item.get('total_quotes', 0)} quotes found")
        elif 'books' in item:
            print(f"Data: {item.get('total_books', 0)} books found")
        elif 'api_data' in item:
            print(f"Data: {item.get('total_items', 0)} API items found")
        elif 'paragraphs' in item:
            print(f"Data: {len(item.get('paragraphs', []))} paragraphs found")
        
        print("-" * 40)

def main():
    """Run all examples"""
    print("Web Scraper Collection - Example Usage")
    print("=" * 50)
    
    try:
        # Example 1: Basic usage
        basic_data = example_basic_usage()
        
        # Example 2: Individual scrapers
        example_individual_scrapers()
        
        # Example 3: Custom configuration
        custom_data = example_custom_configuration()
        
        # Display summary
        if basic_data:
            display_summary(basic_data)
        
        print("\nExample completed successfully!")
        print("Check the generated files:")
        print("- example_output.json (complete data)")
        print("- example_summary.csv (summary table)")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have internet connection and required packages installed.")

if __name__ == "__main__":
    main()
