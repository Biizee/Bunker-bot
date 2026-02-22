import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import math

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



async def roll_bunker_info(users):
    live_count = math.floor(len(users) / 2)
    years_to_live = random.randint(0, 3)
    months_to_live = random.randint(0, 11)
    while years_to_live == 0 and months_to_live == 0:
        years_to_live = random.randint(0, 3)
        months_to_live = random.randint(0, 11)
    text_to_live = f"{years_to_live} роки і {months_to_live} місяців"
    food_time = ((years_to_live * 12) + months_to_live) - random.randint(-10, 10)
    if food_time <= 0:
        if random.choice([True, False]):
            food_time = random.randint(1,3)
        else:
            food_time = 0
    b_desc = random.choice([f"Давно покинутий бункер. Має {live_count} спальних місць та запас їжі на {text_to_live}. На підлозі багато піску та перекотиполе, а всі поверхні в пилу. Не має в собі багато меблів чи приладдя, від кожного звуку можна почути ехо. Електроенергія присутня і працює, але світло все одно тьмяне та іноді може мигати. Вам необхідно протриматись {text_to_live}", 
                            f"Абсолютно новий бункер, зі всім що необхідно для комфортних умов проживання, {live_count} спальних кімнат, кімната з тренажерами, кухня, столова, велика душова і вітальня, але, на жаль, в нього не встигли завести їжу, тож удачі вам прожити в цьому бункері решту життя({text_to_live}).", 
                            f"Побудований з лего бункер. Дуже сумнівно, що він довго протримається, тож, аби зберегти його якнайдовше, всі жителі мусять вести себе дуже обережно, адже прожити потрібно {text_to_live}. Добре омебльований, але все з лего, має {live_count} спальних місць(з лего). Є запас їжі на {food_time} місяців. Електропостачання в нормі, з водою часто проблеми (лего труби дають про себе знати)."
                            ])

    return b_desc

async def update_info_text(user):
    if users[user]["profession"]["hide"]:
        o_prof = "??????????"
    else:
        o_prof = users[user]["profession"]["value"] + "(" + users[user]["profession"]["levels"] + ")"
    
    if users[user]["age"]["hide"]:
        o_age = "??????????"
    else:
        o_age = users[user]["age"]["value"]
    
    if users[user]["kicked"]:
        o_kicked = "Kicked"
    else:
        o_kicked = "Alive"
    
    if users[user]["inventory"]["hide"]:
        o_inv = "??????????"
    else:
        o_inv = users[user]["inventory"]["value"]

    return [o_prof, o_age, o_kicked, o_inv]



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

    a = await roll_bunker_info(users_list)

    for member in guild.members:
        if role in member.roles and not member.bot:
            #print(f"{member.name}")
            cp = prof.copy()
            u_prof = random.choice(cp)
            u_age = random.randint(10, 90)

            users.update({
                    member.name:{
                        "profession": {
                            "value": u_prof,
                            "levels": random.choice(["NOOB", "PRO", "HACKER", "GOD"]),
                            "hide": True,
                        },
                        "age": {
                            "value": u_age,
                            "hide": True,
                        },
                        "inventory": {
                            "value": random.choice(["Покебол з батьком/вітчимом", "Ізомер, Світловий конус", "Миска риса", "Мультитул", "Риска миса", "Гойдомобіль", "Радіаційні Зірочки",  "Двері", "Халат", "10кг урану", "Ядерна зброя", "Пульт від ядерної зброї", "250к тротила", "Одна додаткова Хромосома", "Диплом з філософії", "Біблія", "Бейблейд", "Чакапай", "Кокаїн", "Клоунська перука", "Програвач платівок", "Платівка з треком “Смарагдове небо 24 години”", "Красіва пляшка з водою", "Набір гральних кубиків", "Номери телефонів мам кожного гравця", "Телефон", "Екофлоу заряджена на 67%", "Біткойн", "Куплений слон", "Диплом міжнара", "Чіпси з крібом", "Посвідчення клоуна", "Пустий гаманець", "Пачка мівіни", "Сухарики зі смаком перемоги", "Повістка", "Серп і молот", "Посібник “Як навчитися жартувати”", "Водяний пістолет"]),
                            "hide": True,
                        },
                        "kicked": False,
                    }
                })

            text = f"Your profession - {u_prof}({users[member.name]['profession']['levels']}).\nYour age - {u_age}.\nYour inventory - {users[member.name]['inventory']['value']}."

            try:
                await member.send(a)
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

===
{user} - {d[2]}
profession:              age:                           inventory:
{d[0]}              {d[1]}             {d[3]}
"""

            try:
                msg = await member.send(text_about_others)
                dm_message.update({member.name: [member.id, msg.id]})

            except discord.Forbidden:
                pass

    await interaction.response.send_message(f"Sent messages to {sent} users with role **{role.name}**", ephemeral=True)



@bot.tree.command(name="edit", description="Uncover info about urself")
@app_commands.describe(info="Type category (profession / age / inventory)")
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

===
{target} - {d[2]}
profession:              age:                           inventory:
{d[0]}              {d[1]}             {d[3]} 
"""
        await message.edit(content=text)

    await interaction.response.send_message(f"Your info was uncovered!", ephemeral=True)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)