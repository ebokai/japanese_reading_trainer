import pygame
import random
import os
import time
from collections import defaultdict

class HiraganaPracticeGame:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hiragana_folder = "hiragana"
        self.image_width = 72
        self.word_length = random.randint(3, 6)



        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hiragana Practice Game")

        self.hiragana_images = self.load_hiragana_images(self.hiragana_folder)
        self.pronunciation = self.extract_pronunciation(self.hiragana_folder)
        self.total_width = self.word_length * self.image_width
        self.word, self.correct_pronunciation = self.generate_new_word()

        self.font = pygame.font.Font(None, 36)
        self.input_text = ""
        self.white = (255, 255, 255)
        self.input_bg_color = (0, 0, 128)

        self.running = True

        self.correct_response_times = []
        self.incorrect_response_times = []
        self.start_time = time.perf_counter()
        self.mean_correct_time = 0.0
        self.mean_incorrect_time = 0.0
        self.character_stats = defaultdict(lambda: [0, 0])  # Stores [correct_count, incorrect_count]
        self.score = 0

    def load_hiragana_images(self, folder):
        hiragana_images = []
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder, filename))
                hiragana_images.append(image)
        return hiragana_images

    def extract_pronunciation(self, folder):
        pronunciation = [filename.split(".png")[0] for filename in os.listdir(folder) if filename.endswith(".png")]
        return pronunciation

    def generate_new_word(self):
        self.word_length = random.randint(2,4)
        self.total_width = self.word_length * self.image_width
        indices = [random.randint(0, len(self.hiragana_images) - 1) for i in range(self.word_length)]
        word = [self.hiragana_images[i] for i in indices]
        correct_pronunciation = "".join(self.pronunciation[i] for i in indices)
        return word, correct_pronunciation

    def run(self):
        message = ""

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        result = self.handle_enter_key()
                        message = result
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            self.display_game(message)
            pygame.display.flip()

        pygame.quit()

    def handle_enter_key(self):
        

        is_correct = self.input_text == self.correct_pronunciation
        if is_correct:
            message = "Correct pronunciation!"
            self.correct_response_times.append(time.perf_counter() - self.start_time)
            self.character_stats[self.correct_pronunciation][0] += 1
            self.score += 1
        else:
            message = "Incorrect pronunciation. Correct pronunciation: " + self.correct_pronunciation
            self.incorrect_response_times.append(time.perf_counter() - self.start_time)
            self.character_stats[self.correct_pronunciation][1] += 1
            self.score -= 1

        self.mean_correct_time = self.calculate_mean_time(self.correct_response_times)
        self.mean_incorrect_time = self.calculate_mean_time(self.incorrect_response_times)

        print(f'mean response time (correct): {self.mean_correct_time:.2f}')
        print(f'mean response time (incorrect): {self.mean_incorrect_time:.2f}')
        self.word, self.correct_pronunciation = self.generate_new_word()
        self.input_text = ""
        self.start_time = time.perf_counter()
        return message

    def calculate_mean_time(self, response_times):
        return sum(response_times) / len(response_times) if response_times else 0.0

    def get_most_common_incorrect_characters(self, count=5):
        incorrect_characters = [(char, counts[1]) for char, counts in self.character_stats.items()]
        incorrect_characters.sort(key=lambda x: x[1], reverse=True)
        return incorrect_characters[:count]

    def display_game(self, message=""):
        self.screen.fill((0, 0, 0))

        x = (self.screen_width - self.total_width) // 2
        y = 200

        for hiragana_char in self.word:
            self.screen.blit(hiragana_char, (x, y))
            x += self.image_width

        text_surface = self.font.render(self.input_text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.screen_width // 2, y + 100)
        pygame.draw.rect(self.screen, self.input_bg_color, (text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, text_rect.height + 10))
        self.screen.blit(text_surface, text_rect)

        if message:
            message_surface = self.font.render(message, True, self.white)
            message_rect = message_surface.get_rect()
            message_rect.center = (self.screen_width // 2, y + 150)
            self.screen.blit(message_surface, message_rect)

        score_surface = self.font.render(f"Score: {self.score}", True, self.white)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_surface, score_rect)

        pygame.display.flip()

if __name__ == "__main__":
    game = HiraganaPracticeGame()
    game.run()
