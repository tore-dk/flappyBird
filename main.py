import pygame
import time
import random
import math

pygame.init()
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))

# BACKGROUND INITIATE
# IDE MAN KAN TAGE MODULO AF LÆNGDEN AF SKÆRMEN OG BRUGE DET TIL AT HAVE LANG SKÆRM
bgIMG = pygame.image.load('flappyBackground.png')
# RIGHT SIZE FOR THE BACKGROUND
bg_width = bgIMG.get_rect().width
bg_height = bgIMG.get_rect().height
bg_scale = height / bg_height
bg_width = math.ceil(bg_scale * bg_width)
bg_height = math.ceil(bg_scale * bg_height)
bgIMG = pygame.transform.scale(bgIMG, (bg_width, bg_height))


bg_count = width // bg_height + 2
bgIMG_list = []
bgX = []
bgY = []
bg_strech = 0
for i in range(bg_count):
    bgIMG_list.append(bgIMG)
    bgX.append(bg_strech)
    bg_strech += bg_width
    bgY.append(height - bgIMG.get_rect().height)


def show_bg(x, y, index):
    screen.blit(bgIMG_list[index], (x, y))


# BALL START
ballIMG = pygame.image.load('newBird.png')
ballIMG = pygame.transform.scale(ballIMG, (math.ceil(128/1.5), math.ceil(90/1.5)))
ball_height = ballIMG.get_rect().height
ball_width = ballIMG.get_rect().width
ballX = 300
ballY = (2*height)/3
ball_velocity = -0
ball_acceleration = 4


def update_ball(x, y):
    screen.blit(ballIMG, (x, y))


def ball_jump():
    global ball_velocity
    ball_velocity = -30


# PIPES IN PAIRS
pipecount = width//700 + 2
pipeIMG = []
pipe2IMG = []
pipeX = []
pipeY = []
pipe_state = []
pipe_speed = 8
pipe_gap = []
for i in range(pipecount):
    pipeIMG.append(pygame.image.load('flappy.png'))
    pipe2IMG.append(pygame.transform.flip(pygame.image.load('flappy.png'), True, True))
    pipeX.append(width)
    pipe_state.append(False)
    gap = random.randrange(250, 400)
    pipe_gap.append(gap)
    # WHEN EDITING PIPE Y  IT IS IMPORTANT -
    # TO EDIT IT BELOW, TOO (INSIDE 'pipe_reset')
    pipeY.append(random.randrange(gap + 50, height - 50))

pipe_state[0] = True


def pipe(x, index, space):
    screen.blit(pipeIMG[index], (x, pipeY[index]))
    screen.blit(pipe2IMG[index], (x, pipeY[index] - space - 1080))


def pipe_reset(num):
    global pipeX, pipeY
    pipeX[num] = width
    pipeY[num] = random.randrange(gap + 50, height - 50)


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


# BEFORE GAME
titleIMG = pygame.image.load('flappyBirdText.png')
title_height = titleIMG.get_rect().height
title_width = titleIMG.get_rect().width
titleIMG = pygame.transform.scale(titleIMG, (int(title_width/2), int(title_height/2)))
wait = True
while wait:
    for i in range(bg_count):
        bgX[i] -= pipe_speed/5
        if bgX[i] < -2304:
            bgX[i] = width - pipe_speed/5
        show_bg(bgX[i], bgY[i], i)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            wait, go = False, False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_jump()
                wait = False
    # BIRD FLYING UP N DOWN
    if ballY < height/2:
        ball_velocity += 0.2
    else:
        ball_velocity -= 0.2
    ballY += ball_velocity

    update_ball(ballX, ballY)
    screen.blit(titleIMG, (width / 3, height / 2 - titleIMG.get_rect().height/2))
    pygame.display.update()


# GAME LOOP IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
while go:
    # BACKGROUND
    screen.fill((0, 0, 0))

    # UPDATE NEW BACKGROUND
    for i in range(bg_count):
        bgX[i] -= pipe_speed/5
        if bgX[i] < -bg_width:
            bgX[i] = width - pipe_speed/5
        show_bg(bgX[i], bgY[i], i)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_jump()

    # UPDATE PIPES
    for i in range(pipecount):
        # NEW PIPES AND RESETTING PIPES
        if pipeX[i] < -281:
            pipe_reset(i)
            pipe_state[i] = False
        elif pipeX[i] < width - 700:
            pipe_state[(i + 1) % pipecount] = True
        # UPDATE PIPE ON SCREEN
        if pipe_state[i]:
            pipe(pipeX[i], i, pipe_gap[i])
            pipeX[i] -= pipe_speed
        # IS THE BALL INSIDE THE PIPE?
        if ballX < (pipeX[i] + 281) and ballX + ball_width > pipeX[i]:
            if ballY + ball_height > pipeY[i] or ballY < pipeY[i] - pipe_gap[i]:
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
