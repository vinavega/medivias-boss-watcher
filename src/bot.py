# bot.py
import requests
import os
import discord
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import asyncio

servList = ['Legacy']
mobsList = ['broodmother','archiona','arcestar','yeti','gieffrin','thousand eyes']
usersList = []

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

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
                for servName in servList:
                    page = requests.get("https://mediviastats.info/recent-deaths.php?server="+ servName)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    for mobName in mobsList:
                        a = soup(text=re.compile(mobName, re.IGNORECASE))
                        if a:
                            print(a)
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
    
    elif message.content.startswith('@mobs'):
        await channel.send("Lista de mobs procurados: " + str(mobsList))

    elif message.content.startswith('@servers'):
        await channel.send("Lista de servers procurados: " + str(servList))

    elif message.content.startswith('@addmob'):
        mob = message.content.replace("@addmob ", "")
        mobsList.append(mob.lower())
        await channel.send(mob + " adicionado com sucesso na lista de mobs procurados")

    elif message.content.startswith('@addserv'):
        serv = message.content.replace("@addserv ", "")
        servList.append(serv.lower())
        await channel.send(serv + " adicionado com sucesso na lista de servers")
    
    elif message.content.startswith('@rmmob'):
        mob = message.content.replace("@rmmob ", "")
        mobsList.remove(mob.lower())
        await channel.send(mob + " removido com sucesso da lista de mobs procurados")

    elif message.content.startswith('@rmserv'):
        serv = message.content.replace("@rmserv ", "")
        servList.remove(serv.lower())
        await channel.send(serv + " removido com sucesso da lista de servers")
        
client.run(TOKEN)