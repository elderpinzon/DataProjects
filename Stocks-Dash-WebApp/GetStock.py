import datetime as dt
import numpy as np
import pandas_datareader.data as web

def get_yahoo_single_stock(stock_name):
    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()
    
    stock_data = web.DataReader(stock_name, 'yahoo', start, end)
    return stock_data.reset_index()
