import aiohttp
import asyncio
from dataclasses import dataclass
from random import uniform
from time import time

BITCOIN_SHORT_NAME = "BTC"
ETHERIUM_SHORT_NAME = 'ETH'


@dataclass(frozen=True)
class Measurement:
    currency: str
    value: float
    created_at: float


async def currency_value_stream(currency: str):
    """
    Асинхронный генератор для получения значений фьючерса currency
    Прирост в скорости выполнения ~ 30% по сравнению с обычным генератором
    """
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={currency}USDT'
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url=url) as data:
                curr = await data.json()
                yield Measurement(
                    currency=currency,
                    value=round(float(curr["price"]), 2),
                    created_at=round(time(), 1)
                )


# # раскомментить для теста
# async def currency_value_stream(currency: str):
#     while True:
#         await asyncio.sleep(0.3)
#         yield Measurement(
#             currency=currency,
#             value=uniform(100, 1001) if currency == ETHERIUM_SHORT_NAME else 10000,
#             created_at=round(time(), 1)
#         )


async def currencies_pair_generator():
    """ Асинхронный генератор для получения значений фьючерсов """
    btc_async = currency_value_stream(BITCOIN_SHORT_NAME)
    eth_async = currency_value_stream(ETHERIUM_SHORT_NAME)
    while True:
        btc_measurement = await anext(btc_async)
        eth_measurement = await anext(eth_async)
        yield btc_measurement, eth_measurement
