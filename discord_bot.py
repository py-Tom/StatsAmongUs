import discord
import os
from save_stats import save_stats
from graph import graph_it
from db_operations import select_entry
import cv2
import numpy as np

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return None

    if message.channel.name == "channel name":  # paste channel name
        if message.attachments and message.content.startswith("$stats"):
            print(f"Got attachment: {message.attachments}")
            for attachment in message.attachments:
                file_name = f"temp/{message.author.name}_{attachment.filename}"
                await attachment.save(file_name)
                save_stats(file_name, str(message.author))
                data = select_entry(str(message.author))
                graph_it(data)
                channel = client.get_channel("channel id")  # paste channel id
                await channel.send(f"{message.author.mention}'s Stats:")
                img1 = cv2.imread(f"temp/fig_sankey_{message.author.name}.png")
                img2 = cv2.imread(f"temp/fig_winrate_{message.author.name}.png")
                vis = np.concatenate((img1, img2), axis=1)
                cv2.imwrite(f"temp/out{message.author.name}.png", vis)
                await channel.send(
                    file=discord.File(f"temp/out{message.author.name}.png")
                )
                #  await channel.send(file=discord.File(f"temp/fig_sankey_{message.author.name}.png"))
                #  await channel.send(file=discord.File(f'temp/fig_winrate_{message.author.name}.png'))
                os.remove(f"temp/fig_winrate_{message.author.name}.png")
                os.remove(f"temp/fig_sankey_{message.author.name}.png")
                os.remove(f"temp/out{message.author.name}.png")
                os.remove(file_name)


client.run("PASTE-TOKEN-HERE")  # paste token here
