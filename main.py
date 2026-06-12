import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "النبطشي استلم الشيفت يا رياسه ومستعد للخدمة الشاقة!"

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

@tasks.loop(seconds=30)
async def check_voice_channel():
    if os.path.exists("last_channel.txt"):
        with open("last_channel.txt", "r") as f:
            channel_id = f.read().strip()
            if channel_id:
                for guild in bot.guilds:
                    voice_client = discord.utils.get(bot.voice_clients, guild=guild)
                    if not voice_client or not voice_client.is_connected():
                        channel = bot.get_channel(int(channel_id))
                        if channel:
                            try:
                                await channel.connect()
                                print("النبطشي صلح وضعه ودخل الروم أوتوماتيك!")
                            except:
                                pass

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Score Saver is online and ready')
    check_voice_channel.start()
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        if voice_client:
            await voice_client.move_to(channel)
        else:
            await channel.connect()
            
        with open("last_channel.txt", "w") as f:
            f.write(str(channel.id))
            
        await ctx.send('النبطشي حضر اسكورك امانه معايا')
    else:
        await ctx.send('ناديني جوه الفويس تشانل يسطا')

@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        
        if os.path.exists("last_channel.txt"):
            os.remove("last_channel.txt")
            
        await ctx.send('استاذن انا بقى')
    else:
        await ctx.send('انت بتطردني منين يسطا انا مفيش')

keep_alive()
bot.run(TOKEN)
