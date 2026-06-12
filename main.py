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

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        if voice_client:
            await voice_client.move_to(channel)
        else:
            await channel.connect()
            
        await ctx.send(f'النبطشي حضر اسكورك امانه معايا')
    else:
        await ctx.send('ناديني جوه الفويس تشانل يسطا')

@bot.command()
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send('استاذن انا بقى')
    else:
        await ctx.send('انت بتطردني منين يسطا انا مفيش')

keep_alive()
bot.run(TOKEN)