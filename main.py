from flask import Flask
from threading import Thread
import os
import discord
import re
from discord.ext import commands

# Flask app setup
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Start Flask in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.tree.command(name="loona", description="loona")
async def loona_command(interaction: discord.Interaction):
    await interaction.response.send_message("loona2")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    try:
        guild = discord.Object(id=1197944095700697260)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to the guild {guild.id}")
        print(f"Commands available: {bot.tree.get_commands()}")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.event
async def on_message(message):

    if message.author.bot: 
        return

    loonaWords = [
        "loona", "loonaverse", "loonation", "orbits", "loossemble", "artms",
        "chuu", "yves", "heejin", "hyunjin", "haseul", "yeojin", "vivi", "kim lip", 
        "jinsoul", "choerry", "gowon", "hyeju", "jinsoo", "olivia hye", "hi high",
        "butterfly", "favorite", "so what", "why not", 
        "paint the town", "star", "stylish", "voice", "egoist", "new", "vivid",
        "the carol", "kiss later", "love cherry motion", "one & only", "heat",
        "queendom", "yyxy", "odd eye", "mobius", "virtual angel", "air force",
        "odd eye circle", "air force one", "ttyl", "heart attack",
        "sweet crazy love", "12:00", "flip that", "hula hoop", "pose", "dagab",
        "luminous", "dance on my own", "satellite", "day & night", "frozen",
        "rain 51db"
    ]


    otherWords = [
        # BTS
        "bts", "bangtan", "army", "namjoon", "jin", "yoongi", "hoseok", "jimin", "taehyung", "jungkook",

        # NCT (All Subunits)
        "nct", "nctzen", "nct 127", "nct dream", "wayv", "taeil", "johnny", "taeyong", "yuta", "doyoung",
        "jaehyun", "jungwoo", "mark", "haechan", "renjun", "jeno", "jaemin", "chenle", "jisung",
        "kun", "ten", "winwin", "lucas", "hendery", "xiaojun", "yangyang", 

        # Riize
        "riize", "briize", "shotaro", "eunseok", "sungchan", "wonbin", "seunghan", "sohee", "anton",

        # EXO
        "exo", "exol", "suho", "xiumin", "lay", "baekhyun", "chen", "chanyeol", "kai", "sehun",

        # Stray Kids (SKZ)
        "skz", "stray kids", "stay", "bang chan", "lee know", "changbin", "hyunjin", "han",
        "felix", "seungmin", "jeongin",

        # TXT (Tomorrow X Together)
        "txt", "tomorrow x together", "moa", "soobin", "yeonjun", "beomgyu", "taehyun", "huening kai",

        # ATEEZ
        "ateez", "atiny", "hongjoong", "seonghwa", "yunho", "yeosang", "san", "mingi", "wooyoung", "jongho",

        # Enhypen
        "enhypen", "engene", "heeseung", "jay", "jake", "sunghoon", "sunoo", "jungwon", "niki",

        # Seventeen
        "seventeen", "carat", "svt", "scoups", "jeonghan", "joshua", "jun", "hoshi", "wonwoo", "woozi", "dk", "mingyu",
        "the8", "seungkwan", "vernon", "dino",

        # Treasure
        "treasure", "hyunsuk", "jihoon", "yoshi", "junkyu", "jaehyuk", "asahi", "doyoung", "haruto", "jeongwoo", "junghwan",

        # The Boyz
        "the boyz", "tbz", "deobi", "sangyeon", "jacob", "younghoon", "hyunjae", "juyeon", "kevin", "chanhee", "changmin", "juhaknyeon", "sunwoo", "eric",

        # Monsta X
        "monsta x", "monbebe", "shownu", "minhyuk", "kihyun", "hyungwon", "jooheon",

        # P1Harmony
        "p1harmony", "piwon", "p1ece", "keeho", "theo", "jiung", "intak", "soul", "jongseob",

        # EPEX
        "epex", "zenith", "wish", "keum", "mu", "amin", "baekseung", "ayden", "jeff", "yewang",

        # BoyNextDoor
        "boy next door", "bnd", "bonedo", "boynextdoor", "taesan", "jaehyun", "leehan", "riwoo"


    ]

    girlWords = [
        # BLACKPINK
        "blackpink", "blink", "jennie", "jisoo", "rosé", "lisa",

        # TWICE
        "twice", "once", "nayeon", "jeongyeon", "momo", "sana", "jihyo", 
        "mina", "dahyun", "chaeyoung", "tzuyu",

        # Red Velvet
        "red velvet", "reveluv", "irene", "seulgi", "wendy", "joy", "yeri",

        # ITZY
        "itzy", "midzy", "yeji", "lia", "ryujin", "chaeryeong", "yuna",

        # Aespa
        "aespa", "karina", "giselle", "winter", "ningning",

        # NewJeans
        "newjeans", "minji", "hanni", "danielle", "haerin", "hyein",

        # LE SSERAFIM
        "lesserafim", "fearnot", "chaewon", "sakura", "yunjin", "kazuha", "eunchae",

        # IVE
        "ive", "dive", "yujin", "gaeul", "rei", "wonyoung", "liz", "leeseo",

        # Kep1er
        "kep1er", "keplian", "chaehyun", "youngeun", "dayeon", "yujin", 
        "xiaoting", "mashiro", "hikaru", "bahiyyih", "xiaoting", "yeseo",

        # LOONA
        "loona", "orbit", "heejin", "hyunjin", "haseul", "yeojin", "vivi", 
        "kim lip", "jinsoul", "choerry", "yves", "chuu", "gowon", "olivia hye",

        # Dreamcatcher
        "dreamcatcher", "insomnia", "jiu", "sua", "siyeon", "handong", "yoohyeon", "dami", "gahyeon",

        # Everglow
        "everglow", "sihyeon", "mia", "onda", "aisha", "yiren",

        # GFRIEND
        "gfriend", "buddy", "sowon", "yerin", "eunha", "yuju", "sinb", "umji",

        # Billlie
        "billlie", "belllieve", "moon sua", "siyoon", "tsuki", "sheon", "haram", "suhyeon", "haram",

        # STAYC
        "stayc", "swith", "sumin", "sieun", "isa", "seeun", "yoon", "j",

        # fromis_9
        "fromis_9", "fromis", "flover", "saerom", "hayoung", "gyuri", "jiheon", "seoyeon", 
        "jisun", "chaeyoung", "nakyung"
    ]

    # Helper function to match whole words
    def matches_keyword(message, word_list):
        pattern = r'\b(?:' + '|'.join(re.escape(word) for word in word_list) + r')\b'
        match = re.search(pattern, message.lower())
        if match:
            print(f"DEBUG: Matched keyword: {match.group()}")  # Log the matched keyword
        return match


    # Check for matches
    if matches_keyword(message.content, loonaWords):
        print("DEBUG: Matched loonaWords")
        await message.channel.send("loona")
        await message.add_reaction("😍")

    if matches_keyword(message.content, otherWords):
        print("DEBUG: Matched otherWords")
        await message.add_reaction("🐟")

    if matches_keyword(message.content, girlWords):
        print("DEBUG: Matched girlWords")
        await message.add_reaction("🙂‍↕️")

    await bot.process_commands(message)



# Run Discord bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))


