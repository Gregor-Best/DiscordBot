from discord.ext import commands
import datetime
import asyncio
import re

def parseTime(message):
    regex = re.compile(r"^(?:(?P<days>[0-9]+)[d,D] ?)?(?:(?P<hours>[0-9]+)[h,H] ?)?(?:(?P<minutes>[0-9]+)[m,M] ?)?(?:(?P<seconds>[0-9]+)[s,S] )?(?P<message>.*)$")
    match = regex.match(message)
    if match is None or not match.group(0):
        raise commands.BadArgument("Failed to parse time.")
    groups = match.groupdict(default=0)
    delta = datetime.timedelta(days=int(groups['days']), hours=int(groups['hours']), minutes=int(groups['minutes']), seconds=int(groups['seconds']))
    if delta <= datetime.timedelta():
        raise commands.BadArgument("Duration must be greater than 1 second.")
    date = datetime.datetime.now() + delta
    return date, groups['message']

# @asyncio.coroutine
# async def check_times(bot, reminders):
#     while True:
#         await asyncio.sleep(1)
#         print(reminders)
#         now = datetime.datetime.now()
#         if now > reminders[0][0]: # datetime has expired
#             # await send_reminder(bot, reminders[0])
#             print(reminders[0])
#             reminders.pop(0)

class Reminder_Object:
    def __init__(self, time, message, user, channel, server):
        self.time = time
        self.message = message
        self.user = user
        self.channel = channel
        self.server = server

class Reminder:
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []
        bot.loop.create_task(self.check_times())

    async def check_times(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            await asyncio.sleep(1)
            if len(self.reminders) > 0 and datetime.datetime.now() > self.reminders[0].time:
                reminder = self.reminders.pop(0)
                server = self.bot.get_server(reminder.server)
                channel = server.get_channel(reminder.channel)
                user = server.get_member(reminder.user)
                await self.bot.send_message(channel, content="{0.mention}: {1}".format(user, reminder.message))

    @commands.group(pass_context=True)
    async def remindme(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                time, message = parseTime(ctx.message.content[10:])
            except Exception as e:
                await self.bot.say(e)
                return
            reminder = Reminder_Object(time, message, ctx.message.author.id, ctx.message.channel.id, ctx.message.server.id)
            self.reminders.append(reminder)
            self.reminders.sort(key=lambda reminder: reminder.time)
            await self.bot.say("Ok I'll remind you then :)")

    @remindme.command()
    async def list(self):
        reminds = ""
        for reminder in self.reminders:
            reminds = "{}\n{}\t'{}'\t{}\t{}".format(reminds, reminder.time, reminder.message, reminder.user, reminder.channel)
        print(reminds)
        await self.bot.say("{}".format(reminds))


def setup(bot):
    bot.add_cog(Reminder(bot))

# if __name__ == "__main__":
#     message = "5s do the thing"
#     date, message = parseTime(message)
#     reminders = [(date, message)]
#     asyncio.Task(check_times("bot", reminders))
#     asyncio.Task(second())
#     asyncio.get_event_loop().run_forever()


    # if date: # remind on a date or at a time
    #     date_regex = re.compile(r"^(?:(?P<day>[1-9]|[1-2][0-9]|3[0-1])/)(?:(?P<month>[1-9]|1[0-2])/)(?:(?P<year>[0-9]{4}))?$")
    #     time_regex = re.compile(r"^(?P<hour>[0-9]*)(?::(?P<minutes>[0-9]*))?(?::(?P<seconds>[0-9]*))?(?: ?(?P<period>am|pm))? (?P<message")
    # else: # remind in a duration
    #     regex = re.compile(r"(?:(?P<days>[0-9]{1,5})d)?(?:(?P<hours>[0-9]{1,5})h)?(?:(?P<minutes>[0-9]{1,5})m)?(?:(?P<seconds>[0-9]{1,5})s)?$")
