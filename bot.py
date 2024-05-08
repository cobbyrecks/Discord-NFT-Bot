import discord
import json
import requests
import os
import websockets

from datetime import datetime, timezone
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Specify the collection slug you want sales information on
# I used newblastcity in this bot
collection_slug = "newblastcity"


def get_latest_sale_info():
    url = f"https://api.opensea.io/api/v2/events/collection/{collection_slug}"

    params = {
        "event_type": "sale",
        "limit": 1  # latest sale
    }

    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Extract latest sale event
    latest_sale_event = next((event for event in data.get("asset_events", []) if event["event_type"] == "sale"), None)

    if not latest_sale_event:
        return None

    latest_sale_timestamp = latest_sale_event["closing_date"]
    # Convert quantity to ETH
    latest_sale_amount = float(latest_sale_event["payment"]["quantity"]) / (10 ** latest_sale_event["payment"]["decimals"])
    latest_sale_image_url = latest_sale_event["nft"]["image_url"]
    latest_sale_opensea_url = latest_sale_event["nft"]["opensea_url"]
    latest_sale_name = latest_sale_event["nft"]["name"]

    # Convert timestamp to datetime
    latest_sale_datetime = datetime.fromtimestamp(latest_sale_timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    return {
        "name": latest_sale_name,
        "amount": latest_sale_amount,
        "timestamp": latest_sale_datetime,
        "image_url": latest_sale_image_url,
        "opensea_url": latest_sale_opensea_url
    }


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    await subscribe_to_collection()


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome!\n"
        f"I will serve you with the latest {collection_slug} collection sales info"
    )


@bot.command(name="latest", help=f"Displays the latest {collection_slug} collection latest sale")
async def show_latest_collection_sale(ctx):
    data = get_latest_sale_info()
    if data:
        await ctx.send(
            f"Latest Sale!\n\n"
            f"Name: {data['name']}\n"
            f"Amount sold: {data['amount']} ETH\n"
            f"Timestamp: {data['timestamp']}\n"
            # f"Image URL: {data['image_url']}\n"
            f"OpenSea URL: {data['opensea_url']}\n"
        )
    else:
        await ctx.send("No sale data found for the specified collection.")


async def subscribe_to_collection():
    uri = f"wss://stream.openseabeta.com/socket/websocket?token={API_KEY}"

    while True:  # # Infinite loop to keep listening for messages
        async with websockets.connect(uri) as websocket:
            channel = bot.get_channel(CHANNEL_ID)
            # Sending heartbeat message
            heartbeat_message = {
                "topic": "phoenix",
                "event": "heartbeat",
                "payload": {},
                "ref": 0
            }
            await websocket.send(json.dumps(heartbeat_message))

            # Subscribing to the collection
            subscribe_message = {
                "topic": f"collection:{collection_slug}",
                "event": "phx_join",
                "payload": {},
                "ref": 1  # Use any appropriate reference number
            }
            await websocket.send(json.dumps(subscribe_message))

            # Listen for sale messages
            async for message in websocket:
                parsed_message = json.loads(message)
                if parsed_message["event"] == "item_sold" or parsed_message["event"] == "item_transferred":
                    await channel.send(f"Latest Updates!:\n\n{parsed_message}")


bot.run(TOKEN)
