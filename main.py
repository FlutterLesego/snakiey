# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface, score):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)

    # Draw the score text
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(score_text, (10, 10))

    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def get_level(score):
    if score < 10:
        return 1
    elif score < 20:
        return 2
    elif score < 30:
        return 3
    elif score < 40:
        return 4
    else:
        return 5

def game_over_screen(surface, score):
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    play_again_text = font.render("Play Again", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))

    play_again_rect = play_again_text.get_rect(center=(width // 3, 3 * width // 4))
    exit_rect = exit_text.get_rect(center=(2 * width // 3, 3 * width // 4))

    surface.fill((0, 0, 0))
    surface.blit(text, (width // 2 - text.get_width() // 2, width // 3))
    surface.blit(score_text, (width // 2 - score_text.get_width() // 2, width // 2))
    pygame.draw.rect(surface, (0, 0, 0), play_again_rect, border_radius=10)
    surface.blit(play_again_text, play_again_rect.topleft)
    pygame.draw.rect(surface, (0, 0, 0), exit_rect, border_radius=10)
    surface.blit(exit_text, exit_rect.topleft)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    return True
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def fading_text_animation(surface, text, duration):
    font = pygame.font.SysFont(None, 36)
    alpha = 255

    for frame in range(60):  # Fading animation duration (60 frames)
        surface.fill((0, 0, 0))
        alpha -= 4
        text_surface = font.render(text, True, (255, 255, 255, alpha))
        text_rect = text_surface.get_rect(center=(width // 2, 30))
        surface.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(duration // 60)  # Adjust the delay for smoother animation

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True
    score = 0  # Initialize the score
    speeds = [5, 10, 15, 20, 25]  # Adjust these values as needed
    level = 0
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(speeds[level])
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))
            score += 1  # Increment the score when a snack is eaten

            # Update the level and speed based on the score
            new_level = get_level(score)
            if new_level != level:
                level = new_level
                fading_text_animation(win,f"Level {level}", 1500)
                if level < len(speeds):
                    clock.tick(speeds[level])  # Set the new speed based on the level

                if level == 5:
                    # Reached the maximum level, cap the speed at the fastest value
                    clock.tick(speeds[-1])

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', score)  # Print the final score
                if game_over_screen(win, score):
                    s.reset((10, 10))
                    score = 0
                    level = 0
                    break

        redrawWindow(win, score)  # Pass the score to the redrawWindow function

    pygame.quit()

if __name__ == "__main__":
    main()