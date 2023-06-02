# Тестовое задание

## Настройка и запуск
1) создать и активировать окружение (python >= 3.11)
2) установить зависимости
```
pip install -r requirements.txt
```
3) находясь в корневой папке, для запуска прописать в терминале
```
python stream.py
```

##

Ремврки:
 1) Происходит событие А влияющее на изменение btc и eth одинаково, например, обрушение FTX.
Является ли это влиянием цены btc на eth? Технически нет, но при выполнени ТЗ такие события опущены.
 2) Если изменения в курсе двух фьючерсов это исключительно покупка/продажа, то установить зависимость 
невозможно.
 3) Также опускаем одновременность получения значения двух разных фьючерсов
 4) Хорошо было бы анализировать по сглаживанию и использовать scipy, но решил начать с простого, также не использовал
 python-binance (а надо было пробовать)
 
Рассмотрим картинку:

![Иллюстрация 1](https://github.com/LeonKilgoreTrout/pure-ethusdt/blob/main/images/currency_derivatives.png)

Ось x => номер замера

Ось y => производные функций изменения фьючерсов  

В основном нас интересуют кейсы в красных кругах, когда прирост двух фьючерсов практически одинаков


Также если предположить, что ETHUSDT априори зависим от BTCUSDT

![Иллюстрация 2](https://github.com/LeonKilgoreTrout/pure-ethusdt/blob/main/images/currency_derivatives.png)


