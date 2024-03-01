import discord
from requests import get
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You Having fun"))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'rizz' in message.content.lower():
        pickup_line = fetch_pickup_line()
        if pickup_line:
            await message.channel.send(pickup_line)
        else:
            await message.channel.send("I'm sorry, I couldn't fetch a pickup line at the moment. Can you try again later?")

    if 'quote' in message.content.lower():
        quote = fetch_quote()
        await message.channel.send(quote)

def fetch_pickup_line():
    try:
        pickup = get("https://vinuxd.vercel.app/api/pickup").json()["pickup"]
        return pickup
    except Exception as e:
        print(f"An error occurred while fetching pickup line: {e}")
        return None

def fetch_quote():
    try:
        response = get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                quote = data[0]['q'] + " - " + data[0]['a']
                return quote
            else:
                return "Sorry, no quote found."
        else:
            return f"Failed to fetch quote. Status code: {response.status_code}"
    except Exception as e:
        print(f"An error occurred while fetching quote: {e}")
        return "Sorry, I couldn't fetch a quote at the moment."

client.run(os.getenv('BOT_TOKEN'))
