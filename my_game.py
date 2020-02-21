import pygame
import random
import math
from pygame import mixer

# initialize
pygame.init()
height = 600
width = 500
screen = pygame.display.set_mode(size=(width, height))
score = 0
clock = pygame.time.Clock()
life = 3

# icon
pygame.display.set_caption("Space invaders_ my first game")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player default position
player_img = pygame.image.load('space-invaders2_.png')
playerX = (width - 50) // 2
playerY = height - 150
player_move_horizontal = 0
player_move_vertical = 0
player_life = pygame.image.load('heart.png')

# space back ground
back_ground = pygame.image.load('space_background.jpg')

# bottom city
city = [pygame.image.load('cityscape.png'),
        pygame.image.load('cityscape 2.png'),
        pygame.image.load('cityscape3.png')]
cloud = [pygame.image.load('cloud_1.png'),
         pygame.image.load('cloud_2.png')]

# Enemies

# single enemies
enemy_img = pygame.image.load('ghost.png').convert()
enemyX = random.randrange(0, width - 25, 25)
enemyY = random.randrange(50, 125, 25)
enemy_move_horizontal = 0.27
enemy_move_vertical = 50
enemy_die = False
e_speed = 0.3

# multiple enemies
max_enemies = 6
list_enemy_img = [enemy_img for i in range(max_enemies)]
list_enemyX = []
list_enemyY = []
for i in range(max_enemies):
    list_enemyX.append(random.randrange(0, width - 25, 25))
    list_enemyY.append(random.randrange(50, 125, 25))
list_enemy_move_horizontal = [enemy_move_horizontal for i in range(max_enemies)]
list_enemy_move_vertical = [enemy_move_vertical for i in range(max_enemies)]

# bullet
# if bullet_ready false, it cant be seen
bullet_img = pygame.image.load('bullet_no_bg.png').convert()
bulletX = 0
bulletY = playerY
bullet_move_vertical = 0.5
bullet_move_horizontal = 0
bullet_ready = True

# Score_value
font = pygame.font.Font('freesansbold.ttf', 32)

# game over
game_over_text = pygame.font.Font('freesansbold.ttf', 64)

# play music
pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.mixer.music.load('Anh Thanh Nien - HuyR.mp3')
pygame.mixer.music.play(-1)


def show_game_over():
    text_display = game_over_text.render("GAME OVER", True, (250, 0, 0))
    screen.blit(text_display, (70, 180))
    pygame.event.wait()


def show_score(x, y):
    score_display = font.render("Score :" + str(score), True, (0, 0, 0))
    screen.blit(score_display, (x, y))


def display_bullet(pos_x, pos_y):
    global bullet_ready
    bullet_ready = False
    screen.blit(bullet_img, (pos_x + 12.5, pos_y - 35))


# display ghost_die img when collision happened?..
def display_enemy(pos_x, pos_y, i):
    screen.blit(list_enemy_img[i], (pos_x, pos_y))


def re_spawn_enemy():
    global enemyX, enemyY, enemy_die
    enemyX = random.randrange(0, width - 25, 25)
    enemyY = random.randrange(50, 125, 25)
    enemy_die = False


def re_spawn_enemy_(i):
    global list_enemyX, list_enemyY, enemy_die
    list_enemyX[i] = random.randrange(0, width - 25, 25)
    list_enemyY[i] = random.randrange(50, 125, 25)
    enemy_die = False


def is_collision(enemy, bullet):
    distance = math.sqrt(
        math.pow(enemy[0] - bullet[0], 2) + math.pow(enemy[1] - bullet[1], 2))
    if distance < 56:
        return True
    else:
        return False


def re_spawn_player():
    global playerX, playerY
    playerX = (width - 50) // 2
    playerY = height - 150


def display_city():
    for place in range(0, width, 50):
        if place % 15 == 0:
            screen.blit(city[0], (place, height - 50))
        elif place % 10 == 0:
            screen.blit(city[1], (place, height - 50))
        else:
            screen.blit(city[2], (place, height - 50))


