from bs4 import BeautifulSoup as bs
import requests

url = 'https://www.amazon.com/-/es/frecuencia-actualizaci%C3%B3n-sincronizaci%C3%B3n-adaptativa-anticipada/dp/B0CVM2GJCN/ref=sr_1_3'

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

response = requests.get(url, headers=HEADERS)
soup = bs(response.text, "html.parser")
# print(soup)

# get title and price
title = soup.find(id='productTitle').get_text()
price = soup.find("span", class_='aok-offscreen').get_text()

# find_all won't work with get_text()
price = soup.find_all("span", attrs={"class": "aok-offscreen"}).get_text()

print(title)
print(price)
