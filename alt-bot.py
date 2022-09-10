import random
import json
import ffmpeg
import time
import numpy
import datetime as dt
import discord
import asyncio
secondTime = False
from discord.ext import tasks, commands
from discord.ext.commands import MemberConverter
from discord.utils import get
client = commands.Bot(command_prefix = '$')
converter = MemberConverter()
with open("userList.json", "r") as p:
    userList = json.load(p)
    print(userList)
    print(type(userList))
    

with open("subList.json", "r") as p:
    subList = json.load(p)

initiated = False
@client.event
async def on_ready():
    print("initiated")
    initiated = True
    print (initiated)


@client.command(pass_context=True)
@commands.has_any_role("basic", "vip", "premium", "royalty")
async def generate(ctx):
    user = ctx.author
    username = str(user)
    with open("subList.json", "r") as p:
        subList = json.load(p)
    print(subList[username])
    if subList[username] != "0":
        with open("userList.json", "r") as p:
            userList = json.load(p)
        role_names = [role.name for role in user.roles]
        print(user)
        if username not in userList:
            userList[username] = 1
            print("this user has generated " + str(userList[username]) + " accounts")
        else:
            userList[username] += 1
            print("this user has generated " + str(userList[username]) + " accounts")
        with open("userList.json", "w") as p:
            json_object = json.dumps(userList, indent = 4)  
            print(json_object) 
            p.write(json_object)
            altList = open("alts.txt")
            altlines = altList.readlines()
            if len(altlines) > 0:
                if "basic" in role_names:
                    if userList[username] <= 10:
                       await sendAlt(ctx, user)
                    else:
                        await ctx.send("you have exceeded your maximim daily accounts. Please come back later or updgrade your plan")
                elif "vip" in role_names: 
                    if userList[username] <= 25:
                       await sendAlt(ctx, user)
                    else:
                        await ctx.send("you have exceeded your maximim daily accounts. Please come back later or upgrade your plan")
                elif "premium" in role_names: 
                    if userList[username] <= 35:
                       await sendAlt(ctx, user)
                    else:
                        await ctx.send("you have exceeded your maximim daily accounts. Please come back later or upgrade your plan")
                elif "royalty" in role_names:
                    if userList[username] <= 50:
                       await sendAlt(ctx, user)
                    else:
                        await ctx.send("you have exceeded your maximim daily accounts. Please come back later")
                else:
                    await ctx.send("there has been an issue. Please contact staff. err: no role")
            else:
                await ctx.send("there are no more alts in stock. Please wait for a restock")

