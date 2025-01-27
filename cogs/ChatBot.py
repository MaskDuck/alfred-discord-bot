import nextcord
import assets
import time
import os
import traceback
import helping_hand
import assets
import random
import External_functions as ef
import helping_hand
from nextcord.ext import commands, tasks

#Use nextcord.slash_command()

def requirements():
    return ['wolfram']

models = ['BlenderBot','DialoGPT','Wolfram Scientific','PopCat']


class ChatBot(commands.Cog):        
    def __init__(self, client, wolfram):
        self.client = client
        self.wolfram = wolfram
        self.models = models
        self.past_response = {}
        self.generated = {}
        self.auth = os.getenv("transformers_auth")
        self.headers = {"Authorization": f"Bearer {self.auth}"}
        self.BASE_URL = "https://api-inference.huggingface.co/models"

    def moderate_variables(self, id, input_text, output):
        if len(self.past_response[id])>=50:
            
            self.past_response[id].pop(0)
            self.generated[id].pop(0)            
        self.past_response[id].append(input_text)
        self.generated[id].append(output)

    @commands.Cog.listener()
    async def on_message(self, message):
        conditions = [            
            message.clean_content.lower().startswith("alfred "),
            message.guild and message.guild.id not in self.client.config['respond'],
            not message.author.bot
        ]
        if all(conditions):
            if not self.client.is_ready():
                return
            print(message.content, message.guild)
            if message.guild.id not in self.generated:
                self.generated[message.guild.id] = []
                
            if message.guild.id not in self.past_response:
                self.past_response[message.guild.id] = []
                
            input_text = message.clean_content[6:]
            
            if self.client.re[10].get(message.guild.id, 1) == 3:
                a = await ef.wolf_spoken(self.wolfram, input_text)

            if self.client.re[10].get(message.guild.id, 1) in (1,2):
                API_URL = f"{self.BASE_URL}/facebook/blenderbot-400M-distill"
                payload = {
                    "inputs": {
                        "past_user_inputs": self.past_response[message.guild.id],
                        "generated_responses": self.generated[message.guild.id],
                        "text": input_text,
                    },
                    "parameters": {"repetition_penalty": 1.33},
                }
                
                if self.client.re[10].get(message.guild.id, 1) == 2:
                    API_URL = f"{self.BASE_URL}/microsoft/DialoGPT-large"
                    payload = {
                        "inputs": input_text
                    }
                output = await ef.post_async(API_URL, header=self.headers, json=payload)
                print(output)
                a = output['generated_text']
                self.moderate_variables(message.guild.id, input_text, a)
            if self.client.re[10].get(message.guild.id, 1) == 4:
                a = await ef.get_async(f"https://api.popcat.xyz/chatbot?msg={ef.convert_to_url(input_text)}&owner=Batman&botname=Alfred",kind="json")
                a = a['response']

            await message.reply(a)
                
                
                

    @nextcord.slash_command("model")
    async def changeM(self, inter, model = ef.defa(choices=models)):
        if not model:
            mod = models[self.client.re[10].get(inter.guild.id, 1)-1]
            await inter.send(
                embed=ef.cembed(
                    description=f"Current model is {mod}",
                    color=self.client.re[8]
                )
            )
            return
        if not inter.user.guild_permissions.manage_guild:
            d = assets.Emotes(self.client).animated_wrong
            await inter.send(
                ephemeral = True,
                embed=ef.cembed(
                    title="Permissions Denied",
                    description=f"{d} You cannot change the model of this server, you need Manage server permissions",
                    color=self.client.re[8],
                    thumbnail=self.client.user.avatar.url
                )
            )
            return
        self.client.re[10][inter.guild.id] = self.models.index(model)+1
        message = f"Switched to {model}"
        await inter.send(
            embed=ef.cembed(
                title="Done",
                description=message,
                color=self.client.re[8],
                thumbnail=self.client.user.avatar.url
            )
        )   
    
            


def setup(client,**i):
    client.add_cog(ChatBot(client,**i))