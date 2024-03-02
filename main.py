import discord
from requests import get
from dotenv import load_dotenv
import os
from flask import Flask, render_template
from threading import Thread

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

@app.route('/')
def index():
    return '''<body style="margin: 0; padding: 0;">
    <iframe width="100%" height="100%" src="https://bot-status-phi.vercel.app/" frameborder="0" allowfullscreen></iframe>
  </body>'''

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()
print("Server Running Because of Zcy")

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

# Global flags to track whether a command is currently being processed
fetching_quote = False
fetching_pickup_line = False

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You Having fun"))
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global fetching_quote, fetching_pickup_line  # Declare global variables

    if message.author == client.user:
        return

    if 'rizz' in message.content.lower() and not fetching_pickup_line:
        fetching_pickup_line = True
        pickup_line = fetch_pickup_line()
        if pickup_line:
            await message.channel.send(pickup_line)
        else:
            await message.channel.send("I'm sorry, I couldn't fetch a pickup line at the moment. Can you try again later?")
        fetching_pickup_line = False

    if 'quote' in message.content.lower() and not fetching_quote:
        fetching_quote = True
        quote = fetch_quote()
        await message.channel.send(quote)
        fetching_quote = False

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
                quote_text = data[0]['q']
                quote_author = data[0]['a']
                return f"{quote_text} - {quote_author}"
            else:
                return "Sorry, no quote found."
        else:
            return f"Failed to fetch quote. Status code: {response.status_code}"
    except Exception as e:
        print(f"An error occurred while fetching quote: {e}")
        return "Sorry, I couldn't fetch a quote at the moment."

client.run(os.getenv('BOT_TOKEN'))
