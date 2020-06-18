## FORSLAG
# ILDKUGLER
# MULTIPLAYER (ONLINE)
# KØDÆDENDE PLANTER
# BUTIK (MED POINT)
import pygame
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


# BIRD START
birdIMG = pygame.image.load('newBird.png')
birdIMG = pygame.transform.scale(birdIMG, (math.ceil(128 / 1.5), math.ceil(90 / 1.5)))
bird_height = birdIMG.get_rect().height
bird_width = birdIMG.get_rect().width
birdX = 100
birdY = (2 * height) / 3
bird_velocity = -0
bird_acceleration = 4

bird_up = pygame.transform.rotate(birdIMG, 15)
bird_down = pygame.transform.rotate(birdIMG, -15)


def update_bird(x, y, img=birdIMG):
    screen.blit(img, (x, y))


def ball_jump():
    global bird_velocity
    bird_velocity = -30


# PIPES IN PAIRS
gap_upper = 400
gap_lower = 250
between_pipes = 500
pipecount = width//between_pipes + 2
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
    gap = random.randrange(gap_lower, gap_upper)
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
    pipe_gap[num] = random.randrange(gap_lower, gap_upper)
    pipeY[num] = random.randrange(pipe_gap[num] + 50, height - 50)


# COLLISIONS ARE BEING CHECKED IN THE LOOP FOR THE PIPES

# RESET VARIABLES WHEN DEAD
def reset():
    global pipeX, pipeY, pipe_state, pipe_gap, birdX, birdY, bird_acceleration, bird_velocity, score, pipe_speed, gap_upper
    # RESET PIPES
    gap_upper = 400
    pipe_speed = 8
    pipeX = []
    pipeY = []
    pipe_state = []
    pipe_gap = []
    for j in range(pipecount):
        pipeX.append(width)
        pipe_state.append(False)
        new_gap = random.randrange(gap_lower, gap_upper)
        pipe_gap.append(gap)
        pipeY.append(random.randrange(gap + 50, height - 50))
    pipe_state[0] = True
    # RESET BIRD
    birdX = 100
    birdY = (2 * height) / 3
    bird_velocity = -0
    bird_acceleration = 4
    score = 0


# QUIT GAME
go = True


def game_over():
    global go, running, wait, high_score
    running = True
    game_over_text = pygame.image.load('flappyBirdGameOver.png')
    end = True
    while end:
        screen.fill((0, 0, 0))
        for j in pygame.event.get():
            if j.type == pygame.QUIT:
                end, running, go = False, False, False
            if j.type == pygame.KEYDOWN:
                if j.key == pygame.K_SPACE:
                    end = False
                    reset()
                    ball_jump()
        for j in range(bg_count):
            show_bg(bgX[j], bgY[j], j)
        screen.blit(game_over_text, (width/2 - 544, 100))
        finalscore = sfont.render('FINAL SCORE : ' + str(score), True, (252, 160, 72))
        wide = finalscore.get_rect().width
        screen.blit(finalscore, (width/2 - wide/2, 500))
        if score > high_score:
            high_score = score
        show_high_score_in_middle()
        pygame.display.update()


# SCORE
score = 0
font_size = 64
sfont = pygame.font.Font('freesansbold.ttf', font_size)
textX, textY = 10, 10


def show_score(x, y):
    thescore = sfont.render("Score: " + str(score), True, (255, 255, 0))
    screen.blit(thescore, (x, y))


high_score = 0


def show_high_score_in_middle():
    h_score = sfont.render('HIGH SCORE: ' + str(high_score), True, (255, 0, 0))
    h_score_width = h_score.get_rect().width
    screen.blit(h_score, (width/2 - h_score_width/2, 600))


# BEFORE GAME VARIABLES
titleIMG = pygame.image.load('flappyBirdText.png')
title_height = titleIMG.get_rect().height
title_width = titleIMG.get_rect().width
titleIMG = pygame.transform.scale(titleIMG, (int(title_width/2), int(title_height/2)))


def before_game():
    global birdY, birdX, bird_velocity, wait, go, running
    for i in range(bg_count):
        bgX[i] -= pipe_speed / 5
        if bgX[i] < -2304:
            bgX[i] = width - pipe_speed / 5
        show_bg(bgX[i], bgY[i], i)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            wait, go, running = False, False, False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_jump()
                wait = False
    # BIRD FLYING UP N DOWN
    if birdY < height / 2:
        bird_velocity += 0.2
    else:
        bird_velocity -= 0.2
    birdY += bird_velocity

    update_bird(birdX, birdY)
    screen.blit(titleIMG, (width / 3, height / 2 - titleIMG.get_rect().height / 2))
    pygame.display.update()


# ACTUAL GAME IT STARTS HERE
running = True
while running:
    birdX = 100
    wait, go = True, True
    # BEFORE GAME LOOP
    while wait:
        before_game()

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
                go, wait, running = False, False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_jump()
        if not go:
            break

        # UPDATE PIPES
        for i in range(pipecount):
            # NEW PIPES AND RESETTING PIPES
            if pipeX[i] < -281:
                pipe_reset(i)
                pipe_state[i] = False
                birdX += 10
                gap_upper -= 10
                pipe_speed += 0.5
            elif pipeX[i] < width - between_pipes:
                pipe_state[(i + 1) % pipecount] = True
            # UPDATE PIPE ON SCREEN
            if pipe_state[i]:
                pipe(pipeX[i], i, pipe_gap[i])
                pipeX[i] -= pipe_speed
            # IS THE BALL INSIDE THE PIPE?
            if birdX < (pipeX[i] + 281) and birdX + bird_width > pipeX[i]:
                if birdY + bird_height > pipeY[i] or birdY < pipeY[i] - pipe_gap[i]:
                    game_over()
            # ADD SCORE AFTER PIPE
            if pipeX[i] + 250 > birdX >= pipeX[i] + 250 - pipe_speed:
                score += 1

        # UPDATE BALL
        bird_velocity += bird_acceleration
        birdY += bird_velocity
        if bird_velocity < 0:
            update_bird(birdX, birdY, bird_up)
        elif bird_velocity > 0:
            update_bird(birdX, birdY, bird_down)
        else:
            update_bird(birdX, birdY)
        if birdY > height - bird_height or birdY < 0:
            game_over()

        # UPDATE SCORE
        show_score(textX, textY)

        pygame.display.update()
