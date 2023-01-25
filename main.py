# My modules
import json_manager

import os, sys, random
from typing import Optional
import discord
from discord import app_commands
import aiocron

settings = json_manager.ReadFile(os.getcwd() + '/settings.json')
adminIds = settings['adminIds']
online_presence = settings['online-presence']

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)        
        self.synced = False

    async def on_ready(self):
        if(not self.synced):
            await tree.sync()
            self.synced = True

            await changePresence()
            aiocron.crontab('0 */1 * * *', func=changePresence, start=True)
            print(f'Logged in as {client.user} (ID: {client.user.id}) \n------')

client = MyClient(intents=discord.Intents.default())
tree = app_commands.CommandTree(client)

#/- FUNCTIONS
async def changePresence():
    await client.change_presence(activity= discord.Game(online_presence[random.randint(0, len(online_presence) - 1)]));


@tree.command()
async def clear_all(interaction: discord.Interaction):
    """Clears all existing text from this channel"""
    await interaction.response.send_message(f'Clearing all chat...', ephemeral= True)
    await interaction.channel.purge()    

@tree.command()
@app_commands.rename(amountToDelete = 'number')
@app_commands.describe(amountToDelete = 'Amount of messages to delete in this channel')
async def clear(interaction: discord.Interaction, amountToDelete: int):
    """Clears x amount of messages from this channel"""    
    await interaction.response.send_message(f'Clearing {amountToDelete} message(s)...', ephemeral= True)

    msgs = []
    async for msg in interaction.channel.history(limit= amountToDelete): 
        msgs.append(msg);   

    await interaction.channel.delete_messages(msgs)

@tree.command()
@app_commands.rename(user = 'user')
@app_commands.describe(user = 'The selected user')
async def clear_user(interaction: discord.Interaction, user: discord.User):
    """Deletes all messages from a given user"""    
    await interaction.response.send_message(f'Clearing all messages by {user}...', ephemeral= True)
    msgs = []
    async for msg in interaction.channel.history(): 
        if(msg.author.id != user.id): continue
        msgs.append(msg);   
    await interaction.channel.delete_messages(msgs)

@tree.command(name="shutdown", description="Shuts the bot down")
async def self(interaction: discord.Interaction): 
    if(not (interaction.user.id in adminIds)): # Stops anyone but the admins to turn shut off the bot.
        await interaction.response.send_message(f'You do not have permission to run that command!', ephemeral= True)    
        return 

    print(f'{interaction.user} has shutdown the bot!')
    await interaction.response.send_message(f'Shutting down...', ephemeral= True)    
    sys.exit(0)

token = open('token.txt', 'r')
client.run(token.read())
token.close()