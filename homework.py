"""Модуль фитнес-трекера."""
from dataclasses import dataclass
from typing import Dict, List, Type


class KeyOrDataError(Exception):
    """Ошибка входных данных.

    Вызывается, когда в словарь передан неверный ключи и (или)
    передано неверное кол-во параметров
    """


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращает строку-информацию о тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: str
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Класс бега."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_OFFSET = 20

    def get_spent_calories(self) -> float:
        """Вычисление потраченных калорий при беге."""
        return (
            (
                self. CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_MEAN_SPEED_OFFSET
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Класс спортивной ходьбы."""

    height: int

    CALORIES_MEAN_SPEED_MULTIPLIER = 0.029
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_GRADE = 2

    def get_spent_calories(self) -> float:
        """Получение количества затраченных калорий при спортивной ходьбе."""
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    self.get_mean_speed() ** self.CALORIES_MEAN_SPEED_GRADE
                    // self.height
                )
                * self.CALORIES_MEAN_SPEED_MULTIPLIER
            )
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Класс плавания."""

    length_pool: int
    count_pool: int

    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_OFFSET = 1.1

    def get_mean_speed(self) -> float:
        """Вычисление средней скорости при плавании."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Вычисление потраченных калорий при плавании."""
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_OFFSET)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
        )


TRAININGS: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return TRAININGS[workout_type](*data)
    except (KeyError, TypeError):
        raise KeyOrDataError(
            'Передан неверный ключ и (или)'
            'количество входных параметров не совпадает с необходимым',
        )


def main(training: Training) -> None:
    """Вывод полученный информации о результатах тренировки."""
    print(training.show_training_info().get_message())  # noqa: T201


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
