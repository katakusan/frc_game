from typing import Any
import pygame
from pygame.sprite import Group
import random
import os

FPS = 60
WIDTH = 800
HIGHT = 800

WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)


pygame.init()
screen = pygame.display.set_mode((WIDTH,HIGHT))
pygame.display.set_caption("testw")
clock = pygame.time.Clock()

note = pygame.image.load(os.path.join("note.png"))
robot= pygame.image.load(os.path.join("car.png"))
cube = pygame.image.load(os.path.join("cube.png"))
background = pygame.image.load(os.path.join("background.jpg"))
background1 = pygame.image.load(os.path.join("background1.jpg"))

write = pygame.font.match_font('arial')
def write_1(surf, text, size, x, y):
    font = pygame.font.Font(write, size)
    text_surface =font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = robot
        #self.image.fill(GREEN )
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HIGHT)
        self.speed = 8

    def update(self):
        mykeyslist = pygame.key.get_pressed()
        if mykeyslist[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if mykeyslist[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if mykeyslist[pygame.K_UP]:
            self.rect.y -= self.speed
        if mykeyslist[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HIGHT:
            self.rect.bottom = HIGHT

            
    def shoot(self):
        gun = Gun(self.rect.centerx, self.rect.top)
        all_sprites.add(gun)
        gun_1.add(gun)


    
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = cube
        self.image_ori_width = 50
        self.image_ori_hight = 50 
        self.image_ori = pygame.transform.scale(self.image_ori,(self.image_ori_width,self.image_ori_hight))
        self.image = self.image_ori.copy()
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(5,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = random.randrange(0,3)

    def rot(self):
        self.total_degree += self.rot_degree
        self.rot_degree = self.rot_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rot()
        self.rect.y += self.speedy
        if self.rect.top > HIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0 , WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedx = random.randrange(-3,3)
            self.speedy = random.randrange(5,10)
        self.rect.x += self.speedx

class Gun(pygame.sprite.Sprite):
    def __init__(self , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = note 
        self.image = pygame.transform.scale(self.image,(30,30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class skill(pygame.sprite.Sprite):
    def __init__(self , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
rock_1 = pygame.sprite.Group()
gun_1 = pygame.sprite.Group()
player = Player()
rock = Rock()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rock_1.add(r)
running = True
socre = 0
# 遊戲迴圈

while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rock_1,gun_1,True,True)
    for hit in hits:
        if hits :
            socre += 1
        r = Rock()
        all_sprites.add(r)
        rock_1.add(r)

    kick = pygame.sprite.spritecollide(player,rock_1 ,False, pygame.sprite.collide_mask )
    if kick:
        running = False



    #畫面顯式
    screen.fill((BLACK))
    screen.blit(background1,(0,0))
    screen.blit(background1,(0,400))
    write_1(screen, str(socre), 18 , WIDTH/2, HIGHT/9)
    all_sprites.draw(screen)
    pygame.display.update()


pygame.quit()


