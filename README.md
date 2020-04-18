# MarketWatcher

[ *Blog post here* ](https://www.genemoynihan.com/2020/04/18/Market-Watcher.html)

Simple python script to grab closing price data from Yahoo finance and email it to a specific inbox.

Default scheduling would be for this to run every morning pre market open.

The default logic is based on the two variables defined at the top of the file in INTERVALS and TICKERS.

TICKERS specifies the list of stocks you wish to track (any ticker from Yahoo finance should be fine to use here)

INTERVALS specified the time frames you wish to compare prices over. For example with INTERVALs = [0, 1, 7, 30] the price movement for yesterdays close would be generated fothe prior day, week and month.

Once all the data has been athered the two tables (one for last price and one for the historic price movements) are converted to html and send to the specified email.

I would recommend setting up a throwaway gmail account to function as the email sender for security reasons as the password needs to be stored somewhere for this script to work.

This script is simply a test and shouldn't be used in seriousness, there are several large flaws with the closing price retrieval logic with regards market events and corporate actions.
