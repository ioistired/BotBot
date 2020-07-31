# import discord
from discord.ext import commands

from bot import BotBase, Context


class Moderation(commands.Cog):

    def __init__(self, bot: BotBase):
        self.bot = bot

    @commands.command(name='cleanup')
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def cleanup(self, ctx: Context, limit: int = 50):
        """Deletes messages related to bot commands from the channel.

        `limit`: the number of messages to process, can be a maximum of 100 messages.
        """
        to_delete = []

        if not 0 < limit <= 100:
            raise commands.BadArgument('You can only delete between 1 and 100 messages.')

        async for message in ctx.channel.history(limit=limit):

            context = await self.bot.get_context(message)
            if message.author == self.bot.user or context.command is not None:
                to_delete.append(message)

        await ctx.channel.delete_messages(to_delete)


def setup(bot: BotBase):
    bot.add_cog(Moderation(bot))
