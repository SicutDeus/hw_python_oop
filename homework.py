from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
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
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    SPEAD_COEF = 18
    SPEAD_OFFSET = 20

    def get_spent_calories(self) -> float:
        return (
            (self.SPEAD_COEF * self.get_mean_speed() - self.SPEAD_OFFSET)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    height: int
    WEIGHT_COEF = 0.035
    SPEED_GRADE = 2
    COEF_CALORIE = 0.029

    def get_spent_calories(self) -> float:
        return (
            (
                self.WEIGHT_COEF * self.weight
                + (self.get_mean_speed() ** self.SPEED_GRADE // self.height)
                * self.COEF_CALORIE
            )
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    LEN_STEP = 1.38
    MEAN_SPEED_OFFSET = 1.1
    MEAN_SPEED_COEF = 2
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM \
            / self.duration

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_OFFSET)
            * self.MEAN_SPEED_COEF
            * self.weight
        )


TRAINING_DICT = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    return TRAINING_DICT[workout_type](*data)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
