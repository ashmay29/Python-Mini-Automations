import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = " "

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = " "

MY_EMAIL = " "
MY_PASS = " "

stocks_params = {
    "apikey": STOCK_API_KEY,
    "function": "TIME_SERIES_DAILY",
    "outputsize": "compact",
    "symbol": STOCK,
    "datatype": "json",
}
response = requests.get(STOCK_ENDPOINT, params=stocks_params)
response.raise_for_status()
stock_data = response.json()
stock_list = list(stock_data["Time Series (Daily)"].items())
yesterday_close = float(stock_list[0][1]['4. close'])
day_before_yesterday_close = float(stock_list[1][1]['4. close'])
difference_in_stock_price = round(abs(yesterday_close - day_before_yesterday_close), 2)
diff_percent = round((difference_in_stock_price / yesterday_close) * 100, 3)

if diff_percent > 3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "language": "en",
        "sortBy": "relevancy",
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    news_data = response.json()
    news_articles = []
    for i in range(3):
        news_articles.append(news_data['articles'][i])
    message_mail = [f"Headline: {article['title']}\nBrief: {article['description']}" for article in news_articles]
    email_body = "\n\n".join(message_mail)
    
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    if yesterday_close> day_before_yesterday_close:
        msg['Subject'] = f"{STOCK}: 🔺{diff_percent}%"
    else:
        msg['Subject'] = f"{STOCK}: 🔻{diff_percent}%"

    msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASS)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=msg.as_string()
            )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email:{e}")

