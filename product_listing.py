from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urljoin
import pandas as pd

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

visited_urls = set()

def get_product_info(url):
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error in getting webpage: {url}")
        return None

    soup = bs(response.text, "html.parser")

    title_element = soup.select_one('#productTitle')
    title = title_element.text.strip() if title_element else None

    rating_element = soup.select_one('#acrPopover')
    rating_text = rating_element.attrs.get('title') if rating_element else None
    rating = rating_text.replace('out of 5 stars', '') if rating_text else None

    price_element = soup.select_one('span.a-price').select_one('span.a-offscreen')
    price_total = price_element.text
    price = price_total.strip()[1:] if price_element else None

    image_element = soup.select_one('#landingImage')
    image = image_element.attrs.get('src') if image_element else None

    description_element = soup.select_one('#feature-bullets')
    description = description_element.text.strip() if description_element else None

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "image": image,
        "description": description,
        "url": url
    }

def parse_listing(listing_url):
    global visited_urls
    response = requests.get(listing_url, headers=HEADERS)
    soup = bs(response.text, "html.parser")
    link_elements = soup.select("[data-asin] h2 a")
    page_data = []

    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get("href"))
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print(f"Scraping product from {full_url[:100]}", flush=True)
            product_info = get_product_info(full_url)
            if product_info:
                page_data.append(product_info)

    next_page_el = soup.select_one('a.s-pagination-next')
    if next_page_el:
        next_page_url = next_page_el.attrs.get('href')
        next_page_url = urljoin(listing_url, next_page_url)
        print(f'Scraping next page: {next_page_url}', flush=True)
        page_data += parse_listing(next_page_url)

    return page_data

def main():
    data = []
    search_url = "https://www.amazon.com/s?k=bose&rh=n%3A12097479011&ref=nb_sb_noss"
    data = parse_listing(search_url)
    df = pd.DataFrame(data)
    df.to_csv("/home/axel/Code/Python/alexAnalyst/amazon_scraper/headphones.csv", index=False)


if __name__ == '__main__':
    main()
