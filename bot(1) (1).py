import os
import random

import discord
from discord import app_commands

# ============================================================
# CONFIG
# ============================================================

# Set your Discord bot token as an environment variable:
# Windows CMD:
#   set DISCORD_TOKEN=YOUR_BOT_TOKEN
#
# PowerShell:
#   $env:DISCORD_TOKEN="YOUR_BOT_TOKEN"
#
# IMPORTANT: Never put your real bot token directly in this file.
TOKEN = os.getenv("DISCORD_TOKEN")

# Optional:
# Put your Discord SERVER ID here for instant slash-command updates.
# Example:
# GUILD_ID = 123456789012345678
#
# Leave it as 0 to sync the command globally.
GUILD_ID = 0


# ============================================================
# BOT
# ============================================================

class ShipBot(discord.Client):
    def __init__(self):
        # members intent is needed to read the server member list.
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        if GUILD_ID:
            # Guild commands appear much faster while testing.
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print("Slash commands synced to the test server.")
        else:
            await self.tree.sync()
            print("Global slash commands synced.")


bot = ShipBot()


# ============================================================
# READY EVENT
# ============================================================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")


# ============================================================
# /ship COMMAND
# ============================================================

@bot.tree.command(
    name="ship",
    description="Randomly ship two members together!"
)
async def ship(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used inside a Discord server.",
            ephemeral=True
        )
        return

    # Get non-bot members.
    members = [
        member
        for member in guild.members
        if not member.bot
    ]

    if len(members) < 2:
        await interaction.response.send_message(
            "❌ At least 2 members are needed to create a ship.",
            ephemeral=True
        )
        return

    # Pick two different members randomly.
    person1, person2 = random.sample(members, 2)

    # Random compatibility score.
    percentage = random.randint(1, 100)

    if percentage >= 90:
        message = "🔥 Perfect match!"
    elif percentage >= 70:
        message = "💕 Pretty good match!"
    elif percentage >= 40:
        message = "💫 Maybe there is something here..."
    else:
        message = "😂 This ship is going to be interesting!"

    embed = discord.Embed(
        title="💘 SHIP MATCH",
        description=(
            f"💖 **{person1.display_name} × {person2.display_name}**\n\n"
            f"💞 Compatibility: **{percentage}%**\n\n"
            f"{message}"
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    )

    embed.set_footer(
        text=f"Shipped by {interaction.user.display_name}"
    )

    await interaction.response.send_message(embed=embed)


# ============================================================
# START BOT
# ============================================================

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is missing. Set your Discord bot token "
        "as an environment variable before starting the bot."
    )

bot.run(TOKEN)
