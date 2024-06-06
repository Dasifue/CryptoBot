"Модуль для работы с ботом"

import os
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot, types, filters
from utils import coins_list, coin_info

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))  # type: ignore
dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start(message: types.Message) -> None:
    "Корутина отвечает на команду /start"

    first_name = message.chat.first_name
    if first_name is not None:
        text = f"Hello, {first_name}!"
    else:
        text = "Hello, user!"

    buttons = [
        types.InlineKeyboardButton(text="Список криптовалют", callback_data="coins_list"),
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

    await message.answer(text=text, reply_markup=markup)


@dp.callback_query(lambda call: call.data == "coins_list")
async def send_coins(callback_query: types.CallbackQuery) -> None:
    "Корутина отправляет клавиатуру с криптой"

    buttons = []
    async for coin_id, name in coins_list():
        button = types.InlineKeyboardButton(text=name, callback_data=coin_id)
        buttons.append(button)

    markup = types.InlineKeyboardMarkup(inline_keyboard=[buttons])

    text = "Вот список криптовалют"
    await bot.send_message(
        text=text,
        chat_id=callback_query.from_user.id,
        reply_markup=markup,
    )

@dp.callback_query(lambda call: call.data)
async def send_coin_info(callback_query: types.CallbackQuery) -> None:
    "Корутина отправляет пользователю данные о крипте"

    coin_id = callback_query.data
    data = await coin_info(coin_id=coin_id)  # type: ignore
    if data is not None:

        image_url = data.pop('image')
        await bot.send_photo(
            chat_id=callback_query.from_user.id,
            photo=image_url,
            caption=str(data)
        )
    else:
        await bot.send_message(
            text="Не получилось достать информацию",
            chat_id=callback_query.from_user.id,
        )
