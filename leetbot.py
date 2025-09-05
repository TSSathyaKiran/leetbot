import discord
from discord.ext import commands
import requests, datetime
import json
import os

token = ""
channel_id = ""
DATA_FILE = "daily_problem.json"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

TAGS = ['array', 'linked-list', 'queue']

def daily_problems_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    return {"date": None, "problem": None}

def load_daily_problem(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_problems():
    url = f"https://alfa-leetcode-api.onrender.com/problems?tags={'+'.join(TAGS)}&limit=1"
    problem = requests.get(url).json()
    if problem and "problems" in problem:
        return problem["problems"][0]
    return None

def get_daily_problem():
    today = datetime.date.today().isoformat()
    data = daily_problems_data()
    if data["date"] != today:
        problem = get_problems()
        data = {"date": today, "problem": problem}
        load_daily_problem(data)
    return data["problem"]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    )