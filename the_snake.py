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
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Представляет змейку, управляет её движением и состоянием."""

    def __init__(self):
        """Создаёт змейку с начальной длиной и направлением движения."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset(initial=True)

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки.

        Returns:
            tuple: Координаты головы в формате (x, y).
        """
        return self.positions[0]

    def get_next_head_position(self):
        """Вычисляет следующую позицию головы змейки.

        Учитывает текущее направление движения и переход
        через границы игрового поля.

        Returns:
            tuple: Координаты следующей позиции головы (x, y).
        """
        head = self.get_head_position()
        new_x = (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        return (new_x, new_y)

    def reset(self, initial=False):
        """Сбрасывает змейку до одного сегмента в центре игрового поля.

        Args:
            initial (bool): Если True, задаёт направление вправо.
                Иначе выбирает случайное направление.
        """
        self.length = 1
        self.positions = [self.position]
        if initial:
            self.direction = RIGHT
        else:
            self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении.

        Добавляет новую голову и удаляет хвост, если количество
        сегментов превышает установленную длину змейки.
        """
        new_head = self.get_next_head_position()
        self.positions.insert(0, new_head)
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает все сегменты змейки на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Применяет новое направление движения, если оно задано."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object, speed):
    """Обрабатывает управление, изменение скорости и выход из игры.

    Args:
        game_object (Snake): Управляемая игроком змейка.
        speed (int): Текущая скорость игры.

    Returns:
        int: Обновлённая скорость игры.
    """
    directions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }
    opposite_directions = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

        if event.key in SPEED_LEVELS:
            speed = SPEED_LEVELS[event.key]

        new_direction = directions.get(event.key)
        if (
            new_direction is not None
            and game_object.next_direction is None
            and new_direction != opposite_directions[game_object.direction]
        ):
            game_object.next_direction = new_direction

    return speed


def main():
    """Запускает игру и управляет её основным циклом.

    Создаёт змейку и яблоко, обрабатывает управление, движение,
    поедание яблок, столкновения и обновление игрового экрана.
    """
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    speed = DEFAULT_SPEED

    while True:
        clock.tick(speed)
        speed = handle_keys(snake, speed)
        snake.update_direction()

        ate_apple = snake.get_next_head_position() == apple.position

        if ate_apple:
            snake.length += 1

        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        elif len(snake.positions) == GRID_WIDTH * GRID_HEIGHT:
            snake.reset()
            apple.randomize_position(snake.positions)

        elif ate_apple:
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
