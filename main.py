import random
import pygame

FPS = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


class Player:
    def __init__(self):
        self.image = pygame.image.load('Assets/player.png').convert_alpha()
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA, 32)
        self.x = WINDOW_WIDTH/2 - self.image.get_width()/2
        self.y = 650
        self.speed = 5

    def render(self):
        self.surface.blit(self.image, (0, 0))


pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/PublicPixel-z84yD.ttf', 40)
font_ = pygame.font.Font('Fonts/PublicPixel-z84yD.ttf', 23)


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
for i in range(-WINDOW_HEIGHT, WINDOW_HEIGHT, random.randint(1,30)):
    for j in range(0, WINDOW_WIDTH, 26):
        trees.append([random.randint(0, 2), i, j])

player = Player()

intro = True
in_game = False
alpha_level = 0
fade_speed = 4

lef_key = False
right_key = False
space = False

# Game loop
while True:
    dt = clock.tick(FPS)
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # keyboard input & update
    keys = pygame.key.get_pressed()
    if not in_game:
        if keys[pygame.K_SPACE]:
            intro = True
            in_game = True
            alpha_level = 0

    else:
        pass


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
        player.render()
        surface.blit(player.surface, (player.x, player.y))

    if intro:
        alpha_level += fade_speed
    if alpha_level >= 255:
        intro = False
        alpha_level = 255

    # render text
    if not in_game:
        title = font.render('Balkan Force', True, (255, 255, 255))
        button = font_.render('<Press SPACE to start>', True, (255, 255, 255))
        surface.blit(title, (WINDOW_WIDTH/2-230-2, WINDOW_HEIGHT/2-40-2))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 - 2, WINDOW_HEIGHT / 2 - 40 + 2))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 + 2, WINDOW_HEIGHT / 2 - 40 + 2))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230 + 2, WINDOW_HEIGHT / 2 - 40 - 2))
        title = font.render('Balkan Force', True, (255, 255, 0))
        surface.blit(title, (WINDOW_WIDTH / 2 - 230, WINDOW_HEIGHT / 2 - 40))

        surface.blit(button, (WINDOW_WIDTH / 2 - 250 - 1, 650 - 1))
        surface.blit(button, (WINDOW_WIDTH / 2 - 250 - 1, 650 + 1))
        surface.blit(button, (WINDOW_WIDTH / 2 - 250 + 1, 650 + 1))
        surface.blit(button, (WINDOW_WIDTH / 2 - 250 + 1, 650 - 1))
        button = font_.render('<Press SPACE to start>', True, (255, 255, 0))
        surface.blit(button, (WINDOW_WIDTH/2 - 250, 650))

    surface.set_alpha(alpha_level)
    window.blit(surface, (0, 0))

    pygame.display.flip()
    print('fps=', clock.get_fps())

