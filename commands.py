import discord
import requests
import json
import os
from dotenv import load_dotenv
from math import ceil

load_dotenv()

API_KEY = os.getenv('X_RAPID_API_KEY')
API_HOST = os.getenv('X_RAPID_API_HOST')

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


async def cmdconvert(ctx, from_currency: discord.Option(str), to_currency: discord.Option(str),
                     amount: discord.Option(int)):
    print(from_currency, to_currency, amount)
    try:
        url = "https://currency-converter-pro1.p.rapidapi.com/convert"
        querystring = {"from": f"{from_currency}", "to": f"{to_currency}", "amount": f"{amount}"}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        await ctx.respond(
            f"Converting {amount} {from_currency.upper()} = {round(data['result'], 2)} {to_currency.upper()}")
    except Exception as e:
        print(e)
        await ctx.respond("Something went wrong...")


async def cmdlist(ctx):
    try:
        with open("currencies_data.json", "r") as file:
            data = json.load(file)

        elements = len(data["result"])
        last_page = ceil(elements / 10)
        column1, column2 = "", ""
        count, number = 1, 1
        pages = []

        for currency in data["result"]:
            column1 += f"{currency}:\n"
            column2 += f"{data['result'][currency]}\n"
            if count % 10 == 0:
                embed = createEmbed(number, last_page, column1, column2)
                pages.append(embed)
                number += 1
                column1, column2 = "", ""
            count += 1
        embed = createEmbed(number, elements, column1, column2)
        pages.append(embed)
        await ctx.respond(embed=pages[0], view=ListButtons(pages, last_page))
    except Exception as e:
        print(e)
        await ctx.respond("Something went wrong...")


def createEmbed(nr, last_page, column1, column2):
    embed = discord.Embed(
        title="Available Currencies",
        description=f"Page {nr}/{last_page}",
        color=discord.colour.Color.green()
    )
    embed.add_field(name="", value=column1, inline=True)
    embed.add_field(name="", value=column2, inline=True)
    return embed


class ListButtons(discord.ui.View):
    def __init__(self, pages, last_page):
        super().__init__()
        self.pages = pages
        self.last_page = last_page
        self.page = 0

    @discord.ui.button(label="Back", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def back(self, button, interaction):
        if self.page == 0:
            await interaction.response.edit_message(embed=self.pages[self.page])
        else:
            self.page -= 1
            await interaction.response.edit_message(embed=self.pages[self.page])

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next(self, button, interaction):
        if self.page == self.last_page - 1:
            await interaction.response.edit_message(embed=self.pages[self.page])
        else:
            self.page += 1
            await interaction.response.edit_message(embed=self.pages[self.page])
