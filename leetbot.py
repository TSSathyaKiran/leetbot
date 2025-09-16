import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

VALID_TAGS = ["array", "linked-list", "stack", "string"]
VALID_DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]
SKIP_FILE = "skip_data.json"

def load_skip_data():
    if os.path.exists(SKIP_FILE):
        with open(SKIP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_skip_data(data):
    with open(SKIP_FILE, "w") as f:
        json.dump(data, f)

def get_problem(tag, difficulty):
    skip_data = load_skip_data()
    if tag not in skip_data:
        skip_data[tag] = {d: 0 for d in VALID_DIFFICULTIES}
    skip_count = skip_data[tag][difficulty]
    url = f"https://alfa-leetcode-api.onrender.com/problems?tags={tag}&difficulty={difficulty}&limit=1&skip={skip_count}"
    res = requests.get(url, timeout=10)
    if res.status_code != 200:
        return None
    data = res.json()
    problems = data.get("problemsetQuestionList", [])
    if not problems:
        skip_data[tag][difficulty] = 0
        save_skip_data(skip_data)
        return get_problem(tag, difficulty)
    skip_data[tag][difficulty] += 1
    save_skip_data(skip_data)
    return problems[0]

@bot.event
async def on_ready():
    await bot.tree.sync(guild=None)
    print(f'Logged in as {bot.user}')

async def topic_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=tag, value=tag) for tag in VALID_TAGS if current.lower() in tag.lower()]

async def difficulty_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=diff, value=diff) for diff in VALID_DIFFICULTIES if current.lower() in diff.lower()]

@bot.tree.command(name="daily", description="hehe have fun")
@app_commands.describe(topic="choose topic", difficulty="choose difficulty")
@app_commands.autocomplete(topic=topic_autocomplete, difficulty=difficulty_autocomplete)
async def daily(interaction: discord.Interaction, topic: str, difficulty: str):
    topic = topic.lower()
    difficulty = difficulty.upper()
    if topic not in VALID_TAGS:
        await interaction.response.send_message(f"Invalid topic. Choose from: {', '.join(VALID_TAGS)}")
        return
    if difficulty not in VALID_DIFFICULTIES:
        await interaction.response.send_message(f"Invalid difficulty. Choose from: {', '.join(VALID_DIFFICULTIES)}")
        return
    problem = get_problem(topic, difficulty)
    if problem:
        title = problem["title"]
        diff = problem["difficulty"]
        slug = problem["titleSlug"]
        link = f"https://leetcode.com/problems/{slug}/"
        await interaction.response.send_message(f"{title} ({diff}) {link}")
    else:
        await interaction.response.send_message("not found")

bot.run(token)
