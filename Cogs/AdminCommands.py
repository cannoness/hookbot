import os
import discord

from json import loads
from typing import Optional, Literal
from discord.ext import commands, tasks
from discord.ext.commands import Context, Greedy
from dotenv import load_dotenv


load_dotenv()
BOT_TESTING_CHANNEL = os.getenv("BOT_TESTING_CHANNEL")
PRIVILEGED_ROLES = {"admin", "moderator"}
JSON_FILE = os.getenv("JSON_FILE")


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # This will send an announcement to a specific channel on a timer.
    # Use the test_emped.json file to configure an embed to send.
    @tasks.loop(hours=1.0)
    async def create_embed(self, ctx):
        user_roles = [role.name for role in ctx.message.author.roles]
        if PRIVILEGED_ROLES.isdisjoint(user_roles):
            return
        else:
            channel = self.bot.get_channel(int(BOT_TESTING_CHANNEL))
            try:
                with open(JSON_FILE, "r") as file:
                    embed = discord.Embed().from_dict(loads(file.read()))
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                file = discord.File("dummy_img.jpg", filename="dummy_img.jpg")
                embed.set_thumbnail(url="attachment://dummy_img.jpg")
                allowed_mentions = discord.AllowedMentions(everyone=True)
                await channel.send(allowed_mentions=allowed_mentions, file=file, embed=embed)
            except Exception as ex:
                raise Exception(ex)


    # use this command to determine if the bot is running
    @commands.command(name='cpr')
    async def health_check(self, ctx):
        user_roles = set([role.name for role in ctx.message.author.roles])
        if PRIVILEGED_ROLES.isdisjoint(user_roles):
            return
        else:
            await ctx.message.channel.send("I AM STILL ALIVE (and doing science)")


    # This command must be run before / commands like /help will work.
    @commands.command(name="sync")
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) \
            -> None:
        user_roles = set([role.name for role in ctx.message.author.roles])
        if PRIVILEGED_ROLES.isdisjoint(user_roles):
            return
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                ctx.bot.tree.clear_commands(guild=None)
                [ctx.bot.tree.remove_command(c.name) for c in self.bot.tree.get_commands()]
                synced = [c.name for c in self.bot.tree.get_commands()]
            else:
                synced = await ctx.bot.tree.sync(guild=ctx.guild)

            bcommands = [c.name for c in self.bot.tree.get_commands()]
            print(f"registered commands: {', '.join(bcommands)}")
            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0

        try:
            await ctx.bot.tree.sync()
        except discord.HTTPException as ex:
            print(ex)
            await ctx.send(f"Encountered exception {ex}. This has been recorded.")
            raise Exception(ex)
        else:
            ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
