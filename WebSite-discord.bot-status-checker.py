import discord
import asyncio
import aiohttp
import pytz  
from datetime import datetime

# ho settato tutto io non toccare nulla 
TOKEN = 'TOKEN-DEL-TUO-BOT'
CHANNEL_ID =  00000000000 # id canale del canale dove verra mandato embed status
SERVER_URLS = [
    'http://fellarhost.site/', 
    'https://hertool.pages.dev/#'
]  # i tuoi siti


intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

async def fetch_http_status(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return 'online'
            else:
                return 'offline'
    except aiohttp.ClientError:
        return 'offline'

async def check_minecraft_server(address, port):
    server = MinecraftServer(address, port)
    try:
        status = server.status()
        return f"Online: {status.players} players"
    except Exception:
        return 'offline'

async def update_embed_message(message):
    while not client.is_closed():
        async with aiohttp.ClientSession() as session:
            embed = discord.Embed(title="Server Status", color=0x00ff00)

            
            local_tz = pytz.timezone('Europe/Rome')
            italian_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
            embed.set_footer(text=f"Last checked: {italian_time} | Made by Hertool<3")

            
            for url in SERVER_URLS:
                status = await fetch_http_status(session, url)
                color = '🟢' if status == 'online' else '🔴'
                embed.add_field(name=url, value=color, inline=False)


            
            for i in range(5, 0, -1):
                countdown = f"Next check in: {i} seconds"
                embed.description = countdown
                try:
                    await message.edit(embed=embed)
                except discord.HTTPException as e:
                    print(f"Failed to edit message: {e}")
                await asyncio.sleep(1)

           
            embed.description = "Checking status..."
            try:
                await message.edit(embed=embed)
            except discord.HTTPException as e:
                print(f"Failed to edit message: {e}")

            await asyncio.sleep(5)

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("Channel not found!")
        return

    embed = discord.Embed(title="Server Status", description="Checking status...", color=0x00ff00)

    
    local_tz = pytz.timezone('Europe/Rome')
    italian_time = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')
    embed.set_footer(text=f"Last checked: {italian_time} | Made by Hertool<3")

    try:
        message = await channel.send(embed=embed)
        client.loop.create_task(update_embed_message(message))
    except discord.HTTPException as e:
        print(f"Failed to send initial message: {e}")

client.run(TOKEN)
