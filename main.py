import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

prof = ["a", "b", "c", "d"]

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Бот запущен как {bot.user}")

@bot.tree.command(name="info", description="Print to users dm his info")
@app_commands.describe(user="Enter user")
async def test(interaction: discord.Interaction, user: discord.User):
    cp = prof.copy()
    u_prof = random.choice(cp)
    cp.remove(u_prof)
    u_age = random.randint(1,10)
    text = f"Your profession - {u_prof}. \nYour age - {u_age}."
    await user.send(text)
    await interaction.response.send_message("Test", ephemeral=True)
    print(cp)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)