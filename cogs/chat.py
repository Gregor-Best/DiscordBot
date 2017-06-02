from discord.ext import commands
import asyncio

class Chat:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lenny(self):
        await self.bot.say('( ͡° ͜ʖ ͡°)')

    @commands.command()
    async def shrug(self):
        await self.bot.say('¯\\_(ツ)_/¯')

    @commands.command()
    async def ping(self):
        await self.bot.say('Pong!')

def setup(bot):
    bot.add_cog(Chat(bot))
