import discord, json, time, os
from difflib import SequenceMatcher
current_time = time.strftime("%H:%M:%S", time.localtime())
if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\resources\\database.json')&os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\resources\\config.json'):
    print("Resource files found; loading contents.")
else:
    print("One or more resources files were not found; Generating files needed.")
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\resources\\database.json'):
        open(os.path.dirname(os.path.abspath(__file__))+'\\resources\\database.json', "w")
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\resources\\config.json'):
        open(os.path.dirname(os.path.abspath(__file__))+'\\resources\\config.json', "w")
    print("Please configurate new resource files; automatic filling coming soon")
    print()
data = json.load(open(os.path.dirname(os.path.abspath(__file__))+'\\resources\\database.json')); client = discord.Client()
auth = json.load(open(os.path.dirname(os.path.abspath(__file__))+'\\resources\\config.json'))
@client.event
async def rcon(message,responses): #Check for commands
    if ':' in responses:
        match responses:
            case "I can respond to the following messages:":
                await message.channel.send(data["library"])
            case "It is currently:":
                await message.channel.send(str(current_time))
            case "Sending virual hug now:":
                await message.channel.send("https://tenor.com/view/hugging-son-of-abish-abish-mathew-rohan-joshi-virtual-hug-gif-20096755")
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity = discord.Game('around with code'))
def emoji(requested):
    match requested:
        case "broken heart":
            return "\N{BROKEN HEART}"
async def log(message):
    if auth.get("archive_channel"):
        archive = client.get_channel(int(auth.get("archive_channel")))
        await archive.send("Deleted message by: "+message.author.name+"; ||"+message.content+"||; Time of deletion: "+current_time); emoji("broken heart")
        print("DEL; $: "+message.author.name+"; Content: "+message.content+"; Time of deletion: "+current_time)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content:
        new=0.8
        dct=0.75
        for responses in data["library"]:
            Sim=SequenceMatcher(None, message.content.lower(), responses).ratio()
            if Sim > new:
                new=Sim
                print("RE; "+current_time+"; $: "+str(message.author)+"; MSG: "+data["library"].get(responses))
                time.sleep(0.8)
                await message.channel.send(data["library"].get(responses))
                await rcon(message,data["library"].get(responses))
        for words in data["words"]:
            for det in message.content.split():
                Sim=SequenceMatcher(None, det, words).ratio()
                if Sim > dct:
                    dct=Sim
                    await message.delete()
                    await log(message)
client.run(auth["client"].get("token"))