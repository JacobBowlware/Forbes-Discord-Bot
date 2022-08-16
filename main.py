import discord, requests, random

# Discord bot 'api':
TOKEN = 'classified'
client = discord.Client()

# Add commas to the Networth Value:
def get_number(networth):
    return ("{:,}".format(networth))


# Gather Desired Forbes Info:
def get_forbes(y, x=0):
    request_url = f"https://forbes400.herokuapp.com/api/forbes400?limit={y}"
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        # Loop through x (number of forbes memebers desired) and store into list:
        res = ''
        for i in range(x, y):
            name = data[i]['person']['name']
            networth = get_number(int(data[i]['finalWorth']) * 1000000)
            rank = data[i]['rank']
            res += (f'Name: {name} - NetWorth: ${networth} - Rank: {rank}\n')
        return res    
    else:
        return 'Error 2'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Process initial data:
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    # Result Message Layouts/Make command easier to work with:
    random_layout = False
    single_layout = False
    user_command = user_message.split(' ')

    # Stops Bot from Replying to itself:
    if message.author == client.user:
        return

    # Ensures Bot will only be able to respond to messages in 'General' Chat
    if channel == 'general':
        if user_message.lower() == '!f':
            # Forbes_Bot Cheat Sheet:
            await message.channel.send("""
    - !f x,y -
x - List Start Point (Optional)
y - List End Point
Ex: 
    !f 0,10 - Returns Top 10
    !f 10 - Returns Top 10
    !f 390,400 - Returns Last 10
    (Minimum x value of 0, Max y value of 400)
    (Each range must be limited to 30, such that y - x <= 30)
!f random - Random Forbes400 Member
!f limits
!f - Help
    """)
        # If there is more to the command that !f -> Check if desire is 'random', or top x,y:
        elif user_command[0].lower() == '!f':
            if user_message.lower() == '!f random':
                random_layout = True
                rand_num = random.randint(0, 400)
                result = get_forbes(rand_num, rand_num - 1)
            elif user_message.lower() == 'limits':
                await message.channel.send("""Due to Discord's 2,000 character limit majority of searches will be limited to 30 Forbes members or fewer.""")
            else:
                # Check if user_command is valid:
                try:
                    # Check if user_command desires x,y input:
                    try:
                        user_command = user_command[1].split(',')
                        if int(user_command[0]) > 400 or int(user_command[0]) > int(user_command[1]) or int(user_command[0]) < 0:
                            await message.channel.send("Invalid Input or Input is too large for Discord to Handle... Please limit each search to a total of 30 Forbes Members... See '!f' for more info.")
                            return
                        result = get_forbes(int(user_command[1]), int(user_command[0]))
                    except IndexError:
                        # User Only Used 1 Input
                        single_layout = True
                        result = get_forbes(int(user_command[0]))
                # User Entered no valid inputs:
                except ValueError:
                    await message.channel.send("Invalid Input... Use '!f' for assistance.")
                    return
            # Decide which layout to send the response back in:
            if random_layout:
                await message.channel.send(f"""Random Forbes400:
{result}""")
            elif single_layout:
                await message.channel.send(f"""Top {user_command[0]} Forbes:
{result}""")
            else:
                await message.channel.send(f"""Forbes {int(user_command[0])} - {int(user_command[1])}:
{result}""")
        return


client.run(TOKEN)
