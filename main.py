# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 11:56:32 2021

@author: Saahil Bhatia
"""

import yfinance
import mplfinance as mpf
import time
import numpy as np

money = 5000
shares = 0

def buy(price, date):
    global money
    global shares
    if money != 0:
        shares = float(money/price)
        money = 0
        print("Time: %s" % date)
        print("Money: %0.2f" % money)
        print("Shares: %0.2f\n" % shares)

def sell(price, date):
    global money
    global shares
    if shares != 0:
        money = float(shares*price)
        shares = 0
        print("Time: %s" % date)
        print("Money: %0.2f" % money)
        print("Shares: %0.2f\n" % shares)

def plotAnimated(candles, timeIncrements):
    for candleNum in range(3, len(candles.index)):
        candles_to_graph = candles[0:candleNum] 
        plot(candles_to_graph)
        time.sleep(timeIncrements)

def plot(candles):
    mpf.plot(candles, type='candle', addplot=getMACD(candles, 1))

def getMACD(candles, panel):
    exp12 = candles['Close'].ewm(span=12, adjust=False).mean()
    exp26 = candles['Close'].ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    upSignal = []
    downSignal = []
    previousDate = ''
    previousChange = 0
    previousChangeChange = 0
    for date,value in histogram.iteritems():
        currentChange = value
        if previousDate != '':
            currentChange -= histogram[previousDate]
        currentChangeChange = currentChange - previousChange
        
        if currentChange >= 0:
            upSignal.append(candles['Close'][date]*0.99)
            downSignal.append(np.nan)
        elif currentChange < 0:
            downSignal.append(candles['Close'][date]*1.01)
            upSignal.append(np.nan)
        
        else:
            upSignal.append(np.nan)
            downSignal.append(np.nan)            
        previousDate = date
        previousChange = currentChange
        previousChangeChange = currentChangeChange

    return [mpf.make_addplot(histogram,type='bar',width=0.7,panel=panel,
                             color='dimgray',alpha=1,secondary_y=False),
            mpf.make_addplot(macd,panel=panel,color='fuchsia',secondary_y=True),
            mpf.make_addplot(signal,panel=panel,color='b',secondary_y=True),
            mpf.make_addplot(upSignal,color='g',type='scatter',markersize=200,marker='^'),
            mpf.make_addplot(downSignal,color='r',type='scatter',markersize=200,marker='v')]

def OLDgetMACD(candles, panel):
    exp12 = candles['Close'].ewm(span=12, adjust=False).mean()
    exp26 = candles['Close'].ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    upSignal = []
    downSignal = []
    previous = -1.0
    for date,value in histogram.iteritems():
        if value > 0 and previous <= 0:
            upSignal.append(candles['Close'][date]*0.99)
            downSignal.append(np.nan)
            #buy(candles['Close'][date], date)
        elif value < 0 and previous >= 0:
            downSignal.append(candles['Close'][date]*1.01)
            upSignal.append(np.nan)
            #sell(candles['Close'][date], date)
        else:
            upSignal.append(np.nan)
            downSignal.append(np.nan)
        previous = value

    return [mpf.make_addplot(histogram,type='bar',width=0.7,panel=panel,
                             color='dimgray',alpha=1,secondary_y=False),
            mpf.make_addplot(macd,panel=panel,color='fuchsia',secondary_y=True),
            mpf.make_addplot(signal,panel=panel,color='b',secondary_y=True),
            mpf.make_addplot(upSignal,color='g',type='scatter',markersize=200,marker='^'),
            mpf.make_addplot(downSignal,color='r',type='scatter',markersize=200,marker='v')]

def getMinuteCandles(ticker):
    candles = yfinance.Ticker(ticker).history(interval='1m', start='2021-5-12', end='2021-5-13')
    candles = candles[["Open", "High", "Low", "Close"]]
    candles.index.name = 'Date'
    candles.shape
    return candles

#TESTING FUNCTIONS
def getSPYCandles():
    return getMinuteCandles("SPY")

def testAni(candles):
    plotAnimated(candles, 0.1)

def testPlt(candles):
    plot(candles)
    
candles = getSPYCandles()