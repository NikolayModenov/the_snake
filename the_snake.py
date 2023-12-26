from random import choice, randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POINT_WIDTH = (GRID_WIDTH // 2) * GRID_SIZE
CENTER_POINT_HEIGHT = (GRID_HEIGHT // 2) * GRID_SIZE
COORDINATES_CENTRAL_CELL = [CENTER_POINT_WIDTH, CENTER_POINT_HEIGHT]

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (170, 170, 170)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FRAME_COLOR = (93, 216, 228)

DIRECTION_KEYS = {
    pg.K_UP: (DOWN, UP),
    pg.K_DOWN: (UP, DOWN),
    pg.K_LEFT: (RIGHT, LEFT),
    pg.K_RIGHT: (LEFT, RIGHT),
}

SPEED_KEYS = {
    pg.K_z: (5, -4),
    pg.K_x: (25, 4)
}

snake_info = {
    "max": 0,
    "current": 0,
    "speed": 9
}

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


def current_caption():
    """Update the screen title."""
    pg.display.set_caption(
        '"Змейка". Выход - ESC. '
        f'Сложность: {snake_info["speed"]}. '
        'Изменить - Z, X. '
        f'счёт: {snake_info["current"]}. '
        f'рекорд: {snake_info["max"]}'
    )


clock = pg.time.Clock()


def snake_length_control(length):
    """
    If the length of the snake is greater than the maximum,
    then assign it to the 'max' cell,
    otherwise assign it to the 'current' cell.
    """
    if length > snake_info["max"]:
        snake_info["max"] = length
    else:
        snake_info["current"] = length


def handle_keys(game_object):
    """
    Determine the new direction of the target's movement
    according to the pressed key.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            if (
                event.key in DIRECTION_KEYS.keys()
                    and game_object.direction != DIRECTION_KEYS[event.key][0]
            ):
                game_object.direction = DIRECTION_KEYS[event.key][1]
            if (
                event.key in SPEED_KEYS.keys()
                    and snake_info["speed"] != SPEED_KEYS[event.key][0]
            ):
                snake_info["speed"] += SPEED_KEYS[event.key][1]


class GameObject:
    """This class describes the general properties of game objects."""

    def __init__(
            self,
            position: list[int] = COORDINATES_CENTRAL_CELL,
            body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR,
            frame_color: tuple[int, int, int] = FRAME_COLOR
    ):
        self.position = position
        self.body_color = body_color
        self.frame_color = frame_color

    def draw(self, position, body_color):
        """Define how the object will be drawn on the screen."""
        object_rect = pg.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, body_color, object_rect)
        if body_color is not BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, self.frame_color, object_rect, 1)


class Snake(GameObject):
    """
    This class draws a snake in the center of the screen,
    the initial movement of which is chosen randomly.
    """

    def __init__(
            self,
            position: list[int] = COORDINATES_CENTRAL_CELL,
            body_color: tuple[int, int, int] = SNAKE_COLOR,
            frame_color: tuple[int, int, int] = FRAME_COLOR
    ):
        super().__init__(position, body_color, frame_color)
        self.positions = [self.position]
        self.length = len(self.positions)
        self.reset()
        self.hunger = True

    def move(self):
        """
        If the snake has not bitten itself,
        move it in the specified direction.
        Otherwise, erase the snake and create it in the center of the screen.
        If the snake has eaten an apple, do not erase its last cell.
        """
        width, height = self.direction
        self.position = [
            (width * GRID_SIZE + self.get_head_position()[0])
            % SCREEN_WIDTH,
            (height * GRID_SIZE + self.get_head_position()[1])
            % SCREEN_HEIGHT
        ]
        self.positions = [self.position] + self.positions
        self.length = len(self.positions)
        if self.hunger:
            self.draw(
                self.positions[-1],
                BOARD_BACKGROUND_COLOR,
            )
            self.positions.pop(-1)
        else:
            self.hunger = True
        self.draw(self.get_head_position(), self.body_color)

    def reset(self):
        """
        Save the current length of the snake,
        then reset the snake to its initial state.
        """
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        snake_length_control(self.length)
        self.positions = [COORDINATES_CENTRAL_CELL]

    def get_head_position(self):
        """Return the current position of the snake's head."""
        return self.positions[0]

    def update_direction(self):
        """Update the direction of travel"""
        pass


class Apple(GameObject):
    """This class draws an apple in a random place inside the screen."""

    def __init__(
            self,
            position: list[int] = COORDINATES_CENTRAL_CELL,
            body_color: tuple[int, int, int] = APPLE_COLOR,
            frame_color: tuple[int, int, int] = FRAME_COLOR,
    ):
        super().__init__(position, body_color, frame_color)
        self.position = self.randomize_position()

    def randomize_position(
            self,
            list_positions=[COORDINATES_CENTRAL_CELL]
    ) -> list[int]:
        """
        If the coordinates of the apple are included in the specified list,
        then assign new random coordinates to the apple.
        """
        self.position = [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        ]
        while self.position in list_positions:
            self.position = [
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            ]
        return self.position


def main():
    """
    Launch the Snake game.
    Control the snake with the arrow keys on the keyboard.
    If the snake bites itself or fills the entire playing field,
    then reset the game.
    """
    screen.fill(BOARD_BACKGROUND_COLOR)
    current_caption()
    apple = Apple()
    apple.draw(apple.position, apple.body_color)
    snake = Snake()

    while True:
        handle_keys(snake)
        if (
            snake.get_head_position() in snake.positions[1:]
            or snake.length == GRID_HEIGHT * GRID_WIDTH
        ):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
            apple.draw(apple.position, apple.body_color)
        if snake.get_head_position() == apple.position:
            snake.hunger = False
            snake.move()
            apple.randomize_position(snake.positions)
            apple.draw(apple.position, apple.body_color)
        else:
            snake.move()

        pg.display.update()
        current_caption()
        clock.tick(snake_info["speed"])


if __name__ == '__main__':
    main()
