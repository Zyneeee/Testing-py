from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return '''<body style="margin: 0; padding: 0;">
    <iframe width="100%" height="100%" src="https://syntaxcoderz.vercel.app/" frameborder="0" allowfullscreen></iframe>
  </body>'''

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()
print("Server Running Because of Zcy.")
import discord
from discord import Intents
import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
intents = Intents.default()
intents.messages = True  # Enable the message intent

client = discord.Client(intents=intents)

async def fetch_pickup_line():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://vinuxd.vercel.app/api/pickup") as response:
                data = await response.json()
                return data.get("pickup")
    except Exception as e:
        print(f"An error occurred while fetching pickup line: {e}")
        return None

async def fetch_quote():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://zenquotes.io/api/random") as response:
                data = await response.json()
                if data and len(data) > 0:
                    quote_text = data[0]['q']
                    quote_author = data[0]['a']
                    return f"{quote_text} - {quote_author}"
                else:
                    return "Sorry, no quote found."
    except Exception as e:
        print(f"An error occurred while fetching quote: {e}")
        return "Sorry, I couldn't fetch a quote at the moment."

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You Having fun"))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'rizz' in message.content.lower():
        pickup_line = await fetch_pickup_line()
        if pickup_line:
            await message.channel.send(pickup_line)
        else:
            await message.channel.send("I'm sorry, I couldn't fetch a pickup line at the moment. Can you try again later?")

    if 'quote' in message.content.lower():
        quote = await fetch_quote()
        await message.channel.send(quote)

client.run(os.getenv('TOKEN'))
