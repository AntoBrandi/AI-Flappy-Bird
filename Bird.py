import pygame
import os

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]


class Bird:
    # useful constants
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5  # quanto veloce vola

    # costruttore
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0 # tiene traccia dell'ultima volta nella quale ho saltato
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # jump function
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # DISPLACEMENT = calcolo di quanti pixel mi devo muovere sopra o sotto in questo frame
        # basato sulla velocità attuale calcolo di quento devo muovermi in alto o in basso
        # Fisica del gioco con tick_count assimilabile al tempo
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        # evito che la velocità sia troppo alta
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        # eseguo lo spostamento in alto / basso
        self.y = self.y + d

        # eseguo il tilt in alto
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # eseguo il tilt in basso
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    # disegno il bird nelle varie fasi
    def draw(self, win):
        self.img_count += 1

        # check which image should show based on the animation time
        # simulo l'uccello che sbatte le ali
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # when the bird is completely tilted, don't simulate the wings mouvement
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # ruoto l'immagine sulla base dell'inclinazione tilt
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    # rilevare le collisioni
    def get_mask(self):
        return pygame.mask.from_surface(self.img)