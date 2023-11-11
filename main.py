import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("local.env")

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER')


amazon_url = "https://www.amazon.co.uk/Pok%C3%A9mon-Nintendo-Digital-Exclusive-Amazon-co-uk/dp/B0B2X4BMV2/ref=sr_1_1?keywords=pokemon+violet&qid=1664876065&qu=eyJxc2MiOiIxLjM3IiwicXNhIjoiMC42NCIsInFzcCI6IjAuMjIifQ%3D%3D&sprefix=pokemon+%2Caps%2C64&sr=8-1"
headers = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

response = requests.get(url=amazon_url, headers=headers)
data = response.text
soup = BeautifulSoup(data, "html.parser")

product_title = soup.find(name="span", id="productTitle").text
current_price = float(soup.find(name="span", id="priceblock_ourprice", class_="priceBlockBuyingPriceString").text.split("£")[1])

if current_price < 42.99:
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=RECEIVER_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{product_title} only €{current_price}.\n Buy it here: {amazon_url}".encode('utf-8')
        )
