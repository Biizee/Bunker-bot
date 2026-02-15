import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

prof = ["a", "b", "c", "d", "e", "f", "g"]
users = {}
users_list = []
dm_message = {}

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



async def update_info_text(user):
    if users[user]["profession"]["hide"]:
        o_prof = "??????????"
    else:
        o_prof = users[user]["profession"]["value"]
    
    if users[user]["age"]["hide"]:
        o_age = "??????????"
    else:
        o_age = users[user]["age"]["value"]

    return [o_prof, o_age]



@bot.tree.command(name="info", description="Send info to all users")
@app_commands.describe(role="Select role")
async def info(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer(ephemeral=True)
    users_list.clear()
    guild = interaction.guild
    sent = 0
    
    for member in guild.members:
        if role in member.roles and not member.bot:
            users_list.append(member.name)

    for member in guild.members:
        if role in member.roles and not member.bot:
            #print(f"{member.name}")
            cp = prof.copy()
            u_prof = random.choice(cp)
            u_age = random.randint(1, 10)

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

            text = f"Your profession - {u_prof}.\nYour age - {u_age}."

            try:
                await member.send(text)
                #print(users[member.name]["profession"]["value"])
                #users[member.name]["profession"]["hide"] = False
                #print(users[member.name]["profession"])
                sent += 1
            except discord.Forbidden:
                pass
    
    for member in guild.members:
        if role in member.roles and not member.bot:
            text_about_others = ""

            for user in users_list:
                if user != member.name:
                    d = await update_info_text(user)
                    text_about_others += f"""
===========================================
{user}
{d[0]}              {d[1]}
==========================================="""
                    
            try:
                msg = await member.send(text_about_others)
                dm_message.update({member.name: [member.id, msg.id]})

            except discord.Forbidden:
                pass

    await interaction.response.send_message(f"Sent messages to {sent} users with role **{role.name}**", ephemeral=True)



@bot.tree.command(name="edit", description="Uncover info about urself")
@app_commands.describe(info="Type category (profession / age)")
async def edit(interaction: discord.Interaction, info: str):
    await interaction.response.defer(ephemeral=True)
    user_name = interaction.user.name

    try:
        users[user_name][info.lower()]["hide"] = False
    except KeyError:
        await interaction.response.send_message("profession или age, дура",ephemeral=True)
        return


    for other_user in users_list:
        user = await bot.fetch_user(dm_message[other_user][0])
        channel = await user.create_dm()
        message = await channel.fetch_message(dm_message[other_user][1])

        text = ""

        for target in users_list:
            if target != other_user:
                d = await update_info_text(target)
                text += f"""
===========================================
{target}
{d[0]}              {d[1]}
==========================================="""
        await message.edit(content=text)

    await interaction.response.send_message(f"Your info was uncovered!", ephemeral=True)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)