async def sendAlt(ctx, user):
    altList = open("alts.txt")
    lines = altList.readlines()
    altList.close()
    length = len(lines)
    print(length)
    randomindex = random.randint(1, length) - 1
    print(randomindex)
    alt = lines[randomindex]
    print(alt)
    print(user)
    channel = await user.create_dm()
    await channel.send(alt)
    await ctx.send("dmed you :)")
    with open("alts.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i != str(alt):
                f.write(i)
        f.truncate()

        
@client.command(pass_context=True)
@commands.has_role("admin")
async def resetLimit(ctx):
    user = ctx.author
    username = str(user)
    print(user)
    userList[username] = 0
    await ctx.send(str(user) + "'s limit has been reset.")
    with open("userList.json", "w") as p:
        json_object = json.dumps(userList, indent = 4)  
        print(json_object) 
        print(p)
        p.write(json_object)
        print(p)


@client.command()
async def stock(ctx):
    altList = open("alts.txt")
    lines = altList.readlines()
    altList.close()
    length = len(lines)
    print(length)
    await ctx.send("Current stock is " + str(length))

@client.command()
async def redeemBasic(ctx, *args):
    global secondTime
    user = ctx.author
    username = str(user)
    userid = ctx.author.id
    usernameid = str(userid)
    keyList = open("basicKeys.txt")
    lines = keyList.readlines()
    keyList.close()
    length = len(lines)
    print("there are " + str(length) + " basic tier keys left")
    print("redeeming")
    args = str(args)
    #this is the jankiest possible solution and I hate it so fucking much but it works so.......
    if args.endswith(',)'):
        trimArgs = args[:-3]
    if trimArgs.startswith('('):
        trimArgs = trimArgs[2:]
    print("args is equal to " + trimArgs)
    for i in lines:
        key = i
        #if secondTime == False:
        key = key[:-1]
        print(key)
        if trimArgs == key:
            secondTime = True
            print("redeeming " + key)
            role = discord.utils.get(user.guild.roles, name="basic")
            await user.add_roles(role)
            await ctx.send("you have redeemed the key " + key)
            with open("basicKeys.txt", "r") as f:
                d = f.readlines()
                with open("basicKeys.txt", "w") as k:
                    for i in d:
                        print('i="%s"' % str(i))
                        print('key="%s"' % str(key))
                        if str(i[:-1]) != str(key):
                            k.write(i)
                        else:
                            print("found the key as " + i)
            date = dt.datetime.today()
            expiremonth = date.month + 1
            expireday = date.day
            expiredate = str(expiremonth) + " " + str(expireday)
            with open("subList.json", "r") as p:
                subList = json.load(p)
            subList[username] = expiredate
            with open("subList.json", "w") as p:
                json_object = json.dumps(subList, indent = 4)  
                print(json_object) 
                p.write(json_object)
            break

@client.command()
async def redeemVip(ctx, *args):
    global secondTime
    user = ctx.author
    username = str(user)
    userid = ctx.author.id
    usernameid = str(userid)
    keyList = open("vipKeys.txt")
    lines = keyList.readlines()
    keyList.close()
    length = len(lines)
    print("there are " + str(length) + " vip tier keys left")
    print("redeeming")
    args = str(args)
    #this is the jankiest possible solution and I hate it so fucking much but it works so.......
    if args.endswith(',)'):
        trimArgs = args[:-3]
    if trimArgs.startswith('('):
        trimArgs = trimArgs[2:]
    print("args is equal to " + trimArgs)
    for i in lines:
        key = i
        #if secondTime == False:
        key = key[:-1]
        print(key)
        if trimArgs == key:
            secondTime = True
            print("redeeming " + key)
            role = discord.utils.get(user.guild.roles, name="vip")
            await user.add_roles(role)
            await ctx.send("you have redeemed the key " + key)
            with open("vipKeys.txt", "r") as f:
                d = f.readlines()
                with open("vipKeys.txt", "w") as k:
                    for i in d:
                        print('i="%s"' % str(i))
                        print('key="%s"' % str(key))
                        if str(i[:-1]) != str(key):
                            k.write(i)
                        else:
                            print("found the key as " + i)
            date = dt.datetime.today()
            expiremonth = date.month + 1
            expireday = date.day
            expiredate = str(expiremonth) + " " + str(expireday)
            with open("subList.json", "r") as p:
                subList = json.load(p)
            subList[username] = expiredate
            with open("subList.json", "w") as p:
                json_object = json.dumps(subList, indent = 4)  
                print(json_object) 
                p.write(json_object)
            break

@client.command()
async def redeemPremium(ctx, *args):
    global secondTime
    user = ctx.author
    username = str(user)
    userid = ctx.author.id
    usernameid = str(userid)
    keyList = open("premiumKeys.txt")
    lines = keyList.readlines()
    keyList.close()
    length = len(lines)
    print("there are " + str(length) + " premium tier keys left")
    print("redeeming")
    args = str(args)
    #this is the jankiest possible solution and I hate it so fucking much but it works so.......
    if args.endswith(',)'):
        trimArgs = args[:-3]
    if trimArgs.startswith('('):
        trimArgs = trimArgs[2:]
    print("args is equal to " + trimArgs)
    for i in lines:
        key = i
        #if secondTime == False:
        key = key[:-1]
        print(key)
        if trimArgs == key:
            secondTime = True
            print("redeeming " + key)
            role = discord.utils.get(user.guild.roles, name="premium")
            await user.add_roles(role)
            await ctx.send("you have redeemed the key " + key)
            with open("premiumKeys.txt", "r") as f:
                d = f.readlines()
                with open("premiumKeys.txt", "w") as k:
                    for i in d:
                        print('i="%s"' % str(i))
                        print('key="%s"' % str(key))
                        if str(i[:-1]) != str(key):
                            k.write(i)
                        else:
                            print("found the key as " + i)
            date = dt.datetime.today()
            expiremonth = date.month + 1
            expireday = date.day
            expiredate = str(expiremonth) + " " + str(expireday)
            with open("subList.json", "r") as p:
                subList = json.load(p)
            subList[username] = expiredate
            with open("subList.json", "w") as p:
                json_object = json.dumps(subList, indent = 4)  
                print(json_object) 
                p.write(json_object)
            break

@client.command()
async def redeemRoyalty(ctx, *args):
    global secondTime
    user = ctx.author
    username = str(user)
    userid = ctx.author.id
    usernameid = str(userid)
    keyList = open("royaltyKeys.txt")
    lines = keyList.readlines()
    keyList.close()
    length = len(lines)
    print("there are " + str(length) + " royalty tier keys left")
    print("redeeming")
    args = str(args)
    #this is the jankiest possible solution and I hate it so fucking much but it works so.......
    if args.endswith(',)'):
        trimArgs = args[:-3]
    if trimArgs.startswith('('):
        trimArgs = trimArgs[2:]
    print("args is equal to " + trimArgs)
    for i in lines:
        key = i
        #if secondTime == False:
        key = key[:-1]
        print(key)
        if trimArgs == key:
            secondTime = True
            print("redeeming " + key)
            role = discord.utils.get(user.guild.roles, name="royalty")
            await user.add_roles(role)
            await ctx.send("you have redeemed the key " + key)
            with open("royaltyKeys.txt", "r") as f:
                d = f.readlines()
                with open("royaltyKeys.txt", "w") as k:
                    for i in d:
                        print('i="%s"' % str(i))
                        print('key="%s"' % str(key))
                        if str(i[:-1]) != str(key):
                            k.write(i)
                        else:
                            print("found the key as " + i)
            date = dt.datetime.today()
            expiremonth = date.month + 1
            expireday = date.day
            expiredate = str(expiremonth) + " " + str(expireday)
            with open("subList.json", "r") as p:
                subList = json.load(p)
            subList[username] = expiredate
            with open("subList.json", "w") as p:
                json_object = json.dumps(subList, indent = 4)  
                print(json_object) 
                p.write(json_object)
            break     

        

@client.command()
async def dababy(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    player = vc.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source='suge.mp3'))
    time.sleep(232)
    await ctx.guild.voice_client.disconnect()

