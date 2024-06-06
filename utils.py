"Модуль для работы с HTTP запросами и прочим"

import os
import typing
import aiohttp
from dotenv import load_dotenv

load_dotenv()

headers = {
    'x-cg-demo-api-key': os.getenv("API_KEY")
}


async def coins_list() -> typing.AsyncGenerator[tuple[str, str], None]:
    "Корутина для получения списка криптовалют"
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=5&page=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            for coin in await response.json():
                yield coin['id'], coin['name']


async def coin_info(coin_id: str) -> dict[typing.Any, typing.Any] | None:
    "Корутина получает данные об конкретной крипте"
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            if response.status != 200:
                return None

            data = await response.json()

            return {
                'name': data['name'],
                'name_rus': data['localization']['ru'],
                'link': data['links']['homepage'],
                'image': data['image']['large'],
                'current_price_usd': data['tickers'][0]['last'],
                'volume': data['tickers'][0]['volume'],
            }


async def get_image(url: str) -> bytes | None:
    "Корутина получает байт код картинки"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            if response.start == 200:
                return await response.content.read()
            else:
                return None
