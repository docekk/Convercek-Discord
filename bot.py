import os
import discord
import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('X_RAPID_API_KEY')
API_HOST = os.getenv('X_RAPID_API_HOST')

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


def start_bot():
    bot = discord.Bot()

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    @bot.slash_command(name="convert", description="Converts a currency")
    async def convert(ctx, from_currency: discord.Option(str), to_currency: discord.Option(str),
                      amount: discord.Option(int)):
        await commands.cmdconvert(ctx, from_currency, to_currency, amount)

    @bot.slash_command(name="list", description="List of currencies")
    async def list(ctx):
        await commands.cmdlist(ctx)

    bot.run(TOKEN)
