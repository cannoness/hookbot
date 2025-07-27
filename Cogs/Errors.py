import os

from types import TracebackType
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TESTING_CHANNEL = os.getenv("BOT_TESTING_CHANNEL")


class Errors(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            tb = TracebackType.tb_next
            return await ctx.send(f"{error.with_traceback(tb)}")
        if isinstance(error, commands.errors.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            return await ctx.send(f"This command is on cooldown for user {ctx.message.author.display_name}, "
                                  f"try again after {int(minutes)}m {int(seconds)}s.", ephemeral=True)
        if isinstance(error, commands.errors.CommandNotFound):
            return await ctx.send(f"This command does not exist.", ephemeral=True)

        bot_channel = self.bot.get_channel(int(BOT_TESTING_CHANNEL))
        await bot_channel.send(f"Error encountered: {error}.")
        return await ctx.send(f"Error was encountered! Logged to admins.")


async def setup(bot):
    await bot.add_cog(Errors(bot))
