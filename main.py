import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

prof = ["a", "b", "c", "d"]
users = {}

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

@bot.tree.command(name="info", description="Send info to all users")
@app_commands.describe(role="Select role")
async def info(interaction: discord.Interaction, role: discord.Role):
    guild = interaction.guild
    sent = 0

    for member in guild.members:
        if role in member.roles and not member.bot:
            #print(f"{member.name}")
            cp = prof.copy()
            u_prof = random.choice(cp)
            u_age = random.randint(1, 10)

            text = f"Your profession - {u_prof}.\nYour age - {u_age}."

            try:
                await member.send(text)
                users.update({
                    member.name:{
                        "profession": {
                            "value": u_prof,
                            "hide": True
                        },
                        "age": {
                            "value": u_age,
                            "hide": True
                        }
                    }
                })
                #print(users[member.name]["profession"]["value"])
                #users[member.name]["profession"]["hide"] = False
                #print(users[member.name]["profession"])
                sent += 1
            except discord.Forbidden:
                pass

    await interaction.response.send_message(f"Sent messages to {sent} users with role **{role.name}**", ephemeral=True)
    users.append([u_prof, u_age])

bot.run(token, log_handler=handler, log_level=logging.DEBUG)