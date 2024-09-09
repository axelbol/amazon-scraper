# Libraries
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

def get_soup_url(url):
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print('Error getting the webpage')
        exit(-1)

    soup = bs(response.text, "html.parser")
    return soup

def get_reviews(soup):
    base_url = 'https://www.amazon.com'
    # css selectors | get review content
    reviews_element = soup.select('div[data-hook="review"]', limit=8)
    reviews_data = []

    for review in reviews_element:
        r_author_element = review.select_one('span.a-profile-name')
        r_author = r_author_element.text if r_author_element else None

        r_rating_element = review.select_one('i[data-hook="review-star-rating"] span.a-icon-alt')
        r_rating = r_rating_element.text.replace(' out of 5 stars', '') if r_rating_element else 'No rating'

        r_title_element = review.select_one('a[data-hook="review-title"]')
        r_title_span_element = r_title_element.select_one("span:not([class])") if r_title_element else None
        r_title = r_title_span_element.text if r_title_span_element else None

        r_body_element = review.select_one('span[data-hook="review-body"] span')
        r_body = r_body_element.text if r_body_element else 'No review body'

        r_date_element = review.select_one('span[data-hook="review-date"]')
        r_date = r_date_element.text if r_date_element else 'No review date'

        r_href_element = review.select_one('a[data-hook="review-title"]')
        r_href = r_href_element.get('href') if r_href_element else None
        full_url = base_url + r_href if r_href else None

        # Add the data to the list
        reviews_data.append({
            'review_author': r_author,
            'review_rating': r_rating,
            'review_title': r_title,
            'review_body': r_body,
            'review_date': r_date,
            'review_href': full_url
        })

        df_reviews_data = pd.DataFrame(reviews_data)

    return df_reviews_data



def main():
    search_url = 'https://www.amazon.com/-/en/frecuencia-actualizaci%C3%B3n-sincronizaci%C3%B3n-adaptativa-anticipada/dp/B0CVM2GJCN/ref=sr_1_3'
    soup = get_soup_url(search_url)
    # print(soup.prettify())
    data = get_reviews(soup)
    # print(data)
    # df = pd.DataFrame(data=data)
    data.to_csv('/home/axel/Code/Python/alexAnalyst/amazon_scraper/amz.csv')

if __name__ == '__main__':
    main()
