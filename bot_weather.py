import os
import requests
import telebot
from telebot import apihelper
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv('telegram_token')
weather_token = os.getenv('weather_token')
bot = telebot.TeleBot(telegram_token)
apihelper.proxy = {'https': 'socks5://96.96.33.133:1080'}

@bot.message_handler(commands=['start'])
def hello_text(message):
    #Приветственное слово бота
    text = 'Привет! Данный бот подсказывает погоду на текущий момент. Введи, пожалуйста, название города.'
    bot.send_message(message.chat.id, text)
        
@bot.message_handler(content_types=['text'])      
def conversation_with_user(message):
    #Общение с пользователем и отдача запрошенных данных
    bot.send_message(message.chat.id, f'Принято. Запрос обрабатывается.')
    result = get_weather(message)
    bot.send_message(message.chat.id, result)
    bot.send_message(message.chat.id, 'Интересует погода где-нибудь ещё? Жду название города')

def get_weather(message):
    #Запрос погоды
    params = {'q': message.text, 'appid': weather_token, 'units':'metric', 'lang':'ru'}
    url = 'http://api.openweathermap.org/data/2.5/weather'
    search = requests.get(url, params = params)
    if search.json().get('cod') != 200:
        return 'Такого города в базе нет'
    temperature = search.json().get('main')['temp']
    description = search.json().get('weather')[0]['description']
    pressure_mmhg = round(search.json().get('main')['pressure'] * 0.75006375541921,2)
    wind = search.json().get('wind')['speed']
    text=f'В городе {message.text}, температура = {temperature} градусам, {description}, давление = {pressure_mmhg} мм. рт. ст., скорость ветра = {wind} м/с'
    return text

if __name__ == '__main__':
    bot.polling(none_stop=True)
