from epicstore_api.api import EpicGamesStoreAPI as API 
import telebot
import time
import json
import datetime

bot = telebot.TeleBot(open('./token.cred', 'r').readline().replace('\n', ''))
chat_id = -1001190014655 #Replace with your channel ID

prev_free_games = []

while True:
    free_games = API(country="RU").get_free_games()["data"]["Catalog"]['searchStore']["elements"]
    for g in free_games:
        title = g['title']
        release_date = g["effectiveDate"]
        image = ''
        for i in g['keyImages']:
            if i['type'] == "Thumbnail":
                image = i['url']
                break
        game_object = {"title": title, "release_date": release_date, "image": image}
        if game_object['title'] not in list(map(lambda x: x['title'], prev_free_games)):
            prev_free_games.append(game_object)
            # if image == 
            msg = f"New giveaway game appeared\n{game_object['title']}\nat\n{game_object['release_date']}!\n"
            bot.send_photo(chat_id,game_object['image'], caption=msg)
        elif game_object['release_date'] != map(lambda x: x['release_date'] if (x['title'] == game_object['title']) else False, prev_free_games):
            for i, j in enumerate(prev_free_games):
                if j["title"] == game_object['title']:
                    prev_free_games.pop(i)
                    prev_free_games.append(game_object)
                    break
            msg = f"The giveaway date of game \n{game_object['title']}\nhas changed to\n{game_object['release_date']}!\n"
            bot.send_photo(chat_id,game_object['image'], caption=msg)
            pass