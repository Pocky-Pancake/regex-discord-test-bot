import nextcord, os, re
from dotenv import load_dotenv

load_dotenv()

test_channel_id = os.getenv('TARGET')

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)

@client.event
async def on_ready():
    print("bot ready")

@client.event
async def on_message(message):
    if message.channel.id == test_channel_id:
        pass