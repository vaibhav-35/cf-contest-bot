import discord
from discord import message
from discord.client import Client
from discord.ext import commands
import json
import requests
from datetime import datetime
import time
from threading import * 
import asyncio


#--------------------------------------------------------------------------------------------------------------
sendList = []

def getContest():

    req = requests.get("https://codeforces.com/api/contest.list?gym=false")

    contests = req.json()['result']
    list = []
    dt = None
    for contest in contests:
        if contest['phase']=='FINISHED':
            break
        else:
            embedVar = discord.Embed(title=contest['name'], description='https://codeforces.com/contests', color=0x00ff00)
            ts = int(contest['startTimeSeconds']) + 5*3600+30*60
            date_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S').split(' ')
            date = date_time[0].split('-')
            dt = date[2]+date[1]+date[0]
            date = date[2]+'/'+date[1]+'/'+date[0]
            time = date_time[1]
            dt = date+time
            currday = datetime.now().strftime('%d')
            if int(currday) > int(date[:2]):
                continue
            embedVar.add_field(name="Date", value=date, inline=False)
            embedVar.add_field(name="Time", value=time, inline=False)
        list.append([embedVar,dt])
    return list

list = getContest()
#-------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) 

@bot.command()
async def sendhere(ctx):
    await ctx.send("OK i will send update in this channel")
    await ctx.send(ctx.message.id)
    bot.loop.create_task(SendContest(ctx.message.id))


@bot.command()
async def contests(ctx):
    for i in range(len(list)-1,-1,-1):
        em = list[i][0]
        await ctx.send(embed=em)

@bot.command()
async def tc(ctx):
    flag = True
    time = datetime.now
    for i in range(len(list)-1,-1,-1):
        em = list[i][0]
        t = list[i][1]
        if int(t[:2]) == time().day:
            flag = False
            await ctx.send(embed=em)
    if flag:
        await ctx.send("No contest today")

#--------------------------------------------------------------

async def SendContest(chID):
    await bot.wait_until_ready()
    channel = bot.get_channel(chID)
    while True:
        time = datetime.now
        list = getContest()
        for i in range(len(list)-1,-1,-1):
            t = time().day - int(list[i][1][8:10])
            if t<=3:
                print(time().day)
                print(int(list[i][1][8:10]))
                print("------------------")
                if not list[i][1] in sendList:
                    sendList.append(list[i][1])
                    await channel.send(embed=list[i][0])
        await asyncio.sleep(60*60)

#---------------------------------------------------------------
            

bot.run('put your token here')