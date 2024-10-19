import os
import json
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="/app/src/config/.env")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

with open("/app/src/bad_words.json", "r") as file:
    bad_words_data = json.load(file)
    bad_words = bad_words_data.get("bad_words", [])

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = discord.utils.get(bot.guilds)
    if guild:
        existing_channel = discord.utils.get(guild.text_channels, name="staff-bot-alerts")
        if not existing_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True),
                discord.utils.get(guild.roles, permissions=discord.Permissions(administrator=True)): discord.PermissionOverwrite(view_channel=True)
            }
            await guild.create_text_channel("staff-bot-alerts", overwrites=overwrites)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for bad_word in bad_words:
        if bad_word in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message contained a word that is not allowed and has been removed.")
            alerts_channel = discord.utils.get(message.guild.text_channels, name="staff-bot-alerts")
            if alerts_channel:
                await alerts_channel.send(f"Warning: {message.author.mention} used inappropriate language in {message.channel.mention}.")
            return

    await bot.process_commands(message)

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not member.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been kicked from the server.", ephemeral=True)
        alerts_channel = discord.utils.get(interaction.guild.text_channels, name="staff-bot-alerts")
        if alerts_channel:
            await alerts_channel.send(f"{member.mention} was kicked by {interaction.user.mention}. Reason: {reason}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you cannot kick {member.mention} because they have kick permissions.", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not member.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been banned from the server.", ephemeral=True)
        alerts_channel = discord.utils.get(interaction.guild.text_channels, name="staff-bot-alerts")
        if alerts_channel:
            await alerts_channel.send(f"{member.mention} was banned by {interaction.user.mention}. Reason: {reason}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you cannot ban {member.mention} because they have ban permissions.", ephemeral=True)

@bot.tree.command(name="mute", description="Mute a member in the server")
@app_commands.checks.has_permissions(manage_roles=True)
async def mute(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await interaction.guild.create_role(name="Muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)

    if mute_role in member.roles:
        await interaction.response.send_message(f"{member.mention} is already muted.", ephemeral=True)
    else:
        await member.add_roles(mute_role, reason=reason)
        await interaction.response.send_message(f"{member.mention} has been muted.", ephemeral=True)
        alerts_channel = discord.utils.get(interaction.guild.text_channels, name="staff-bot-alerts")
        if alerts_channel:
            await alerts_channel.send(f"{member.mention} was muted by {interaction.user.mention}. Reason: {reason}")

bot.run(TOKEN)
