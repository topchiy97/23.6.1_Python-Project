import telebot
from config import keys, TOKEN
from extentions import APIExeption, СurrensyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def greeting(message: telebot.types.Message):
    text = f'Приветствую, {message.chat.username}! Я бот-конвертер, возвращаю актуальные курсы валют.\n\
Увидеть список всех доступных валют: /values\n\
Попросить помощь: /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def instruction(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n"первая валюта" \
"вторая валюта" \
"количество первой валюты".\n\
Пример корректного ввода: доллар рубль 1.\n\
При введении дробного количества используйте точку.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value_list(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIExeption('Количество введенных параметров должно быть равно 3')

        quote, base, amount = values
        total_base = СurrensyConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
