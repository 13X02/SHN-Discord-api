

import discord
import os
import requests
from dotenv import load_dotenv
from PIL import Image,ImageFilter  
from PIL import ImageEnhance  , ImageOps


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
    elif message.content.startswith('$blur'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            img = img.filter(ImageFilter.GaussianBlur(radius=10))
            img.save('blurred.png')
            await message.channel.send(file=discord.File('blurred.png'))
        else:
            await message.channel.send("Invalid Image format ")
            print("Error:", response.status_code, response.text)
    elif message.content.startswith('$help'):
        await message.channel.send("```$removebg <image url> - Removes background from image \n$blur <image url> - Blurs the image \n$grayscale <image url> - Converts image to grayscale \n$invert <image url> - Inverts the image \n$enhance <image url> - Enhances the image \n$flip <image url> - Flips the image \n$mirror <image url> - Mirrors the image \n$rotate <image url> - Rotates the image```")
    elif message.content.startswith('$grayscale'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            gray_image = ImageOps.grayscale(img)
            gray_image.save('gray.png')
            await message.channel.send(file=discord.File('gray.png'))
    elif message.content.startswith('$invert'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            inverted_image = ImageOps.invert(img)
            inverted_image.save('inverted.png')
            await message.channel.send(file=discord.File('inverted.png'))
    elif message.content.startswith('$enhance'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            enhancer = ImageEnhance.Contrast(img)
            enhanced_image = enhancer.enhance(2)
            enhanced_image.save('enhanced.png')
            await message.channel.send(file=discord.File('enhanced.png'))
    elif message.content.startswith('$flip'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            flipped_image = ImageOps.flip(img)
            flipped_image.save('flipped.png')
            await message.channel.send(file=discord.File('flipped.png'))
    elif message.content.startswith('$mirror'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            mirrored_image = ImageOps.mirror(img)
            mirrored_image.save('mirrored.png')
            await message.channel.send(file=discord.File('mirrored.png'))
    elif message.content.startswith('$rotate'):
        if not message.attachments:
            url = message.content[9:]           
        else:
            url = message.attachments[0].url
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            img = Image.open(response.raw)
            rotated_image = img.rotate(90)
            rotated_image.save('rotated.png')
            await message.channel.send(file=discord.File('rotated.png'))
    

client.run(os.getenv('TOKEN'))

