import datetime as dt
import numpy as np
import pandas_datareader.data as web

def get_yahoo_single_stock(stock_name):
    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()
    
    stock_data = web.DataReader(stock_name, 'yahoo', start, end)
    return stock_data.reset_index()


def GetLastTwelveMonths(df):

    today = df.Date.values[-1]
    twelve_months_back = today - np.timedelta64(365, 'D')
    df_twelve_months = df[df['Date'] > twelve_months_back].reset_index()

    return df_twelve_months
    

def GetMinimumPriceAndDate(df):

    min_date = df.iloc[df['Close'].idxmin()].Date
    min_price = df.iloc[df['Close'].idxmin()].Close
    return min_price, min_date

def GetBeforeAfterMin(df):

    df_twelve_months = GetLastTwelveMonths(df)
    min_price, min_date = GetMinimumPriceAndDate(df_twelve_months)
    df_after_min = df_twelve_months[df_twelve_months['Date'] >= min_date]
    df_before_min = df_twelve_months[df_twelve_months['Date'] < min_date]

    return df_before_min, df_after_min


def FitTrendLine(df):
    x = np.arange(len(df))
    fit = np.polyfit(x, df['Close'], 1)
    fit_fn = np.poly1d(fit)
    return fit_fn(x), fit
