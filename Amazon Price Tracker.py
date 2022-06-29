from email.mime.text import MIMEText

from bs4 import BeautifulSoup
import requests
from pprint import pprint
import lxml
from email.message import EmailMessage
import smtplib

my_email = "anthonylovesuma@gmail.com"
reciever = "anturiarte16@gmail.com"
password = "qccbxhlioqisnzbu"

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
ACCEPT_LANGUAGE = "en-US"

# URL = "https://www.amazon.com/Apple-MLWK3AM-A-AirPods-Pro/dp/B09JQMJHXY/ref=sr_1_1_sspa?crid=2YFM8H1V8BO07&keywords=airpods&qid=1656456826&sprefix=airpod%2Caps%2C124&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyMTZOTFBDSEFBTkomZW5jcnlwdGVkSWQ9QTAxMDk2MzBPRzIxRExXV0xTVlMmZW5jcnlwdGVkQWRJZD1BMDI2OTgyNjI5VzVZMDVGTFdBTDQmd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl"
URL = "https://www.amazon.com/dp/B08PZHYWJS/ref=fs_a_mdt2_us0"
price_target = 500

headers = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE
}

website_response = requests.get(url=URL, headers=headers)

website_html = website_response.text

# pprint(website_html)

soup = BeautifulSoup(website_html, "lxml")

title = soup.find(name="span", id="productTitle").getText().strip()
whole = soup.find(name="span", class_="a-price-whole").getText()
decimal = soup.find(name="span", class_="a-price-fraction").getText()

price = float(f"{whole}{decimal}")

def send_email():
    #create and format email message
    newMessage = EmailMessage()
    newMessage['Subject'] = "Amazon Price Alert!"
    newMessage['From'] = my_email
    newMessage['To'] = reciever
    newMessage.set_content(f"The {title} is now ${price}\n{URL}\n")

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(newMessage)

if price <= price_target:
    send_email()
    print("Price alert sent!!!")
else:
    print(f"The price of the {title} is still over ${price_target}.")