def display_cloud():
    for place in range(0, width, 50):
        if place % 100 == 0:
            screen.blit(cloud[0], (place, height - 100))
        else:
            screen.blit(cloud[1], (place, height - 100))


def display_background():
    # screen.blit(back_ground, (0, 0))
    display_city()
    display_cloud()
    for i in range(life):
        screen.blit(player_life, (width - 50 - i * 50, 0))


def init_player(pos_x, pos_y):
    screen.blit(player_img, (pos_x, pos_y))


def eat_the_ship(ship, enemy):
    distance = math.sqrt(
        math.pow((enemy[0] - ship[0]), 2) + math.pow((enemy[1] - ship[1]), 2))
    if distance < 55:
        return True
    else:
        return False


# Game loop
num_enemies = 1
running = True
while running:
    # set screen RGB
    screen.fill((250, 250, 250))
    display_background()
    # display enemy if it reach the cloud or it catch the ship, we lose
    for i in range(num_enemies if num_enemies <= max_enemies else max_enemies):
        if list_enemyX[i] <= 0:
            list_enemyX[i] = 0
            list_enemy_move_horizontal[i] = e_speed
            list_enemyY[i] += list_enemy_move_vertical[i]
        elif list_enemyX[i] >= width - 50:
            list_enemyX[i] = width - 50
            list_enemy_move_horizontal[i] = -e_speed
            list_enemyY[i] += list_enemy_move_vertical[i]

        if list_enemyY[i] + 50 >= (height - 100):
            print('lose')
            list_enemyY[i] = width - 50
            show_game_over()
            running = False

        if eat_the_ship([playerX, playerY], [list_enemyX[i], list_enemyY[i]]):
            print('ate')
            life -= 1
            if life > 0:
                re_spawn_enemy()
                re_spawn_player()
            else:
                show_game_over()
                running = False
        # check collision event:
        collision = is_collision([list_enemyX[i], list_enemyY[i]], [bulletX, bulletY])
        if collision and bullet_ready is False:
            score += 10
            # sound
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            # reload
            bulletY = playerY
            bullet_ready = True
            # re-spawn enemy
            enemy_die = True
            e_speed += 0.01
            num_enemies += 1
            re_spawn_enemy_(i)

        list_enemyX[i] += list_enemy_move_horizontal[i]
        display_enemy(list_enemyX[i], list_enemyY[i], i)

    # If player press something
    for event in pygame.event.get():
        # if quit
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is press, check left or right
        if event.type == pygame.KEYDOWN:
            # keydown mean press
            if event.key == pygame.K_RIGHT:
                player_move_horizontal = 0.3
                print("->right")
            if event.key == pygame.K_LEFT:
                player_move_horizontal = -0.3
                print("->left")
            if event.key == pygame.K_UP:
                player_move_vertical = -0.3
                print("->up")
            if event.key == pygame.K_DOWN:
                player_move_vertical = 0.3
                print("->down")
            if event.key == pygame.K_SPACE:
                if bullet_ready:
                    bullet_sound = mixer.Sound('Gun+Shot2.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    display_bullet(bulletX, bulletY)
                # -> bullet not ready
                print("->fire")

        if event.type == pygame.KEYUP:
            # keyup mean release
            if event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_LEFT or \
                    event.key == pygame.K_UP or \
                    event.key == pygame.K_DOWN or \
                    event.key == pygame.K_SPACE:
                player_move_horizontal = 0
                player_move_vertical = 0
                print("stop")

    # player movement
    playerX += player_move_horizontal
    playerY += player_move_vertical
    if playerX <= 0:
        playerX = 0
    elif playerX >= width - 50:
        playerX = width - 50
    if playerY <= 0:
        playerY = 0
    elif playerY >= height - 125:
        playerY = height - 125

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_ready = True
    if not bullet_ready:
        display_bullet(bulletX, bulletY)
        bulletY -= bullet_move_vertical

    show_score(0, 0)
    init_player(playerX, playerY)
    pygame.display.update()
    # end loop

pygame.quit()
quit()
