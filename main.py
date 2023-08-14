import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_KEY = os.environ.get("ALPHA_KEY")
news_key = os.environ.get("NEWS_KEY")
twilio_key = os.environ.get("TWILIO_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")

alpha_endpoint = 'https://www.alphavantage.co/query'
news_endpoint = 'https://newsapi.org/v2/everything'
twilio_phone = os.environ.get("TWILIO_PHONE")
end_phone = os.environ.get("END_PHONE")


stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'outputsize': 'compact',
    'apikey': ALPHA_KEY,
}

alpha_request = requests.get(url=alpha_endpoint, params=stock_params).json()["Time Series (Daily)"]

date_list = [value for (key, value) in alpha_request.items()]
yesterday_stock = float(date_list[1]['4. close'])
before_yesterday_stock = float(date_list[2]['4. close'])
difference = yesterday_stock-before_yesterday_stock

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
getting_percentage = abs(round((difference / yesterday_stock) * 100))

if getting_percentage > 2:
    news_params = {
        'q': COMPANY_NAME,
        'searchIn': 'title',
        'apiKey': news_key,
    }
    news_request = requests.get(url=news_endpoint, params=news_params).json()["articles"]
    three_news = news_request[:3]

    formatted_news = [f'{STOCK}: {up_down}{getting_percentage}%\n\nHeadlines:{article["title"]}\n\nBrief:{article["description"]}' for article in three_news]
    client = Client(ACCOUNT_SID, twilio_key)
    for new in formatted_news:
        message = client.messages \
                        .create(
                             body=f'Tesla: {new}',
                             from_=twilio_phone,
                             to=end_phone
                         )

