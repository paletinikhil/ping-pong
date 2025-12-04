import pygame
from .paddle import Paddle
from .ball import Ball
pygame.mixer.init()

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.target_score = 3  # default winning score

        self.snd_wall_bounce = pygame.mixer.Sound("assets/sounds/mechanical-bling.wav")
        self.snd_paddle_hit = pygame.mixer.Sound("assets/sounds/mechanical-crate-pick-up.wav")
        self.snd_score = pygame.mixer.Sound("assets/sounds/yeah-boy.mp3")
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, 
                         snd_paddle_hit=self.snd_paddle_hit,
                         snd_wall_bounce=self.snd_wall_bounce,
                         snd_score=self.snd_score)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)




    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        
        self.ball.move(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.target_score or self.ai_score >= self.target_score:
            winner = "Player" if self.player_score >= self.target_score else "AI"
            msg = f"{winner} Wins!"

            # Show winner message
            screen.fill((0, 0, 0))
            title_font = pygame.font.SysFont("Arial", 60)
            small_font = pygame.font.SysFont("Arial", 30)

            text = title_font.render(msg, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 3))
            screen.blit(text, text_rect)

            # Replay options
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]

            for i, line in enumerate(options):
                opt_text = small_font.render(line, True, (255, 255, 255))
                opt_rect = opt_text.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
                screen.blit(opt_text, opt_rect)

            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                            # Reset for new match
                            if event.key == pygame.K_3:
                                self.target_score = 3  # first to 2 wins = best of 3
                            elif event.key == pygame.K_5:
                                self.target_score = 5  # first to 3 wins = best of 5
                            elif event.key == pygame.K_7:
                                self.target_score = 7  # first to 4 wins = best of 7

                            self.player_score = 0
                            self.ai_score = 0
                            self.ball.reset()
                            waiting = False
