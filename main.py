import nextcord, os, re
from dotenv import load_dotenv

load_dotenv()

test_channel_id = int(os.getenv('TARGET'))
log_channel_id = int(os.getenv('LOG'))

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)

open("last_regex", "a").close()

async def doLog(content):
    print(content)
    log_channel = await client.fetch_channel(log_channel_id)
    await log_channel.send(content=content)

@client.event
async def on_application_command_error(ctx, error):
    error = getattr(error, "original", error)
    raise error
    await doLog(error)

@client.event
async def on_ready():
    print("bot ready")

@client.event
async def on_message(message):
    if message.channel.id == test_channel_id and not message.author.bot:
        await doLog("found message")
        f = open("last_regex")
        try:
            regex_match = re.search(f"{f.readline()}", message.content)
            if regex_match:
                await doLog("found regex match")
                embed = nextcord.Embed(title="Match found!", description=f"{regex_match}", color=0x3cb371)
                embed.add_field(name="Span:", value=f"{regex_match.span()}", inline=False)
                embed.add_field(name="Group:", value=f"{regex_match.group()}", inline=False)
                embed.set_footer(text=f"String: {message.content}")
                await message.channel.send(embed=embed)
            else:
                await doLog("regex match not found")
                embed = nextcord.Embed(title="Match not found!", description="No match.", color=0xe34234)
                await message.channel.send(embed=embed)
        except:
            await doLog("regex match failed")
            await message.channel.send("regex match failed")
        f.close()

@client.slash_command(description="Change the current regex checker value.")
async def set_regex(interaction:nextcord.Interaction, regex:str = nextcord.SlashOption(description="Regex")):
    f = open("last_regex", "w")
    f.write(regex)
    f.close()
    await doLog(f"Regex set to `{regex}`.")
    await interaction.response.send_message(f"Regex set to `{regex}`.")

@client.slash_command(description="Check current regex checker value.")
async def check_regex(interaction:nextcord.Interaction):
    f = open("last_regex", "r")
    regex = f.readline()
    f.close()
    await doLog("/check_regex called.")
    await interaction.response.send_message(f"Current regex is set to `{regex}`.")

client.run(os.getenv('TOKEN'))
