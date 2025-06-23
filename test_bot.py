import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables from .env file
load_dotenv('bottoken.env')  # change if your env file name differs

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID is not set in environment variables.")

async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Hello! Your Telegram bot is working correctly.")

if __name__ == "__main__":
    asyncio.run(main())
