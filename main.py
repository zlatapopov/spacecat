import time
from sprite import *
import pygame as pg

def dialogue_mode(sprite, text):
    sprite.update()
    screen.blit(space, (0, 0))
    screen.blit(sprite.image, sprite.rect)

    text1 = f1.render(text[text_number], True, pg.Color("white"))
    screen.blit(text1, (280, 450))
    if text_number < len(text) - 1:
        text2 = f1.render(text[text_number + 1], True, pg.Color("white"))
        screen.blit(text2, (280, 470))



pg.init()
pg.mixer.init()

size = (800, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Космические коты")

FPS = 120
clock = pg.time.Clock()

is_running = True
mode = "start_scene"

meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()
space = pg.image.load("screen.png").convert()
space = pg.transform.scale(space, size)

heart = pg.image.load("heart.png").convert_alpha()
heart = pg.transform.scale(heart,(30,30))
heart_count = 3

capitan = Captain()
alien = Alien()
starship = Starship()
start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, инопланетные коты,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и муряне в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите муриан!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? Мяуанцы? Мяуриане?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден SKYSMART.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              "",
              ""]

text_number = 0
f1 = pg.font.Font("font.otf", 25)
pg.mixer.music.load("Tense_Intro.wav")
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play()
laser_sound = pg.mixer.Sound("laser_sound.wav")
win_sound = pg.mixer.Sound("win_sound.wav")

while is_running:

    # СОБЫТИЯ
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
            if mode == "start_scene":
                text_number += 2
                if text_number > len(start_text):
                   text_number = 0
                   mode = "meteorites"
                   start_time = time.time()
                    #ошибка

            if mode == "alien_scene":
                text_number += 2
                if text_number > len(alien_text):
                   text_number = 0
                   alien.rect.topleft = (-30,600)
                   alien.mode = "up"
                   mode = "moon"

                   start_time = time.time()
                   starship.switch_mode()
            if mode == "moon":
                if event.key == pg.K_SPACE:
                    lasers.add(Laser(starship.rect.midtop))
                    laser_sound.play()

            if mode == "final_scene":
                text_number += 2
                if text_number > len(final_text):
                    text_number = 0
                    mode = "end"



    # ОБНaОВЛЕНИЯ
    if mode == "start_scene":
        dialogue_mode(capitan, start_text )



    if mode == "meteorites":
        if time.time() - start_time > 15.0:
            mode = "alien_scene"
        if random.randint(1,100) == 1:
            meteorites.add(Meteorite())

        starship.update()
        meteorites.update()

        hits = pg.sprite.spritecollide(starship, meteorites,True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        screen.blit(space, (0, 0))
        screen.blit(starship.image, starship.rect)
        meteorites.draw(screen)
        for i in range(heart_count):
            screen.blit(heart, (i * 30, 0))

    if mode == "alien_scene":
        dialogue_mode(alien, alien_text)

    if mode == "moon":
        if time.time() - start_time > 5.0:
            mode = "final_scene"
            pg.mixer.music.fadeout(3)
            win_sound.play()
        if random.randint(1,100) == 1:
            mice.add(Mouse_starship())
        starship.update()
        meteorites.update()
        hits = pg.sprite.spritecollide(starship, mice, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False
        hits = pg.sprite.groupcollide(mice, lasers, True, True)

        starship.update()
        mice.update()
        lasers.update()

        screen.blit(space, (0, 0))
        screen.blit(starship.image, starship.rect)
        mice.draw(screen)
        lasers.draw(screen)


    if mode == "final_scene":
        dialogue_mode(alien, final_text)

    pg.display.flip()
    clock.tick(FPS)
