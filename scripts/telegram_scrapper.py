from telethon import TelegramClient
import os
import csv
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')  # Adjust the path to your .env file

# Replace these with your credentials
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')

# Set up Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Function to preprocess text
def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove non-Amharic/English characters and extra spaces
    text = re.sub(r'[^፩-፺ሀ-ፐa-zA-Z0-9\s.,!?]', '', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Function to scrape channel data
async def scrape_channel(client, channel_name, writer):
    print(f"Fetching data from {channel_name}...")
    async for message in client.iter_messages(channel_name, limit=500):  # Set limit to 500
        if message.text:
            clean_text = preprocess_text(message.text)
            writer.writerow([channel_name, message.id, clean_text, message.date])
    print(f"Finished scraping {channel_name}")

# Main function to fetch data from all channels and save to a single CSV file
async def main():
    # Open the CSV file and prepare the writer
    with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Message ID', 'Message Text', 'Date'])  # Updated header

        # List of channels to scrape
        channels = [
       # Existing channel
        "@ZemenExpress",
        "@nevacomputer",
        "@meneshayeofficial",
        "@Leyueqa",
        "@ethio_brand_collection",
            # Add more channels here
        ]

        # Iterate over channels and scrape data into the single CSV file
        for channel in channels:
            await scrape_channel(client, channel, writer)
            print(f"Scraped data from {channel}")

# Run the client
with client:
    client.loop.run_until_complete(main())
