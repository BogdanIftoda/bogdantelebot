from unicodedata import name
from urllib import response
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


#constants
telegram_api = '5188322582:AAHdRPB-FT-UhWNEek0vc5HwifWxEFKr83o'
weather_api = '953434794e55860bccd0fde0f40b954a'

def chech_city(city):
    city_api = 'https://countriesnow.space/api/v0.1/countries/cities'
    response = requests.post(city_api, data={'country': 'Ukraine'})
    cities = response.json().get('data')
    if city in cities:
        return True
    return False

def callApi(city):
    api_get_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api}'
    response = requests.get(api_get_url)
    weather = response.json().get('main')
    return weather


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Enter city:")

def weather(update, context):
    city = update.message.text
    if chech_city(city):

        response = callApi(city)
        text = f'Temperature in {city} is {round(response.get("temp"))}°C'
    else:
        text = 'Wrong city'
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=text)    


def main():    
  
    updater = Updater(token=telegram_api, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text, weather)


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


    # updater.start_webhook(listen="136.123.2.23",        
    #                     port=80,                       
    #                     url_path=telegram_api) 
    # updater.bot.setWebhook('https://bogdantelebot.herokuapp.com/' + telegram_api) 
    # updater.idle()

if __name__ == '__main__':
    main()