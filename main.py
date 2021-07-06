import os
import discord
from keep_alive import keep_alive
from replit import db
import datetime

my_secret = os.environ['TOKEN']

client = discord.Client()

commands = ['help', 'open', 'create', 'list', 'hello', 'view', 'see', 'delete']

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

      d =  { cdate : ['Repository Created!']}
      db[repo_name] = d

      await message.channel.send("Your repository has been successfully added! Check out other commands to get updates regarding project status!")

    else:
      await message.channel.send("Your repository has **already** been added! Check out other commands to get updates regarding project status!")

  if message.content.startswith('&list'):
    keys = list(db.keys())

    list_of_repos = ''

    if len(keys) == 0:
      await message.channel.send("No Repositories added yet!")
    else:
      i = 1
      for key in keys:
        list_of_repos += str(i) + ". " + key + '\n\n'
        i+=1
      
      await message.channel.send("\n\n**Repositories**" + "\n >>> " + list_of_repos)

  if message.content.startswith('&view'):
    keys = list(db.keys())

    repo_name = message.content[6:]

    if repo_name not in list(db.keys()):
      await message.channel.send("Not found!")
    else:        
      d = db[repo_name]
      # d - {date_time string : [title, description]}

      keys = d.keys()
      # values = d.values()

      details = ''

      for date_time in keys:
        details += str(date_time) + " (UTC) \n" 
        
        i = 0
        for mess in d[date_time]:
          if i == 0:
            details +=  '```\n' + str(mess) + '\n```'
          else:
            details +=  '\n' + str(mess) + '\n'
          i +=1

        details += "\n\n"
      
      await message.channel.send("\n\n**" + repo_name + "**\n >>> " + details)


  if((str(message.author) == 'GitHub#0000')):

    title = desc = ""

    for i in range(len(message.embeds)):      
      title = str(message.embeds[i].title)
      desc = str(message.embeds[i].description)

      content_list = []
      content_list.append(title)

      if(desc != "Embed.Empty"):
        content_list.append(desc)

      now = datetime.datetime.now()
      cdate = now.strftime("%Y-%m-%d %H:%M:%S")

      details_old = dict()

      keys = list(db.keys())

      if(len(keys) > 0):

        for key in keys:
          if(key in title):
            details_old = db[key]
            details_old[cdate] = content_list
            db[key] = details_old

    # await message.delete()

      await message.channel.send("Title : " + title + "\n\nDescription : "+ desc) 

  if message.content.startswith('&'): 
    keyword = message.content.partition(' ')[0]

    if(keyword[1:] not in commands):
      await message.channel.send(keyword + ' is not a valid command! Check &help, to view commands')

  if message.content.startswith('&hello'):            
    await message.channel.send('Hello!' +  f"{message.author.mention}")

  if message.content.startswith('&help'):      
    await message.delete()

    help_message = "\n&hello\n - Hello\n```&hello```\n\n" + "&help\n - Check commands\n```&help```\n\n"  + "&create\n - Add repository to the list\n```&create <repo-name>```\n\n"  + "&list\n - To list all added repositories\n```&list```\n\n"  + "&view\n - To view the proceedings of the project\n```&view <repo-name>```\n\n"

    embed=discord.Embed(title="\n**Commands**\n\n",  description=help_message, color=0xFF5733)
    embed.set_author(name = "GitNote", icon_url = "https://firebasestorage.googleapis.com/v0/b/eye-testing-interface.appspot.com/o/icon.png?alt=media&token=39e1ac07-af1c-4d94-914a-031a6489efc0")
    
    await message.channel.send(embed=embed)

    # await message.channel.send("\n**Commands**\n\n>>> {}".format(help_message))

  if message.content.startswith('&delete'):
    del db[message.content[8:]]

    await message.channel.send(message.content[8:] + ' deleted!')

  if message.content.startswith('&see'):

    for key in db.keys():
      await message.channel.send(str(key) + " : " + str(db[key]) + "\n\n")



keep_alive()
client.run(my_secret)


