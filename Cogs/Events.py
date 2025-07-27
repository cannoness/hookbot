import os
import discord

from discord.ext import commands, tasks
from dotenv import load_dotenv

from Utilities.DatabaseActions import DatabaseActions

load_dotenv()
GUILD_ID = int(os.getenv("GUILD_ID"))
BOT_TESTING_CHANNEL = os.getenv("BOT_TESTING_CHANNEL")
PRIVILEGED_ROLES = {'admins', "moderators"}


class Events(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_
        self.guild = None
        self.db_actions = DatabaseActions()

        self.daily_reset.start()


    def cog_unload(self):
        self.daily_reset.cancel()


    # daily reset takes place any time you need to reset something, ie, a message on a timer, remove a timeout, etc.
    # example given for sending a dm after a certain action (e.g., checking calendar events) has taken place.
    @tasks.loop(hours=24)
    async def daily_reset(self):
        calendar_alerts = self.db_actions.check_calendar_for_updates()
        if len(calendar_alerts) > 0:
            for ids, message in calendar_alerts:
                discord_id = self.guild.get_member(ids)
                await self._send_dm_to_single_user(discord_id, message)
        if len(calendar_alerts) > 0:
            bot_channel = self.bot.get_channel(int(BOT_TESTING_CHANNEL))
            await bot_channel.send(f"Sending alerts to : {calendar_alerts}")


    @daily_reset.before_loop
    async def before_daily_reset(self):
        print('waiting to reset for the day...')
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(GUILD_ID)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to Discord!')


    @staticmethod
    async def _send_dm_to_single_user(user, message):
        embed = discord.Embed(description=message)
        try:
            await user.send(embed=embed)
        except Exception as ex:
            raise Exception(ex)



async def setup(bot):
    await bot.add_cog(Events(bot))
