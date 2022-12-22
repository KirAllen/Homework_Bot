import requests
import datetime
from config import tg_bot_token, weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message:types.Message):
    await message.reply("Хеллоу! Введите название города, а я покажу, какая там нынче погодка!")

@dp.message_handler()
async def get_weather(message: types.Message):
        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
            )
            data = r.json()
            # print(data)

            city = data["name"]
            cur_weather = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***"
                  f"Погода нынче: {city}\n Температура: {cur_weather}C\n"
                  f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind}м/с\n"
                  f"Восход Солнца: {sunrise}\nЗакат Солнца:{sunset}\nДлинна дня: {length_of_the_day}\n"
                  f"Хорошего дня!")
        except:
            await message.reply("\U00002620 Error! Try to enter the name of the city again! \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)