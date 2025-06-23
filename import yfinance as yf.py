import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
import datetime

# --- Settings ---
ticker = "^NDX"  # Nasdaq100 Index (QQQ = ETF alternative)
period = "60d"
interval = "30m"

# --- Fetch data ---
print("Downloading data...")
df = yf.download(ticker, period=period, interval=interval)

# --- Clean data ---
df.dropna(inplace=True)

# --- Calculate RSI ---
rsi_period = 14
rsi = RSIIndicator(close=df["Close"], window=rsi_period)
df["RSI"] = rsi.rsi()

# --- Signal Logic ---
df["Signal"] = None
df.loc[df["RSI"] < 30, "Signal"] = "BUY"
df.loc[df["RSI"] > 70, "Signal"] = "SELL"

# --- Show latest ---
latest = df.tail(5)[["Close", "RSI", "Signal"]]
print("\nRecent Signals:\n")
print(latest)
