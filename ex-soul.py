import discord, json, time, os, difflib
current_time = time.strftime("%H:%M:%S", time.localtime())
data = json.load(open(os.path.dirname(os.path.abspath(__file__))+'\\resources\\database.json')); client = discord.Client()
auth = json.load(open(os.path.dirname(os.path.abspath(__file__))+'\\resources\\config.json'))
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
def rcon(pack):
        match pack[1]:
            case "txt":
                return pack[0]
            case "cmd":
                match pack[2]: 
                    case "test":
                        os.system("echo:")
                        os.system("echo Test passed!")
                    case _:
                        os.system(pack[2])
                return pack[0]
            case "format":
                match pack[2]:
                    case "time":
                        quary=current_time
                    case _:
                        con=0.8
                        for mem in data["memory"]:
                            package=[data["memory"].get(mem).split(";"),difflib.SequenceMatcher(None, pack[2], mem).ratio()]
                            if package[1] > con:
                                con=package[1]
                                quary=package[0]
                return str(pack[0]).format(quary)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content:
        con=0.8
        dct=0.7
        for responses in data["phrases"]["responses"]:
            package=[data["phrases"]["responses"].get(responses).split(";"),difflib.SequenceMatcher(None, message.content.lower(), responses).ratio()]
            if package[1] > con:
                con=package[1]
                await message.channel.send(rcon(package[0]))
        #for cmd in data["phrases"]["commands"]:
        #    package=[message.content.split(";"),data["phrases"]["commands"].get(cmd).split(";")]
        #    if package[0][0] == package[1][0]:
        #        match package[0][0]:
        #            case "run":
        #                os.system(package[0][1])
        #                await message.channel.send(package[1][1])
        for words in data["words"]:
            for det in message.content.split():
                Sim=difflib.SequenceMatcher(None, det, words).ratio()
                if Sim > dct:
                    dct=Sim
                    await message.delete()
                    await log(message)
client.run(auth["client"].get("token"))