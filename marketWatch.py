###
# LIBRARIES
###

import datetime as dt
import yfinance as yf
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl

# Set the precision to 2 decimal places
pd.options.display.float_format = '{:.2f}'.format

###
# GLOBAL VARS
###

# For email configuration and formatting
TLS_PORT = 465 # no change
EMAIL_PASS = "12345" # change
SENDER_EMAIL = "sender@mail.com" # change
REC_EMAIL = "receiver@mail.com" # change
MSG_TITLE = "Market Update - "+str(dt.date.today()) # no change

# Time Intervals
# Depending on the intervals you wish to compare against, change these
# e.g. yesterday close compared to two days ago, one month ago etc...
INTERVALS = [0, 1, 7, 30, 90, 180, 365]

# Tickers to watch, lookup any new ones to add on Yahoo finance
TICKERS = ['^FTSE', 'VOD.L', 'HSBA.L']

###
# Functions
###

# Helper function to help adjust weekends to weekdays
# Should be enhanced for trading holidays but I'm lazy...
def getLastWorkingDate(date):
    if date.weekday() == 5:
        return date - dt.timedelta(days = 1)
    elif date.weekday() == 6:
        return date - dt.timedelta(days = 2)
    else:
        return date

# Retrive the closing prices for the tickers for each of the
#   days for the INTERVALS specified in the past
def getCloses(last_working_date):
    results = pd.DataFrame()
    for i in INTERVALS:
        date = last_working_date - dt.timedelta(days = i)
        date = getLastWorkingDate(date)
        print("Retrieving data for date:", date)
        res = yf.download(TICKERS, start=date - dt.timedelta(days=4), end=date + dt.timedelta(days=1))[-1:]
        results = results.append(res["Adj Close"])
    return results

# Once closing prices are retrieved calculate the difference
#   between last close and those prices.
def getDiffs(closing_prices):
    diff_results = pd.DataFrame()
    diff_results["INTERVALS"] = INTERVALS
    diff_results = diff_results.set_index('INTERVALS')
    for nm in closing_prices:
        print("Calculating differences for:", nm)
        diffs=[]
        current_price = closing_prices[nm][0]
        for prc in closing_prices[nm]:
            diff = 100*(current_price-prc)/prc
            diffs.append(diff)
        diff_results[nm] = diffs
    return diff_results.drop(0)

# Generate an email and send it via the gmail smtp server
# I would recommend generating a dev gmail account for this purpose
#   to avoid any chance of your main account being compromised
def sendEmail(msg):
    message = MIMEMultipart("alternative")
    message["Subject"] = MSG_TITLE
    message["From"] = SENDER_EMAIL
    message["To"] = REC_EMAIL
    msg = MIMEText(msg, "html")
    message.attach(msg)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", TLS_PORT, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, REC_EMAIL, message.as_string())

# Grab last close price for all tickers specified as well as
#   the differences (% change) for intervals in the last year
# Once the data has been gathered change the tables to html and
#   pass to the email send function
def main():
    last_working_date = dt.date.today() - dt.timedelta(days = 1)
    last_working_date = getLastWorkingDate(last_working_date)
    closing_prices = getCloses(last_working_date)
    price_diffs = getDiffs(closing_prices)
    closing_prices = closing_prices[0:1].to_html(formatters={'Name': lambda x: '<b>' + x + '</b>'})
    price_diffs = price_diffs.to_html(formatters={'Name': lambda x: '<b>' + x + '</b>'})
    sendEmail(closing_prices + price_diffs)

main()
