import discord
from discord.ext import commands
import os
import asyncio
import markovify
from config import *

filedir = os.path.dirname(os.path.realpath(__file__))

bot = commands.Bot(command_prefix="sus ", case_insensitive=True, max_messages=5000)
model_cache = {}

def load_model_from_file(user_id):
    path = os.path.join(filedir, "data", "models", str(user_id))
    if not os.path.exists(path):
        return False
    with open(path, "r") as file:
        model_cache[user_id] = markovify.NewlineText.from_json(file.read())
    return True

def train_model(user_id):
    training_data = ""
    file_list = os.listdir(os.path.join(filedir, "data", "channels"))
    for filename in file_list:
        with open(os.path.join(filedir, "data", "channels", filename), "r") as file:
            lines = file.readlines()
            for line in lines:
                delimiter = line.find("\t")
                if delimiter < 0:
                    continue
                if str(user_id) != line[:delimiter]:
                    continue
                training_data += line[(delimiter + 1):] + "\n"
    model = markovify.NewlineText(training_data)
    model_cache[user_id] = model
    with open(os.path.join(filedir, "data", "models", str(user_id)), "w") as file:
        file.write(model.to_json())

@bot.event
async def on_ready():
    print("Connected to Discord!")

@bot.command()
@commands.has_permissions(administrator=True)
async def download(ctx):
    for channel_id in DATA_CHANNELS:
        await ctx.send(f"Downloading channel {str(channel_id)}...")
        channel = bot.get_channel(channel_id)
        with open(os.path.join(filedir, "data", "channels", str(channel_id)), "w") as file:
            async for msg in channel.history(limit=None): # TODO: limit=None does not work
                content = msg.clean_content.replace("\n", " ")
                file.write(f"{msg.author.id}\t{content}\n")
                await asyncio.sleep(0.03)
    await ctx.send("All done!")

@bot.command()
async def run(ctx, *, member:discord.Member):
    if not member.id in model_cache:
        if not load_model_from_file(member.id):
            train_model(member.id)
    model = model_cache[member.id]
    await ctx.send(model.make_sentence())
bot.run(BOT_TOKEN)