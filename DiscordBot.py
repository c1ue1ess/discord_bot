import discord
import random

#KURT is the username the bot scans for
KURT = 'georgiboi'
# answered bool stops bot from asking KURT more than once each time he comes online
answered = False

#gets a new url by reading a random number of lines from file
def get_url():
    f = open("urls", "r")
    rand = random.randint(1, 16)
    for i in range(1, rand):
        url = f.readline()
    f.close()
    return url

class MyClient(discord.Client):
    #prints ready in console when ready
    async def on_ready(self):
        print('ready')

    #if username is KURT and status is online ask if want to buy a lawnmower
    async def on_member_update(self, before, after):
        global answered
        if KURT in after.name and 'online' in after.status:
            answered = False
            await client.get_channel(846695050427498506).send('Hey Kurt, wanna buy a lawnmower? [yes/no]')

    async def on_message(self, message):
        global answered
        if not answered:
            # if KURT says yes
            if KURT in message.author.name and 'yes' in message.content:
                answered = True

                # send "Thats great [IMAGE] kurt is now a proud owner of x lawnmower" then wait for next online
                image = discord.Embed()
                image.set_image(url=get_url())
                await message.channel.send(':partying_face: That\'s great!\nKurt is now a proud owner of his own lawnmower!! :partying_face:', embed=image)

                # if KURT says no
            elif KURT in message.author.name and 'no' in message.content:
                answered = True

                await message.channel.send('thats cool :upside_down:') # add on an emoji here

                # if message author the same as the bot account return, stops infinite looping
            elif message.author == self.user:
                return


# setting intents for the bot (adding presence to defaults)
# intents also needed to be changed in bot page
intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = MyClient(intents=intents)

# beefing up the security with a token read from a file on the ssd instead of hard coding it in
token_file = open("token_file", "r")
token = tokenfile.readline()
token_file.close()
client.run(token)
