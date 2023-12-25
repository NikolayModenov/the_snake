from random import choice, randint

import pygame

pygame.init()

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

BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FRAME_COLOR = (93, 216, 228)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


def handle_keys(game_object, event):
    """
    Determine the new direction of the target's movement
    according to the pressed key.
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and game_object.direction != DOWN:
            game_object.next_direction = UP
        elif event.key == pygame.K_DOWN and game_object.direction != UP:
            game_object.next_direction = DOWN
        elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
            game_object.next_direction = LEFT
        elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
            game_object.next_direction = RIGHT


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

    @staticmethod
    def checking_boundaries(current_position: list[list[int]]):
        """
        If a moving game object goes over the edge of the screen,
        release it from the opposite side.
        """
        if current_position[0][0] < 0:
            current_position[0][0] = SCREEN_WIDTH - GRID_SIZE
        elif current_position[0][0] > (SCREEN_WIDTH - GRID_SIZE):
            current_position[0][0] = 0
        if current_position[0][1] < 0:
            current_position[0][1] = SCREEN_HEIGHT - GRID_SIZE
        if current_position[0][1] > (SCREEN_HEIGHT - GRID_SIZE):
            current_position[0][1] = 0

    @staticmethod
    def randomize_position() -> list[int]:
        """Assign random coordinates to the game object."""
        width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return [width, height]

    def draw(self):
        """
        Define how the object will be drawn on the screen,
        by default 'pass'.
        """
        pass


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
        self.positions = [position]
        self.body_color = body_color
        self.frame_color = frame_color
        self.length = len(self.positions)
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.hunger = True

    def update_direction(self):
        """
        Change the direction of the snake's movement
        if it has been changed.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, surface=screen):
        """
        If the snake has not bitten itself,
        move it in the specified direction.
        Otherwise, erase the snake and create it in the center of the screen.
        If the snake has eaten an apple, do not erase its last cell.
        """
        width, height = self.direction
        new_position = [
            [(width * GRID_SIZE + self.positions[0][0]),
             (height * GRID_SIZE + self.positions[0][1])]
        ]
        self.checking_boundaries(new_position)
        self.positions = new_position + self.positions
        self.length = len(self.positions)
        if self.length == 1:
            self.get_head_position()
        if self.positions[0] in self.positions[1:]:
            self.reset()
        else:
            self.draw()
            last_rect = pygame.Rect(
                (self.positions[-1][0], self.positions[-1][1]),
                (GRID_SIZE, GRID_SIZE)
            )
            if self.hunger is True:
                pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
                self.positions.pop(-1)
            else:
                self.hunger = True

    def draw(self, surface=screen):
        """
        Draw all the cells of the snake's body
        in the form of colored squares with frames.
        """
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, self.frame_color, rect, 1)

    def get_head_position(self, surface=screen):
        """
        Draw the snake's head
        in the form of a colored square with a frame.
        """
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, self.frame_color, head_rect, 1)
        return head_rect

    def reset(self, surface=screen):
        """Erase the snake and draw a new one in the center of the screen."""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        self.positions.clear()
        self.positions += [COORDINATES_CENTRAL_CELL]
        self.get_head_position()


class Apple(GameObject):
    """This class draws an apple in a random place inside the screen."""

    def __init__(
            self,
            position: list[int] = [],
            body_color: tuple[int, int, int] = APPLE_COLOR,
            frame_color: tuple[int, int, int] = FRAME_COLOR,
    ):
        super().__init__(position)
        self.position = self.randomize_position()
        self.body_color = body_color
        self.frame_color = frame_color

    def draw(self, surface=screen):
        """
        Draw an apple in the form of a colored square with a frame
        and return the information about the drawn square.
        """
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, self.frame_color, rect, 1)
        return rect

    def draw_eaten_apple(self, surface=screen):
        """Erase the eaten apple."""
        pygame.draw.rect(surface, SNAKE_COLOR, self.draw())


def main():
    """
    Launch the Snake game.
    Control the snake with the arrow keys on the keyboard.
    If the snake bites itself or fills the entire playing field,
    then reset the game.
    """
    game_apple = Apple()
    game_apple.draw()

    game_snake = Snake()
    game_snake.get_head_position()

    while True:
        if game_snake.length == GRID_HEIGHT * GRID_WIDTH:
            game_snake.reset()
        for event in pygame.event.get():
            handle_keys(game_snake, event)
            game_snake.update_direction()
            if event.type == pygame.QUIT:
                pygame.quit()
        if game_snake.get_head_position().colliderect(game_apple.draw()):
            game_apple.draw_eaten_apple()
            while game_apple.position in game_snake.positions:
                game_apple.position = game_apple.randomize_position()
            game_apple.draw()
            game_snake.hunger = False
        game_snake.move()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
