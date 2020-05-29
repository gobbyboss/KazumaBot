import discord
from discord.ext import commands
from random import seed
from random import random 
from random import randint
import requests, json
from datetime import datetime, timedelta
from threading import Timer

seed(5)
client = commands.Bot(command_prefix = '!')
kNum = 0
King = "No king has been crowned yet" #Needs to have something here so !currentKing works when program first starts
inGame = False
current_time = datetime.now()

#Used for kanji quiz feature (minutes)
#Currently, the program will wait at least 1 hour between questions
min_interval = 60

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    global current_time
    global kNum
    global King
    global inGame
    global min_interval
#test
    async def Weather(Channel):
        await Channel.send(str(round(current_temperature * 1.8 - 459.67)) + "°F is the current temp in Fayetteville.")
        await Channel.send(str(weather_description))

    #Todo: Finish kanji quiz
    #Determines when to send the kanji quiz question
    timeInMinutes = (current_time.hour * 60) + current_time.minute
    timeOfMessage = datetime.now()
    messageInMinutes = (timeOfMessage.hour * 60) + timeOfMessage.minute
    diff = messageInMinutes - timeInMinutes
    if diff >= min_interval or diff <= min_interval - (min_interval * 2):
        chance = randint(1,10)
        #Makes it a 20% chance for the question to appear with each message after min_interval minutes has passed
      #  if chance <= 2:
           # await message.channel.send("placeholder")

    if message.content == "Kazuma" or message.content == "kazuma":
        await message.channel.send("Hai hai...")

    if message.content == "!rps":
      channel = message.channel
      await channel.send("Janken desu ka? Mou ii no " + message.author.mention + " san...")
      await channel.send("Saaaa, (R)ock (P)aper or (S)cissors?")
      rpsList = ["Rock", "Paper", "Scissors"]
      def check(m):
          return ((m.content == 'R' or m.content == 'r' or m.content == 'S' or m.content == 's' or m.content == 'P' or m.content == 'p') and (m.channel == channel))
      user = await client.wait_for('message', check=check) 
      cpu = rpsList[randint(0,2)]
      await channel.send(cpu)

      if user.content == "R" or user.content == "r":
          userNum = 0
      if user.content == "P" or user.content == "p":
          userNum = 1
      if user.content == "S" or user.content == "s":
          userNum = 2
      if cpu == "Rock":
          cpuNum = 0
      if cpu == "Paper":
          cpuNum = 1
      if cpu == "Scissors":
          cpuNum = 2

      if userNum == cpuNum:
          await channel.send("Baaaaaka. Be creative next time.")
      if userNum == 0 and cpuNum == 1:
          await channel.send("Ohoho. Wrong move idiot. That's what rock pickers get.")
      if userNum == 0 and cpuNum == 2:
          await channel.send("Ehhhh. Get a hold of this dirty rock abuser. GG go outside.")
      if userNum == 1 and cpuNum == 0:
          await channel.send("Paper eh. Just like your ego you flimsy dog")
      if userNum == 1 and cpuNum == 2:
          await channel.send("Bringing paper to a scissor fight? Classic rookie mistake there bud")
      if userNum == 2 and cpuNum == 0:
          await channel.send("Get crushed nerd. Next time don't use safety scissors.")
      if userNum == 2 and cpuNum == 1:
          await channel.send("Ow ow ow. That's cheating you simp")

    #lol  
    if str(message.author) in [""]:
        await message.delete()
        await message.channel.send("REEEEEEEEEE!")
    
    if message.content == "!king":
        if inGame:
            await message.channel.send("Still searching for a new king")
        else:
            await message.channel.send("A new king shall be crowned! Correctly guess my number (1-50)")
            kNum = randint(1,50)
            inGame = True
    
    if message.content == "!currentKing":
        await message.channel.send(King)
    
    if message.content == "!weather":
        channel = message.channel
        await channel.send("Tenki da ne? Ojiisan...")
        await channel.send("As I am a dumb bot, I can only tell you (F)ayetteville, (B)entonville, (A)ustin, or (NY)New York right now")
        channel = message.channel
        def wCheck(m): #Weather Check
            return((m.content == "F" or m.content == 'f' or m.content == 'B' or m.content == 'b' or
            m.content == "A" or m.content == "a" or m.content == "NY" or m.content == "ny" or m.content == "Ny" or m.content == "nY") and (m.channel == channel))
        wUser = await client.wait_for('message', check=wCheck)
        api_key = "b296835e1a68470f007cfab4af69ba8f" #Weather API
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&id="
        city = "default"
        if wUser.content == "F" or wUser.content == "f":
            city_url = "4110486"
            complete_url = complete_url + city_url
            city = "Fayettevile"
        
        if wUser.content == "B" or wUser.content == "b":
            city_url = "4101260"
            complete_url = complete_url + city_url
            city = "Bentonville"

        if wUser.content == "A" or wUser.content == "a":
            city_url = "4671654"
            complete_url = complete_url + city_url
            city = "Austin"

        if wUser.content == "NY" or wUser.content == "ny" or wUser.content == "Ny" or wUser.content == "nY":
            city_url = "5128581"
            complete_url = complete_url + city_url
            city = "New York"
            
        response = requests.get(complete_url)
        x = response.json() 
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            z = x["weather"]
            weather_description = z[0]["description"]
        else:
            print("City not found...")
        await channel.send("Currently the Weather in " + city + " is " + weather_description + ".")
        if current_temperature>70:
            await channel.send("Hot just like your mom lol. Right now it is "  + str(round(current_temperature * 1.8 - 459.67)))
        if current_temperature < 71 and current_temperature > 50:
            await channel.send("Temps are normal just like your loser. It's " + str(round(current_temperature * 1.8 - 459.67)))
        if current_temperature < 32 and current_temperature > 50:
            await channel.send("Hope ur dick dont shrink. It's " + str(round(current_temperature * 1.8 - 459.67))) 
    
    try:
        content = int(message.content)
        if content == kNum:
            inGame = False
            King = message.author
            await message.channel.send("Congrats on the new king!")
            kNum = randint(1,50)
    except:
        pass
 
    
    if message.content == "!Help":
        await message.channel.send("**Current list of Commands**")
        await message.channel.send("!king: Guess the number to become king!")
        await message.channel.send("!rps: Rock Paper Scissors")
        await message.channel.send("!weatherReport: Start a daily weather report at that specific time")
        await message.channel.send("!weather: The current weather in Fayetteville")

    if message.content == "!toss":
        flip = randint(1,2)
        if flip == 1:
            await message.channel.send("Heads")
        if flip == 2:
            await message.channel.send("Tails")

client.run("")