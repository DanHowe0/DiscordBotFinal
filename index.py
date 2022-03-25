#database manipulation
import json

# Import discord modules for the bot
import discord
from discord.ext import commands

#load the dotenv library for .env files
from dotenv import load_dotenv

#Other imports
import os

#set up intents for the client
intents = discord.Intents().all()

#Get the prefix for the server
def get_prefix(client, ctx):
  return "="

# Initialise the bot client
client = commands.Bot(
  command_prefix = get_prefix,
  intents = intents
)

#set up access permissions for the client
client.developers = [
  428369959501168650 # DanHowe0
]

client.testers = []

# load all the cogs from the assets folder
for i in os.listdir("./assets"):
  if i.endswith(".py"):
    client.load_extension(f"assets.{i[:-3]}")


# load all the cogs from the listeners folder
for i in os.listdir("./listeners"):
  if i.endswith(".py"):
    client.load_extension(f"listeners.{i[:-3]}")
    
#load the bot token from environment variables
load_dotenv()
token = os.getenv("TOKEN")

#run the client
client.run(token)