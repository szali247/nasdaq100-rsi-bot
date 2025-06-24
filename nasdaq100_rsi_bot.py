import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio
import time
import logging
import os

# Set up logging
LOG_FILE = "/tmp/nasdaq_bot.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load token and chat ID
load_dotenv('bottoken.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

print("BOT_TOKEN:", BOT_TOKEN)
print("CHAT_ID:", CHAT_ID)

bot = Bot(token=BOT_TOKEN)

def fetch_data():
    df = yf.download("NQ=F", period="5d", interval="15m")
    df.dropna(inplace=True)
    return df

def calculate_rsi(df, window=14):
    rsi = RSIIndicator(close=df["Close"].squeeze(), window=window)
    df["RSI"] = rsi.rsi()
    return df

def detect_fvg(df):
    signals = []
    for i in range(1, len(df)):
        curr_low = df["Low"].iloc[i].item()
        prev_high = df["High"].iloc[i - 1].item()
        curr_high = df["High"].iloc[i].item()
        prev_low = df["Low"].iloc[i - 1].item()

        if curr_low > prev_high:
            signals.append("Buy FVG")
        elif curr_high < prev_low:
            signals.append("Sell FVG")
        else:
            signals.append(None)
    signals.insert(0, None)
    df["FVG_Signal"] = signals
    return df

def detect_order_blocks(df):
    df["Order_Block"] = None
    for i in range(2, len(df)):
        c0 = df["Close"].iloc[i].item()
        o0 = df["Open"].iloc[i].item()
        c1 = df["Close"].iloc[i - 1].item()
        o1 = df["Open"].iloc[i - 1].item()

        if c0 > o0 and c1 < o1:
            df.at[df.index[i], "Order_Block"] = "Bullish OB"
        elif c0 < o0 and c1 > o1:
            df.at[df.index[i], "Order_Block"] = "Bearish OB"
    return df

def find_strong_signals(df):
    import pandas as pd

    recent = df.iloc[-1]

    rsi_val = float(recent["RSI"].iloc[0])  # <-- updated here

    fvg_val = recent["FVG_Signal"]
    if hasattr(fvg_val, 'item'):
        try:
            fvg = fvg_val.item()
        except:
            fvg = str(fvg_val)
    else:
        fvg = str(fvg_val)

    ob_val = recent["Order_Block"]
    if hasattr(ob_val, 'item'):
        try:
            ob = ob_val.item()
        except:
            ob = str(ob_val)
    else:
        ob = str(ob_val)

    if pd.isna(fvg) or fvg == 'nan':
        fvg = None
    if pd.isna(ob) or ob == 'nan':
        ob = None

    signals = []

    if rsi_val < 30 and fvg == "Buy FVG" and ob == "Bullish OB":
        signals.append("🟢 STRONG BUY SIGNAL (RSI < 30, Buy FVG, Bullish OB)")
    elif rsi_val > 70 and fvg == "Sell FVG" and ob == "Bearish OB":
        signals.append("🔴 STRONG SELL SIGNAL (RSI > 70, Sell FVG, Bearish OB)")

    if not signals:
        if rsi_val < 30:
            signals.append("🟢 RSI below 30: Possible buy opportunity")
        elif rsi_val > 70:
            signals.append("🔴 RSI above 70: Possible sell opportunity")

        if fvg is not None:
            signals.append(f"📉 Fair Value Gap detected: {fvg}")
        if ob is not None:
            signals.append(f"📦 Order Block detected: {ob}")

    return signals



async def send_telegram_alert(messages):
    if messages:
        text = "\n".join(messages)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=f"📊 Nasdaq100 Bot Alert:\n{text}")
            print("✅ Alert sent.")
        except Exception as e:
            print("❌ Failed to send alert:", e)
    else:
        print("No messages to send.")


def main():
    df = fetch_data()
    df = calculate_rsi(df)
    df = detect_fvg(df)
    df = detect_order_blocks(df)
    
    signals = find_strong_signals(df)
    print("Signals found:", signals)  # Add this debug line
    
    if signals:
        asyncio.run(send_telegram_alert(signals))
    else:
        print("No strong signals found, no alert sent.")


if __name__ == "__main__":
    import threading
    import time
    from http.server import BaseHTTPRequestHandler, HTTPServer

    # Background dummy server for Render's health checks
    def keep_alive():
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
        server = HTTPServer(("0.0.0.0", 8000), Handler)
        server.serve_forever()

    # Start dummy server in background
    threading.Thread(target=keep_alive, daemon=True).start()

    # Main trading bot loop
     while True:
        logging.info("⏳ Running Nasdaq100 Bot cycle...")
        try:
            main()
            logging.info("✅ Bot cycle completed successfully.")
        except Exception as e:
            logging.error(f"❌ Error occurred: {e}")
        logging.info("🔁 Waiting 15 minutes for next run...\n")
        time.sleep(900)
