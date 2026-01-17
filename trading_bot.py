# api key info placed into rest function
# get data function (add technical indicators)
# run function to place orders and sell if ema and sma is above a certain value

import pandas as pd
from alpaca_trade_api.rest import REST #use alpaca api
import pandas_ta as ta #technical analysis
import time #check time interval to prevent overloading alpaca

API = 'Your API Key'
API_SECRET = 'Your API Secret'
URL = "https://paper-api.alpaca.markets"

api = REST(API, API_SECRET, URL)

ticker = 'SPY' #placeholder
ATR = 1.5
RR_ratio = 2
interval = 60

position = 0 #has bot entered a trade
buy_price = 0


def get_data(ticker):
    data = api.get_bars(ticker, 'day', limit=200)
    data = data[data['symbol'] == ticker]
    data['SMA50'] = data['close'].rolling(50).mean()
    data['SMA200'] = data['close'].rolling(200).mean()
    data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
    data['RSI'] = ta.momentum.rsi(data['close'], 14)
    data['ATR'] = ta.volatility.AverageTrueRange(
        high=data['high'], low=data['low'], close=data['close'], window=14
    ).average_true_range()
    return data

while True:
    try:
        data = get_data(ticker)
        latest = data.iloc[-1]
        account = api.get_account()
        cash = float(account.cash)

        # BUY
        if latest['EMA20'] > latest['SMA50'] and latest['SMA50'] > latest['SMA200'] and position == 0:
            shares = int(cash // latest['close'])
            if shares > 0:
                api.submit_order(symbol=ticker, qty=shares, side='buy', type='market', time_in_force='gtc')
                position = shares
                buy_price = latest['close']
                print(f"BUY {shares} shares at ${buy_price:.2f}")

        # SELL
        if position > 0:
            stop = buy_price - ATR * latest['ATR']
            take = buy_price + RR_ratio * (buy_price - stop)
            if latest['EMA20'] < latest['SMA50'] or latest['close'] <= stop or latest['close'] >= take:
                api.submit_order(symbol=ticker, qty=position, side='sell', type='market', time_in_force='gtc')
                print(f"SELL {position} shares at ${latest['close']:.2f}")
                position = 0
                buy_price = 0

    except Exception as e:
        print("Error:", e)

    time.sleep(interval)
