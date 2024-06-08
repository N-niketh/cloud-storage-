import discord
import os
from discord.ext import commands
from config import *
import time
import flask
from flask import Flask,render_template,request,redirect,url_for
from flask_app import *
keep_alive()
global startTime
startTime = time.time()





import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['1.1.1.1']



class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=[':'], intents=discord.Intents.all(), help_command=None)
        self.synced = False

    async def on_ready(self):
        channel = bot.get_channel(1133036643499130981)
        await bot.wait_until_ready()
        await bot.change_presence(
          activity=discord.Activity(type=discord.ActivityType.watching, name=":help"), status=discord.Status.idle)

        if not self.synced:
          await bot.tree.sync()
          self.synced = True
        print(f"Logged in as {bot.user}")
        print(f"{bot.user.id}")
        await channel.send("Online!!")
    async def setup_hook(self):
      for name in os.listdir('cogs'):
          if name.endswith('.py'):
              try:
                  await self.load_extension(f"cogs.{name[:-3]}")
                  print('Loaded: cogs.{}'.format(name[:-3]))
              except Exception as error:
                  print(f'cogs.{name[:-3]} cannot be loaded. [{error}]')

bot = MyBot() 

try:  


  bot.run(TOKEN)

except:
  os.system("kill 1")