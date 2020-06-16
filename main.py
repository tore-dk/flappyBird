import pygame
import time
import random

pygame.init()
width, height = 3000, 864
screen = pygame.display.set_mode((width, height))

velocity = 100

# BACKGROUND INITIATE
# IDE MAN KAN TAGE MODULO AF LÆNGDEN AF SKÆRMEN OG BRUGE DET TIL AT HAVE LANG SKÆRM
bg_count = width // 2304 + 2
bgIMG_list = []
bgX = []
bgY = []
bgIMG = pygame.image.load('flappyBackground.png')
bg_strech = 0
for i in range(bg_count):
    bgIMG_list.append(bgIMG)
    bgX.append(bg_strech)
    bg_strech += 2304
    bgY.append(0)


def show_bg(x, y, index):
    screen.blit(bgIMG_list[index], (x, y))


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
pipecount = width//700 + 2
pipeIMG = []
pipe2IMG = []
pipeX = []
pipeY = []
pipe_state = []
pipe_speed = 20
for i in range(pipecount):
    pipeIMG.append(pygame.image.load('flappy.png'))
    pipe2IMG.append(pygame.transform.flip(pygame.image.load('flappy.png'), True, True))
    pipeX.append(width)
    pipeY.append(random.randrange(250, height-250, 5))
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
go = True


def end():
    global go
    go = False
    game_over = pygame.image.load('flappyBirdGameOver.png')
    screen.fill((0, 0, 0))
    for j in range(bg_count):
        show_bg(bgX[j], bgY[j], j)
    screen.blit(game_over, (width/2 - 544, 100))
    finalscore = sfont.render('FINAL SCORE : ' + str(score), True, (252, 160, 72))
    wide = finalscore.get_rect().width
    screen.blit(finalscore, (width/2 - wide/2, 500))
    pygame.display.update()
    time.sleep(5)


# SCORE
score = 0
font_size = 64
sfont = pygame.font.Font('freesansbold.ttf', font_size)
textX, textY = 10, 10


def show_score(x, y):
    thescore = sfont.render("Score: " + str(score), True, (255, 255, 0))
    screen.blit(thescore, (x, y))


# GAME LOOP
while go:
    time.sleep(.02)

    # BACKGROUND
    screen.fill((0, 0, 0))

    # UPDATE NEW BACKGROUND
    for i in range(bg_count):
        bgX[i] -= pipe_speed/5
        if bgX[i] < -2304:
            bgX[i] = width - pipe_speed/5
        show_bg(bgX[i], bgY[i], i)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                time.sleep(5)
            if event.key == pygame.K_SPACE:
                ball_velocity = -40

    # UPDATE PIPES
    for i in range(pipecount):
        # NEW PIPES AND RESETTING PIPES
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
        # ADD SCORE AFTER PIPE
        if pipeX[i] + 250 > ballX >= pipeX[i] + 250 - pipe_speed:
            score += 1

    # UPDATE BALL
    ballY += ball_velocity
    ball_velocity += ball_acceleration
    update_ball(ballX, ballY)
    if ballY > height or ballY < 0:
        end()

    # UPDATE SCORE
    show_score(textX, textY)

    pygame.display.update()
