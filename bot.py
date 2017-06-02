#!/usr/bin/python3

from discord.ext import commands
import discord
import json, asyncio
import logging
import os

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
log_handle = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
log.addHandler(log_handle)

description = "Discord bot."

bot = commands.Bot(command_prefix='!', description=description, pm_help=None)

@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('----------')

@bot.command(hidden=True)
asyncio def load_cog(cog):
    cog_upper = cog[0].upper() + cog[1:]
    try:
        bot.load_extension(cog_id)
        await bot.say('Cog {} has been loaded.'.format(cog_upper))
        return
    except (ImportError, discord.ClientException) as e:
        await bot.say('Error loading cog {}.'.format(cog_upper))
        return

def read_credentials():
    with open('credentials.json') as f:
        return json.load(f)

if __name__ == '__main__':
    credentials = read_credentials()
    token = credentials['token']
    bot.client_id = credentials['client_id']

    try:
        bot.load_extension("cogs.cogs")
        print('Loaded {}'.format("Cogs"))
    except (ImportError, discord.ClientException) as e:
        print('Error loading cog {}\n{}: {}'.format("Cogs", type(e).__name__, e))

    bot.run(token)
    handlers = log.handlers[:]
    for hand in handlers:
        hand.close()
        log.removeHandler(hand)
