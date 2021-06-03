import discord
from discord.ext import commands
import random

KURT = 'georgiboi' #KURT is the username the bot scans for
answered = False # switch for asking KURT only once
closed = False # swtich to stop most commands being made
yes = ("yes", "Yes", "yes.", "Yes.", "yea", "yea.", "Yea", "Yea.", "yep", "yep.", "Yep", "Yep.")
no = ("no", "no.", "No", "No.", "nope", "nope.", "Nope.", "Nope", "nah", "nah.", "Nah." "Nah")


intents = discord.Intents.default() # setting intents for the bot
intents.members = True # intents also needed to be changed in bot page
intents.presences = True # if theyre changed here

#initialise bot for commands (replaces client) and add help
bot = commands.Bot(command_prefix='?', intents=intents)
help = commands.DefaultHelpCommand()
bot.help_command = help

def get_url(): # gets a new url by stopping at a random number of lines from file
    f = open("urls", "r")
    rand = random.randint(1, 16)
    print("lawnmower number: {}".format(rand))
    for i in range(1, rand):
        url = f.readline()
    f.close()
    # if url not set, get another url
    if not url:
        url=get_url()
    return url


class Events(commands.Cog): # Events class lets me use self variable
    def __init__(self, bot): # constructor
        self.bot = bot

# define bot events
    @commands.Cog.listener()
    async def on_ready(self): #prints ready in console when ready
        print('ready')

    @commands.Cog.listener()
    async def on_member_update(self, before, after): # wait for KURT online
        if closed:
            return
        else:
            global answered
            if KURT in after.name and 'online' in after.status:
                answered = False
                channel = after.guild.get_channel(846695050427498506)
                await channel.send('Hey Kurt, wanna buy a lawnmower? [yes/no]')

    @commands.Cog.listener()
    async def on_message(self, message): # dialogue with KURT
        if closed:
            return
        else:
            global answered
            if not answered:
                # if KURT says yes
                if KURT in message.author.name and message.content in yes:
                    answered = True
                    image = discord.Embed()
                    url=get_url()
                    image.set_image(url=url)
                    await message.channel.send(':partying_face: That\'s great!\nKurt is now a proud owner of his own lawnmower!! :partying_face:', embed=image)

                    # if KURT says no
                elif KURT in message.author.name and message.content in no:
                    answered = True
                    await message.channel.send('thats cool :upside_down:') # add on an emoji here

# define bot commands
    @commands.command()
    async def leave(self, ctx): # ?leave - makes him go away temporarily
        """Makes the bot leave the channel.
        """
        await ctx.channel.send("I'll be off then :(")
        global closed
        closed = True

    @commands.command()
    async def comeback(self, ctx): # ?comeback makes the bot come back
        """asks him to come back
        """
        global closed
        closed = False
        await ctx.channel.send("iiiim bbaaacckk")

    @commands.command()
    async def status(self, ctx): # ?status - gives the answered bool
        """Check if the salesman is willing to sell.
        """
        if closed:
            return
        else:
            if not answered:
                await ctx.channel.send("Waiting for a response...")
            else:
                await ctx.channel.send("I have nothing else to say.")

    @commands.command()
    async def inquire(self, ctx): # ?inquire - asks if that person wants to buy a lawnmower too
        """Inquire on a lawnmower yourself.
        """
        if closed:
            return
        else:
            user = ctx.author
            image = discord.Embed()
            url=get_url()
            image.set_image(url=url)
            to_send = ':partying_face: That\'s great!\n{} is now a proud owner of their own lawnmower!! :partying_face:'.format(user)
            await ctx.channel.send(to_send, embed=image)


@bot.command()
async def logoff(ctx): # ?logoff - closes the bot
    """closes the bot
    """
    await ctx.channel.send("bye bye :wave:")
    await ctx.bot.close()


# beefing up the security with a token read from a file
token_file = open("token_file", "r")
token = token_file.readline()
token_file.close()

#add Events Cog to bot
bot.add_cog(Events(bot))
bot.run(token)
