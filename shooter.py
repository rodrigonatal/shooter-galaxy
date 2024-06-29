from typing import Any
from pygame import *
from time import time as timer
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x , size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if  keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 45, 50)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = randint(0, 25)
            self.rect.x = randint(0, 700)
            lost = lost + 1

class Bullet (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y   <= 0:
            self.kill()

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = randint(0, 25)
            self.rect.x = randint(0, 700)
            
lost = 0
window = display.set_mode((700, 500))
display.set_caption("space shooting")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
rocket = Player("rocket.png", 15, 400, 15 , 95, 105)
alien = sprite.Group()
for i in range (5):
    ufo = Enemy('ufo.png', randint(95, 700 - 95 ), 0, randint(2, 4), 55, 55)
    alien.add(ufo)
asteroid = sprite.Group()
for i in range (2):
    aster = Meteor('asteroid.png', randint(95, 700 - 95), 0 , 2, 65, 65 )
    asteroid.add(aster)
bullets = sprite.Group()

run = True
finish = False
clock = time.Clock()
FPS = 60


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
shoot = mixer.Sound('fire.ogg')


font.init()
font1 = font.Font(None, 35)
font2 = font.Font(None, 85)
font3 = font.Font( None, 30)
win = font2.render("YOU WIN", True, (255, 255, 255))
lose = font2.render ("YOU LOSE", True, (255, 255, 255))
finish = False
poin = 0
num_fire = 0
rel_time = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time== False:
                    num_fire = num_fire + 1
                    shoot.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:            
        window.blit(background, (0,0))
        score= font1.render('Score:' + str(poin), True, (255, 255, 255))
        missed = font1.render('Missed:' + str(lost),True , (255, 255, 255))

        rocket.reset()
        rocket.update()
        alien.draw(window)
        alien.update()
        bullets.draw(window)
        bullets.update()
        asteroid.draw(window)
        asteroid.update()
        window.blit (score, (10,20))
        window.blit (missed, (10,40))
        if poin == 7:
            window.blit(win, (185, 250))
            finish = True
        collide = sprite.groupcollide(alien, bullets, True, True)
        collide = sprite.groupcollide(asteroid, bullets, False, True)
        for c in collide:
            poin += 1
            ufo = Enemy('ufo.png', randint(95, 700 - 95 ), 0 , randint(2, 4), 55, 55)
            alien.add(ufo)
        if sprite.spritecollide(rocket, alien, False) or lost == 10 or sprite.spritecollide(rocket, asteroid, False):
            window.blit(lose, (185, 250))
            finish = True
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font3.render ('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        display.update()
        clock.tick(FPS)