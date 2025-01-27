from functools import lru_cache
import nextcord
import os
import datetime
import requests
import assets
import urllib.parse
import External_functions as ef
from nextcord.ext import commands

def requirements():
    return ["re"]
  
  
def main(client, re):
    space = ef.SpaceX(re[8])  
    
    def convert_to_url(name):
        name = urllib.parse.quote(name)
        return name

    @client.command()
    @commands.check(ef.check_command)
    async def gen(ctx, *, text):
        print(ctx.guild.name)
        re[0]+=1
        API_URL2 = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
        header2 = {"Authorization": f"Bearer {os.environ['transformers_auth']}"}
        payload2 = {
            "inputs": text,
            "parameters": {"max_new_tokens": 100, "return_full_text": True},
        }

        output = await ef.post_async(API_URL2, header2, payload2)
        print(output)
        o = output[0]["generated_text"]
        
        await ctx.reply(
            embed=ef.cembed(
                title="Generated text", description=o, color=re[8],thumbnail=client.user.avatar.url
            )
        )
      
      
    @client.command()
    @commands.check(ef.check_command)
    async def kanye(ctx):
        re[0] += 1
        text = await ef.get_async("https://api.kanye.rest", kind="json");text=text["quote"]
        embed = nextcord.Embed(
            title="Kanye Rest", description=text, color=nextcord.Color(value=re[8])
        )
        embed.set_thumbnail(
            url="https://i.pinimg.com/originals/3b/84/e1/3b84e1b85fb0a8068044df8b6cd8869f.jpg"
        )
        await ctx.send(embed=embed)
        
        
    @client.command()
    @commands.check(ef.check_command)
    async def age(ctx, name):
        try:
            re[0] += 1
            text = eval(
                 requests.get(
                    f"https://api.agify.io/?name={name}").content.decode()
            )
            st = ""
            for i in text:
                st += i + ":" + str(text[i]) + "\n"
            await ctx.send(
                embed=nextcord.Embed(
                    title="Agify", description=st, color=nextcord.Color(value=re[8])
                )
            )
        except:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Oops",
                    description="Something went wrong",
                    color=nextcord.Color(value=re[8]),
                )
            )
            
    @client.command()
    @commands.check(ef.check_command)
    async def apis(ctx, page: int = 0):
        re[0]+=1
        a = await ef.get_async("https://api.publicapis.org/entries",kind="json")
        b=a['entries']
        embeds=[]
        for i in range(a['count']):
            text=f"{b[i]['Description']}\n\n\nAuth: {b[i]['Auth'] if b[i]['Auth']!='' else None}\nHTTPS: {b[i]['HTTPS']}\nCors: {b[i]['Cors']}\nCategory: {b[i]['Category']}"
            embed = ef.cembed(
                title=b[i]['API'],
                description=text,
                color=re[8],
                url=b[i]['Link'],
                footer=f"{i+1} of {a['count']}"
            )
            embeds.append(embed)

        await assets.pa(ctx, embeds, start_from=page, restricted=False)
            
            
    @client.command()
    @commands.check(ef.check_command)
    async def ip(ctx, *, ip):
        re[0] + re[0] + 1
        ip = convert_to_url(ip)
        print(ip)
        print(f"https://ipinfo.io/{ip}/geo")
        a = await ef.get_async(f"https://ipinfo.io/{ip}/geo",kind="json")
        st = ""
        if "status" not in list(a.keys()):
            for i in list(a.keys()):
                st += f"**{i}**:\n{a[i]}\n\n"
            embed = nextcord.Embed(
                title=ip, description=st, color=nextcord.Color(value=re[8])
            )
            embed.set_thumbnail(url=client.user.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="Oops",
                description="Oops, couldnt find it :confused:",
                color=nextcord.Color(value=re[8]),
            )
            embed.set_thumbnail(url=client.user.avatar.url)
            await ctx.send(embed=embed)
            
            
    @client.command(aliases=["cat"])
    @commands.check(ef.check_command)
    async def cat_fact(ctx):
        re[0] + re[0] + 1
        a = await ef.get_async("https://catfact.ninja/fact", kind="json")
        embed = nextcord.Embed(
            title="Cat Fact", description=a["fact"], color=nextcord.Color(value=re[8])
        )
        embed.set_thumbnail(url="https://i.imgur.com/u1TPbIp.png?1")
        await ctx.send(embed=embed)
    
    @client.command()
    @commands.check(ef.check_command)
    async def lyrics(ctx, *, song):
        embed=await ef.ly(song, re)
        await ctx.send(embed=embed)

    @client.group()
    @commands.check(ef.check_command)
    async def spacex(ctx):        
        if not ctx.invoked_subcommand:
            await ctx.send(
                embed=ef.cembed(
                    title="Oops",
                    description="We couldnt find that sub-command, it's either history or latest",
                    image="https://thumbs.gfycat.com/CoarseAdventurousIbis-max-1mb.gif",
                    color=re[8]
                )
            )
            return

    @spacex.command()
    async def history(ctx):
        embeds = await space.history()
        await assets.pa(ctx, embeds, start_from=0, restricted=False)

    @spacex.command()
    async def latest(ctx):
        await space.setup()
        embed=ef.cembed(
            title=space.name,
            description=f"Time: {space.time}\nVisit the [official website](https://www.spacex.com/) for more",
            thumbnail=space.thumbnail, footer="This feature is still in its beta stage, sorry for inconvenience",color=space.color,
            image = "https://static01.nyt.com/images/2021/01/30/business/29musk-print/29musk-1-videoSixteenByNineJumbo1600.jpg"

        )
        embed.add_field(name="Youtube",value=f"[Link]({space.youtube})", inline=True)
        embed.add_field(name="Wikipedia", value=f"[Link]({space.wikipedia})", inline=True)
        await ctx.send(embed=embed)

    @client.command(aliases = ['dictionary', 'dict', 'dict_h'])
    @commands.check(ef.check_command)
    async def diction(ctx, *, text):
        try:
            mean = ef.Meaning(word = text, color = re[8])
            await mean.setup()
            await assets.pa(ctx, mean.create_texts(), start_from=0, restricted=False)
        except Exception as e:
            await ctx.send(
                embed=ef.cembed(
                    title="Something is wrong",
                    description="Oops something went wrong, I gotta check this out real quick, sorry for the inconvenience",
                    color=nextcord.Color.red(),
                    thumbnail=client.user.avatar.url
                )
            ) 
    
                    
