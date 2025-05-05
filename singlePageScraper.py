from playwright.sync_api import sync_playwright
import csv
import json

def scrape_pakwheels():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        
        print("Navigating to site...")
        page.goto("https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/vg_gli/yr_2013_2016/?page=1", timeout=60000, wait_until="domcontentloaded")

        try:
            print("Waiting for listings to load...")
            page.wait_for_selector("li.classified-listing")

            print("Fetching all listings...")
            cars = page.query_selector_all("li.classified-listing")

            print(f"Found {len(cars)} cars")

            with open("pakwheels_listings.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Price", "Location", "Year", "Link", "Mileage", "Fuel", "Engine", "Transmission", "Last_updated", "Image_url"])

                for car in cars:
                    try:
                        
                        title_el = car.query_selector("a.car-name.ad-detail-path")  

                        title = title_el.get_attribute("title").strip()
                        link = "https://www.pakwheels.com" + title_el.get_attribute("href")

                        price_el = car.query_selector("div.price-details")
                        price = price_el.inner_text().strip() if price_el else "N/A"
                        
                        location_el = car.query_selector("ul.search-vehicle-info li")
                        location = location_el.inner_text().strip() if location_el else "N/A"
                        
                        gallery_el = car.query_selector("ul.gallery")
                        if gallery_el:
                            gallery_info = gallery_el.get_attribute("data-galleryinfo")
                            if gallery_info:
                                try:
                                    gallery_data = json.loads(gallery_info)
                                    if gallery_data and len(gallery_data) > 0:
                                        image_url = gallery_data[0]["src"]
                                    else:
                                        image_url = "N/A"
                                except:
                                    image_url = "N/A"
                            else:
                                image_url = "N/A"
                        else:
                            image_url = "N/A"
                        
                        details_list = car.query_selector_all("ul.search-vehicle-info-2 li")
                        year = details_list[0].inner_text().strip() if len(details_list) > 0 else "N/A"
                        mileage = details_list[1].inner_text().strip() if len(details_list) > 1 else "N/A"
                        fuel = details_list[2].inner_text().strip() if len(details_list) > 2 else "N/A"
                        engine = details_list[3].inner_text().strip() if len(details_list) > 3 else "N/A"
                        transmission = details_list[4].inner_text().strip() if len(details_list) > 4 else "N/A"
                        
                        updated_el = car.query_selector("div.dated")
                        last_updated = updated_el.inner_text().strip() if updated_el else "N/A"
                        
                        print(f"Title: {title}")
                        print(f"Price: {price}")
                        print(f"Location: {location}")
                        print(f"Link: {link}")
                        print(f"Mileage: {mileage}")
                        print(f"Fuel: {fuel}")
                        print(f"Engine: {engine}")
                        print(f"Transmission: {transmission}")
                        print(f"Updated: {last_updated}")
                        print(f"Year: {year}")
                        print(f"Image: {image_url}")
                        print("-" * 40)

                        writer.writerow([title, price, location, year, link, mileage, fuel, engine, transmission, last_updated, image_url])

                    except Exception as e:
                        print(f"Error scraping one listing: {str(e)}")

            print("Scraping completed and saved to pakwheels_listings.csv")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_pakwheels()
