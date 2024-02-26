import pygame
import database


class Achievement:
    def __init__(self, name, condition, image_path):
        self.name = name
        self.condition = condition
        self.image = pygame.image.load(image_path)
        self.achieved = False

        self.achievement_sound = pygame.mixer.Sound('C:/GamePirate/audio/ach.mp3')

    def check_and_display(self, screen, user_data):
        if not self.achieved and self.condition(user_data):
            self.achieved = True
            screen.blit(self.image, (50, 50))  # Настройте положение
            self.achievement_sound.play()
            pygame.display.update()
            pygame.time.wait(3000)  # Показать на 3 секунды
            database.save_achievement(user_data['username'], self.name)
