import pygame
import sys
import random

from pygame.locals import *

import time

pygame.init()
clock = pygame.time.Clock()
fps = 60

width = 800
height = 736
Z = [width, height]
screen = pygame.display.set_mode(Z)
pygame.display.set_caption('Flappy Bird')


# Font
font = pygame.font.SysFont('Bauhaus 93', 60)
font1 = pygame.font.SysFont(None, 24)

white = (255, 255, 255)

# Game variables
ground_scrool = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # 1.5 sec
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
starting_text = 'Veritas Aequitas '

# Images
background = pygame.image.load('img/bg.png')
ground_image = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

# from pyvidplayer import Video

#Video

# vid = Video('img/video1.mp4')
# vid.set_size((800,736))

# def after_dead():
#      vid.draw(K_PRINTSCREEN,(0,0))
#      pygame.display.update()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(height) / 2 - 100
    score = 0
    return score



class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            # img = pygame.image.load(f'img/bird{num}.png')
            img = pygame.image.load(f'img/birdberkay.jpg')


            self.images.append(img)

        # First image
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying == True:
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 616:
                self.rect.y += int(self.vel)

        # Jump
        # Mouse button has been clicked
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
                self.rect.bottom += self.vel

            # Mouse button has been relased
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # # Rotate bird whenever its in the sky
            if self.rect.bottom < 616:
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1.5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        # Delete the old pipes
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(height) / 2 - 100)
bird_group.add(flappy)

# Restart button
button = Button(width // 2 - 70, height // 2 - 100, button_img)

run = True
while run:

    clock.tick(fps)

    screen.blit(background, (0, 0))

    # Drawing Background
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    screen.blit(ground_image, (ground_scrool, 620))
    img = font1.render(starting_text, True, white)
    if not flying:
        screen.blit(img, (width/2-150, 200))


    # Check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(width) / 2 - 50, 20)
    # Looking for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    print(game_over)
    if game_over == True:
        # after_dead()
        if button.draw():
            game_over = False
            score =reset_game()

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            dice = random.randint(1, 5)

            if dice == 1:
                top_pipe = Pipe(width, height - 100, +1)
            else:
                btm_pipe = Pipe(width, int(height) / 2 - 70 + pipe_height, -1)
                top_pipe = Pipe(width, int(height) / 2 - 70 + pipe_height, +1)
                pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        ground_scrool -= scroll_speed
        if abs(ground_scrool) > 35:
            ground_scrool = 0
        pipe_group.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True



    pygame.display.update()
