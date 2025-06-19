# Web Scraper Collection

A comprehensive Python web scraping tool that demonstrates scraping different types of websites with proper rate limiting, error handling, and data export functionality.

## Features

- **Multi-site scraping**: Scrapes different types of websites (news, quotes, books, APIs)
- **Rate limiting**: Built-in delays between requests to be respectful to servers
- **Error handling**: Robust error handling with logging
- **Data export**: Saves data to both JSON and CSV formats
- **Modular design**: Easy to extend with new scrapers

## Scraped Sites

1. **News Site Demo** (`httpbin.org/html`) - Demonstrates HTML parsing
2. **Quotes Site** (`quotes.toscrape.com`) - Scrapes quotes with authors and tags
3. **Books Site** (`books.toscrape.com`) - Extracts book information including prices and ratings
4. **JSON API** (`jsonplaceholder.typicode.com`) - Demonstrates API data collection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/abhishekrajpura/web-scraper-collection.git
cd web-scraper-collection
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:
```bash
python web_scraper.py
```

### Programmatic Usage

```python
from web_scraper import WebScraper

# Initialize scraper
scraper = WebScraper(delay_range=(1, 3))

# Run all scrapers
data = scraper.run_all_scrapers()

# Save results
scraper.save_to_json("my_data.json")
scraper.save_to_csv("my_summary.csv")
```

### Individual Scrapers

```python
# Scrape specific sites
quotes_data = scraper.scrape_quotes_site()
books_data = scraper.scrape_books_site()
api_data = scraper.scrape_json_api()
```

## Output Files

The scraper generates two output files:

- **`scraped_data.json`**: Complete scraped data in JSON format
- **`scraped_summary.csv`**: Summary table with URL, title, type, and item counts

## Configuration

### Rate Limiting

Adjust the delay between requests:
```python
scraper = WebScraper(delay_range=(2, 5))  # 2-5 seconds between requests
```

### Custom Headers

The scraper uses a realistic User-Agent string by default. You can modify headers in the `__init__` method.

## Code Structure

```
web_scraper.py          # Main scraper class and functions
├── WebScraper         # Main scraper class
├── scrape_news_site   # HTML content scraper
├── scrape_quotes_site # Quotes with metadata
├── scrape_books_site  # Product listings
├── scrape_json_api    # API endpoint scraper
└── save_to_*          # Export functions
```

## Ethical Considerations

This scraper is designed with ethical web scraping practices:

- **Rate limiting**: Implements delays between requests
- **Respectful headers**: Uses realistic User-Agent strings
- **Error handling**: Gracefully handles server errors
- **Timeout limits**: Prevents hanging requests
- **Test sites**: Uses scraping-friendly sites for demonstration

## Extending the Scraper

To add a new scraper:

1. Create a new method in the `WebScraper` class:
```python
def scrape_new_site(self, url: str) -> Dict[str, Any]:
    soup = self._get_page(url)
    # Your scraping logic here
    return {
        'url': url,
        'title': 'Site Title',
        'data': extracted_data,
        'type': 'new_site_type'
    }
```

2. Add it to the `run_all_scrapers` method

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## Legal Notice

This tool is for educational purposes. Always:
- Check robots.txt before scraping
- Respect rate limits
- Follow website terms of service
- Use scraped data responsibly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

**Connection Errors**: 
- Check your internet connection
- Some sites might block automated requests

**Import Errors**:
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**No Data Scraped**:
- Check if target websites are accessible
- Verify website structure hasn't changed

### Logging

The scraper includes detailed logging. Check console output for debugging information.

## Example Output

```json
{
  "url": "http://quotes.toscrape.com/",
  "title": "Quotes to Scrape",
  "quotes": [
    {
      "text": "The world as we have created it is a process of our thinking.",
      "author": "Albert Einstein",
      "tags": ["change", "deep-thoughts", "thinking", "world"]
    }
  ],
  "total_quotes": 10,
  "type": "quotes_site"
}
```