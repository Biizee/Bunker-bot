import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import math

prof = ["a", "b", "c", "d", "e", "f", "g"]
inventory = ["Покебол з батьком/вітчимом", "Ізомер, Світловий конус", "Миска риса", "Мультитул", "Риска миса", "Гойдомобіль", "Радіаційні Зірочки",  "Двері", "Халат", "10кг урану", "Ядерна зброя", "Пульт від ядерної зброї", "250к тротила", "Одна додаткова Хромосома", "Диплом з філософії", "Біблія", "Бейблейд", "Чакапай", "Кокаїн", "Клоунська перука", "Програвач платівок", "Платівка з треком “Смарагдове небо 24 години”", "Красіва пляшка з водою", "Набір гральних кубиків", "Номери телефонів мам кожного гравця", "Телефон", "Екофлоу заряджена на 67%", "Біткойн", "Куплений слон", "Диплом міжнара", "Чіпси з крібом", "Посвідчення клоуна", "Пустий гаманець", "Пачка мівіни", "Сухарики зі смаком перемоги", "Повістка", "Серп і молот", "Посібник “Як навчитися жартувати”", "Водяний пістолет"]
health = ["Здоровий", "Клептоманія", "Альцгеймер", "Деменція", "Беброк", "Склероз", "Дальтонік", "Дилсексія", "Ахерон мейнер", "Рак мозку(67)", "Синдром автоброварні", "Спотворення смаку", "Ligma", "Техно-органічний вірус", "Синдром Капгра", "Синдром порушення цілісності сприйняття власного тіла", "Нестача зубів", "Аутизм", "Беброк", "Клоун", "Нестача однієї Хромосоми", "Катаракта", "Залежність від енергетиків", "Геншфаг", "Порушення сприйняття світу і часу", "Психоз", "Рижий", "Сліпий", "Смурфік", "Фанат Titanfall", "Роздвоєння особистості", "Понівірус"]
users ={}
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
    
    b_desc = "## **Бункер:**\n"
    b_desc += random.choice([f"Давно покинутий бункер. Має {live_count} спальних місць та запас їжі на {text_to_live}. На підлозі багато піску та перекотиполе, а всі поверхні в пилу. Не має в собі багато меблів чи приладдя, від кожного звуку можна почути ехо. Електроенергія присутня і працює, але світло все одно тьмяне та іноді може мигати. Вам необхідно протриматись {text_to_live}.\n\n", 
                            f"Абсолютно новий бункер, зі всім що необхідно для комфортних умов проживання, {live_count} спальних кімнат, кімната з тренажерами, кухня, столова, велика душова і вітальня, але, на жаль, в нього не встигли завести їжу, тож удачі вам прожити в цьому бункері решту життя({text_to_live}).\n\n", 
                            f"Побудований з лего бункер. Дуже сумнівно, що він довго протримається, тож, аби зберегти його якнайдовше, всі жителі мусять вести себе дуже обережно, адже прожити потрібно {text_to_live}. Добре омебльований, але все з лего, має {live_count} спальних місць(з лего). Є запас їжі на {food_time} місяців. Електропостачання в нормі, з водою часто проблеми (лего труби дають про себе знати).\n\n"
                            ])
    b_desc += "## **Катастрофа:**"
    b_desc += random.choice(["Вся земля стала Паркур Цивілізацією і ви відмовились жити в такому світі сховавшись в бункері.", 
                            "У світі з'явилося купу маніяків, тож щоб вижити треба бігати і лагодити генератори в бункері.",
                            "Всіх людей відправило до світу майнкрафту, де вся нежить і монстри мутували і стали набагато небезпечнішими, тому виживуть тільки кращі з кращих (роблоксерам не вижити).",
                            "Всі люди в світі стали рижими і їх масово почали палити на вогнищі інопланетні сили.", "Катастрофа всеукраїнського масштабу— Софійка вийшла на полювання і буде нищити все на своєму шляху.",
                            "Планета взірвалася і ми відправилися в космічну подорож на великому кораблі де живе АМОГУС. Потрібно вижити.",
                            "Всю землю огорнула безкінечна зима, сніг з вітром ускладнюють комунікацію між поселеннями, а з кожним днем температура падає і падає. Хто знає, як скоро ви помрете від переохолодження або ж від клоунів у вигляді членів вашого бункера.",
                            "Більшість людей купила Titanfall 2 за порадою школяра з Польщі, але, на щастя у вашому мозку ще залишились пара звивин і ви всі не купили це лайно, правда тепер життя на поверхні межує з життям в Сашківцях (повсюду бидлани). Ви не хочете це терпіти і єдине, що вам залишається робити- це перечекати пару рочків\місяців, поки люди усвідомлять свою помилку і покаяться за свої гріхи перед Аллахом.",
                            "IShowSpeed помер і тепер 90% школоти об’єднались і захватили владу у всіх країнах, крім Казахстана, адже тепер їм не буде кого дивитись((("
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

    if users[user]["health"]["hide"]:
        o_h = "??????????"
    else:
        o_h = users[user]["health"]["value"]

    return [o_prof, o_age, o_kicked, o_inv, o_h]

async def build_all_users_text(current_user):

    text = "```text\n" 
    
    for target in users_list:
        if target != current_user:
            d = await update_info_text(target)
            
            row1_left = f"Profession: {d[0]}"
            row1_right = f"Age: {d[1]}"
            row2_left = f"Inventory: {d[3]}"
            row2_right = f"Health: {d[4]}"
            
            max_left = max(len(row1_left), len(row2_left)) + 5
            
            text += f"=== {target} [{d[2]}] ===\n"
            text += f"{row1_left:<{max_left}} | {row1_right}\n"
            text += f"{row2_left:<{max_left}} | {row2_right}\n\n"
            
    text += "```" 
    return text

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
            copy_prof = prof.copy()
            copy_inventory = inventory.copy()
            copy_health = health.copy()

            users.update({
                    member.name:{
                        "profession": {
                            "value": random.choice(copy_prof),
                            "levels": random.choice(["NOOB", "PRO", "HACKER", "GOD"]),
                            "hide": True,
                        },
                        "age": {
                            "value": random.randint(10, 90),
                            "hide": True,
                        },
                        "inventory": {
                            "value": random.choice(copy_inventory),
                            "hide": True,
                        },
                        "health":{
                            "value": random.choice(copy_health),
                            "hide": True,
                        },
                        "kicked": False,
                    }
                })

            text = f"Your profession - {users[member.name]['profession']['value']}({users[member.name]['profession']['levels']}).\nYour age - {users[member.name]['age']['value']}.\nYour inventory - {users[member.name]['inventory']['value']}.\nYour health - {users[member.name]['health']['value']}."

            try:
                await member.send(a)
                await member.send(text)
                sent += 1
            except discord.Forbidden:
                pass
    
    for member in guild.members:
        if role in member.roles and not member.bot:
            text_about_others = await build_all_users_text(member.name)

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

            text = await build_all_users_text(other_user)
            await message.edit(content=text)

    await interaction.response.send_message(f"Your info was uncovered!", ephemeral=True)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)