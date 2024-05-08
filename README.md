# Discord NFT Bot

## Introduction
This Discord bot provides information about the latest sales on a specified collection on OpenSea. It listens for sale events in real-time and provides updates in the specified Discord channel. In this bot, the example collection slug used is NewBlastCity.


## Features
- Displays details of the latest sale including name, amount sold, timestamp, and OpenSea URL.
- Listens for real-time sale events and sends updates to the Discord channel.

## Setup

### 1. Set Up a Discord Bot
- You may follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to create and set up a Discord bot. Generate a bot token during this process.
- Enable Privileged Gateway Intents for the bot. Go to the "Bot" tab in the Discord Developer Portal, scroll down to the "Privileged Gateway Intents" section, and enable the intents required for your bot (`Presence Intent`, `Server Members Intent` and `Message Content Intent`).

### 2. Set Up Channel and Add the Bot
- Create a Discord channel where you want the bot to send updates.
- Add the bot to your Discord server using the bot's invite link or by following the instructions in the official Discord documentation.
- Obtain the channel ID where you want the bot to send updates. You can do this by right-clicking on the channel and selecting "Copy ID."

### 3. Install Requirements
- This program was run on Python 3.12
- Install the required dependencies using `pip install -r requirements.txt`.

### 4. Get OpenSea API Key
- Obtain an API key from OpenSea to access their API. You can get it by following the instructions on the [OpenSea website](https://docs.opensea.io/reference/api-keys).

### 5. Store API Key, Token, and Channel ID in a .env File
- Create a `.env` file in the project directory.
- Add the following variables to the `.env` file:
```plaintext
DISCORD_TOKEN=<Your Discord Bot Token>
API_KEY=<Your OpenSea API Key>
CHANNEL_ID=<Your Discord Channel ID>
```
Replace `<Your Discord Bot Token>`, `<Your OpenSea API Key>`, and `<Your Discord Channel ID>` with your actual values.

### 6. Run the Bot
- Run the bot using `python bot.py`.

## Usage
- Use the `!latest` command in any text channel to view the latest sale information for the specified collection slug.
- The bot automatically sends a message to the channel whenever there is a new sale for the specified collection.

## Dependencies
- discord.py: Python library for Discord bot development.
- requests: HTTP library for making API requests.
- websockets: Library for implementing WebSocket communication.

## License
This project is licensed under the [MIT License](LICENSE).
