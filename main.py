from random import randint
import pygame
from pygame import display
from pygame import event
from pygame import key
from pygame.time import Clock
from pygame.image import load
from pygame.transform import scale
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide

### Inicialização do jogo ### 

pygame.init()

### Criação do Canvas e do fundo ###

tamanho_do_canvas = (1280, 720)

fundo = scale(
    load('images/space.jpg'),
    tamanho_do_canvas
)

display.set_caption(
    'Dunofausto e as torradas espaciais'
)

canvas = display.set_mode(
    size = tamanho_do_canvas,
    display = 0,
    depth = 0
)

### Criação das classes dos personagens ###

### Dunofausto ###

class Dunofausto(Sprite):
    def __init__(self, torrada):
        super().__init__()

        self.image = load('images/dunofausto_small.png')
        self.rect = self.image.get_rect(center=(10, 360))
        self.torrada = torrada
        self.velocidade = 3

    def tacar_torrada(self):
        if len(self.torrada) < 10: 
            self.torrada.add(
                Torrada(self.rect.center[0], self.rect.center[1])
            )

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade

### Torrada ###

class Torrada(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('images/toast_small.png')
        self.rect = self.image.get_rect(
            center = (x, y)
        )

    def update(self):
        self.rect.x += 3
        if self.rect.x > tamanho_do_canvas[0]:
            self.kill

### Inimigo ###

class Inimigo(Sprite):
    def __init__(self):
        super().__init__()

        self.image = load('images/inimigo_1.png')
        self.rect = self.image.get_rect(
            center = (1280, randint(20, 580))
        )

    def update(self):
        self.rect.x += -2

### Grupos ###

grupo_torrada = Group()

grupo_inimigo = Group()
grupo_inimigo.add(Inimigo())

dunofausto = Dunofausto(grupo_torrada)
grupo_dunofausto = GroupSingle(dunofausto)

clock = Clock()
mortes = 0
round = 0

while True:

### Eventos ###

    clock.tick(120)

    if round % 120 == 0:
        if mortes < 20:
            grupo_inimigo.add(Inimigo())
        for _ in range(int(mortes/20)):
            grupo_inimigo.add(Inimigo())

    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit()

        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                dunofausto.tacar_torrada()

    if groupcollide(grupo_torrada, grupo_inimigo, True, True):
        mortes += 1

### Atualização do display ###

    canvas.blit(fundo, (0, 0))

    grupo_dunofausto.draw(canvas)
    grupo_dunofausto.update()

    grupo_torrada.draw(canvas)
    grupo_torrada.update()

    grupo_inimigo.draw(canvas)
    grupo_inimigo.update()

    display.update()
    round += 1
