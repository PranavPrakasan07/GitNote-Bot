import os
import discord
import requests
import json
from keep_alive import keep_alive
from replit import db

my_secret = os.environ['TOKEN']

client = discord.Client()



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if((str(message.author) == 'GitHub#0000')):

    s = ""

    for i in range(len(message.embeds)):
      s += str(message.embeds[i].title)

    await message.delete()

# await message.channel.send("Message :" + f"{message.author.mention}" + str((message.embeds)) + "Message : " + s) 

    await message.channel.send("Message : " + s) 

  if message.content.startswith('&hello'):            
    await message.channel.send('Hello!' +  f"{message.author.mention}")

  if message.content.startswith('&help'):      
    await message.delete()

    help_message = "&hello - Hello\n&help - Help\n"

    embed=discord.Embed(title="\n**Commands**\n\n",  description=help_message, color=0xFF5733)
    embed.set_author(name = "ISA-VIT", icon_url = "https://firebasestorage.googleapis.com/v0/b/isa-vit.appspot.com/o/icon.png?alt=media&token=c8fbffbb-ab51-4b49-a83b-8fb40626d8f8")
    
    await message.channel.send(embed=embed)

    # await message.channel.send("\n**Commands**\n\n>>> {}".format(help_message))


keep_alive()
client.run(my_secret)


