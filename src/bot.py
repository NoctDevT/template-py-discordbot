import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This is going to be a file at the same level as bot.py that you will create
# be sure to add this in and add in your discord token as a variable like 
# TOKEN=DISCORD_BOT_TOKEN but replace the DISCORD_BOT_TOKEN for the actual token. 
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_extensions():
    for folder in ['commands', 'events']:
        for filename in os.listdir(f'./{folder}'):
            if filename.endswith('.py') and filename != '__init__.py':
                bot.load_extension(f'{folder}.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

if __name__ == '__main__':
    token = os.getenv('TOKEN')  
    load_extensions()
    bot.run(token)
