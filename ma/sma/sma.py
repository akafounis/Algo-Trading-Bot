import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


s = 0
tickerSymbol = 'AMZN'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(start='2015-1-1', end='2019-1-4')
close = tickerDf['Close']
sma20 = close.rolling(window=20).mean()
plt.figure(figsize=(12, 6))
plt.plot(close, label='AMZN Adj Close', linewidth=2)
plt.plot(sma20, label='20 day rolling SMA', linewidth=1.5)
plt.xlabel('Date')
plt.ylabel('Adjusted closing price ($)')
plt.title('Price with 20 SMA')
plt.legend()
plt.show()
tickerDf['20 sma'] = close.rolling(window=20).mean()
tickerDf['Signal'] = 0  # spaei se 2 stiles Buy_Signal & Sell_Signal ---> def signal(data):

#agores = 0
#oxi = 0
flag1 = -1
for i in range(20, tickerDf.shape[0]):
    if tickerDf['Close'].iloc[i] < tickerDf['20 sma'].iloc[i]:
        if flag1 != 1:
            tickerDf['Signal'][i] = 1
            flag1 = 1
    else:
        if flag1 != 0:
            tickerDf['Signal'][i] = 0
            flag1 = 0
print(tickerDf)