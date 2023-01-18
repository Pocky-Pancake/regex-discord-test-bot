import nextcord, os, re
from dotenv import load_dotenv

load_dotenv()

test_channel_id = os.getenv('TARGET')

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)

open("last_regex", "a").close()

@client.event
async def on_ready():
    print("bot ready")

@client.event
async def on_message(message):
    if message.channel.id == test_channel_id:
        f = open("last_regex", "r")
        try :
            regex_match = re.search(rf"{f.readline()}", message.content)
            if regex_match:
                embed = nextcord.Embed(title="Match found!", description=f"{regex_match}", color=0xe34234)
                embed.add_field(name="Span:", value=f"{regex_match.span()}", inline=False)
                embed.add_field(name="Group:", value=f"{regex_match.group()}", inline=False)
                embed.set_footer(text=f"String: {regex_match.string()}")
            else:
                embed = nextcord.Embed(title="Match not found!", description="No match.", color=0x3cb371)
        except:
            pass
        else:
            print("regex match failed")
            message.channel.send("regex match failed")
        f.close()

@client.slash_command(description="Change the current regex checker value.")
async def set_regex(interaction:nextcord.Interaction, regex:str = nextcord.SlashOption(description="Regex")):
    f = open("last_regex", "w")
    f.write(regex)
    f.close()
    await interaction.response.send_message(f"Regex set to `{regex}`.")

@client.slash_command(description="Check current regex checker value.")
async def check_regex(interaction:nextcord.Interaction):
    f = open("last_regex", "r")
    regex = f.readline()
    f.close()
    await interaction.response.send_message(f"Current regex is set to `{regex}`.")
