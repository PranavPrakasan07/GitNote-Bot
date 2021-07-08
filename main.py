import os
import discord
from keep_alive import keep_alive
from replit import db
import datetime
import smtplib
import random

my_secret = os.environ['TOKEN']

client = discord.Client()

greetings = [
  ['Bonjour ', 'French'],
  ['Zdravstvuyte ', 'Russian'],
  ['Nǐn hǎo ', 'Chinese'],
  ['Hi ', 'English'],
  ['Salve ', 'Italian'],
  ['Konnichiwa ', 'Japanese'],
  ['Guten Tag ', 'German'],
  ['Goedendag ', 'Dutch'],
  ['Namaste ', 'Hindi'],
  ['God dag ', 'Swedish/Norwegian']
]

commands = [
    'help', 
    'open', 
    'create', 
    'list', 
    'hello', 
    'view_d', 
    'view_s', 
    'delete',
    'dm_report_s', 
    'dm_report_d',
]

def detail_report(repo_name):
  keys = list(db.keys())

  if repo_name not in list(db.keys()):
    return 'Repository **not** found!'
  else:
      d = db[repo_name]
      # d - {date_time string : [title, description]}

      keys = d.keys()
      # values = d.values()

      details = ''

      for date_time in keys:
          details += '\n' + str(date_time) + " (UTC) \n"

          i = 0
          for mess in d[date_time]:
              if i == 0:
                  details += '```\n' + str(mess) + '\n```'
              else:
                  details += '\n' + str(mess) + '\n'
              i += 1
          
          details += '\n\n'

          if (len(details) > 1000):
            mess = "\n\n**" + repo_name + "**\n >>> " + details
            details = ''
            return mess

      #details += "\n**__Important__**\n\n"

      return("\n\n**" + repo_name + "**\n >>> " + details)

