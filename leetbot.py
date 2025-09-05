import discord
from discord.ext import commands, tasks
import requests, datetime, random

token = ""
channel_id = 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TAGS = ['array', 'linked-list', 'queue']

def get_problem():
    url = f"https://alfa-leetcode-api.onrender.com/problems?tags={'+'.join(TAGS)}&limit=1"
    problem = requests.get(url).json()
    if problem and "problems" in problem:
        return problem["problems"][0]
    return None

