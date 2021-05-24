import telebot as tg
from telebot import types
import user
from user import user
from prs import Parser
from prsprice import Parser2
from price import max_price_handler, min_price_handler

bot = tg.TeleBot('1821911933:AAEot5pS0BhCQHhSm8eN1s0HUl5_U3Jh36Q')
item = str()
users = dict()


def prepare_keyboard():
    buttons_names = ["Avito", "Citilink", "DNS", "Все доступные магазины"]
    keyboard = types.InlineKeyboardMarkup()
    for b in range(buttons_names.__len__()):
        keyboard.add(types.InlineKeyboardButton(text=buttons_names[b], callback_data=buttons_names[b]))
    return keyboard


def prepare_reply_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help = types.KeyboardButton(text="/help")
    keyboard.add(help)
    return keyboard


def prepare_list(d):
    markups = types.InlineKeyboardMarkup()
    t = 0
    if d.__len__() < 8:
        t = d.__len__()
    else:
        t = 8
    for x in range(t):
        btn = types.InlineKeyboardButton(text=list(dict(d).keys())[x] + " " + list(dict(d).values())[x][1],
                                         url=list(dict(d).values())[x][0], callback_data="shop")
        markups.add(btn)
    return markups


@bot.callback_query_handler(func=lambda call: True)
def answer_on_call(call):
    # print(users[call.message.chat.id].item)
  #  if call.data == "Цена":
   #     bot.send_message(call.message.chat.id, "Напиши максимальную цену")
   #     max_price_handler(user(message.text))
   #     bot.send_message(call.message.chat.id, "Напиши минимальную цену")
   #     min_price_handler(user(message.text))
  #      bot.send_message(call.message.chat.id, "Напиши наименование")
  #  pr = Parser2(users[call.message.chat.id])
    if call.data == "Avito":
        bot.send_message(call.message.chat.id, "Вот что я нашел на " + call.data, reply_markup=prepare_list(pr.avito()))
    elif call.data == "Citilink":
        bot.send_message(call.message.chat.id, "Вот что я нашел в " + call.data,
                         reply_markup=prepare_list(pr.citilink()))
    elif call.data == "DNS":
        bot.send_message(call.message.chat.id, "Вот что я нашел в " + call.data, reply_markup=prepare_list(pr.dns()))
    elif call.data == "Все доступные магазины":
        bot.send_message(call.message.chat.id, "Вот что я нашел на Avito", reply_markup=prepare_list(pr.avito()))
        bot.send_message(call.message.chat.id, "Вот что я нашел в Citilink", reply_markup=prepare_list(pr.citilink()))
        bot.send_message(call.message.chat.id, "Вот что я нашел в DNS", reply_markup=prepare_list(pr.dns()))
    else:
        pr = Parser(users[call.message.chat.id])
    if call.data == "Avito":
        bot.send_message(call.message.chat.id, "Вот что я нашел на " + call.data, reply_markup=prepare_list(pr.avito()))
    elif call.data == "Citilink":
        bot.send_message(call.message.chat.id, "Вот что я нашел в " + call.data,
                         reply_markup=prepare_list(pr.citilink()))
    elif call.data == "DNS":
        bot.send_message(call.message.chat.id, "Вот что я нашел в " + call.data, reply_markup=prepare_list(pr.dns()))
    elif call.data == "Все доступные магазины":
        bot.send_message(call.message.chat.id, "Вот что я нашел на Avito", reply_markup=prepare_list(pr.avito()))
        bot.send_message(call.message.chat.id, "Вот что я нашел в Citilink", reply_markup=prepare_list(pr.citilink()))
        bot.send_message(call.message.chat.id, "Вот что я нашел в DNS", reply_markup=prepare_list(pr.dns()))


@bot.message_handler(content_types=['text'])
def recieve_mes(message):
    if not users.keys().__contains__(message.chat.id):
        users[message.chat.id] = user(message.text)
    if message.text == "/help":
        bot.send_message(message.chat.id,
                         "Я ищу товары по разным магазинам, просто напиши мне название товара и его его найду",reply_markup=prepare_reply_keyboard())
    elif message.text == "/start":
        bot.send_message(message.chat.id,
                         "Я ищу товары по разным магазинам, просто напиши мне название товара и его его найду",reply_markup=prepare_reply_keyboard())
    else:
        users[message.chat.id] = message.text
        bot.send_message(message.chat.id, "Вот где я могу поискать нужный вам товар", reply_markup=prepare_keyboard())


bot.polling(none_stop=True)
