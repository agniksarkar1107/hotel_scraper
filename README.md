# Hotel Scraper using Selenium

## Overview
This project is a web scraper that extracts hotel details from Booking.com based on a given city, number of hotels, and check-in/check-out dates. The scraped data includes hotel names, descriptions, ratings, prices, facilities, and more, and is saved in a JSON file.

## Features
- Scrapes hotel listings from Booking.com.
- Extracts details like name, description, price, rating, room type, facilities, and more.
- Saves the data in a structured JSON format.
- Uses Selenium WebDriver with ChromeDriver.
- Bypasses basic bot detection mechanisms.

## Requirements
Ensure you have the following installed before running the script:

- Python (>=3.7)
- Google Chrome (latest version recommended)
- ChromeDriver (managed automatically by `webdriver-manager`)
- Required Python packages:
  ```
  selenium
  webdriver-manager
  ```
  Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

## Installation & Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/agniksarkar1107/hotel-scraper.git
   cd hotel-scraper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have Google Chrome installed on your system.

## Usage
Run the script using the following command:
```bash
python scraper.py
```
It will prompt you to enter:
- City name
- Number of hotels to scrape
- Check-in date (YYYY-MM-DD)
- Check-out date (YYYY-MM-DD)

Example:
```
Enter the city to scrape hotels from: New York
Enter the number of hotels to scrape: 5
Enter check-in date (YYYY-MM-DD): 2025-03-01
Enter check-out date (YYYY-MM-DD): 2025-03-05
```

Once completed, the scraped data will be saved as `New_York_hotels.json`.

## Data Extracted
The script extracts the following details (if available):
- Hotel Name
- Description
- Hotel Type
- Image URL
- Booking Website Link
- Price per Night
- Address (City, State, Country)
- Latitude & Longitude
- Check-in & Check-out Times
- Rating & Review Count
- Room Type
- Facilities (WiFi, Parking, Pool, Breakfast, etc.)
- Distance from City Center
- Nearby Attractions

## Notes
- Booking.com’s website structure may change over time, which might require updating the scraper.
- Ensure Chrome and ChromeDriver are up to date to prevent compatibility issues.

## License
This project is licensed under the MIT License.

## Disclaimer
This scraper is intended for educational and research purposes only. Scraping websites without permission may violate their terms of service. Use responsibly.

## Author
**Agnik Sarkar**  
agnikbosconian@gmail.com  
GitHub: [yourusername](https://github.com/agniksarkar1107)

