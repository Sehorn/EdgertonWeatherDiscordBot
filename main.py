"""
This is a Discord bot that fetches real-time weather information for Edgerton, Kansas,
and reports it to a Discord server.
"""

import os
import requests
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token and API key from environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Enable the required intents
intents = Intents.default()
intents.message_content = True

# Create the bot instance with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def bothi(ctx):
    """Command handler for !bothi."""
    await ctx.send('Hello Guys!')

@bot.command()
async def weather(ctx):
    """Command handler for !weather."""
    city = 'Edgerton'
    state = 'KS'
    country = 'US'
    url = (
        f'http://api.openweathermap.org/data/2.5/weather?q={city},{state},'
        f'{country}&appid={OPENWEATHERMAP_API_KEY}&units=imperial'
    )
    try:
        response = requests.get(url, timeout=10)  # Adding a timeout of 10 seconds
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_report = (
            f"🌤️ **Weather in {city}, {state}:**\n"
            f"🌡️ **Temperature:** {temperature}°F\n"
            f"💧 **Humidity:** {humidity}%\n"
            f"🌬️ **Wind Speed:** {wind_speed} mph\n"
            f"📝 **Description:** {weather_description}\n"
        )
        await ctx.send(weather_report)
    except requests.exceptions.RequestException as e:
        await ctx.send(f'Failed to get the weather data: {e}')

# Run the bot with your token
bot.run(DISCORD_BOT_TOKEN)
