import discord
from discord.ext import commands
from discord import app_commands
import requests

token = ""

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

VALID_TAGS = ["array", "linked-list", "stack",  "string"]

def get_problem(tag):
    url = f"https://alfa-leetcode-api.onrender.com/problems?tags={tag}&limit=1"
    res = requests.get(url).json()
    if "problemsetQuestionList" in res and res["problemsetQuestionList"]:
        return res["problemsetQuestionList"][0]
    return None

@bot.event
async def on_ready():
    await bot.tree.sync(guild=None)  
    print(f'Logged in as {bot.user}')


async def topic_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=tag, value=tag)
        for tag in VALID_TAGS if current.lower() in tag.lower()
    ]

@bot.tree.command(name="daily", description="hehe have fun")
@app_commands.describe(topic="choose topic")
@app_commands.autocomplete(topic=topic_autocomplete)
async def daily(interaction: discord.Interaction, topic: str):
    topic = topic.lower()
    if topic not in VALID_TAGS:
        await interaction.response.send_message(
            f"Invalid topic. Choose from: {', '.join(VALID_TAGS)}"
        )
        return

    problem = get_problem(topic)
    if problem:
        title = problem["title"]
        diff = problem["difficulty"]
        slug = problem["titleSlug"]
        link = f"https://leetcode.com/problems/{slug}/"
        await interaction.response.send_message(f"{title} ({diff}) {link}")
    else:
        await interaction.response.send_message("not found")

bot.run(token)
