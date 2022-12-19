import logging

from aiogram import Bot, Dispatcher, executor, types

import config

logging.basicConfig(level=logging.INFO)
from weather import get_coordinates
from api import get_weather
import keyboards


bot = Bot(token=config.BOT_API)
dp = Dispatcher(bot)


def weather() -> str:
    wthr = get_weather(get_coordinates())
    return f'{wthr.location}, {wthr.description}\n' \
           f'Temperature is {wthr.temperature}°C, feels like {wthr.temperature_feeling}°C'

def wind() -> str:
    wthr = get_weather(get_coordinates())
    return f'{wthr.wind_direction} wind {wthr.wind_speed} m/s'

def sun_time() -> str:
    wthr = get_weather(get_coordinates())
    return f'Sunrise: {wthr.sunrise.strftime("%H:%M")}\n' \
           f'Sunset: {wthr.sunset.strftime("%H:%M")}\n'


@dp.message_handler(commands=['start', 'weather'])
async def show_weather(message: types.Message):
    await message.answer(text=weather(),
                         reply_markup=keyboards.WEATHER)


@dp.message_handler(commands='help')
async def show_help_message(message: types.Message):
    await message.answer(text=f'This bot can get the current weather from your IP address.',
                         reply_markup=keyboards.HELP)


@dp.message_handler(commands='wind')
async def show_wind(message: types.Message):
    await message.answer(text=wind(), reply_markup=keyboards.WIND)


@dp.message_handler(commands='sun_time')
async def show_sun_time(message: types.Message):
    await message.answer(text=sun_time(), reply_markup=keyboards.SUN_TIME)


@dp.callback_query_handler(text='weather')
async def process_callback_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=weather(),
        reply_markup=keyboards.WEATHER
    )


@dp.callback_query_handler(text='wind')
async def process_callback_wind(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=wind(),
        reply_markup=keyboards.WIND
    )


@dp.callback_query_handler(text='sun_time')
async def process_callback_sun_time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=sun_time(),
        reply_markup=keyboards.SUN_TIME
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
