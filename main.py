

import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()

intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$removebg'):

        if not message.attachments:
            url = message.content[10:]           
        else:
            url = message.attachments[0].url

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data={
                'image_url': url,
                'size': 'auto'
            },
            headers={'X-Api-Key': os.getenv('API_KEY')},
        )
        if response.status_code == requests.codes.ok:
            with open('no-bg.png', 'wb') as out:
                print("debug")
                out.write(response.content)
                await message.channel.send(file=discord.File('no-bg.png'))
                
        else:
            await message.channel.send("Invalid Image format ")
            print("Error:", response.status_code, response.text)

client.run(os.getenv('TOKEN'))

