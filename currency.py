from time import time
from async_retriever import Measurement


class CurrencyList(list):
    """
    Наследуется от списка, имеет ограниченную длину, которая зависит от кол-ва добавленных элементов
    Measurement, хранящихся упорядоченно с возврастающим таймстемпом. Если Measurement был создан
    более ttl (time to live) секунд назад, он будет удален из начала списка.
    """

    def __init__(self, ttl: int = 3600):
        super().__init__()
        self.max_value = None
        self.ttl = ttl
        self.min_value = None
        self.follow_changes = False

    def _drop_old(self):
        """
        Удаление Measurement из начала списка, когда он устаревает. Если значение было экстремумом,
        обновляем экстремум
        """
        try:
            first = self[0]
            if first.created_at + self.ttl < time():
                self.pop(0)
            if first.value == self.min_value:
                self.min_value = min([measurement.value for measurement in self])
            elif first.value == self.max_value:
                self.max_value = max([measurement.value for measurement in self])

        except IndexError:
            pass

    def _set_max(self, value: float):
        """
        Если значение больше максимального, обновляем максимальное значение списка. Относительно
        максимального значения ищём прирост
        """
        if self.max_value:
            if value > self.max_value:
                self.max_value = value
        else:
            self.max_value = value

    def _set_min(self, value: float):
        """
        Если значение меньше максимального, обновляем минимальное значение списка. Относительно
        минимального значения ищём спад
        """
        if self.min_value:
            if value < self.min_value:
                self.min_value = value
        else:
            self.min_value = value

    def append(self, measurement: 'Measurement') -> None:
        passed_class = measurement.__class__.__name__
        if passed_class != 'Measurement':
            raise TypeError('Passed measurement value should be a "Measurement" instance, not "%s".' % passed_class)
        super().append(measurement)
        self._set_min(value=measurement.value)
        self._set_max(value=measurement.value)
        self._drop_old()

    def to_list(self):
        """ Возвращает список значений. Используется для построения графика """
        return [measurement.value for measurement in self]
