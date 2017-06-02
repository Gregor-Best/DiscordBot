import discord
from discord.ext import commands
import asyncio
import os

SLASH = '\\' if os.name == 'nt' else '/'

def get_extensions(bot):
    cogs = []
    for root, _, files in os.walk('cogs'):
        for filename in files:
            path = os.path.join(root, filename)
            if path.endswith('py') and all(key not in path for key in ['pycache', 'cogs.py']):
                cogs.append(path.replace(SLASH, '.')[:-3])
    return cogs

def load_extensions(bot):
    cogs = get_extensions(bot)
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print('Loaded {}'.format(cog))
        except (ImportError, discord.ClientException) as e:
            print('Error loading cog {}\n{}: {}'.format(cog, type(e).__name__, e))

class Cogs:
    def __init__(self, bot):
        self.bot = bot
        load_extensions(bot)


    @commands.group(pass_context=True)
    async def cogs(self, ctx):
        """Modify loaded cogs"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid cog subcommand passed.')

    @cogs.command()
    async def load(self, cog):
        cog_upper = cog[0].upper() + cog[1:]
        cog_lower = cog.lower()
        cog_id = "cogs.{}".format(cog_lower)
        cog_path = "cogs{0}{1}.py".format(SLASH, cog_lower)

        if self.bot.get_cog(cog_upper):
            await self.bot.say('Cog {} is already loaded.'.format(cog_upper))
            return

        if not os.path.isfile(cog_path):
            await self.bot.say('Cog {} not found.'.format(cog_upper))
            return

        try:
            self.bot.load_extension(cog_id)
            await self.bot.say('Cog {} has been loaded.'.format(cog_upper))
            return
        except (ImportError, discord.ClientException) as e:
            await self.bot.say('Error loading cog {}.'.format(cog_upper))
            return

    @cogs.command()
    async def remove(self, cog):
        cog_upper = cog[0].upper() + cog[1:]
        cog_id = "cogs.{}".format(cog.lower())

        if cog_upper in ["Cogs"]:
            await self.bot.say('Cannot remove {}.'.format(cog_upper))
            return

        if not self.bot.get_cog(cog_upper):
            await self.bot.say('Cog {} is not loaded.'.format(cog_upper))
            return

        try:
            self.bot.unload_extension(cog_id)
            await self.bot.say('Cog {} has been removed.'.format(cog_upper))
            return
        except (ImportError, discord.ClientException) as e:
            await self.bot.say('Error removing cog {}.'.format(cog_upper))
            return

    @cogs.command()
    async def restart(self, cog):
        cog_upper = cog[0].upper() + cog[1:]
        cog_lower = cog.lower()
        cog_id = "cogs.{}".format(cog_lower)
        cog_path = "cogs{0}{1}.py".format(SLASH, cog_lower)

        if not os.path.isfile(cog_path):
            await self.bot.say('Cog {} not found.'.format(cog_upper))
            return

        try:
            self.bot.unload_extension(cog_id)
            self.bot.load_extension(cog_id)
            await self.bot.say('Cog {} has been restarted.'.format(cog_upper))
            return
        except (ImportError, discord.ClientException) as e:
            await self.bot.say('Error restarting cog {}.'.format(cog_upper))
            return


def setup(bot):
    bot.add_cog(Cogs(bot))
