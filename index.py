#database manipulation
import json

# Import discord modules for the bot
import discord
from discord.ext import commands

#load the dotenv library for .env files
from dotenv import load_dotenv

#Other imports
import os


# put data into variables
server_info = json.load(open("db/server_data.json", "r"))
welcome_info = json.load(open("db/welcome_data.json", "r"))
error_log = json.load(open("db/error_log.json", "r"))
global_locks = json.load(open("db/global_locks.json", "r"))

#set up intents for the client
intents = discord.Intents().all()

#Get the prefix for the server
def get_prefix(client, ctx):
  with open("db/server_data.json", "r") as f:
    return json.load(f)[str(ctx.guild.id)]["prefix"]

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

#set the variables into the client, for access in cogs
client.server_info = server_info
client.welcome_info = welcome_info
client.global_locks = global_locks
client.error_log = error_log
  
# create a log function for each server
async def errlog(ctx, e, dest):
  
  id = client.error_log["count"]
  client.error_log["count"] += 1
  client.error_log.update({id: {"guildID": ctx.guild.id, "error": str(e), "from": dest}})
  
  with open("db/error_log.json", "w") as f:
    json.dump(client.error_log, f, indent=2)
    
  if client.server_info[str(ctx.guild.id)]["logchannel"] != None:
    
    channel = client.get_channel(client.server_info[str(ctx.guild.id)]["logchannel"])
    
    await channel.send("There was an error with the following ID: `" + str(id) + "`\nWe have details of this error, and will look to find a fix shortly.")
    
client.errlog = errlog

# on ready function for if the client gets reset

# Scan all messages (moderation etc)
@client.event
async def on_message(ctx):
  pass

  # do moderation here



  #-------------------
  await client.process_commands(ctx)

# Send a message when the user leaves
@client.event
async def on_member_remove(ctx):
  if client.welcome_info[str(ctx.guild.id)]["enabled"]:
    try:
      sysChan = ctx.guild.system_channel
      lchannel = client.welcome_info[str(ctx.guild.id)]["Lchannel"]
      
      channel = sysChan if lchannel == None else client.get_channel(lchannel)

      default =  ctx.name + " left. Goodbye!"
      lmessage = client.welcome_info[str(ctx.guild.id)]["Lmessage"]

      msg = default if lmessage == None else fix(lmessage, ctx)
      await channel.send(msg)
    except Exception as e:
      await client.errlog(ctx, e, "on_member_remove")

#function to put all the variables correctly into messages
def fix(msg, ctx):
  new = []
  for i in msg.split(" "):
    if i == "{user}":
      new.append(ctx.name+ctx.discriminator)
    elif i == "{guild.name}":
      new.append(ctx.guild.name)
    else:
      new.append(i)

  return " ".join(new)

client.fix = fix

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