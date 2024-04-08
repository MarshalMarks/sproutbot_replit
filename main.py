import discord
import os
import random
from datetime import datetime
from replit import db

token = os.environ['TOKEN']

# Initialize Discord
intents = discord.Intents.default()
intents.message_content = True  # Add this line to include message content
client = discord.Client(intents=intents)

help_message = "**Commands:**\n"
help_message += "**$sprout ping** - sends a message if the bot is online\n"
help_message += "**$sprout help** - displays this help message\n"
help_message += "**$sprout add <prompt>** - adds a new prompt to the prompt list\n"
help_message += "**$sprout list** - displays the prompt list\n"
help_message += "**$sprout delete <index>** - deletes a prompt from the prompt list\n"
help_message += "**$sprout announce** - announces this week's prompt\n"

pingMessages = []
pingMessages.append('I\'m up and running!')
pingMessages.append('Hello! Hope you\'re doing well.')
pingMessages.append('Sproutbot is online!')
pingMessages.append('My name is Sproutbot. Nice to meet you!')


def get_announcement():
  output = "Today will start the next prompt! "
  output += "It'll take place from today until next {0}. ".format(
      datetime.now().strftime('%A'))
  output += "The prompt for this one is **\"{0}\"**!".format(db["prompts"][0])
  del db["prompts"][0]
  return output


@client.event
async def on_ready():
  # Initialize database if not present
  if "prompts" not in db:
    db["prompts"] = []
  print(db["prompts"])

  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if not message.content.startswith('$sprout'):
    return

  arguments = message.content.split(' ')

  if len(arguments) < 2:
    await message.channel.send(
        'Omg haiii :3 (if you want help, type $sprout help)')
    return

  if message.content.startswith('$sprout ping'):
    await message.channel.send(pingMessages[random.randint(
        0,
        len(pingMessages) - 1)])
    print(message.content)
    return

  if message.content.startswith('$sprout help'):
    await message.channel.send(help_message)
    print(message.content)
    return

  if message.content.startswith('$sprout announce'):
    if (len(db["prompts"]) == 0):
      await message.channel.send("No prompts in the list rn! x~x")
      return
    await message.channel.send(get_announcement())

  if message.content.startswith('$sprout add'):
    if len(arguments) == 2:
      await message.channel.send(
          'You didn\'t give me a prompt to add :(\n**Format:** $sprout add <prompt>'
      )
      return
    prompt = ' '.join(arguments[2:])
    db["prompts"].append(prompt)
    await message.channel.send(
        'Added \"{0}\" to the database! :D'.format(prompt))

  if message.content.startswith('$sprout list'):
    if len(db["prompts"]) == 0:
      await message.channel.send(
          'The prompt list is empty :( use $sprout add <prompt> to add a prompt!'
      )
      return
    output = "**Prompt List:**\n"
    for i, prompt in enumerate(db["prompts"]):
      output += f"{i+1}: {prompt}\n"
    await message.channel.send(output)
    return

  if message.content.startswith('$sprout delete'):
    if len(arguments) < 3:
      await message.channel.send(
          'You didn\'t give me an index to delete :( please use $sprout delete <index>'
      )
      return
    elif len(arguments) > 3:
      await message.channel.send(
          'Waaauw, so many arguments! x~x I just need one number')
      return

    try:
      index = int(arguments[2]) - 1
    except ValueError:
      await message.channel.send(
          'The index has to be a number! x~x Please use $sprout delete <index>'
      )
      return

    if len(db["prompts"]) == 0:
      await message.channel.send(
          'There are no prompts to delete! You can add one with $sprout add <prompt>'
      )
      return
    elif index < 0 or index >= len(db["prompts"]):
      await message.channel.send(
          'That index is out of bounds! Needs to be between 1 and {0}'.format(
              len(db["prompts"])))
      return

    del db["prompts"][index]
    await message.channel.send(
        'Deleted prompt {0} from the database!'.format(index + 1))


client.run(token)
