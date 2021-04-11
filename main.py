from epicstore_api.api import EpicGamesStoreAPI as API 
import telebot
import time
import json
import datetime
from dateutil import parser

bot = telebot.TeleBot(open('./token.cred', 'r').readline().replace('\n', ''))
chat_id = -1001190014655 #Replace with your channel ID

prev_free_games = []

while True:
    free_games = API(country="RU").get_free_games()["data"]["Catalog"]['searchStore']["elements"]
    for g in free_games:
        title = g['title']
        release_date = g["effectiveDate"].replace('Z', '').replace('T', " ")[:-4]
        image = 'https://raw.githubusercontent.com/HoolyPanda/egs-giveaways/main/kojimba.png'
        for i in g['keyImages']:
            if i['type'] == "Thumbnail":
                image = i['url']
                break
        game_object = {"title": title, "release_date": release_date, "image": image}
        if game_object['title'] not in list(map(lambda x: x['title'], prev_free_games)):
            prev_free_games.append(game_object)
            # if image == ''
            msg = f"New giveaway appeared\n{game_object['title']}\nat\n{game_object['release_date']}!\n"
            bot.send_photo(chat_id,game_object['image'], caption=msg)
        for game in prev_free_games:
            if game['title'] == game_object['title']:
                if game['release_date'] != game_object['release_date']:
                    for i, j in enumerate(prev_free_games):
                        if j["title"] == game_object['title']:
                            prev_free_games.pop(i)
                            prev_free_games.append(game_object)
                            break
                    msg = f"The giveaway date of game \n{game_object['title']}\nhas changed to\n{game_object['release_date']}!\n"
                    bot.send_photo(chat_id,game_object['image'], caption=msg)
                    pass
        n = list(map(lambda x: x['release_date'] if (x['title'] == game_object['title']) else False, prev_free_games))
        game_date = g["effectiveDate"].replace('Z', '').replace('T', " ")[:-4]
        game_date = parser.parse(game_date)
        today = datetime.datetime.now()
        if game_date.year == today.year and game_date.month == today.month and game_date.day == today.day:
            if game_date.hour == today.hour:
                msg = f"{game_object['title']}'s giveaway starts now!"
                bot.send_photo(chat_id,game_object['image'], caption=msg)
    time.sleep(3600)