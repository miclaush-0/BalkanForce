import random
import time

import pygame

FPS = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load('Assets/bullet.png').convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.x = x
        self.y = y

    def render(self):
        self.surface.blit(self.image, (0, 0))


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('Assets/enemy.png').convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.x = x
        self.y = y

    def render(self):
        self.surface.blit(self.image, (0, 0))


class Player:
    def __init__(self):
        self.image = pygame.image.load('Assets/player.png').convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.x = WINDOW_WIDTH / 2 - self.image.get_width() / 2
        self.y = 640
        self.speed = 0.4
        self.score = 0

    def render(self):
        self.surface.blit(self.image, (0, 0))


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/PublicPixel-z84yD.ttf', 40)
font_ = pygame.font.Font('Fonts/PublicPixel-z84yD.ttf', 30)

# loading graphics
grass = []
for i in range(0, 4):
    path = 'Assets/Tiles/grass' + str(i) + '.png'
    grass.append(pygame.image.load(path))

tree = []
for i in range(0, 3):
    path = 'Assets/Tiles/tree' + str(i) + '.png'
    tree.append(pygame.image.load(path))

# pre tiles generation
background = []
for i in range(-WINDOW_HEIGHT, WINDOW_HEIGHT, 32):
    for j in range(0, WINDOW_WIDTH, 32):
        background.append([random.randint(0, 3), i, j])

trees = []
for i in range(-WINDOW_HEIGHT, WINDOW_HEIGHT, random.randint(20, 30)):
    for j in range(0, WINDOW_WIDTH, 26):
        if random.randint(0, 100) > 30:
            trees.append([random.randint(0, 2), i, j])

# generating first enemies
enemies = [Enemy(random.randint(0, 9) * 64, -70), Enemy(random.randint(0, 9) * 64, -70)]


player = Player()

# bullets
bullets = []

file = open('data', 'r')
last_score = file.read()
file.close()
intro = True
in_game = False
alpha_level = 0
fade_speed = 4
enemy_speed = 0.1
bullet_dt = time.time()
space = False

score = 0

# Game loop
while True:
    dt = clock.tick(FPS)
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if in_game and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x+player.width/2-6, player.y))

    # keyboard input & player update
    keys = pygame.key.get_pressed()
    if not in_game:
        if keys[pygame.K_SPACE]:
            intro = True
            in_game = True
            alpha_level = 0
            score = 0
    else:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player.x - player.speed*dt <= 0:
                player.x = 0
            else:
                player.x -= player.speed * dt
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player.x + player.speed * dt >= WINDOW_WIDTH - player.width:
                player.x = WINDOW_WIDTH - player.width
            else:
                player.x += player.speed * dt

    # render & update background
    for i in background:
        surface.blit(grass[i[0]], (i[2], i[1]))
        i[1] += 0.5
        if i[1] > WINDOW_HEIGHT:
            i[1] = -WINDOW_HEIGHT
            i[0] = random.randint(0, 3)

    for i in trees:
        surface.blit(tree[i[0]], (i[2], i[1]))
        i[1] += 0.5
        if i[1] > WINDOW_HEIGHT:
            i[1] = -WINDOW_HEIGHT
            i[0] = random.randint(0, 2)

    if in_game:
        # update & render player
        player.render()
        surface.blit(player.surface, (player.x, player.y))

        # update & render enemies
        for enemy in enemies:
            enemy.y += enemy_speed *dt
            if enemy.x > WINDOW_WIDTH-63 or enemy.x < 0:
                enemies.remove(enemy)
            if enemy.y >= 700:
                last_score = str(score)
                file = open('data', 'w')
                file.write(str(last_score))
                file.close()
                in_game = False
            enemy.render()
            surface.blit(enemy.surface, (enemy.x, enemy.y))

        # update & render bullets
        for bullet in bullets:
            if bullet.y <= -20:
                bullets.remove(bullet)
            bullet.y -= dt * 0.5
            bullet.render()
            surface.blit(bullet.surface, (bullet.x, bullet.y))


        # update & delete enemies and bullets
        for bullet in bullets:
            for enemy in enemies:
                if bullet.x >= enemy.x and bullet.x <= enemy.x + enemy.width:
                    if bullet.y > enemy.y and bullet.y <  enemy.y+enemy.height:
                        try:
                            bullets.remove(bullet)
                            enemies.remove(enemy)
                        except:
                            pass
                        score += 2



        # enemies spawn
        if len(enemies) <= score/10 and len(enemies) <= 12:
            x = random.randint(0, WINDOW_WIDTH-63)
            if WINDOW_WIDTH%63 != 0:
                x -= WINDOW_WIDTH%63
            y = -70
            enemies.append(Enemy(x, y))

    if intro:
        alpha_level += fade_speed
    if alpha_level >= 255:
        intro = False
        alpha_level = 255


    # render text
    if not in_game:
        title = font.render('Balkan Force', True, (255, 255, 255))
        button = font_.render('<Press SPACE>', True, (255, 255, 255))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 - 2, WINDOW_HEIGHT / 2 - 40 - 2))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 - 2, WINDOW_HEIGHT / 2 - 40 + 2))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 + 2, WINDOW_HEIGHT / 2 - 40 + 2))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 + 2, WINDOW_HEIGHT / 2 - 40 - 2))
        title = font.render('Balkan Force', True, (255, 255, 0))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230, WINDOW_HEIGHT / 2 - 40))

        surface.blit(button, (WINDOW_WIDTH / 2 - 200 - 1, 650 - 2))
        surface.blit(button, (WINDOW_WIDTH / 2 - 200 - 1, 650 + 2))
        surface.blit(button, (WINDOW_WIDTH / 2 - 200 + 1, 650 + 2))
        surface.blit(button, (WINDOW_WIDTH / 2 - 200 + 1, 650 - 2))
        button = font_.render('<Press SPACE>', True, (255, 255, 0))
        surface.blit(button, (WINDOW_WIDTH / 2 - 200, 650))

        last_ = font_.render('last score', True, (255, 255, 0))
        surface.blit(last_, (280, 50))
        last_ = font_.render(last_score, True, (255, 255, 0))
        surface.blit(last_, (400, 100))

    if in_game:
        score_ = font_.render(str(score), True, (255, 255, 0))
        surface.blit(score_, (500, 50))

    surface.set_alpha(alpha_level)
    window.blit(surface, (0, 0))

    pygame.display.flip()
