from playwright.sync_api import sync_playwright
import csv
import json

def scrape_pakwheels():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        base_url = "https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/vg_gli/yr_2013_2016/?page="
        page_num = 1
        total_scraped = 0

        print("Getting total number of pages...")
        page.goto(base_url + "1", timeout=120000, wait_until="domcontentloaded")
        page.wait_for_selector("ul.pagination", timeout=20000)
        
        last_page_link = page.query_selector("ul.pagination li.last a")
        total_pages = 1
        
        if last_page_link:
            try:
                href = last_page_link.get_attribute("href")
                page_num_str = href.split("page=")[-1]
                total_pages = int(page_num_str)
            except (ValueError, IndexError):
                print("Could not parse last page number, defaulting to 1")
        
        print(f"Total pages found: {total_pages}")

        with open("pakwheels_listings.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price", "Location", "Year", "Link", "Mileage", "Fuel", "Engine", "Transmission", "Last_updated", "Image_url"])

            while page_num <= total_pages:
                print(f"\nNavigating to page {page_num} of {total_pages}...")
                page.goto(base_url + str(page_num), timeout=120000, wait_until="domcontentloaded")

                try:
                    page.wait_for_selector("li.classified-listing", timeout=20000)
                    cars = page.query_selector_all("li.classified-listing")

                    if not cars:
                        print("No more cars found. Ending scraping.")
                        break

                    print(f"Found {len(cars)} cars on page {page_num}")

                    for car in cars:
                        try:
                            title_el = car.query_selector("a.car-name.ad-detail-path")
                            if not title_el:
                                continue

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
                                        image_url = gallery_data[0]["src"] if gallery_data else "N/A"
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
                            total_scraped += 1

                        except Exception as e:
                            print(f"Error scraping one listing: {str(e)}")

                except Exception as e:
                    print(f"Failed to load or parse page {page_num}: {str(e)}")
                    break

                page_num += 1 

        print(f"\nScraping completed. Total cars scraped: {total_scraped}")
        browser.close()

if __name__ == "__main__":
    scrape_pakwheels()
