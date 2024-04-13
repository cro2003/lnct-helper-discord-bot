import discord
import rgpvApi
import lnctApi
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def getResult(enrollId, semester, message):
    result = rgpvApi.result(enrollId, 24)
    data = json.loads(result.getMain(semester))
    if data.get('error'):
        await message.edit(content=data['error'])
        return
    content = f'Student Name: {data["name"]}\n'\
              f'Enrollment Number: {data["enrollId"]}\n'\
              f'Status: {data["status"]}\n'\
              f'SGPA: {data["sgpa"]}\n'\
              f'CGPA: {data["cgpa"]}\n'
    for subject in data['subjects']:
        content += f'{subject["subject"]} - {subject["grade"]}\n'
    await message.edit(content=content)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$result'):
        try:
            enrollId = str(message.content.split(' ')[1])
            semester = int(message.content.split(' ')[2])
        except IndexError:
            await message.channel.send('Invalid Command! \nUsage: $result <enrollId> <semester>')
            return
        msg = await message.channel.send('Fetching Result...')
        await getResult(enrollId, semester, msg)
        return
    elif message.content.startswith('$profile'):
        try:
            username = str(message.content.split(' ')[1])
            password = int(message.content.split(' ')[2])
        except IndexError:
            await message.channel.send('Invalid Command! \nUsage: $result <username> <password>')
            return
        accsoft = lnctApi.accsoft()

    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        return

client.run(TOKEN)