import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Încarcă variabilele de mediu din fișierul .env
load_dotenv()

# Citește tokenul din variabila de mediu
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

MARKETPLACE_CHANNELS = [
    924090048339664926, 924090338392543252, 924090284126658560, 
    1332500699795296427, 1332500782569881692, 1332500849464971305
]  # ID-urile canalelor marketplace

MESSAGE_CONTENT = """
🔔 **Salutare!** Pentru a avea acces la canalele de market, fiecare membru trebuie să invite doi prieteni pe server. 
Am implementat această regulă pentru a ajuta la creșterea comunității și pentru a ne asigura că serverul devine un loc activ și de încredere pentru toți utilizatorii.
Invitațiile vor fi verificate automat, iar odată ce ai adus doi prieteni, vei primi acces la secțiunea de market.
Asigură-te că invitațiile sunt valide, altfel accesul nu va fi acordat.
"""  # Mesajul pe care vrei să-l mențină

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Necesită activare în Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)

async def maintain_market_message(channel):
    """Menține mesajul fixat în canalul de marketplace."""
    async for message in channel.history(limit=50):
        if message.author == bot.user and MESSAGE_CONTENT in message.content:
            await message.delete()
            break
    await channel.send(MESSAGE_CONTENT)

@bot.event
async def on_ready():
    print(f"Botul este conectat ca {bot.user}")
    for channel_id in MARKETPLACE_CHANNELS:
        channel = bot.get_channel(channel_id)
        if channel:
            await maintain_market_message(channel)

@bot.event
async def on_message(message):
    if message.channel.id in MARKETPLACE_CHANNELS and message.author != bot.user:
        await maintain_market_message(message.channel)
    await bot.process_commands(message)

# Rulează botul folosind tokenul din variabila de mediu
bot.run(TOKEN)
