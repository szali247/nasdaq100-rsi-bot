# nasdaq100-rsi-bot
Telegram bot that sends RSI and FVG-based stock alerts


# 📈 Nasdaq100 CFD Trading Signal Bot

A semi-automated Python trading bot that generates real-time intraday signals for **Nasdaq100 CFDs (CDT)** using **price action** strategies such as **Fair Value Gaps (FVGs)**.

## 🧠 Purpose

This project was built to:

- Improve trading discipline through systematic analysis
- Generate trade alerts based on clean price action (FVGs first, later OBs & Liquidity)
- Deliver real-time notifications via Telegram
- Serve as a learning and portfolio project demonstrating Python, APIs, and financial logic

---

## 🔧 Technologies Used

- **Python 3.10+**
- `tvdatafeed` – to fetch live 15m TradingView candle data
- `pandas` – for data manipulation
- `requests` – to send Telegram alerts
- **Telegram Bot API** – for real-time signal delivery
- `CSV` – for logging signals for review and journaling

---

##  Features

- ✅ **Live 15-minute candle data** pulled from TradingView (CDT symbol on CAPITALCOM)
- ✅ **Fair Value Gap detection logic** (bullish & bearish)
- ✅ **Telegram signal alerts** with timestamp and signal type
- ✅ **Duplicate-safe CSV logging** to store each unique signal
- 🔜 Modular code design for:
  - Order Block detection
  - Liquidity sweep detection
  - Risk-to-reward calculation
  - Chart plotting



