import os
import discord
from keep_alive import keep_alive
from replit import db
import datetime

my_secret = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if(message.content.startswith('&create')):
    repo_name = message.content[8:]

    if(repo_name not in list(db.keys())):
      now = datetime.datetime.now()
      cdate = now.strftime("%Y-%m-%d %H:%M:%S")
      db[repo_name] = dict({ cdate : ['created']})

      await message.channel.send("Your repository has been successfully added! Check out other commands to get updates regarding project status!")

    else:
      await message.channel.send("Your repository has **already** been added! Check out other commands to get updates regarding project status!")

  if message.content.startswith('&list_repo'):
    keys = db.keys()

    list_of_repos = ''

    if len(keys) == 0:
      await message.channel.send("No Repositories added yet!")
    else:
      for key in keys:
        list_of_repos += key + '\n\n'
      
      await message.channel.send("\n\n**Repositories**" + "\n >>> " + list_of_repos)


  if((str(message.author) == 'GitHub#0000')):

    title = desc = ""

    for i in range(len(message.embeds)):      
      title = str(message.embeds[i].title)
      desc = str(message.embeds[i].description)

      content_list = [title]

      if(desc != "Embed.Empty"):
        content_list.append(desc)

      now = datetime.datetime.now()
      cdate = now.strftime("%Y-%m-%d %H:%M:%S")

      details = dict({cdate : content_list})
      keys = db.keys()

      if(len(keys) > 0):

        for key in keys:
          if(key in title):
            db[key] = details

    # await message.delete()

      await message.channel.send("Title : " + title + "\n\nDescription : "+ desc) 

  if message.content.startswith('&hello'):            
    await message.channel.send('Hello!' +  f"{message.author.mention}")

  if message.content.startswith('&help'):      
    await message.delete()

    help_message = "\n&hello\n - Hello\n```&hello```\n\n" + "&help\n - Check commands\n```&help```\n\n"

    embed=discord.Embed(title="\n**Commands**\n\n",  description=help_message, color=0xFF5733)
    embed.set_author(name = "GitNote", icon_url = "https://firebasestorage.googleapis.com/v0/b/eye-testing-interface.appspot.com/o/icon.png?alt=media&token=39e1ac07-af1c-4d94-914a-031a6489efc0")
    
    await message.channel.send(embed=embed)

    # await message.channel.send("\n**Commands**\n\n>>> {}".format(help_message))

keep_alive()
client.run(my_secret)


