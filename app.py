import os
import requests
import discord
from datetime import datetime
from time import sleep

TOKEN = ''

client = discord.Client()
actual_state = {}

async def update_status(channel):
    global actual_state
    while True:
        result = requests.get("https://covid19-brazil-api.now.sh/api/report/v1").json()
        if result:
            if result != actual_state:
                actual_state = result

                totals = {
                    "cases": 0,
                    "deaths": 0
                }
                message = "Novas Notícias 😢\n"
                message += "```"
                for data in result['data']:
                    totals['cases'] += data['cases']
                    totals['deaths'] += data['deaths']

                    message += "{state}:\n- Casos: {cases}\n- Mortes: {deaths}\n\n".format(
                            state=data['state'],
                            cases=data['cases'],
                            deaths=data['deaths']
                        )
                message += "```\n"

                message += "Totais\n"
                message += "```"
                message += "Casos: {}\n".format(str(totals['cases']))
                message += "Mortes: {}\n".format(str(totals['deaths']))
                message += "```"

                await channel.send(message)
        sleep(10)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for channel in client.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            await update_status(channel)


client.run(TOKEN)
