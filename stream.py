import asyncio
from attrs import define
import time
from dataclasses import replace
from typing import Callable
from time import time
import matplotlib.pyplot as plt
from compare_funcs import naive, miss_both_changing
from currency import CurrencyList
from async_retriever import currencies_pair_generator, Measurement


@define
class Stream:
    """ Стриминг значений фьючерсов """
    btc_stream = CurrencyList()
    eth_stream = CurrencyList()
    new_eth_stream = CurrencyList()

    async def _process_values(self, change_func: Callable[[float, float], float], running_time: int | float = None):
        """ Вычисляем значения (биткойна, эфира, изменения эфира, нового эфира и т д) в течение running_time """
        time_expired = running_time + int(time()) if running_time else float("inf")
        async for btc_measurement, eth_measurement in currencies_pair_generator():
            if time_expired > time():
                btc_diff = self._diff_value(self.btc_stream, btc_measurement)
                eth_diff = self._diff_value(self.eth_stream, eth_measurement)
                coeff = change_func(btc_diff, eth_diff)
                new_measurement_value = eth_measurement.value * (1 + coeff)
                new_eth_measurement = replace(eth_measurement,
                                              value=round(new_measurement_value, 2),
                                              currency='NEW_ETH')
                self._follow(new_eth_measurement)
            else:
                break

    def _follow(self, measurement: Measurement, percent: float = 0.) -> None:
        """
        Проверяем изменение текущего измерения по сравнению с экстремумами,
        если изменение больше чем percent процентов, выводит сообщение
        """
        stream = self.new_eth_stream
        if len(stream):
            current_measurement_value = measurement.value
            increasing = (current_measurement_value / stream.max_value - 1) * 100
            decreasing = - (current_measurement_value / stream.min_value - 1) * 100
            if increasing > percent:
                stream.max_value = current_measurement_value
                stream.min_value = current_measurement_value
                print('%sUSDT фьючерс вырос на %s процентов!' % (measurement.currency, increasing))
            if decreasing > percent:
                stream.max_value = current_measurement_value
                stream.min_value = current_measurement_value
                print('%sUSDT фьючерс упал на %s процентов!' % (measurement.currency, decreasing))
        self.new_eth_stream.append(measurement)

    def _diff_value(self, stream: CurrencyList, measurement: Measurement) -> float:
        """ Относительное изменение биткойна/эфира """
        if len(stream):
            previous_measurement_value = stream[-1].value
            current_measurement_value = measurement.value
            stream.append(measurement)
            return current_measurement_value / previous_measurement_value - 1
        else:
            stream.append(measurement)
        return 0

    def start(self, change_func: Callable = naive, running_time: int | float = None):
        coro = self._process_values(running_time=running_time, change_func=change_func)
        asyncio.run(coro)

    def _plot_stream(self, stream: CurrencyList):
        """ Добавление списка фьючерсов на график """
        assert len(stream), 'Empty CurrencyList given'
        x = list(range(len(self.eth_stream)))
        label = stream[0].currency
        plt.plot(x, stream.to_list(), '-o', label=label)

    def visualize_eth_values(self):
        """ Запускает интерактивный векторный график, после выполнения .start(*args) """
        self._plot_stream(self.eth_stream)
        self._plot_stream(self.new_eth_stream)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    streaming = Stream()
    streaming.start(change_func=miss_both_changing)
    # # расскоментить чтобы посмотреть график, но при это необходимо передать running_time в start()
    # s.visualize_eth_values()