@client.command()
async def valorant(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    player = vc.play(discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg.exe', source='valorant.mp3')) 
    time.sleep(1.7)
    await ctx.guild.voice_client.disconnect()

@client.command()
async def ralph(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/806917670473170987/842004596662337556/profileIcon_hs2lqfz01yn41.jpg")

@client.command()
async def fortnite(ctx):
    await ctx.send("https://media.discordapp.net/attachments/813080224421642310/842055589374722088/ezgif.com-gif-maker_1.gif")

@client.command()
async def pm(ctx, *args):
    print("ctx is " + str(ctx))
    print(type(args))
    user = ctx.author
    username = str(user)
    print(type(user))
    print(user)
    message = str(user) + " says: "
    iteration = 0
    for i in args:
        iteration += 1
        print(str(i))
        if iteration > 1:
            message = message + str(i) + " "
        else:
            receiver = i
            print(receiver)
            receiver = await converter.convert(ctx, receiver)
    channel = await receiver.create_dm()
    await channel.send(message)
    await ctx.send("I pmed " + str(receiver) + "your message")
    
@client.command()
async def telephone(ctx, *args):
    print("ctx is " + str(ctx))
    print(type(args))
    user = ctx.author
    username = str(user)
    print(type(user))
    print(user)
    message = str(user) + " says: "
    iteration = 0
    for i in args:
        iteration += 1
        print(str(i))
        message = message + str(i) + " "
    channel = client.get_channel(847945415155253338)
    await channel.send(message)
    await ctx.send("your message has been delivered to the other line")

class MyCog(commands.Cog):
    def __init__(self):
        self.checktime.start()

    def cog_unload(self):
        self.checktime.cancel()

    @tasks.loop(seconds=0.5)
    async def checktime(self):
            date = dt.datetime.today()
            if dt.datetime.now().hour == 23:
                if dt.datetime.now().minute == 59:
                    if dt.datetime.now().second == 59:
                        with open("userList.json", "w") as p:
                            userList = {}
                            json_object = json.dumps(userList, indent = 4)  
                            print(json_object) 
                            p.write(json_object)
                            print(p)
                            print("reset daily generations")
            with open("subList.json", "r") as p:
                subList = json.load(p)
            for i in subList:
                #print(i + subList[i])
                if subList[i] ==  str(date.month) + " " + str(date.day):
                    subList[i] = "0"
                    print("removed role")
                    with open("subList.json", "w") as p:
                        print("reseting sub time")
                        json_object = json.dumps(subList, indent = 4)
                        p.write(json_object)
                    



timeChecker = MyCog()
        
client.run('') #insert ur bot token in here
