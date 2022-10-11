from dataclasses import dataclass
from typing import ClassVar, List


class UnsupportedTypeTraining(Exception):
    """Исключение для неподдерживаемых типов тренировки."""
    print(Exception)


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Please Implement this method")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEF_CALORIE_1: int = 18
    COEF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""

        return ((self.COEF_CALORIE_1 * self.get_mean_speed() - self.
                 COEF_CALORIE_2) * self.weight / self.M_IN_KM * self
                .duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_1: ClassVar[float] = 0.035
    COEF_2: ClassVar[int] = 2
    COEF_3: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        weight = self.weight
        height = self.height
        calorie = weight * ((self.COEF_1 + (speed ** self.
                             COEF_2 // height) * self.COEF_3)) * (self.
                              duration * self.MIN_IN_HOUR)
        return calorie


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    COEF_1: ClassVar[float] = 1.1
    COEF_2: ClassVar[int] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Расчет средней скорости"""
        temp = self.length_pool * self.count_pool
        mean_speed = temp / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""
        mean_speed = self.get_mean_speed()
        temp = (mean_speed + self.COEF_1) * self.COEF_2
        calorie = temp * self.weight
        return calorie

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in types_of_workout.keys():
        raise UnsupportedTypeTraining('Неподдерживаемый тип тренировки')
    training_object = types_of_workout.get(workout_type)
    return training_object(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
