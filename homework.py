class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        type_s = f'Тип тренировки: {self.training_type}; '
        dur_s = f'Длительность: {format(round(self.duration,3), ".3f")} ч.; '
        dist_s = f'Дистанция: {format(round(self.distance,3), ".3f")} км; '
        speed_s = f'Ср. скорость: {format(round(self.speed,3), ".3f")} км/ч; '
        calorie_s = f'Потрачено ккал: {format(round(self.calories,3), ".3f")}.'
        return type_s + dur_s + dist_s + speed_s + calorie_s


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: int = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        name = self.__class__.__name__
        dur = self.duration
        dist = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        info_message = InfoMessage(name, dur, dist, mean_speed, spent_calories)
        return info_message


class Running(Training):
    k_calorie_1 = 18
    k_calorie_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (self.k_calorie_1 * self.get_mean_speed() - self.k_calorie_2) \
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR


class SportsWalking(Training):
    coef_calorie_1 = 0.035
    coef_calorie_2 = 2
    coef_calorie_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = self.get_mean_speed()**self.coef_calorie_2 \
            // self.height
        spent_calories = spent_calories * self.coef_calorie_3 * self.weight
        spent_calories = self.coef_calorie_1 * self.weight + spent_calories
        spent_calories = spent_calories * self.duration * self.MIN_IN_HOUR
        return spent_calories


class Swimming(Training):
    LEN_STEP: int = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM \
            / self.duration

    def get_spent_calories(self) -> float:
        coef_calorie_1 = 1.1
        coef_calorie_2 = 2
        return (self.get_mean_speed() + coef_calorie_1) * coef_calorie_2 \
            * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
