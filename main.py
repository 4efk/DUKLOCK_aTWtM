import pygame
import random

_author_ = '4efk'

pygame.init()

window = pygame.display.set_mode((500, 550))
pygame.display.set_caption('ALE ČAU')
font1 = pygame.font.SysFont('comicsans', 100)
font2 = pygame.font.SysFont('comicsans', 25)
font3 = pygame.font.SysFont('comicsans', 50)
font4 = pygame.font.SysFont('comicsans', 30)

music_dict = {'main_page':'soundtrack_2.wav', 'credits':'soundtrack_2.wav', 'die':'astronomia_instrumental.wav', 'game':'game_soundtrack_5.wav'}
die_sounds = [pygame.mixer.Sound('die_sound_1.wav'), pygame.mixer.Sound('die_sound_2.wav')]

x = 250
y = 368
height = 132
width = 63
speed = 4
falling_speed = 1
lives = 50
score = 0
new_highscore = False
drawing_guide = 'main_page'
walking_skin_1 = [pygame.image.load('duklock_skin_1_right_small.png'),
                  pygame.image.load('duklock_skin_1_left_small.png')]
falling_stuff = [(pygame.image.load('demonetized.png'), -10), (pygame.image.load('monetized.png'), 5)]
what_is_falling = []

walking_count = 0


def redraw_main_page():
    window.fill((0, 0, 0))
    window.blit(font1.render('DUKLOCK', True, (255, 0, 0)), (81, 10))
    window.blit(font2.render('and the way to monetization', True, (255, 255, 255)), (136, 75))
    window.blit(font3.render('PLAY', True, (255, 220, 0)), (208, 175))#(208, 295), (175, 200)
    window.blit(font3.render('CREDITS', True, (255, 220, 0)), (175, 275))#(175, 328), (275, 300)
    window.blit(font2.render('game by 4efk', True, (255, 255, 255)), (385, 530))
    window.blit(pygame.image.load('duklock_skin_2_right_small.png'), (75, 368))
    window.blit(pygame.image.load('brmbrm.png'), (270, 10))
    pygame.display.update()


def redraw_credits():
    window.fill((0, 0, 0))
    window.blit(font4.render('PROGRAMOVÁNÍ', True, (255, 0, 0)), (165, 30))
    window.blit(font4.render('4efk', True, (255, 255, 255)), (228, 80))
    window.blit(font4.render('SKINY DUKLOCKA', True, (255, 0, 0)), (160, 180))
    window.blit(font4.render('u/DrunkenGilaMonster', True, (255, 255, 255)), (140, 230))
    window.blit(font4.render('HUDBA', True, (255, 0, 0)), (215, 330))
    window.blit(font4.render('4efk', True, (255, 255, 255)), (228, 380))
    window.blit(font4.render('hudba souboru', True, (255, 255, 255)), (177, 410))
    window.blit(font4.render('astronomia_instrumental.wav', True, (255, 255, 255)), (105, 425))
    window.blit(font4.render('mi nepatří', True, (255, 255, 255)), (200, 445))
    window.blit(font4.render('BACK', True, (255, 220, 0)), (430, 520))#(430, 485)(520, 535)
    pygame.display.update()


def redraw_game():
    global x
    global walking_count
    global speed
    global falling_speed
    global score
    global lives
    window.fill((10, 255, 0))
    falling_stuff_and_catching_function()
    window.blit(walking_skin_1[walking_count], (x, y))

    if score == 10000:
        falling_speed = 2

    if score == 40000:
        falling_speed = 3
        speed = 5

    if lives > 100:
        lives = 100

    if lives <= 0:
        die()

    window.blit(font3.render(f'{lives}', True, (0, 0, 0)), (425, 10))
    window.blit(font3.render(f'{score}', True, (0, 0, 0)), (10, 10))
    pygame.display.update()
    score += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x += speed
        walking_count = 0

    if keys[pygame.K_a]:
        x -= speed
        walking_count = 1
#    print(pygame.mouse.get_pos())#441 454


