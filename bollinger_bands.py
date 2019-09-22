import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
#from pandas.io.data import DataReader
from datetime import datetime

def symbol_to_path(symbol, base_dir="data"):
    """Return stock data (adjusted close) for given symbols from CSV files """
    #return os.path.join(base_dir, "{}.csv".format(str(symbol)))
    return os.path.join("data/{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols: #add SPY for reference absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',parse_dates=True, usecols=['Date','Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns = {'Adj Close':symbol})
        df = df.join(df_temp)
        if symbol == 'SPY': #drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df

def plot_data(df,title="Stock prices"):
    ax = df.plot(title=title,fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.plot(df)
    plt.show()

def get_rolling_mean(values,window):
    test = pd.DataFrame(values)
    return test.rolling(window).mean()
    # return pd.rolling_mean(values,window=window)

def get_rolling_std(values,window):
    #return pd.rolling_std(values, window=window)
    test = pd.DataFrame(values)
    return test.rolling(window).std()

def get_bollinger_bands(rm,rstd):
    upper_band = rm + rstd*2
    lower_band = rm - rstd*2
    return upper_band, lower_band

def test_run():
    dates = pd.date_range('2015-01-01','2015-12-31')
    symbols = ['SPY']
    df = get_data(symbols,dates)

    rm_SPY = get_rolling_mean(df['SPY'],window=20)

    rstd_SPY = get_rolling_std(df['SPY'],window=20)

    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    #Plot
    ax = df['SPY'].plot(title="Bollinger Bands",label='SPY')
    rm_SPY.plot(label='Rolling mean',ax=ax)
    upper_band.plot(label='upper band',ax=ax)
    lower_band.plot(label='lower band',ax=ax)

    #Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()


if __name__ == "__main__":
    test_run()
