import pygame
import sys
import easygui
import database

from settings import screen_width, screen_height
from overworld import Overworld
from level import Level
from ui import UI
from achievements import Achievement

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        screen.fill((50, 50, 50))
        draw_text('Меню', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()
        button_start = pygame.Rect(50, 100, 200, 50)
        button_quit = pygame.Rect(50, 200, 200, 50)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_start.collidepoint((mx, my)):
            if click:
                break
        if button_quit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, (0, 0, 0), button_start)
        pygame.draw.rect(screen, (0, 0, 0), button_quit)

        draw_text('Начать', font, (255, 255, 255), screen, 60, 110)
        draw_text('Выйти', font, (255, 255, 255), screen, 60, 210)

        pygame.display.update()


def get_username():
    return easygui.enterbox("Введите ваше имя:", title="Регистрация имени")


class Game:
    def __init__(self):
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        self.level_completed = False

        self.level_bg_music = pygame.mixer.Sound('C:/GamePirate/audio/level_music.mp3')
        self.overworld_bg_music = pygame.mixer.Sound('C:/GamePirate/audio/overworld_music.mp3')

        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)

        self.ui = UI(screen)

        self.achievements = [
            Achievement("начало", lambda user_data: user_data['max_level'] >= 1 and user_data['level_completed'],
                        "C:/GamePirate/graphics/achievments/winner.png"),
            Achievement("богатеем", lambda user_data: user_data['coins'] >= 100,
                        "C:/GamePirate/graphics/achievments/rich.png"),
            Achievement("победа",
                        lambda user_data: user_data['max_level'] >= 5 and user_data['level_completed'],
                        "C:/GamePirate/graphics/achievments/noob.png")
        ]
        self.user_achievements = database.get_user_achievements(username)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
            self.level_completed = True
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)
        self.level_bg_music.stop()

    def change_coins(self, amount):
        self.coins += amount
        database.save_coins(username, self.coins)

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

            user_data = {'username': username, 'max_level': self.max_level, 'coins': self.coins,
                         'level_completed': self.level_completed}
            for achievement in self.achievements:
                if achievement.name not in self.user_achievements:
                    achievement.check_and_display(screen, user_data)
            self.level_completed = False

            pygame.display.update()


main_menu()
username = get_username()
coins_collected = database.get_user_coins(username)

game = Game()
game.coins = coins_collected

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((screen_width, screen_height))
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    screen.fill('blue')
    game.run()

    pygame.display.update()
    clock.tick(60)