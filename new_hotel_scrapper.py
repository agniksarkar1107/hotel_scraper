import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Bypass bot detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# Scrape hotel data from Booking.com
def scrape_booking_hotels(city, num_hotels, checkin_date, checkout_date):
    driver = init_driver()
    
    url = f"https://www.booking.com/searchresults.html?ss={city.replace(' ', '+')}&checkin={checkin_date}&checkout={checkout_date}"
    driver.get(url)
    time.sleep(5)

    hotels = []
    hotel_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")[:num_hotels]

    for hotel in hotel_elements:
        try:
            name = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
        except:
            name = "N/A"

        try:
            description = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='property-card-description']").text
        except:
            description = "N/A"

        try:
            price_per_night = hotel.find_element(By.XPATH, ".//span[contains(@data-testid, 'price-and-discounted-price')]").text
        except:
            try:
                price_per_night = hotel.find_element(By.XPATH, ".//span[contains(@aria-hidden, 'true')]").text
            except:
                price_per_night = "N/A"

        try:
            rating = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='review-score']").text
        except:
            rating = "N/A"

        try:
            num_reviews = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='review-score'] span").text
        except:
            num_reviews = "N/A"

        try:
            stars = len(hotel.find_elements(By.CSS_SELECTOR, "span[data-testid='rating-stars'] svg"))
        except:
            stars = "N/A"

        try:
            image = hotel.find_element(By.CSS_SELECTOR, "img[data-testid='image']").get_attribute("src")
        except:
            image = "N/A"

        try:
            address = hotel.find_element(By.CSS_SELECTOR, "span[data-testid='address']").text
            address_parts = address.split(", ")
            state = address_parts[-2] if len(address_parts) > 2 else "N/A"
            country = address_parts[-1] if len(address_parts) > 1 else "N/A"
        except:
            address, state, country = "N/A", "N/A", "N/A"

        try:
            distance_from_center = hotel.find_element(By.CSS_SELECTOR, "span[data-testid='distance']").text
        except:
            distance_from_center = "N/A"

        try:
            hotel_link = hotel.find_element(By.CSS_SELECTOR, "a[data-testid='title-link']").get_attribute("href")
        except:
            hotel_link = "N/A"

        # Click on hotel link to get extra details
        check_in_time, check_out_time, room_type, facilities, user_rating_category, latitude, longitude, hotel_chain, wifi, parking, pool, breakfast, nearby_attractions, hotel_type = (
            "N/A", "N/A", "N/A", [], "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", [], "N/A"
        )

        if hotel_link != "N/A":
            try:
                driver.execute_script("window.open(arguments[0]);", hotel_link)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)

                try:
                    check_in_time = driver.find_element(By.XPATH, "//div[contains(text(),'Check-in')]/following-sibling::div").text
                except:
                    check_in_time = "N/A"

                try:
                    check_out_time = driver.find_element(By.XPATH, "//div[contains(text(),'Check-out')]/following-sibling::div").text
                except:
                    check_out_time = "N/A"

                try:
                    room_type = driver.find_element(By.XPATH, "//div[contains(text(),'Room type')]/following-sibling::div").text
                except:
                    room_type = "N/A"

                try:
                    facility_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'facilities')]//li")
                    facilities = [fac.text for fac in facility_elements if fac.text.strip() != ""]
                except:
                    facilities = []

                try:
                    user_rating_category = driver.find_element(By.XPATH, "//div[contains(@class,'review-score-badge')]").text
                except:
                    user_rating_category = "N/A"

                try:
                    hotel_chain = driver.find_element(By.XPATH, "//div[contains(text(),'Hotel Chain')]/following-sibling::div").text
                except:
                    hotel_chain = "N/A"

                try:
                    latitude = driver.find_element(By.XPATH, "//meta[@property='booking_com:latitude']").get_attribute("content")
                    longitude = driver.find_element(By.XPATH, "//meta[@property='booking_com:longitude']").get_attribute("content")
                except:
                    latitude, longitude = "N/A", "N/A"

                try:
                    wifi = "Yes" if "WiFi" in facilities else "No"
                    parking = "Yes" if "Parking" in facilities else "No"
                    pool = "Yes" if "Swimming pool" in facilities else "No"
                    breakfast = "Yes" if "Breakfast" in facilities else "No"
                except:
                    wifi, parking, pool, breakfast = "N/A", "N/A", "N/A", "N/A"

                try:
                    nearby_attraction_elements = driver.find_elements(By.XPATH, "//ul[@data-testid='attractions']//li")
                    nearby_attractions = [attr.text for attr in nearby_attraction_elements if attr.text.strip() != ""]
                except:
                    nearby_attractions = []

                try:
                    hotel_type = driver.find_element(By.XPATH, "//div[contains(@class, 'property-type-badge')]").text
                except:
                    hotel_type = "N/A"

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"Error fetching details for {name}: {e}")

        hotel_data = {
            "name": name,
            "description": description,
            "type": hotel_type,
            "hotel_chain": hotel_chain,
            "image": image,
            "website": hotel_link,
            "price_per_night": price_per_night,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "latitude": latitude,
            "longitude": longitude,
            "check_in_time": check_in_time,
            "check_out_time": check_out_time,
            "rating": rating,
            "num_reviews": num_reviews,
            "stars": stars,
            "room_type": room_type,
            "facilities": facilities,
            "distance_from_center": distance_from_center,
            "wifi": wifi,
            "parking": parking,
            "pool": pool,
            "breakfast": breakfast,
            "nearby_attractions": nearby_attractions,
            "user_rating_category": user_rating_category,
        }

        hotels.append(hotel_data)

    driver.quit()

    with open(f"{city}_hotels.json", "w", encoding="utf-8") as f:
        json.dump(hotels, f, indent=4, ensure_ascii=False)

    print(f"Scraped {len(hotels)} hotels in {city} and saved as JSON.")
if __name__ == "__main__":
    user_city = input("Enter the city to scrape hotels from: ")
    user_num_hotels = int(input("Enter the number of hotels to scrape: "))
    user_checkin = input("Enter check-in date (YYYY-MM-DD): ")
    user_checkout = input("Enter check-out date (YYYY-MM-DD): ")
    scrape_booking_hotels(user_city, user_num_hotels, user_checkin, user_checkout)