def short_report(repo_name):
  keys = list(db.keys())

  if repo_name not in list(db.keys()):
    return 'Repository **not** found!'
  else:
    d = db[repo_name]
    # d - {date_time string : [title, description]}

    keys = d.keys()
    # values = d.values()

    details = ''

    for date_time in keys:
        details += str(date_time) + " (UTC) \n"
        details += '```\n' + str(d[date_time][0])

        if (len(d[date_time]) > 1):
            details += ', ' + str(d[date_time][1].rpartition(') ')[-1])

        details += '\n```\n\n'

        if (len(details) > 1000):
          mess = "\n\n**" + repo_name + "**\n >>> " + details
          details = ''
          return mess

    return "\n\n**" + repo_name + "**\n >>> " + details

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (message.content.startswith('&create')):
        repo_name = message.content[8:]

        if (repo_name not in list(db.keys())):
            now = datetime.datetime.now()
            cdate = now.strftime("%Y-%m-%d %H:%M:%S")

            d = {cdate: ['Repository Created!']}
            db[repo_name] = d

            await message.channel.send(
                "Your repository has been successfully added! Check out other commands to get updates regarding project status!"
            )

        else:
            await message.channel.send(
                "Your repository has **already** been added! Check out other commands to get updates regarding project status!"
            )

    if message.content.startswith('&list'):
        keys = list(db.keys())

        list_of_repos = ''

        if len(keys) == 0:
            await message.channel.send("No Repositories added yet!")
        else:
            i = 1
            for key in keys:
              list_of_repos += str(i) + ". " + key + '\n\n'
              i += 1

              if(len(list_of_repos)> 1000):
                mess = "\n\n**Repositories**" + "\n >>> " + list_of_repos
                list_of_repos  = ''
                await message.channel.send(mess)

            await message.channel.send("\n\n**Repositories**" + "\n >>> " + list_of_repos)

    if message.content.startswith('&view_d'):
      repo_name = message.content[8:]
      response = detail_report(repo_name)

      await message.channel.send(response)

    if ((str(message.author) == 'GitHub#0000')):

        title = desc = ""

        for i in range(len(message.embeds)):
            title = str(message.embeds[i].title)
            desc = str(message.embeds[i].description)

            content_list = []
            content_list.append(title)

            if (desc != "Embed.Empty"):
                content_list.append(desc)

            now = datetime.datetime.now()
            cdate = now.strftime("%Y-%m-%d %H:%M:%S")

            details_old = dict()

            keys = list(db.keys())

            if (len(keys) > 0):

                for key in keys:
                    if (key in title):
                        details_old = db[key]
                        details_old[cdate] = content_list
                        db[key] = details_old

            await message.delete()

            # await message.channel.send("Title : " + title + "\n\nDescription : "+ desc)

    if message.content.startswith('&'):
        keyword = message.content.partition(' ')[0]

        if (keyword[1:] not in commands):
            await message.channel.send(
                keyword +
                ' is not a valid command! Check `&help`, to view commands')

    if message.content.startswith('&hello'):

      await message.delete()
      r = random.randint(0,9)
      await message.channel.send(greetings[r][0] + f"{message.author.mention}!" + '        || ~ ' + greetings[r][1] + ' ||')

    if message.content.startswith('&help'):
        await message.delete()

        help_message = "\n\n&hello - Hello\n```&hello```\n\n" + "&help - Check commands\n```&help```\n\n" + "&create - Add repository to the list\n```&create <repo-name>```\n\n" + "&list - To list all added repositories\n```&list```\n\n" + "&view_s - To view the proceedings of the project in short\n```&view_s <repo-name>```\n\n" + "&view_d - To view the proceedings of the project in detail\n```&view_d <repo-name>```\n\n"+ "&dm_report_s - To get the proceedings of the project as a private message in short\n```&dm_report_s <repo-name>```\n\n"+ "&dm_report_d - To get the proceedings of the project as a private message in detail\n```&dm_report_d <repo-name>```\n\n"+ "&delete - To delete the stored repository details\n```&delete <repo-name>```\n\n"

        embed = discord.Embed(title="\n**__Commands__**",
                              description=help_message,
                              color=0xFF5733)
        embed.set_author(
            name="GitNote",
            icon_url=
            "https://firebasestorage.googleapis.com/v0/b/eye-testing-interface.appspot.com/o/icon.png?alt=media&token=39e1ac07-af1c-4d94-914a-031a6489efc0"
        )

        await message.channel.send(embed=embed)

        # await message.channel.send("\n**Commands**\n\n>>> {}".format(help_message))

    if message.content.startswith('&delete'):

      if message.content[8:] in db:
        del db[message.content[8:]]

        await message.channel.send(message.content[8:] + ' details deleted!')
        
      else:
        await message.channel.send(message.content[8:] + ' not found!')

    if message.content.startswith('&view_s'):
      repo_name = message.content[8:]
      response = short_report(repo_name)
      await message.channel.send(response)

    if message.content.startswith('&dm_report_s'):
      repo_name = message.content[13:]
      member = message.author

      await message.delete()
      await member.send(short_report(repo_name))

    if message.content.startswith('&dm_report_d'):
      repo_name = message.content[13:]
      member = message.author

      await message.delete()
      await member.send(detail_report(repo_name))
    
    if message.content.startswith('&set_timer'):
      repo_name = message.content[11:]
      member = message.author

      await message.delete()
      await member.send(detail_report(repo_name))  

    if message.content.startswith('&send_mail'):

      username, password, receiver, repo_name = message.content[11:].split(' ')

      # creates SMTP session
      s = smtplib.SMTP('smtp.gmail.com', 587)

      # start TLS for security
      s.starttls()

      # Authentication
      # s.login("sender_email_id", "sender_email_id_password")
      s.login(username, password)

      # message to be sent
      message = detail_report(repo_name)

      # sending the mail
      # s.sendmail("sender_email_id", "receiver_email_id", message)
      s.sendmail(username, receiver, message)

      # terminating the session
      s.quit()


keep_alive()
client.run(my_secret)