# PASS = "frjrudsgokigcrky"
import datetime as dt
import pandas as pd
import random
import smtplib

df = pd.read_csv("Automated-email-sender/data.csv")

MY_EMAIL = "add-your-own-email-here"
MY_PASSWORD = "add-your-own-app-password-after-2factor-auth"

today = dt.datetime.now().date()
today_month = today.month
today_day = today.day

for index, row in df.iterrows():
    if row['month'] == today_month and row['day'] == today_day:
        file_path = f"Automated-email-sender/letter_templates/letter_{random.randint(1,3)}.txt"
        PLACEHOLDER = "[Name]"

        # print(f"Reading from file: {file_path}")
        
        with open(file_path, 'r') as letter:
            letter_contents = letter.read()

        # print(f"Original letter contents:\n{letter_contents}")    

        letter_contents = letter_contents.replace(PLACEHOLDER, row['name'])

        # print(f"Modified letter contents:\n{letter_contents}")

        with smtplib.SMTP("smtp.gmail.com",587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL,MY_PASSWORD)
            connection.sendmail(
                from_addr = MY_EMAIL,
                to_addrs = row['email'],
                msg = f"Subject:HAPPY BIRTHDAY:\n\n{letter_contents}"
                )
        