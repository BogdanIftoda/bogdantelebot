import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# constants
telegram_api = '5188322582:AAHdRPB-FT-UhWNEek0vc5HwifWxEFKr83o'
weather_api = '953434794e55860bccd0fde0f40b954a'

def check_city(city):
    city_api = 'https://countriesnow.space/api/v0.1/countries/cities'
    response = requests.post(city_api, data={'country': 'Ukraine'})
    cities = response.json().get('data')
    if city.capitalize() in cities:
        return True
    return False


def callApi(city, location=None):
    if location:
        lat, lon = location
        api_get_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weather_api}'
        response = requests.get(api_get_url)
        weather = response.json().get('main')
        city = response.json().get('name')
        return weather, city
    else:
        api_get_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api}'
        response = requests.get(api_get_url)
        weather = response.json().get('main')
        return weather


def start(update, context):
    button = [[telegram.KeyboardButton('get weather by location', request_location=True)],
              [telegram.KeyboardButton('get weather by city')]]
    reply_kb_markup = telegram.ReplyKeyboardMarkup(button,
                                                   resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Press the button:", reply_markup=reply_kb_markup)


def weather(update, context):
    message = update.message
    if message.location:
        current_position = (message.location.latitude, message.location.longitude)
        print(message)
        response, city = callApi(message.text, current_position)
        text = f'Temperature in {city} is {round(response.get("temp"))}°C'
    elif check_city(message.text):
        response = callApi(message.text)
        text = f'Temperature in {message.text} is {round(response.get("temp"))}°C'
    else:
        text = 'Wrong message'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def main():
    updater = Updater(token=telegram_api, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.location | Filters.text, weather)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
