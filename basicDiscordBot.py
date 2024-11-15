import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        try:
            guild = discord.Object(id="ENTER SERVER ID")
            await self.tree.sync(guild=guild)
            print("Slash commands synchronized")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("Hello"):
            await message.channel.send(f"Hello there {message.author}")
        if message.content.startswith("hello"):
            await message.channel.send(f"Hello there {message.author}")


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='-', intents=intents) # Used for slash commands

GUILD_ID = discord.Object(id="ENTER SERVER ID")

@client.tree.command(name="greet", description="Greets the user", guild=GUILD_ID)
async def greet(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

@client.tree.command(name="printer", description="I will print what you say", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="kick", description="Kick a user from the server", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True)    # Restricted to people with a role of "Administrator" only
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if member.guild_permissions.administrator:
        await interaction.response.send_message(f"Cannot ban another admin.", ephemeral=True)
        return

    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.display_name} has been kicked. Reason: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Can't kick {member.display_name}. Error: {e}", ephemeral=True)

@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You can't use this command", ephemeral=True)

@client.tree.command(name="ban", description="Ban a user from the server", guild=GUILD_ID)
@app_commands.checks.has_permissions(administrator=True) # Only admins can use this command
async def ban(interaction: discord.Interaction ,member: discord.Member, reason: str = "No reason"):
    if member.guild_permissions.administrator:
        await interaction.response.send_message(f"Cannot ban an admin.", ephemeral=True)
        return
    
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.display_name} has been banned for the following reason: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Couldnt ban the member. Error: {e}", ephemeral = True)

@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You dont have permission to use this command")

@client.tree.command(name="avatar", description="Get a member's avatar", guild=GUILD_ID)
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)

    await interaction.response.send_message(embed=embed)

client.run('ENTER DISCORD BOT TOKEN')
