import configparser
from GLC import GLC
import telebot
from telebot import types

bot = telebot.TeleBot("", parse_mode="MARKDOWN")
mm = types.ReplyKeyboardMarkup(row_width=2)
button1 = types.KeyboardButton("Поиск")
mm.add(button1)
markup = types.InlineKeyboardMarkup()
btn = types.InlineKeyboardButton(text='Отслеживать', callback_data="yes")
markup.add(btn)
config = configparser.ConfigParser()
config.read('s.ini')
glc = GLC(config['main']['cookie'], config['main']['url'])


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    f = open("users", "a+", encoding='utf-8')
    f.write(call.message.text + "\n")
    f.close()


@bot.message_handler(func=lambda m: True)
def mess(message):
    ulist = glc.get_user_list()
    if message.text == "/start":
        for user in ulist:
            bot.send_message(message.chat.id, user, reply_markup=markup)
    else:
        f = open("users", encoding='utf-8').readlines()
        ulist = ""
        for user in f:
            if glc.get_user_loc(user) == config['main']['adr']:
                ulist += user
            else:
                bot.send_message(message.chat.id, "Никого нет", reply_markup=markup)
            if ulist != "":
                bot.send_message(message.chat.id, ulist, reply_markup=markup)


bot.infinity_polling()
