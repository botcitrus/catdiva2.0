import discord
from discord.ext import commands
from discord.utils import get
#Код не мой
import asyncio
import datetime
import random
import json

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["экономика"]

    @commands.command()
    async def timely(self, ctx):
        with open('./Data/DataBase/economy.json','r') as f:
            money = json.load(f)
        if not str(ctx.author.id) in money:
            money[str(ctx.author.id)] = {}
            money[str(ctx.author.id)]['Money'] = 0
 
        if not str(ctx.author.id) in queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы получили свои 300 монет')
            await ctx.send(embed= emb)
            money[str(ctx.author.id)]['Money'] += 300
            queue.append(str(ctx.author.id))
            with open('./Data/DataBase/economy.json','w') as f:
                json.dump(money,f)
            await asyncio.sleep(12*60)
            queue.remove(str(ctx.author.id))
        if str(ctx.author.id) in queue:
            emb = discord.Embed(description=f'**{ctx.author}** Вы уже получили свою награду')
            await ctx.send(embed= emb)

    @commands.command()
    async def balance(self, ctx, member:discord.Member = None):
        if member == ctx.author or member == None:
            with open('./Data/DataBase/economy.json','r') as f:
                money = json.load(f)
            emb = discord.Embed(description=f'У **{ctx.author}** {money[str(ctx.author.id)]["Money"]} монет')
            await ctx.send(embed= emb)
        else:
            with open('./Data/DataBase/economy.json','r') as f:
                money = json.load(f)
            emb = discord.Embed(description=f'У **{member}** {money[str(member.id)]["Money"]} монет')
            await ctx.send(embed= emb)
    
    @commands.command()
    async def shop(self, ctx):
        with open('./Data/DataBase/economy.json','r') as f:
            money = json.load(f)
        emb = discord.Embed(title="Магазин")
        for role in money['shop']:
            emb.add_field(name=f'Цена: {money["shop"][role]["Cost"]}',value=f'<@&{role}>',inline=False)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions( administrator = True)
    async def addshop(self, ctx, role:discord.Role, cost:int):
        with open('./Data/DataBase/economy.json','r') as f:
            money = json.load(f)
        if str(role.id) in money['shop']:
            await ctx.send("Эта роль уже есть в магазине")
        if not str(role.id) in money['shop']:
            money['shop'][str(role.id)] ={}
            money['shop'][str(role.id)]['Cost'] = cost
            await ctx.send('Роль добавлена в магазин')
        with open('./Data/DataBase/economy.json','w') as f:
            json.dump(money,f)   

    @commands.command()
    @commands.has_permissions( administrator = True)
    async def removeshop(self, ctx, role:discord.Role):
        with open('./Data/DataBase/economy.json','r') as f:
            money = json.load(f)
        if not str(role.id) in money['shop']:
            await ctx.send("Этой роли нет в магазине")
        if str(role.id) in money['shop']:
            await ctx.send('Роль удалена из магазина')
            del money['shop'][str(role.id)]
        with open('./Data/DataBase/economy.json','w') as f:
            json.dump(money,f)   

    @commands.command()
    async def buy(self, ctx, role:discord.Role):
        with open('./Data/DataBase/economy.json','r') as f:
            money = json.load(f)
        if str(role.id) in money['shop']:
            if money['shop'][str(role.id)]['Cost'] <= money[str(ctx.author.id)]['Money']:
                if not role in ctx.author.roles:
                    await ctx.send('Вы купили роль!')
                    for i in money['shop']:
                        if i == str(role.id):
                            buy = discord.utils.get(ctx.guild.roles,id = int(i))
                            await ctx.author.add_roles(buy)
                            money[str(ctx.author.id)]['Money'] -= money['shop'][str(role.id)]['Cost']
                else:
                    await ctx.send('У вас уже есть эта роль!')
        with open('./Data/DataBase/economy.json','w') as f:
            json.dump(money,f)
    
    @commands.command() 
    async def give(self, ctx, member:discord.Member, arg:int):
        with open('./Data/DataBase/economy.json','r') as f:
            money = json.load(f)
        if money[str(ctx.author.id)]['Money'] >= arg:
            emb = discord.Embed(description=f'**{ctx.author}** подарил **{member}** **{arg}** монет')
            money[str(ctx.author.id)]['Money'] -= arg
            money[str(member.id)]['Money'] += arg
            await ctx.send(embed = emb)
        else:
            await ctx.send('У вас недостаточно денег')
        with open('./Data/DataBase/economy.json','w') as f:
            json.dump(money,f)               

def setup(client):
    client.add_cog(economy(client))          