import telebot
from config import keys, TOKEN
from extension import ConvertionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handlers(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \
    <Для получения всех доступных валют наберите: /values>"
    bot.send_message(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
        bot.reply_to(message, text)

@bot.message_handlers(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertionExeption('слишком много параметров')

        quote, base, amount = values

        quote_ticker, base_ticker = keys[quote], keys[base]

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()