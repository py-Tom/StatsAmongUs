# StatsAmongUs
Discord bot that collects statistics from Among Us. It takes printscreen of stats table form the game and uses optical character recognition for excracting information. Next it puts it into local database and sends graphs back to player.

<img src="/_/stats.png" height="280" width="262" />  <img src="/_/graph.png" height="280" width="670" />

# How to use
* Clone this repo
* Install OCR-tessaract https://github.com/tesseract-ocr/tesseract
* Install Orca https://github.com/plotly/orca
* Install other requirements `pip install -r requirements.txt`
* Create own discord bot https://discord.com/developers/applications
* Copy Token and paste it into discord_bot.py file
* Add bot to your discord channel
* Run db_operations.py to create new database
* Run discord_bot.py and wait until bot will appear online
* Bot will now collect stats into db and send graphs.

<img src="/_/discord.png" />
