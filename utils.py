"Модуль для работы с HTTP запросами и прочим"

import os
import typing
import aiohttp
from dotenv import load_dotenv

load_dotenv()

headers = {
    'x-cg-demo-api-key': os.getenv("API_KEY")
}


async def coins_list(
    vs_currency: str = "usd",
    page: int = 1,
    per_page: int = 5
) -> typing.AsyncGenerator[tuple[str, str], None]:
    "Корутина для получения списка криптовалют"
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "per_page": per_page,
        "page": page,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params, headers=headers) as response:
            for coin in await response.json():
                yield coin['id'], coin['name']


async def coin_info(coin_id: str) -> tuple[str, str] | None:
    "Корутина получает данные об конкретной крипте"
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            if response.status != 200:
                return None

            data = await response.json()

            text = f"{data['name']} ({data['web_slug']})\n{data['links']['homepage'][0]}\n"
            text += f"Current price = ${data['market_data']['current_price']['usd']}\n"
            text += f"Price change 24h = ${data['market_data']['price_change_24h']}\n"
            text += f"{data['description']['en']}"

            if len(text) > 1000:
                text = text[:1000] + "..."
            return text, data['image']['large']


async def get_image(url: str) -> bytes | None:
    "Корутина получает байт код картинки"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            if response.start == 200:
                return await response.content.read()
            else:
                return None
