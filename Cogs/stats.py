import discord
from discord.ext import commands, tasks
import requests
from datetime import datetime

intents = discord.Intents(guilds=True)
client = discord.Client(intents=intents)
intents.members = True

def format_marketcap(marketcap):
    million = 1000000
    billion = 1000000000

    if marketcap < million:
        return f"${marketcap / 1000:.1f}K"
    elif marketcap < billion:
        return f"${marketcap / million:.1f}M"
    else:
        return f"${marketcap / billion:.1f}B"
    
def format_circulating_supply(circulating_supply):
    billion = 1000000000
    million = 1000000

    if circulating_supply >= billion:
        return f"{circulating_supply / billion:.3f}B kls"
    elif circulating_supply >= million:
        return f"{circulating_supply / million:.3f}M kls"
    else:
        return f"{circulating_supply:,.0f} kls"

    



class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = #price feed channel
        self.hashrate_channel =1187905364482588743 # hashrate feed channel
        self.marketcap_channel =1187905657916117102 #marketcap feed channel
        self.circulating_supply_channel =1187905947927064627 #circulating supply feed channel
        self.current_reward_channel =1187906295697784883 #current reward channel
        self.halving_channel=1187906650338762772 #halving feed channel
        self.bot.ready = False
        self.update_kls_price.start() 
        self.update_hashrate.start()
        self.update_marketcap.start()
        self.update_circulating_supply.start()
        self.update_current_reward.start()
        self.update_next_halving.start()
        
        
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
            response = requests.get('https://api.karlsencoin.com/info/price?stringOnly=false')
            data = response.json()

            # Extract the price
            price = data['price']

            # Update the channel's name with the price
            await channel.edit(name=f"Price: ${price}")

            # Set the bot's status
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Price: ${price}"))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the Kalrsen price: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            
    @tasks.loop(minutes=1)
    async def update_marketcap(self):
        try:
            if not self.bot.ready or self.marketcap_channel is None:
                return

            channel = self.bot.get_channel(int(self.marketcap_channel))

            if channel is None:
                print(f'Could not find channel with ID {self.marketcap_channel}')
                return
            
            response = requests.get('https://api.karlsencoin.com/info/marketcap?stringOnly=false')
            data = response.json()
            
            marketcap = data['marketcap']
            
            formatted_marketcap = format_marketcap(marketcap)

            await channel.edit(name=f"MCap: {formatted_marketcap}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the market cap: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            
    
    @tasks.loop(minutes=1)
    async def update_circulating_supply(self):
        try:
            if not self.bot.ready or self.circulating_supply_channel is None:
                return

            channel = self.bot.get_channel(int(self.circulating_supply_channel))

            if channel is None:
                print(f'Could not find channel with ID {self.circulating_supply_channel}')
                return
            
            response = requests.get('https://api.karlsencoin.com/info/coinsupply/circulating?in_billion=false')
            data = response.json()

            # print("Response data:", data)  # Print response data for debugging

            if isinstance(data, (int, float)):
                circulating_supply = data
            elif isinstance(data, dict):
                circulating_supply = data.get('circulating')
            else:
                print("Unexpected data type:", type(data))
                return

            if circulating_supply is not None:
                formatted_circulating_supply = format_circulating_supply(circulating_supply)
                await channel.edit(name=f"cir.Supply: {formatted_circulating_supply}")
            else:
                print("Missing 'circulating' key in response data.")

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


            
            
    @tasks.loop(seconds=30)
    async def update_hashrate(self):
        try:
            if not self.bot.ready or self.hashrate_channel is None: # Don't do anything if the bot isn't ready or the channel hasn't been set
                return

            channel = self.bot.get_channel(int(self.hashrate_channel)) # Make sure to convert the channel ID to an integer

            if channel is None:
                print(f'Could not find channel with ID {self.hashrate_channel}')
                return
            
            response = requests.get('https://api.karlsencoin.com/info/hashrate?stringOnly=false')
            data = response.json()
            
            hashrate = data['hashrate']
            
            formatted_hashrate = "{:.2f}".format(hashrate)

            await channel.edit(name=f"Hashrate: {formatted_hashrate}TH/s")
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the hashrate: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            
    
    @tasks.loop(seconds=30)
    async def update_current_reward(self):
        try:
            if not self.bot.ready or self.current_reward_channel is None:
                return

            channel = self.bot.get_channel(int(self.current_reward_channel))

            if channel is None:
                print(f'Could not find channel with ID {self.current_reward_channel}')
                return

            response = requests.get('https://api.karlsencoin.com/info/blockreward?stringOnly=false')
            data = response.json()

            # print("Response data:", data)  # Print response data for debugging

            current_rewards = data.get('blockreward')  # Use .get() to handle potential missing key

            if current_rewards is not None:
                await channel.edit(name=f"cRewards: {current_rewards}kls/min")
            else:
                print("Missing 'blockreward' key in response data.")

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

            
    @tasks.loop(minutes=10)
    async def update_next_halving(self):
        try:
            if not self.bot.ready or self.halving_channel is None:
                return

            channel = self.bot.get_channel(int(self.halving_channel))

            if channel is None:
                print(f'Could not find channel with ID {self.halving_channel}')
                return
            
            response = requests.get('https://api.karlsencoin.com/info/halving')
            data = response.json()
            
            next_halving_str = data.get('nextHalvingDate')
            next_halving_dt = datetime.strptime(next_halving_str, '%Y-%m-%d %H:%M:%S %Z')
            next_halving = next_halving_dt.strftime('%d/%m/%Y')
            
            await channel.edit(name=f"halving: {next_halving}")

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")



"""
set up bot and register the cog to the bot
"""
def setup(bot):
    bot.add_cog(stats(bot))
    
    
