import pygame
import random
from Player import Player
from Enemy import Enemy

pygame.init()

size    = (800, 600)
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode(size)
screen.fill((255, 255,255))
scoreFont = pygame.font.Font("fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
enemies = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()

def process_keys(keys, hero):
    if keys[pygame.K_w]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_a]:
        hero.sprite.movementVector[0] -= 1
    if keys[pygame.K_s]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d]:
        hero.sprite.movementVector[0] += 1
    if keys[pygame.K_1]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[0]
    if keys[pygame.K_2]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]

def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.shoot(pygame.mouse.get_pos())

def move_entities(hero, enemies, timeDelta):
    score = 0
    hero.sprite.move(screen.get_size(), timeDelta)
    for enemy in enemies:
        enemy.move(enemies, hero.sprite.rect.topleft, timeDelta)
        enemy.shoot(hero.sprite.rect.topleft)
    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta)
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.kill()
            hero.sprite.health -= 1
            if hero.sprite.health <= 0:
                hero.sprite.alive = False
    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta)
        enemiesHit = pygame.sprite.spritecollide(proj, enemies, True)
        if enemiesHit:
            proj.kill()
            score += len(enemiesHit)
    return score

def render_entities(hero, enemies):
    hero.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in enemies:
        enemy.render(screen)

def button(x, y, w, h, action = None):
    click = pygame.mouse.get_pressed()
    mopos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h))
    pygame.draw.rect(screen, (128, 128, 128), (x+2, y+2, w-4, h-4))  
    if x <= mopos[0] <= (x+w) and y <= mopos[1] <= (y+h):
        pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h))
        pygame.draw.rect(screen, (230, 230, 230), (x+2, y+2, w-4, h-4))
        if click[0] == 1 and action != None:
            if action == "play":
                exec(open('main.py').read())
            elif action == "exit":
                quit()

while True:
    click = pygame.mouse.get_pressed()
    mopos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                quit()
    button(150, 450, 200, 60, "play")
    button(450, 450, 200, 60, "exit")
    pygame.display.update()
