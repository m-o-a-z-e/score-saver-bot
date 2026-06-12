import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "النبطشي استلم الشيفت يا رياسه"

def run():
    app.run(host='0.0.0.0', port=7860)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Score Saver is online and ready')
    print('Waiting for someone to call...')
    print('------')
    
    if os.path.exists("last_channel.txt"):
        with open("last_channel.txt", "r") as f:
            channel_id = f.read().strip()
            if channel_id:
                channel = bot.get_channel(int(channel_id))
                if channel:
                    await channel.connect()
                    print("النبطشي رجع الوردية بعد الريستارت أوتوماتيك")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        if voice_client:
            await voice_client.move_to(channel)
        else:
            await channel.connect()
            
        # بيكتب رقم الروم في النوتة عشان يرجع لها لو السيرفر فصل
        with open("last_channel.txt", "w") as f:
            f.write(str(channel.id))
            
        await ctx.send('النبطشي حضر اسكورك امانه معايا ومش همشي لوحدي تاني')
    else:
        await ctx.send('ناديني جوه الفويس تشانل يسطا')

@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        
        # بيقطع النوتة عشان ميدخلش لوحده تاني أبداً إلا لما تناديه
        if os.path.exists("last_channel.txt"):
            os.remove("last_channel.txt")
            
        await ctx.send('استاذن انا بقى')
    else:
        await ctx.send('انت بتطردني منين يسطا انا مفيش')

keep_alive()
bot.run(TOKEN)
