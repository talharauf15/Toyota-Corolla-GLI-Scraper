from playwright.sync_api import sync_playwright

def save_html_snapshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.goto("https://www.pakwheels.com/used-cars/search/-/mk_toyota/md_corolla/vg_gli/yr_2013_2016/?page=1", timeout=60000)

        page.wait_for_timeout(5000)

        html_content = page.content()

        with open("page_snapshot.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("HTML snapshot saved as 'page_snapshot.html'.")

        browser.close()

if __name__ == "__main__":
    save_html_snapshot()