def redraw_die():
    global new_highscore
    highscore_file = open('highscore.txt', 'r')
    highscore = int(highscore_file.readlines()[0])
    window.fill((0, 0, 0))
    window.blit(font3.render('GAME OVER', True, (255, 0, 0)), (145, 100))
    score_text = font2.render(f'score: {score}  highscore:{highscore}', True, (255, 255, 255))
    score_text_cords = score_text.get_rect(center=(250, 130))
    window.blit(score_text, (score_text_cords[0], 130))
    if new_highscore:
        window.blit(font2.render('new highscore!', True, (255, 255, 255)), (188, 147))
    window.blit(font2.render('Dušan už to nezvládl.....', True, (175, 175, 175)), (152, 200))
    window.blit(font2.render('samé žluté dolary, žádné zelené...', True, (175, 175, 175)), (115, 220))
    window.blit(font2.render('žádné peníze, žádné jídlo...zemřel...', True, (175, 175, 175)), (105, 240))
    window.blit(font4.render('RETRY       MAIN MENU', True, (255, 220, 0)), (140, 300))


def is_clicked(x1_x2, y1_y2):
    if x1_x2[0] <= pygame.mouse.get_pos()[0] <= x1_x2[1]:
        if y1_y2[0] <= pygame.mouse.get_pos()[1] <= y1_y2[1] and pygame.mouse.get_pressed()[0]:
            return True
        else:
            pass
    else:
        pass


def click_functions():
    global drawing_guide
    if drawing_guide == 'main_page':
        if is_clicked((208, 295), (175, 200)):
            drawing_guide = 'game'
        elif is_clicked((175, 328), (275, 300)):
            drawing_guide = 'credits'

    if drawing_guide == 'die':
        if is_clicked((137, 210), (300, 315)):
            drawing_guide = 'game'
        if is_clicked((246, 368), (300, 315)):
            drawing_guide = 'main_page'

    if drawing_guide == 'credits':
        if is_clicked((430, 485), (520, 535)):
            drawing_guide = 'main_page'

def falling_stuff_and_catching_function():
     global lives
     touch_del_list = []
     falling_object = random.choice(falling_stuff)
     cordinates = (random.randint(20, 460), random.randint(-1000, -50))

#    random stuff appearing
     if len(what_is_falling) <= 10:
         window.blit(falling_object[0], cordinates)
         what_is_falling.append(list((list(cordinates), falling_object)))

#    random stuff falling
     for i in range(len(what_is_falling)):
         what_is_falling[i][0] = (what_is_falling[i][0][0], what_is_falling[i][0][1] + falling_speed)

#    deleting stuff player touched
     for i in range(len(what_is_falling)):
         if x <= what_is_falling[i][0][0] <= (x + 30) and y <= what_is_falling[i][0][1] <= (y + 30):
             touch_del_list.append(i)
             lives += what_is_falling[i][1][1]

#    deleting stuff that goes too down
     if len(what_is_falling) > 0:
         for i in range(len(what_is_falling)):
             if what_is_falling[i][0][1] >= 550:
                 touch_del_list.append(i)
                 if what_is_falling[i][1][0] == falling_stuff[1][0]:
                     lives += -5

#    final deleting
     for number in touch_del_list:
         what_is_falling[number] = None

     for i in range(what_is_falling.count(None)):
         what_is_falling.remove(None)

#    drawing random stuff
     for falling_object_info in what_is_falling:
         if falling_object_info is not None:
             window.blit(falling_object_info[1][0], tuple(falling_object_info[0]))


def die():
    global drawing_guide
    global lives
    global x
    global y
    global speed
    global falling_speed
    global what_is_falling
    global score
    global new_highscore
    new_highscore = False
    random.choice(die_sounds).play()
    highscore = open('highscore.txt', 'r')
    highscore_str = highscore.readlines()
    if score > int(highscore_str[0]):
        highscore = open('highscore.txt', 'w')
        highscore.write(str(score))
        highscore.close()
    highscore = open('highscore.txt')
    highscore_int = int(highscore.readlines()[0])
    if score >= highscore_int:
        new_highscore = True
    redraw_die()

    x = 250
    y = 368
    speed = 4
    falling_speed = 1
    lives = 50
    score = 0
    what_is_falling = []
    drawing_guide = 'die'


run = True
while run:
    pygame.time.delay(5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    click_functions()

    if drawing_guide == 'main_page':
        redraw_main_page()

    elif drawing_guide == 'game':
        redraw_game()

    elif drawing_guide == 'die':
        redraw_die()

    elif drawing_guide == 'credits':
        redraw_credits()

    if x <= -10:
        x = -10

    elif x >= 445:
        x = 445

    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.load(music_dict[drawing_guide])
        pygame.mixer.music.play(-1)
        drawing_guide_remeber = drawing_guide

    if drawing_guide != drawing_guide_remeber:
        pygame.mixer.music.stop()

pygame.quit()
