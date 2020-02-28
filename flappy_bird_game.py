import pygame
import neat
import time
import os
import random
from Bird import Bird
from Pipe import Pipe
from Base import Base
pygame.font.init()


# importo la dimensione della finestra del gioco
WIN_WIDTH = 600
WIN_HEIGHT = 800

# carico le immagini e le raddoppio come dimensioni


BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

'''OBJECT USED IN THE GAME
BIRD

PIPE

BASE

'''


# disegna la finestra del gioco
def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()


# main loop del game
def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    score = 0
    win = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
    clock = pygame.time.Clock()

    run = True
    while run:
        # faccio in modo che indipendentemente dal pc siano tenuti 30 fps
        clock.tick(30) # al piu farò 30 cicli al secondo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #bird.move()

        # list of removed pipes
        rem = []
        add_pipe = False
        for pipe in pipes:
            # check for collision
            if pipe.collide(bird):
                pass
            # check the position of pipe
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            # check if the pipe has been passed and generate a new one
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        # check if the bird hitted the floor
        if bird.y + bird.img.get_height() <= 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()


main()
