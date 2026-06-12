# Alpaca Paper Trading Bot

This project is a simple algorithmic trading bot built with Python and the Alpaca paper trading API.

The bot retrieves market data for a selected ticker, calculates technical indicators, and places paper trades based on a moving average trend-following strategy. It also includes basic stop-loss and take-profit logic using the Average True Range (ATR).

## Project Overview

The aim of this project is to demonstrate how a basic automated trading strategy can be implemented using Python.

The bot uses technical indicators to identify potential trend-following trade entries. It buys when short-term momentum appears stronger than the longer-term trend, and exits when the trend weakens or when predefined risk-management levels are reached.

This project is designed for educational paper trading only and should not be treated as a production trading system.

## Strategy Logic

The bot currently trades a placeholder ticker:

* `SPY`

The entry condition is based on three moving averages:

* 20-day Exponential Moving Average
* 50-day Simple Moving Average
* 200-day Simple Moving Average

The bot enters a long position when:

* EMA20 is above SMA50
* SMA50 is above SMA200
* the bot is not already in a position

This represents a simple bullish trend-following signal.

## Exit Logic

Once the bot is in a position, it exits if one of the following conditions is met:

* EMA20 falls below SMA50
* the price reaches the ATR-based stop-loss
* the price reaches the take-profit level

The stop-loss is calculated using:

$$
\text{Stop Loss} = \text{Buy Price} - 1.5 \times ATR
$$

The take-profit level is calculated using a risk-reward ratio of 2:

$$
\text{Take Profit} = \text{Buy Price} + 2 \times (\text{Buy Price} - \text{Stop Loss})
$$

## Technical Indicators Used

### Simple Moving Average

The bot calculates:

* 50-day SMA
* 200-day SMA

The SMA is used to identify the broader direction of the trend.

### Exponential Moving Average

The bot calculates:

* 20-day EMA

The EMA gives more weight to recent prices and is used to detect shorter-term momentum.

### Relative Strength Index

The bot calculates the 14-period RSI.

In the current version, RSI is calculated but not yet used in the trade entry or exit rules. It could be added later as a momentum or overbought/oversold filter.

### Average True Range

The bot calculates the 14-period ATR.

ATR is used to create a volatility-adjusted stop-loss, meaning the stop level adapts to recent market volatility.

## What the Code Does

The script:

* Connects to the Alpaca paper trading API
* Retrieves daily market data for the selected ticker
* Calculates SMA50, SMA200, EMA20, RSI, and ATR
* Checks the latest market data
* Buys if the trend-following conditions are met
* Sells if the exit conditions are met
* Repeats the process at a fixed time interval

## Technologies Used

* Python
* Pandas
* Alpaca Trade API
* pandas-ta
* time

## Example Parameters

The current script uses:

* Ticker: `SPY`
* ATR multiplier: `1.5`
* Risk-reward ratio: `2`
* Check interval: `60` seconds
* Data timeframe: daily bars
* Data limit: 200 bars

## Installation

Install the required Python packages:

```bash
pip install pandas alpaca-trade-api pandas-ta
```

## Alpaca Setup

This project requires an Alpaca paper trading account.

You will need:

* Alpaca API key
* Alpaca API secret key
* Alpaca paper trading endpoint

In the script, replace:

```python
API = 'Your API Key'
API_SECRET = 'Your API Secret'
```

with your own Alpaca paper trading credentials.

The script uses the Alpaca paper trading URL:

```python
URL = "https://paper-api.alpaca.markets"
```

## How to Run

Run the script with:

```bash
python trading_bot.py
```

The bot will continue running in a loop and will check the strategy conditions every 60 seconds.

## Example Trade Logic

If the latest data shows:

* EMA20 > SMA50
* SMA50 > SMA200
* no current position is open

then the bot calculates how many shares can be bought using the available account cash and submits a market buy order.

If a position is open, the bot calculates the ATR-based stop-loss and take-profit levels. It then submits a market sell order if the exit conditions are met.

## Risk Management

The strategy uses two simple forms of risk management:

1. Trend-based exit
   The bot exits if EMA20 falls below SMA50.

2. ATR-based stop-loss and take-profit
   The bot uses ATR to create a volatility-adjusted stop-loss and a take-profit target based on a 2:1 reward-to-risk ratio.

## Limitations

This is a simplified educational trading bot and should not be used with real money without significant improvements, testing, and risk controls.

Important limitations include:

* Uses a simple moving average crossover strategy
* Uses daily data but checks the strategy every 60 seconds
* Does not currently verify whether orders were fully filled
* Does not persist position state if the script restarts
* Does not handle partial fills
* Does not include slippage or transaction cost modelling
* Does not include backtesting
* Does not include robust error handling
* Does not account for market hours
* Does not use portfolio-level risk management
* RSI is calculated but not currently used in the strategy rules

## Possible Improvements

Future extensions could include:

* Adding a full backtesting framework
* Saving trade history to a CSV file
* Adding position state persistence
* Checking whether the market is open before placing orders
* Adding RSI as a filter
* Adding maximum risk per trade
* Adding fractional share support
* Adding logging instead of print statements
* Testing the strategy across multiple tickers
* Adding a dashboard to monitor trades
* Comparing performance against a buy-and-hold benchmark
* Adding email or Discord trade alerts

## Purpose

This project was created as a beginner algorithmic trading project to practise:

* using financial APIs
* retrieving market data
* calculating technical indicators
* building rule-based trading strategies
* implementing basic risk management
* working with Python trading libraries
* understanding the structure of an automated paper trading bot

## Disclaimer

This project is for educational and paper trading purposes only. It is not financial advice and should not be used as a live trading system without proper testing, validation, and risk management.
