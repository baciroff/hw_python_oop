from statistics import mean
from turtle import distance


class UnsupportedTypeTraining(Exception):
    """Исключение для неподдерживаемых типов тренировки."""
    print(Exception)


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: '
                f'{self.calories:.3f}.'
                )

    
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
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
        temp = self.action
        distance = temp * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info_obj = InfoMessage(training_type,
                               duration,
                               distance,
                               speed,
                               calories
                               )
        return info_obj


class Running(Training):
    """Тренировка: бег."""

    COEF_CALORIE_1: int = 18
    COEF_CALORIE_2: int = 20

    def __init__(self, action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Расчет израсходованных калорий."""

        mean_speed = self.get_mean_speed()
        temp = self.COEF_CALORIE_1 * mean_speed - self.COEF_CALORIE_2
        calorie = (temp * self.weight
                   / self.M_IN_KM * self.duration * self.MIN_IN_HOUR
                   )
        return calorie


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    
    COEF_1: float = 0.035
    COEF_2: float = 2
    COEF_3: float = 0.029

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        weight = self.weight
        height = self.height
        temp = self.duration * self.MIN_IN_HOUR
        temp_2 = speed ** self.COEF_2 // height
        calorie = weight * ((self.COEF_1 + temp_2 * self.COEF_3)) * temp
        return calorie



class Swimming(Training):
    """Тренировка: плавание."""
    
    LEN_STEP: float = 1.38
    COEF_1: float = 1.1
    COEF_2: float = 2

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                length_pool: float,
                count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

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


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
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

