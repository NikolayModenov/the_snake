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

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


def update_screen_title(game_info, current_score):
    """Update the screen title."""
    pg.display.set_caption(
        '"Змейка". Выход - ESC. '
        f'Сложность: {game_info["speed"]}. '
        'Изменить - Z, X. '
        f'счёт: {current_score}. '
        f'рекорд: {game_info["max"]}'
    )


clock = pg.time.Clock()


def handle_keys(game_object, game_info):
    """
    Convert keystrokes of movement into the direction of movement of the snake,
    close the game when pressing ESC,
    change the speed of movement of the snake with the Z and X buttons.
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
                event.key in DIRECTION_KEYS
                and game_object.direction != DIRECTION_KEYS[event.key][0]
            ):
                game_object.update_direction(DIRECTION_KEYS[event.key][1])
            if (
                event.key in SPEED_KEYS
                and game_info["speed"] != SPEED_KEYS[event.key][0]
            ):
                game_info["speed"] += SPEED_KEYS[event.key][1]


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

    def draw_cell(self, position, is_erase=False):
        """
        Color the cell in the specified location in the default colors,
        if 'erase=True' color the cell in the screen color.
        """
        object_rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        if is_erase:
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, object_rect)
        else:
            pg.draw.rect(screen, self.body_color, object_rect)
            pg.draw.rect(screen, self.frame_color, object_rect, 1)

    def draw(self):
        """An empty method for pytest."""
        pass


class Snake(GameObject):
    """
    This class draws a snake in the center of the screen,
    the initial movement of which is chosen randomly.
    """

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR, frame_color=FRAME_COLOR)
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [self.position]
        self.length = None

    def move(self):
        """
        Add a cell to the beginning of the snake,
        in the specified direction.
        """
        width, height = self.direction
        width_head, height_head = self.get_head_position()
        self.positions.insert(0, [
            (width * GRID_SIZE + width_head) % SCREEN_WIDTH,
            (height * GRID_SIZE + height_head) % SCREEN_HEIGHT
        ])

    def draw(self, drop_tail):
        """
        Specify a place to paint over the snake's head.
        If the snake drop tail:
        paint over the last link of the snake with the condition 'erase=True',
        and then remove the last link of the snake.
        """
        self.draw_cell(self.positions[0])
        if drop_tail:
            # Определяет что хвост не надо закрашивать
            # когда змея съела яблоко или укусила себя.
            self.draw_cell(self.positions[-1], is_erase=True)
            self.positions.pop(-1)

    def reset(self):
        """Reset the snake to its initial state."""
        self.positions = [self.positions[0]]

    def get_head_position(self):
        """Return the current position of the snake's head."""
        return self.positions[0]

    def update_direction(self, direction):
        """Update the direction of movement of the snake."""
        self.direction = direction

    def update_max_score(self, game_info):
        """
        If the length of the snake is greater than the maximum,
        then assign it to the 'max' cell.
        """
        game_info["max"] = max(game_info["max"], len(self.positions))


class Apple(GameObject):
    """This class draws an apple in a random place inside the screen."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR, frame_color=FRAME_COLOR)

    def randomize_position(self, list_positions):
        """
        Assign new random coordinates to the apple
        if the coordinates of the apple are included in the specified list.
        """
        while True:
            self.position = [
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            ]
            if self.position not in list_positions:
                break

    def draw(self):
        """Specify the place where to paint over the apple."""
        self.draw_cell(self.position)


def main():
    """
    Start the snake game,
    control the snake using the arrow keys on the keyboard,
    change the speed of the snake using the Z and X keys.
    If the snake bites itself:
    Update the score and reset the length of the snake.
    """
    game_info = {
        "max": 0,
        "speed": 9
    }

    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        drop_tail = True
        handle_keys(snake, game_info)
        snake.move()
        if (snake.get_head_position() in snake.positions[1:]):
            snake.update_max_score(game_info)
            snake.reset()
            drop_tail = False
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == apple.position:
            drop_tail = False
            apple.randomize_position(snake.positions)
        snake.draw(drop_tail)
        apple.draw()

        pg.display.update()
        update_screen_title(game_info, len(snake.positions))
        clock.tick(game_info["speed"])


if __name__ == '__main__':
    main()
