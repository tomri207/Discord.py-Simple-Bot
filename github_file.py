import discord
from discord.ext import commands
import json
import os

token = 'bot token here'

client = commands.Bot(command_prefix='.')
client.remove_command('help')
os.chdir(r'bot directory here')


@client.event
async def on_ready():
    print('-------------')
    print('Logged in as token:')
    print(token)
    print('Shows chat logs, commands, and much more!')
    print('-------------')


@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = client.get_channel('536182175545163778')
    await client.send_message(channel,  '{}:    {}'.format(author, content))


@client.command()
async def ping():
    await client.say('Pong!')


@client.command()
async def say(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    dm = 'The commands I have learnt are: ```.ping - *Returns \'Pong!\'' \
         '.say - *Makes the bot say anything*' \
         'That is all I have learnt so far! Feel free to DM Tom R.#0123 to give ideas!```'
    await client.send_message(author, dm)
    await client.say('I have DMed you my commands!')


@client.event
async def on_member_join(member):

    channel = client.get_channel('536182175545163778')
    msg = f'{member.mention}, welcome to GPRP, here we have active staff, developers, and gfx designers!' \
          'If you need help just ask!' \
          'Otherwise, just hang out and have fun! You are automatically a Member!' \
          'Make sure to read the rules in <#538509608474378266> , too!'
    await client.send_message(channel, msg)

    role = discord.utils.get(member.server.roles, name='Member')
    await client.add_roles(member, role)


@client.event
async def on_reaction_add(reaction, user):
    channel = client.get_channel('536182175545163778')
    await client.send_message(channel, '{} has added {} to the message: \'{}\''.format(user.name, reaction.emoji, reaction.message.content))


@client.event
async def on_reaction_remove(reaction, user):
    channel = client.get_channel('536182175545163778')
    await client.send_message(channel, '{} has removed {} from the message: \'{}\''.format(user.name, reaction.emoji, reaction.message.content))


@client.event
async def on_member_join(member):
    with open('users1.json', 'r') as f:
        users = json.load(f)

    with open('users1.json') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    with open('users1.json', 'r') as f:
        users = json.load(f)

    async def update_data(users, user):
        if not user.id in users:
            users[user.id] = {}
            users[user.id]['experience'] = 0
            users[user.id]['level'] = 1

    await update_data(users, message.author)

    async def add_experience(users, user, exp):
        users[user.id]['experience'] += exp

    await add_experience(users, message.author, 10)

    async def level_up(user, users, channel):
        experience = users[user.id]['experience']
        lvl_start = users[user.id]['level']
        lvl_end = int(experience ** (1/4))

        if lvl_start < lvl_end:
            await client.send_message(channel, '{} has levelled up to level {}.'.format(user.mention, lvl_end))
            users[user.id]['level'] = lvl_end

    await level_up(message.author, users, message.channel)

    with open('users1.json', 'w') as f:
        json.dump(users, f)


client.run(token)