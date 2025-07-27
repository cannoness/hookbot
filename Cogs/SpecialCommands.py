import datetime
import discord

from discord.ext import commands


class SpecialCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # these are your / commands, example /help is provided for help documentation.
    @commands.hybrid_command(name="help", with_app_command=True)
    async def help(self, interaction, command: str = None, list_commands: bool = False, anon: bool = True) -> None:
        admin = ['cpr', 'help']

        embed = discord.Embed(
            title='Help Menu',
            description='',
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        if list_commands or command is None:
            all_commands = [command.name for command in self.bot.walk_commands() if command.name not in admin]
            command_list = ", ".join(sorted(all_commands))

            embed.add_field(name='The following server commands are available',
                            value=f"{command_list}",
                            inline=False)
            embed.add_field(name='\u200b',
                            value=f"For usage options of a specific command, call /help again with that command name.",
                            inline=False)

        elif command.lower() == 'YOUR COMMAND':
            embed.description = f"""
            *Documentation for command '!YOURCOMMAND'
            *ADD DOCUMENTATION HERE*
            """
            embed.set_footer(text="* This might be indented and have an extra newline due to triple quotes ")

        await interaction.interaction.response.send_message(embed=embed, ephemeral=anon)
        # await interaction.interaction.followup.send(f'testing help command', ephemeral=anon)

    @commands.hybrid_command(name="whois", with_app_command=True)
    async def whois(self, interaction, user: discord.User, anon: bool) -> None:
        # fill in code for determining who a user is, maybe add a link to their intro.
        await interaction.interaction.response.send_message(f'testing whois command',
                                                            ephemeral=anon)


async def setup(bot):
    await bot.add_cog(SpecialCommands(bot))
