import discord
from discord.ext import tasks, commands
import requests

TOKEN = 'YOUR_BOT_TOKEN'  # Replace with your bot's token
GUILD_ID = YOUR_GUILD_ID  # Replace with your server (guild) ID
ROLE_NAME = 'ROLE_NAME'  # Replace with the role name to notify

bot = commands.Bot(command_prefix='!')

last_stock = None  # To store the last fetched stock data

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    check_stock.start()  # Start the periodic task

@tasks.loop(minutes=5)  # Check every 5 minutes
async def check_stock():
    global last_stock
    stock = fetch_stock()

    if stock and stock != last_stock:
        last_stock = stock
        guild = discord.utils.get(bot.guilds, id=GUILD_ID)
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        
        if role:
            channel = discord.utils.get(guild.text_channels, name='general')  # Change channel as needed
            await channel.send(f"{role.mention}, the stock has been updated!\nNew Stock: {stock}")

def fetch_stock():
    url = "https://example.com/bloxfruits/stock"  # Replace with the actual endpoint
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('stock')  # Adjust key to match API response
    else:
        print("Failed to fetch stock data.")
        return None

bot.run(TOKEN)
