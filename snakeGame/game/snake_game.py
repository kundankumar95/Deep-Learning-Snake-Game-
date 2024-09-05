import numpy as np
import pygame
from pygame.locals import *

# Define constants
WIDTH, HEIGHT, BLOCK_SIZE = 600, 400, 20
FPS = 15

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.snake_dir = (0, -BLOCK_SIZE)
        self.food = self._generate_food()
        self.done = False
        self.score = 0
        return self._get_state()

    def _generate_food(self):
        x = np.random.randint(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
        y = np.random.randint(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
        return (x, y)

    def _get_state(self):
        state = np.zeros((WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE))
        for x, y in self.snake:
            state[x // BLOCK_SIZE, y // BLOCK_SIZE] = 1
        state[self.food[0] // BLOCK_SIZE, self.food[1] // BLOCK_SIZE] = 2
        return state

    def step(self, action):
        if action == 0:
            self.snake_dir = (0, -BLOCK_SIZE)
        elif action == 1:
            self.snake_dir = (BLOCK_SIZE, 0)
        elif action == 2:
            self.snake_dir = (0, BLOCK_SIZE)
        elif action == 3:
            self.snake_dir = (-BLOCK_SIZE, 0)

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.snake_dir[0], head_y + self.snake_dir[1])
        if (new_head in self.snake or
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= WIDTH or new_head[1] >= HEIGHT):
            self.done = True
            return self._get_state(), -10, self.done

        self.snake = [new_head] + self.snake[:-1]
        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self._generate_food()
            self.score += 10
            reward = 10
        else:
            reward = 0

        return self._get_state(), reward, self.done

    def render(self):
        self.display.fill((0, 0, 0))
        for x, y in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, (255, 0, 0), (*self.food, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()
        self.clock.tick(FPS)

    def close(self):
        pygame.quit()
