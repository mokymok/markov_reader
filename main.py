import sys, os
import pyttsx3
import discord
from discord import Intents
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get

intents = Intents.all()
bot = commands.Bot(intents = intents, command_prefix = '^')
engine = pyttsx3.init()
loop = asyncio.get_event_loop()
print(loop)
self = discord.User

if 'TOKEN' not in os.environ:
    print('No bot token (TOKEN) in the list of environment variables')
    exit()
token = os.environ['TOKEN']

@bot.event
async def on_ready():
  print('Logged on as', self)
  await bot.change_presence(
      activity = discord.Activity(
          type = discord.ActivityType.listening, 
          name = 'Markov'))

@bot.listen('on_message')
async def tts(ctx):
  messageContent = ctx.content
  if ctx.author.bot == True:
    print(messageContent)
    engine.save_to_file(messageContent, 'filler.mp3')
    engine.runAndWait()
    voice = get(bot.voice_clients, guild=ctx.guild)
    source = FFmpegPCMAudio('filler.mp3')
    player = voice.play(source)
  else:
    return

@bot.command(pass_context=True)
async def join(ctx):
  channel = ctx.author.voice.channel
  await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
  await ctx.voice_client.disconnect()

@bot.command(pass_context=True)
async def test(ctx):
  await ctx.send('This is a test message!', tts=True)

if loop.is_running() == False:
    bot.run(token)