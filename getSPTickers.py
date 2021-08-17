from bs4 import BeautifulSoup
import requests
import pandas
import yfinance
import finplot as fplt
import streamlit as st

def getSPTickers():
    #get S&P 500 tickers from wikipedia
    wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table_id = 'constituents'
    response = requests.get(wiki_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    html_table = soup.find('table', attrs={'id': table_id})
    tickers = pandas.read_html(str(html_table))
    tickers = tickers[0]
    tickers = tickers['Symbol']
    return tickers

def getTickerDailyChange(ticker):
    # get ticker data
    tickerData = yfinance.Ticker(ticker).history(interval='1d', start='2010-1-1', end='2021-2-1')
    tickerData = tickerData[["Open", "Close"]]
    dates = tickerData.reset_index()['Date'];

    # find percentage change
    tickerOpen = tickerData["Open"]
    tickerClose = tickerData["Close"]
    tickerChange = tickerOpen
    for date in dates:
        tickerChange[date] = (tickerClose[date] - tickerOpen[date]) / tickerOpen[date] * 100

    return tickerChange

def launchPage():
    changeGME = getTickerDailyChange("GME")
    changeSP = getTickerDailyChange("^GSPC")
    st.write("""
             # GME stock daily percentage change
             """)
    st.line_chart(changeGME)
    st.write("""
             # S&P 500 stock daily percentage change
             """)
    st.line_chart(changeSP)