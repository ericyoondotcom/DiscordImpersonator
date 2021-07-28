import discord
from discord.ext import commands
import os
from config import *

filedir = os.path.dirname(os.path.realpath(__file__))

bot = commands.Bot(command_prefix="sus ", case_insensitive=True, max_messages=5000)
bot.run(BOT_TOKEN)

@bot.command()
@commands.has_permissions(administrator=True)
async def download(ctx):
    for channel in DATA_CHANNELS:
        ctx.send("Downloading channel " + channel + "...")
        with open(os.path.join(filedir, "data", "channels", channel), "w") as file:
            async for msg in ctx.channel.history(limit=None):
                file.write(f"{msg.user.id}\t{msg.clean_content}\n")
