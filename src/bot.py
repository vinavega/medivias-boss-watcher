# bot.py
import requests
import os
import discord
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NAV = os.getenv('MEU_NICK')

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=None, afk=True)
    print("READY!")

on = None

@client.event
async def on_message(message):
    global on
    channel = message.channel
    if message.content.startswith('@start'):
        if on:
            await channel.send("O serviço já está ativado")
        else:
            await channel.send("Serviço iniciado")
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Medivia's death list"),afk=False)
            on = True
            print("Serviço iniciado")
            while on:
                print("Executando verificação....")
                servList = ['Legacy']
                mobsList = ['broodmother','archiona','arcestar','yeti','gieffrin','thousand eyes']
                for servName in servList:
                    page = requests.get("https://mediviastats.info/recent-deaths.php?server="+ servName)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    for mobName in mobsList:
                        a = soup(text=re.compile(mobName))
                        if a:
                            await channel.send(mobName +" encontrado no "+ servName +" -> "+ str(a))
                print("Execução finalizada, entrando em sleep")
                await asyncio.sleep(60)
            
    elif message.content.startswith('@stop'):
        if not on:
            await channel.send("O serviço já está desligado")
        else:
            await client.change_presence(status=discord.Status.idle, activity=None, afk=True)
            print("Serviço pausado")
            on = False
            await channel.send("Serviço pausado")
    elif message.content.startswith('@status'):
        if on:
            await channel.send("Serviço de monitoramento está rodando")
        else:
            await channel.send("Serviço de monitoramento desligado")
    
client.run(TOKEN)