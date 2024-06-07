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
async def send_coins(
    callback_query: types.CallbackQuery, 
    page: int = 1, 
    edit: bool = False
    ) -> None:
    "Корутина отправляет клавиатуру с криптой"

    buttons = []
    async for coin_id, name in coins_list(page=page):
        button = types.InlineKeyboardButton(text=name, callback_data=f"coin_id:{coin_id}")
        buttons.append(button)

    extra_buttons = []
    if page == 1:
        extra_buttons.append(
            types.InlineKeyboardButton(text="Следующая страница", callback_data=f"page:{page+1}")
        )
    elif page > 1:
        extra_buttons.extend([
            types.InlineKeyboardButton(text="Предыдущая страница", callback_data=f"page:{page-1}"),
            types.InlineKeyboardButton(text="Следующая страница", callback_data=f"page:{page+1}")
        ])

    markup = types.InlineKeyboardMarkup(inline_keyboard=[buttons, extra_buttons])

    text = "Вот список криптовалют"
    if edit:
        await callback_query.message.edit_text(  # type: ignore
            text=text,
            reply_markup=markup
        )
    else:
        await callback_query.message.answer(  # type: ignore
            text=text,
            reply_markup=markup
        )


@dp.callback_query(lambda call: call.data.startswith("page:"))
async def change_page(callback_query: types.CallbackQuery):
    "Корутина для изменения номера страницы"

    page = callback_query.data.replace("page:", "")  # type: ignore
    await send_coins(callback_query=callback_query, page=int(page), edit=True)


@dp.callback_query(lambda call: call.data.startswith("coin_id:"))
async def send_coin_info(callback_query: types.CallbackQuery) -> None:
    "Корутина отправляет пользователю данные о крипте"

    coin_id = callback_query.data.replace("coin_id:", "")  # type: ignore
    data = await coin_info(coin_id=coin_id)
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
