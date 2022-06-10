# import files
import pygame
import random
from pygame import mixer

pygame.init()
pygame.mixer.init()

running = True
GRAVITY = pygame.Vector2()
GRAVITY.y = 9
GRAVITY.x = 0

mass = 0.5
jump_vel = 18
is_jumping = False
vel = 8
position = pygame.Vector2()
position.xy = 366, 266
(width, height) = (800, 600)

# sounds
mixer.music.load('Sounds/background_noise.wav')
score_sound = mixer.Sound('Sounds/score_cheering.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.02)

# score
can_score = True
score_value = 0
font = pygame.font.SysFont('system', 32)
text_x = 10
text_y = 10

# timer
current_time = 0
score_time = 0

# basket position
basket_pos = pygame.Vector2()
basket_pos.xy = 0, 300
move = 1

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height), vsync=1)
pygame.display.set_caption('BasketBall')
basket = pygame.image.load('Sprites/hoop.png')
background = pygame.image.load('Sprites/background.jpg')

# ball
ball = pygame.image.load('Sprites/basketball-ball.png')
ball_rect = ball.get_rect()

# obstacle
obstacle = pygame.image.load('Sprites/saw-tool.png')
obstacle_rect = obstacle.get_rect()
obstacle_pos = pygame.Vector2()
obstacle_pos.xy = 0, 0
obstacle_time = 0
can_spawn = True

# collision
collision_tolerance = -20

# game over text
over_font = pygame.font.SysFont('system', 80)
over = False


def spawn_obstacle():
    global obstacle_pos, obstacle_time, can_spawn
    if can_spawn:
        obstacle_time = pygame.time.get_ticks()
        obstacle_pos.x = random.randint(25, 300)
        obstacle_pos.y = random.randint(100, 400)
        return True
    else:
        return False


def game_over():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    mixer.music.stop()


def richochet():
    global F, mass, jump_vel, is_jumping
    F = (1 / 2) * mass * (jump_vel ** 2)
    position.y -= F
    jump_vel -= 1
    if jump_vel < 0:
        mass = -0.3
    if jump_vel == -19:
        is_jumping = False
        jump_vel = 18
        mass = 0.5


def moving_basket():
    global basket_pos, move
    if basket_pos.y < 200:
        move = -move
    elif basket_pos.y > 400:
        move = -move
    basket_pos.y -= move


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def score_point():
    global can_score, score_time
    if position.distance_to((50, 300)) <= 40 and can_score:
        score_time = pygame.time.get_ticks()
        position.x = random.randint(500, 700)
        position.y = random.randint(200, 500)
        return True
    else:
        return False


# infinte loop so program doesn't end
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # move left
        position.x -= vel
    if keys[pygame.K_d]:  # move right
        position.x += vel
    if not is_jumping:  # jump input
        if keys[pygame.K_w]:
            is_jumping = True
    if is_jumping:  # jumping
        F = (1 / 2) * mass * (jump_vel ** 2)
        position.y -= F
        jump_vel -= 1
        if jump_vel < 0:
            mass = -0.3
        if jump_vel == -19:
            is_jumping = False
            jump_vel = 18
            mass = 0.5

    # bottom limit
    if position.y > 530:
        position.y = 530

    # left and right limits
    if position.x > 740:
        position.x = 740
    elif position.x < -4:
        position.x = -4

    # gravity
    position += GRAVITY

    ball_rect.y = position.y
    ball_rect.x = position.x
    obstacle_rect.x = obstacle_pos.x
    obstacle_rect.y = obstacle_pos.y

    # score
    if score_point():
        score_value += 2
        score_sound.play()
        score_sound.set_volume(0.025)
        can_score = False

    # score timer
    if current_time - score_time > 1000:
        can_score = True

    screen.fill((100, 50, 0))
    screen.blit(background, (0, 0))
    screen.blit(obstacle, obstacle_pos)
    screen.blit(ball, position)
    screen.blit(basket, basket_pos)
    show_score(text_x, text_y)

    if score_value > 10:
        moving_basket()

    if score_value == 30:
        score_value += 2
        move *= 2

    if spawn_obstacle():
        can_spawn = False

    if current_time - obstacle_time > 3000:
        can_spawn = True

    pygame.time.delay(10)

    current_time = pygame.time.get_ticks()

    # collsion
    if ball_rect.colliderect(obstacle_rect):
        over = True
        running = False

    # this needs to be the last always
    pygame.display.flip()
    clock.tick(144)

while over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    obstacle_pos.xy = 20000, 20000
    position.xy = 20000, 20000
    game_over()
    pygame.display.flip()