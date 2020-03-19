import os
import requests
import discord
from time import sleep

TOKEN = ''

client = discord.Client()
actual_state = {}

def sortFunc(e):
    return e['deaths']

async def update_status(channel):
    global actual_state
    while True:
        result = requests.get("https://api.coronaanalytic.com/brazil").json()
        if result:
            totals = {
                'cases': 0,
                'deaths': 0,
                'suspects': 0
            }
            message = "ÚLTIMA ATUALIZAÇÃO: {} {}\n\n".format(result['date'], result['time'])
            result['values'].sort(key=sortFunc, reverse=True)

            if result['values'] != actual_state:
                actual_state = result['values']
                for state in result['values']:
                    message += "{}: Confirmados [{}] | Mortes [{}] | Suspeitas [{}]\n".format(
                        state['state'], state['cases'], state['deaths'], state['suspects']
                    )
                    totals['cases'] += state['cases']
                    totals['deaths'] += state['deaths']
                    totals['suspects'] += state['suspects']

                message += "\n\nConfirmados [{}] | Mortes [{}] | Suspeitas [{}]".format(
                    totals['cases'], totals['deaths'], totals['suspects']
                )
                await channel.send(message)
        sleep(10)
        
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for channel in client.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            await update_status(channel)
        

client.run(TOKEN)