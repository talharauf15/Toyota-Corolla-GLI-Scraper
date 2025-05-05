# Toyota-Corolla-GLI-Scraper

A web scraper that extracts Toyota Corolla GLi listings (2013–2016) from PakWheels.com, including price, location, mileage, engine capacity, and ad details. Built with Playwright for dynamic content scraping.

## 🚗 Overview

This project automates the extraction of Toyota Corolla GLi listings from PakWheels.com. It captures essential details such as:

- **Price**
- **Location**
- **Mileage**
- **Engine Capacity**
- **Ad Details**

The scraper utilizes Playwright to handle dynamic content and simulate user interactions, ensuring accurate data retrieval.

## ⚙️ Requirements

Before running the scraper, ensure you have the following installed:

- Python 3.8 or higher
- Playwright
- Other dependencies listed in `requirements.txt`

## 📦 Installation

1. Clone the repository:

```bash
   git clone https://github.com/talharauf15/Toyota-Corolla-GLI-Scraper.git
   cd Toyota-Corolla-GLI-Scraper
```

2. Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:

   ```bash
   python -m playwright install
   ```

## 🛠️ Usage

To run the scraper:

```bash
python scraper.py
```

The script will:

* Launch a browser instance using Playwright.
* Navigate to the PakWheels Toyota Corolla GLi listings page.
* Extract relevant data from each listing.
* Save the extracted data to `pakwheels_listings.csv`.

## 📄 Output

The `pakwheels_listings.csv` file will contain the following columns:

* `price`: The listed price of the vehicle.
* `location`: The location where the vehicle is available.
* `mileage`: The mileage of the vehicle.
* `engine_capacity`: The engine capacity of the vehicle.
* `ad_details`: Additional details provided in the ad.

## 🧪 Testing

To ensure the scraper functions correctly:

1. Run the scraper:

   ```bash
   python scraper.py
   ```

2. Verify that the `pakwheels_listings.csv` file is generated and contains data.

3. Check the console output for any errors or issues during the scraping process.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
