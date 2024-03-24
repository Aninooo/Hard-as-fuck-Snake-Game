# Snake Game
# Copyright (c) 2024 Bryan Lomerio
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

PLAY_AREA_WIDTH = WIDTH - 40
PLAY_AREA_HEIGHT = HEIGHT - 40
PLAY_AREA_GRID_WIDTH = PLAY_AREA_WIDTH // CELL_SIZE
PLAY_AREA_GRID_HEIGHT = PLAY_AREA_HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

highest_score = 0
SNAKE_SPEED = 10
SPEED_INCREMENT = 8

def display_instructions():
    font = pygame.font.Font(None, 24)
    instruction_texts = [
        "Welcome to Snake Game!",
        "",
        "Use arrow keys to control the snake.",
        "Eat the red squares to grow.",
        "Avoid running into the walls or yourself.",
        "",
        "Press ENTER to start the game.",
        "",
        "*** Warning: This game may not make you happy! ***"  # Warning message
    ]

    total_height = len(instruction_texts) * 20
    start_y = (HEIGHT - total_height) // 2

    for i, text in enumerate(instruction_texts):
        if "*** Warning:" in text:
            text_surface = font.render(text, True, RED)  
        else:
            text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, start_y + i * 20))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

class Snake:
    def __init__(self):
        self.body = [(PLAY_AREA_GRID_WIDTH // 2, PLAY_AREA_GRID_HEIGHT // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def move(self):
        head = self.body[0]
        x, y = head
        if self.direction == pygame.K_UP:
            y -= 1
        elif self.direction == pygame.K_DOWN:
            y += 1
        elif self.direction == pygame.K_LEFT:
            x -= 1
        elif self.direction == pygame.K_RIGHT:
            x += 1

        x = max(0, min(x, PLAY_AREA_GRID_WIDTH - 1))
        y = max(0, min(y, PLAY_AREA_GRID_HEIGHT - 1))

        if (x, y) in self.body[1:]:
            return True  

        self.body.insert(0, (x, y))
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        x, y = tail
        self.body.append((x, y))

  
    def draw(self):
        head_x, head_y = self.body[0]
        pygame.draw.rect(screen, GRAY, (head_x * CELL_SIZE + 20, head_y * CELL_SIZE + 20, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (head_x * CELL_SIZE + 21, head_y * CELL_SIZE + 21, CELL_SIZE - 2, CELL_SIZE - 2))
        pygame.draw.circle(screen, RED, (head_x * CELL_SIZE + 30, head_y * CELL_SIZE + 30), 8)  # Example design: circle
        
        # Draw body segments
        for segment in self.body[1:]:
            pygame.draw.rect(screen, GRAY, (segment[0] * CELL_SIZE + 20, segment[1] * CELL_SIZE + 20, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE + 21, segment[1] * CELL_SIZE + 21, CELL_SIZE - 2, CELL_SIZE - 2))

    def collide_with_wall(self):
        head = self.body[0]
        x, y = head
        return x <= 0 or x >= PLAY_AREA_GRID_WIDTH - 1 or y <= 0 or y >= PLAY_AREA_GRID_HEIGHT - 1

class Food:
    def __init__(self, snake, obstacles):
        self.position = self.new_position(snake, obstacles)

    def new_position(self, snake, obstacles):
        while True:
            x = random.randint(1, PLAY_AREA_GRID_WIDTH - 2)
            y = random.randint(1, PLAY_AREA_GRID_HEIGHT - 2)
            if (x, y) not in snake.body and (x, y) not in [obstacle.position for obstacle in obstacles]:
                return x, y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * CELL_SIZE + 20, self.position[1] * CELL_SIZE + 20, CELL_SIZE, CELL_SIZE))


def draw_play_area():
    pygame.draw.rect(screen, WHITE, (20, 20, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT), 2)

class Obstacle:
    def __init__(self):
        self.position = self.new_position()

    def new_position(self):
        x = random.randint(1, PLAY_AREA_GRID_WIDTH - 2)
        y = random.randint(1, PLAY_AREA_GRID_HEIGHT - 2)
        return x, y

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.position[0] * CELL_SIZE + 20, self.position[1] * CELL_SIZE + 20, CELL_SIZE, CELL_SIZE))


def game():
    global highest_score, SNAKE_SPEED
    snake = Snake()
    obstacles = [Obstacle() for _ in range(5)]  
    food = Food(snake, obstacles)  
    running = True
    game_over = False

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highest_score(highest_score)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != pygame.K_DOWN:
                    snake.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN and snake.direction != pygame.K_UP:
                    snake.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT:
                    snake.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT:
                    snake.direction = pygame.K_RIGHT

        if not game_over:
            if snake.move():
                game_over = True 

            if snake.collide_with_wall():
                game_over = True

            for obstacle in obstacles:
                if snake.body[0] == obstacle.position:
                    game_over = True

            if snake.body[0] == food.position:
                snake.grow()
                food.position = food.new_position(snake, obstacles) 
                # Increase speed
                SNAKE_SPEED += SPEED_INCREMENT

            score = len(snake.body) - 1
            if score > highest_score:
                highest_score = score

            snake.draw()
            food.draw()
            draw_play_area()

            # Draw obstacles
            for obstacle in obstacles:
                obstacle.draw()
        else:
            show_game_over_screen(snake)

        pygame.display.flip()
        clock.tick(SNAKE_SPEED)  


def show_game_over_screen(snake):
    global highest_score, SNAKE_SPEED
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over!", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(game_over_text, text_rect)

    score_text = font.render(f"Score: {len(snake.body) - 1}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)

    highest_score_text = font.render(f"Highest Score: {highest_score}", True, WHITE)
    highest_score_rect = highest_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(highest_score_text, highest_score_rect)

    try_again_text = font.render("Try Again?", True, WHITE)
    try_again_rect = try_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    screen.blit(try_again_text, try_again_rect)

    yes_text = font.render("Yes", True, WHITE)
    yes_rect = yes_text.get_rect(center=(WIDTH // 2 - 50, HEIGHT // 2 + 120))
    screen.blit(yes_text, yes_rect)

    no_text = font.render("No", True, WHITE)
    no_rect = no_text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 + 120))
    screen.blit(no_text, no_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_rect.collidepoint(mouse_pos):
                    SNAKE_SPEED = 10  
                    game() 
                elif no_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()



def get_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(str(score))


def main():
    global highest_score
    running = True
    instructions_displayed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highest_score(highest_score)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    instructions_displayed = True
                elif event.key == pygame.K_ESCAPE:
                    save_highest_score(highest_score)
                    pygame.quit()
                    sys.exit()

        if not instructions_displayed:
            screen.fill(BLACK)
            display_instructions()
        else:
            screen.fill(BLACK)
            game()

        font = pygame.font.Font(None, 24)
        text_surface = font.render("Created by Bryan Lomerio", True, WHITE)
        text_rect = text_surface.get_rect(bottomleft=(10, HEIGHT - 10))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    highest_score = get_highest_score()
    main()

           
