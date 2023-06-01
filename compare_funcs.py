import math


def naive(btc_value: float, eth_value: float) -> float:
    """
    Наивный подход - простое вычитание т. е. предполагается, что эфир
    постоянно зависит от биткойна

    :param btc_value: относительное изменение биткойна ~ производная ф-и биткойна по времени
    :param eth_value: относительное изменение эфира  ~ производная ф-и эфира по времени
    :return: коэффициент на который будет изменён эфир
    """
    return eth_value - btc_value


def miss_both_changing(btc_value: float, eth_value: float):
    """
    Считаем, что если обе величины меняются примерно одинаково (в 1 +- rel_tol раз), -
    значит эфир не изменился

    :param btc_value: относительное изменение биткойна ~ производная ф-и биткойна по времени
    :param eth_value: относительное изменение эфира  ~ производная ф-и эфира по времени
    :return: коэффициент на который будет изменён эфир
    """
    diff = eth_value
    rel_tol = 0.2
    if btc_value != 0:
        if eth_value != 0:
            if math.isclose(btc_value / eth_value, 1, rel_tol=rel_tol):
                diff = 0
    return diff
