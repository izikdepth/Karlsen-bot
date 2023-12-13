import discord
from discord.ext import commands, tasks
import requests

intents = discord.Intents(guilds=True)
client = discord.Client(intents=intents)
intents.members = True

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id =  #price feed channel
        self.bot.ready = False
        self.update_kls_price.start() 
        
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.ready = True
            print(f'Bot is ready. Channel ID: {self.channel_id}')
            
    @tasks.loop(minutes=1)  # Update every minute
    async def update_kls_price(self):
        try:
            if not self.bot.ready or self.channel_id is None: # Don't do anything if the bot isn't ready or the channel hasn't been set
                return

            channel = self.bot.get_channel(int(self.channel_id)) # Make sure to convert the channel ID to an integer

            if channel is None:
                print(f'Could not find channel with ID {self.channel_id}')
                return

            # Fetch Bitcoin price
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=karlsen&vs_currencies=usd')
            data = response.json()

            # Extract the price
            price = data['karlsen']['usd']

            # Update the channel's name with the price
            await channel.edit(name=f"Karlsen : ${price}")

            # Set the bot's status
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Price: ${price}"))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the Bitcoin price: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


        


"""
set up bot and register the cog to the bot
"""
def setup(bot):
    bot.add_cog(stats(bot))