import time, pyautogui
import pygame, random, sys
from pygame.locals import *

screen = pygame.display.set_mode((955, 537))
pygame.display.set_caption("Catch The Egg")
clock = pygame.time.Clock()
fps = 30


def displayStartScreen():
    high_score_file = open("high_score_file.txt", "r")
    highscore = high_score_file.read()
    high_score_file.close()

    name_display = game_font_big.render("Catch The Egg", False, (255,255,255))
    play_display = game_font.render("Press Space Bar to play", False, (255,255,255))
    instructions_display = game_font.render("Press i for instructions", False, (255,255,255))
    exit_display = game_font.render("Press Esc to exit", False, (255,255,255))
    highscore_absolute_display = game_font.render("Highscore", False, (255,255,255))
    highscore_display = game_font.render(highscore, False, (255,255,255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_i:
                    displayInstructions()

        screen.fill((60, 41, 41))
        screen.blit(name_display, (955/2-200-25, 537/2-50-100))
        screen.blit(play_display, (955/2-200-25, 537/2-50-100+150*1))
        screen.blit(instructions_display, (955/2-200-25, 537/2-50-100+150*1.5-20))
        screen.blit(exit_display, (955/2-200-25, 537/2-50-100+150*2-20-20))
        screen.blit(highscore_absolute_display, (750, 200))
        screen.blit(highscore_display, (820, 230))
        pygame.display.update()
        clock.tick(fps)

def displayInstructions():
    instructions1_display = game_font_big.render("Instructions", False, (255,255,255))
    instructions2_display = game_font.render("Task - You have to catch as many eggs as possible.", False, (255,255,255))
    instructions3_display = game_font.render("Controls - Press Left arrow key and right arrow key to", False, (255,255,255))
    instructions4_display = game_font.render("move the basket left and right", False, (255,255,255))
    instructions5_display = game_font.render("Rules - You will gain a point for an egg catch.", False, (255,255,255))
    instructions6_display = game_font.render("You will loose one life for an egg miss.", False, (255,255,255))
    instructions_back_display = game_font.render("Press left arrow to go back", False, (255,255,255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return

        screen.fill((60, 41, 41))
        screen.blit(instructions1_display, (400-100, 50))
        screen.blit(instructions2_display, (50, 100+30*3))
        screen.blit(instructions3_display, (50, 130+30*4))
        screen.blit(instructions4_display, (50+170, 130+30*5))
        screen.blit(instructions5_display, (50, 150+30*6))
        screen.blit(instructions6_display, (50+120, 150+30*7))
        screen.blit(instructions_back_display, (50+120+100, 150+30*11))
        pygame.display.update()
        clock.tick(fps)

def gameLoop():
    global basketX
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if basketX > -30:
                basketX -= basket_moving_speed
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if basketX < 1330 - background.get_height() :
                basketX += basket_moving_speed

        screen.blit(background, (0, 0))
        screen.blit(basket, (basketX, basketY))
        blitScoreAndLives(score, lives)
        fallEggs()
        checkCollisionAndCatch()
        pygame.display.update()
        clock.tick(fps)

def fallEggs():
    global eggX_list
    for i in range(5):
        if eggY_list[i] > 540:
            eggX_list.pop(i)
            eggY_list.pop(i)
            egg_name = egg_list[i]
            egg_list.pop(i)
            egg_list.append(egg_name)
            eggX_list.append(random.randint(100,900))
            eggY_list.append(eggY_list[-1] - gap)
        eggY_list[i] += egg_falling_speed
        screen.blit(egg_list[i], (eggX_list[i], eggY_list[i]))

def displayGameOverScreen():
    global score, lives, egg_falling_speed, egg_list, eggX_list, eggY_list
    game_over_display = game_font_big.render("Game Over", True, (255,255,255))
    play_again_display = game_font.render("Press Space Bar to play again or Esc to exit", True, (255,255,255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    score = 0
                    lives = 5
                    egg_falling_speed = 3
                    egg_list = [egg1, egg2, egg3, egg4, egg5]
                    eggX_list = [random.randint(100, 900), random.randint(100, 900), random.randint(100, 900), random.randint(100, 900), random.randint(100, 900)]
                    eggY_list = [0, 0 - gap * 1, 0 - gap * 2, 0 - gap * 3, 0 - gap * 4]
                    return

        screen.fill((60,41,41))
        screen.blit(game_over_display, (300, 250))
        screen.blit(play_again_display, (150, 350))
        pygame.display.update()
        clock.tick(fps)

def checkCollisionAndCatch():
    global score, lives, egg_falling_speed, basket_moving_speed, gap, basketX, hack_mode
    highscore_score_file = open("high_score_file.txt", "r")
    highscore = highscore_score_file.read()
    highscore_score_file.close()
    if int(highscore) < score:
        highscore_score_file_write = open("high_score_file.txt", "w")
        highscore_score_file_write.write(str(score))
        highscore_score_file_write.close()
    if hack_mode == "on":
        basketX = eggX_list[0] - 80
    for i in range(5):
        eggX = eggX_list[i]
        eggY = eggY_list[i]
        basketX1_C = basketX + 30
        basketX2_C = basketX1_C + 100
        basketY_C = basketY

        if eggY > 480 and eggY < 490:
            eggX_list.pop(i)
            eggY_list.pop(i)
            egg_name = egg_list[i]
            egg_list.pop(i)
            egg_list.append(egg_name)
            eggX_list.append(random.randint(100,900))
            eggY_list.append(eggY_list[-1] - 300)
            lives -= 1
            if lives == 0:
                blitScoreAndLives(score, 0)
                pygame.display.update()
                game_over_sound.play()
                time.sleep(2)
                displayGameOverScreen()
        elif eggY > (basketY_C) and (eggX > basketX1_C and eggX < basketX2_C):
            eggX_list.pop(i)
            eggY_list.pop(i)
            egg_name = egg_list[i]
            egg_list.pop(i)
            egg_list.append(egg_name)
            eggX_list.append(random.randint(100,900))
            eggY_list.append(eggY_list[-1] - 300)
            score += 1
            score_sound.play()
            if score%10 == 0:
                egg_falling_speed += 1
            if score%20 == 0:
                gap -= 20
            if score%30 == 15:
                basket_moving_speed += 1

def blitScoreAndLives(score, lives):
    score_display = game_font.render("Score : "+str(score), False, (255, 255, 255))
    lives_display = game_font.render("Remaining Lives : "+str(lives), False, (255, 255, 255))

    screen.blit(score_display, (0,10))
    screen.blit(lives_display, (0,50))

pygame.font.init()

game_font = pygame.font.Font("04B_19.ttf", 30)
game_font_big = pygame.font.Font("04B_19.ttf", 60)

egg = pygame.image.load("images/egg.png").convert_alpha()
basket = pygame.image.load("images/basket.png").convert_alpha()
background = pygame.image.load("images/bgimage.jpeg")
pygame.mixer.init()
score_sound = pygame.mixer.Sound("sounds/point.wav")
game_over_sound = pygame.mixer.Sound("sounds/die.wav")
basketX = int(955/2-100+25+0.5)
basketY = 437-50
eggX_list = [random.randint(100,900), random.randint(100,900), random.randint(100,900), random.randint(100,900), random.randint(100,900)]
gap = 400
eggY_list = [0,0-gap*1,0-gap*2,0-gap*3,0-gap*4]
egg1 = egg
egg2 = egg
egg3 = egg
egg4 = egg
egg5 = egg
egg_list = [egg1, egg2, egg3, egg4, egg5]
egg_falling_speed = 3
basket_moving_speed = 20
score = 0
lives = 5
hack_mode = "off"
name = ""

if __name__ == '__main__':
    password = pyautogui.password("Please login to your account to play the game", "Catch The Egg")
    if password == "nihar1805":
        name = "Nihar Parikh"
        hack_mode = "off"
    elif password == "khyati2312":
        name = "Khyati Parikh"
        hack_mode = "off"
    elif password == "prakhar-THECoder":
        name = "Prakhar Parikh(Author)"
        hack_mode_val = pyautogui.confirm("Do you want to keep Developer(Hack/God) mode on?", "Catch The Egg")
        if hack_mode_val == "OK":
            hack_mode = "on"
        else:
            hack_mode = "off"
    displayStartScreen()
    gameLoop()