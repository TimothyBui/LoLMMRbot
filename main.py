# Discord bot created by TimothyBui
# a bot designed to show a player's MMR utilizing WhatIsMyMMR.com
# License: Creative Commons Attribution 2.0 Generic (CC BY 2.0)

import os
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands

my_header = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}

# load environment and token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# load discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.')

# show that bot is up and running
@bot.event
async def on_ready():
  print('Bot is active.')

# .mmr SUMMONER NAME 
# takes in user input and pulls mmr from
# https://na.whatismymmr.com/api/v1/summoner?name= 
@bot.command(name='mmr')
async def get_mmr(ctx, *, summoner_name: str):
  response = requests.get(f"https://na.whatismymmr.com/api/v1/summoner?name={summoner_name.replace(' ', '+')}", headers=my_header)
  data = response.json()

  if data.get('error', None):
    await ctx.send(f"This summoner doesn't exist.")
  else:
    mmr = data['ranked']['avg']
    error = data['ranked']['err']
    summary = data['ranked']['summary'].replace('<b>','').replace('</b><br><br><span class="symbol--micro"></span>','\n').replace('</b>','')
    await ctx.send(f"{summoner_name}'s ranked MMR is {mmr}±{error}. \nTier Range: {summary}" if mmr else "That summoner is currently unranked.")

bot.run(TOKEN)