from Tokens import app_id, public_key, app_token, DB_user, DB_password, DB_database
import discord
from discord.ext import commands
import logging
import json
import time

import api

import DB
import mariadb

try: 
    conn = mariadb.connect(
    user=DB_user,
    password=DB_password,
    database=DB_database,
    port=5000
    )
    conn.autocommit = True

except mariadb.Error as ex:
    print("Error: {}".format(ex))
    sys.exit(1)


cur = conn.cursor()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


bot = commands.Bot('!', intents=discord.Intents.default(), activity=discord.Game("the stock market"))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def update(ctx):
    if ctx.message.author.discriminator == "6504" or ctx.message.author.discriminator == "2556": 
        li = DB.SymbolLiFix(DB.GetAllStock(cur))
        res = api.Call(li)
        #print(res)
        #await ctx.send("{}".format(res['quoteResponse']["result"][0]["regularMarketPrice"]))
        for x in range(len(li)):
            print("{a} :: {b}".format(a=res['quoteResponse']["result"][x]["regularMarketPrice"], b=res['quoteResponse']["result"][0]["regularMarketChange"]))
            DB.UpdateStock(li[x], res['quoteResponse']["result"][x]["regularMarketPrice"], res['quoteResponse']["result"][x]["regularMarketChange"], cur)
        await ctx.send("@everyone \n✅Stock data updated!✅", allowed_mentions = discord.AllowedMentions(everyone=True))
    else:
        await ctx.send("❌Only Admins can update stock data.❌")

@bot.command()
async def player(ctx, arg):
    user = DB.GetUser(arg.lower(), cur)
    if user != []:
        await ctx.send("{u}:\n💱Investment: {i}\n ⭕Original Price: ${o:.2f}\n💲Current Price: {s:.2f}:-\n✖️Percent: {p:.2f}%".format(u=arg,s=user[0][3]*9.43,i=user[0][2], p=user[0][4], o=user[0][5]*9.43))

    else:
        await ctx.send("❌ {} is not a player❌".format(arg))

@bot.command()
async def stock(ctx, arg):
    DBstock = DB.GetStock(arg.upper(), cur)
    if DBstock != []:
        await ctx.send("\n💲Current Price: {c:.2f}:-\n✖️Percent: {p:.2f}%".format(c=DBstock[0][1]*9.43,p=DBstock[0][2]))
    else:
        await ctx.send("❌ {} is not a stock symbol❌".format(arg))

@bot.command()
async def JOIN(ctx, arg1, arg2):
    DBstock = DB.GetStock(arg2, cur)
    if DBstock == []:
        DB.AddStock(arg2.upper(), cur)
    res = api.Call([arg2])
    DB.AddPlayer(arg1, arg2, res['quoteResponse']["result"][0]["regularMarketPrice"], cur)
    time.sleep(0.08)
    DB.UpdateStock(arg2.upper(), res['quoteResponse']["result"][0]["regularMarketPrice"], res['quoteResponse']["result"][0]["regularMarketChange"], cur)
    await ctx.send("✅User added: {u}✅\n✅With investment: ${i}✅".format(u=arg1.lower(), i=arg2.upper()))

@bot.command()
async def top(ctx, arg1):
    topPlayers = DB.GetTopPlayers(arg1, cur)
    await ctx.send("✅Top player by day✅")
    for x in range(len(topPlayers)):
        await ctx.send("{u}:\t{s:.2f}:-\t${i}\t{p:.2f}%".format(u=topPlayers[x][0],i=topPlayers[x][1], p=topPlayers[x][3], s=(topPlayers[x][2]*9.43)))

bot.run(app_token)