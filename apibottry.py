import discord, requests

TOKEN = ""
bot = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {bot.user}")

@tree.command(name="daily", description="Fetch test problem")
async def daily(interaction: discord.Interaction):
    url = "https://alfa-leetcode-api.onrender.com/problems?tags=array&limit=1"
    res = requests.get(url).json()

    if "problemsetQuestionList" in res and res["problemsetQuestionList"]:
        p = res["problemsetQuestionList"][0]
        title = p["title"]
        diff = p["difficulty"]
        slug = p["titleSlug"]
        link = f"https://leetcode.com/problems/{slug}/"
        await interaction.response.send_message(f"{title} ({diff}) {link}")
    else:
        await interaction.response.send_message("No problem fetched.")

bot.run(TOKEN)
