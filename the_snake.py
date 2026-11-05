from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED_LEVELS = {
    pygame.K_1: 10,
    pygame.K_2: 20,
    pygame.K_3: 30
}

DEFAULT_SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов змейки."""

    def __init__(self):
        """Инициализирует положение и цвет игрового объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Определяет интерфейс отрисовки игрового объекта."""
        pass


class Apple(GameObject):
    """Представляет яблоко, которое змейка может съесть."""

    def __init__(self, occupied_positions):
        """Создаёт яблоко в случайной свободной клетке игрового поля.

        Args:
            occupied_positions: Координаты клеток, занятых змейкой.
        """
        super().__init__()
        self.randomize_position(occupied_positions)
        self.body_color = APPLE_COLOR

    def randomize_position(self, occupied_positions=None):
        """Перемещает яблоко в случайную незанятую клетку поля.

        Args:
            occupied_positions: Координаты занятых клеток.
                Если не указаны, все клетки считаются свободными.
        """
        if occupied_positions is None:
            occupied_positions = []

        free_positions = []

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                position = (x * GRID_SIZE, y * GRID_SIZE)
                if position not in occupied_positions:
                    free_positions.append(position)
        self.position = choice(free_positions)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)