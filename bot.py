# bot.py
import requests
import os
import discord
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import schedule
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NAV = os.getenv('MEU_NICK')

client = discord.Client()

@client.event
async def on_ready():
    while True:
        schedule.run_pending()
        print("Executando verificação....")
        for guild in client.guilds:
            async for member in guild.fetch_members(limit=None):
             if member.name == NAV:
                break
        servList = ['Legacy','Destiny','Pendulum','Prophecy','Purity']
        mobsList = ['broodmother','archiona','arcestar','yeti','gieffrin','thousand eyes']
        for servName in servList:
          page = requests.get("https://mediviastats.info/recent-deaths.php?server="+ servName)
          soup = BeautifulSoup(page.content, 'html.parser')
          for mobName in mobsList:
            a = soup(text=re.compile(mobName))
            if a:
               await member.send(mobName +" encontrado no "+ servName +" -> "+ str(a))
        print("Execução finalizada, entrando em sleep")
        time.sleep(30)
client.run(TOKEN)
