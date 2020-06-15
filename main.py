import pygame
import time
import random

pygame.init()
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))

velocity = 100

# BALL START
ballIMG = pygame.image.load('ball.png')
ballX = 300
ballY = height
ball_velocity = -velocity
ball_acceleration = 9.8


def update_ball(x, y):
    screen.blit(ballIMG, (x, y))


# CAN BE USED LATER FOR TRIES
def ball_reset():
    global ballY, ball_velocity, ball_acceleration
    ballY = 968
    ball_velocity = -velocity
    ball_acceleration = 9.8


# PIPES IN PAIRS
pipecount = 3
pipeIMG = []
pipe2IMG = []
pipeX = []
pipeY = []
pipe_state = []
pipe_speed = 5
for i in range(pipecount):
    pipeIMG.append(pygame.image.load('flappy.png'))
    pipe2IMG.append(pygame.transform.flip(pygame.image.load('flappy.png'), True, True))
    pipeX.append(width)
    pipeY.append(random.randrange(300, height-300, 20))
    pipe_state.append(False)
pipe_state[0] = True


def pipe(x, index):
    screen.blit(pipeIMG[index], (x, pipeY[index]))
    screen.blit(pipe2IMG[index], (x, pipeY[index] - 200 - 1080))


def pipe_reset(num):
    global pipeX, pipeY
    pipeX[num] = width
    pipeY[num] = random.randrange(300, height-300, 50)


# COLLISIONS ARE BEING CHECKED IN THE LOOP FOR THE PIPES


# QUIT GAME
def end():
    global go
    go = False
    screen.fill((0, 0, 0))
    # QUIT THE GAME


go = True
while go:
    time.sleep(.05)

    # BACKGROUND
    screen.fill((255, 255, 255))

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_velocity = -40

    # UPDATE PIPE(S)
    for i in range(pipecount):
        if pipeX[i] < -281:
            pipe_reset(i)
            pipe_state[i] = False
        elif pipeX[i] < width - 700:
            pipe_state[(i + 1) % pipecount] = True
        if pipe_state[i]:
            pipe(pipeX[i], i)
            pipeX[i] -= pipe_speed
        # IS THE BALL INSIDE THE PIPE?
        if ballX < (pipeX[i] + 281) and ballX + 32 > pipeX[i]:
            if ballY + 32 > pipeY[i] or ballY < pipeY[i] - 200:
                end()

    # UPDATE BALL
    ballY += ball_velocity
    ball_velocity += ball_acceleration
    update_ball(ballX, ballY)
    if ballY > height or ballY < 0:
        end()

    pygame.display.update()