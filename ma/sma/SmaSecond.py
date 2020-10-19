import yfinance as yf
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import pandas as pd

pd.options.mode.chained_assignment = None

register_matplotlib_converters()


def get_stock_data(stock_name, start_date, end_date):
    ticker_data = yf.Ticker(stock_name)
    return ticker_data.history(start=start_date, end=end_date)


def find_sma(number_of_days, closingPrices):
    return closingPrices.rolling(window=number_of_days).mean().to_frame()


def show_graph(stock_name, closing_price_df, sma):
    plt.plot(closing_price_df, label=stock_name + ' Closing Price', linewidth=2)
    plt.plot(sma, label='20 day rolling SMA', linewidth=1.5)
    plt.xlabel('Date')
    plt.ylabel('Adjusted closing price ($)')
    plt.title('Price with 20 SMA')
    plt.legend()


def find_indicators(closing_price_df, sma, stock_data_df):
    # construct sell indicators
    flag = 1
    for i in range(closing_price_df.size):
        if (sma.iloc[i].Close > closing_price_df.iloc[i]):
            if flag != 1:
                # SELL !!!
                stock_data_df['Signal'][i] = closing_price_df.iloc[i]
                stock_data_df['ACTION'][i] = "SELL"
                plt.scatter(x=sma.index[i], y=closing_price_df.iloc[i], color='C3')
                flag = 1
        else:
            flag = 0

    # and now buy indicators
    flag = 1
    for i in range(closing_price_df.size):
        if (sma.iloc[i].Close < closing_price_df.iloc[i]):
            if flag != 1:
                # SELL !!!
                stock_data_df['Signal'][i] = closing_price_df.iloc[i]
                stock_data_df['ACTION'][i] = "BUY"
                plt.scatter(x=sma.index[i], y=closing_price_df.iloc[i], color='C2')
                flag = 1
        else:
            flag = 0


def run_sma_bot(stock, start_p, end_p):
    stock_name = stock
    start_period = start_p
    end_period = end_p
    stock_data_df = get_stock_data(stock_name, start_period, end_period)
    closing_price_df = stock_data_df['Close']
    plt.figure(figsize=(12, 6))
    # find SMAs of 20- and 50-days period
    sma = find_sma(20, closing_price_df)
    # show the Graph to the user
    stock_data_df['Signal'] = 0
    stock_data_df['ACTION'] = 'N'
    show_graph(stock_name, closing_price_df, sma)
    find_indicators(closing_price_df, sma, stock_data_df)
    plt.show()
    return stock_data_df
