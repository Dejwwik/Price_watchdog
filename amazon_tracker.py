import requests, smtplib
from bs4 import BeautifulSoup

EMAIL_FROM = "OWN EMAIL"
EMAIL_TO = "OWN EMAIL"
EMAIL_PASS = "OWN EMAIL PASSWORD"

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language" : "cs-CZ",
}

def send_email(link, price):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_FROM, password=EMAIL_PASS)
        connection.sendmail(from_addr=EMAIL_FROM, 
                            to_addrs=EMAIL_TO,
                            msg=f"Subject:Amazon price alert\n\nA product you are looking for dropped below price. Buy on this link:\n{link}\nfor this price ${price}")


amazon_url = input("YOUR AMAZON URL")
price_for_alert = int(input("YOUR PRICE ALERT"))

response = requests.get(url=amazon_url, headers=headers)
content = response.text

soup = BeautifulSoup(content, "html.parser")
try:
    price = float(soup.select_one(selector="div#corePrice_feature_div div.a-section span.a-price span.a-offscreen").get_text().strip("$"))
except(AttributeError):
    price = None

if (price != None) and (price < price_for_alert):
    send_email(amazon_url, price)
    print("Email sent")

