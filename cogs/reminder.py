from discord.ext import commands
import re

def parseTime(time):
    regex = re.compile(r"(?:(?P<days>[0-9]{1,5})d)?(?:(?P<hours>[0-9]{1,5})h)?(?:(?P<minutes>[0-9]{1,5})m)?(?:(?P<seconds>[0-9]{1,5})s)?$")
    try:
        seconds = int(time)
    except ValueError as e:
        match = regex.match(time)
        if match is None or not match.group(0):
            raise commands.BadArgument("Failed to parse time.") from e

        seconds = 0
        days = match.group('days')


class Reminder:

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    return
    bot.add_cog(Reminder(bot))
