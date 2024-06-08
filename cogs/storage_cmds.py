import discord
from discord import Embed
from discord.ext import commands
import random
import requests
from flask_app import app
from db import db

class Storage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command()
    async def upload(self, ctx):
        member = ctx.author
        
        #lets work on flask
        response = requests.get('http://127.0.0.1:5000')
        data = response.json()
        unique_id = data['unique_id']
        link = f"http://127.0.0.1:5000/{unique_id}"
        check = db.storage.find_one({"user_id":ctx.author.id})
        if check == None:
            a =  db.storage.insert_one({"user_id":ctx.author.id,"unique_id":unique_id})
            print(a)
        else:
            db.storage.update_one({"user_id":ctx.author.id},{"$set":{"unique_id":unique_id}})
     
        embed = Embed(title="📤|UPLOAD", description="please check your DM",color = discord.Color.random())
        await ctx.send(embed = embed )
        embed_dm = Embed(title = "📁|UPLOAD", description=f'Please upload the files on the below link\n{link}', color = discord.Color.random())
        await member.send(embed=embed_dm)
        
    @commands.command()
    async def view(self, ctx):
        check = db.storage.find_one({"user_id": ctx.author.id})
        if check:
            unique_id = check["unique_id"]
            link = f"http://127.0.0.1:5000/view/{unique_id}?view=true"
            embed = Embed(title="👀|View Files", description=f"You can view your files [here]({link})", color=discord.Color.random())
            await ctx.author.send(embed=embed)
            await ctx.send("please check your dm!")
        else:
            embed = Embed(title="👀|View Files", description="You haven't uploaded any files yet.", color=discord.Color.random())
            await ctx.author.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Storage(bot))
