from email.mime.text import MIMEText

from bs4 import BeautifulSoup
import requests
from pprint import pprint
import lxml
from email.message import EmailMessage
import smtplib

my_email = os.environ.get('MY_EMAIL')
reciever = os.environ.get('RECIEVER_EMAIL')
password = os.environ.get('EMAIL_PASSWORD')

USER_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
ACCEPT_LANGUAGE = "en-US"

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

