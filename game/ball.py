import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height,snd_paddle_hit=None,snd_wall_bounce=None,snd_score=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Sound references

        self.snd_wall_bounce = snd_wall_bounce
        self.snd_paddle_hit = snd_paddle_hit
        self.snd_score = snd_score


    def move(self, player, ai):
    # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Top/bottom wall bounce
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if self.snd_wall_bounce: self.snd_wall_bounce.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            if self.snd_wall_bounce: self.snd_wall_bounce.play()

        # Paddle collisions
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        if ball_rect.colliderect(player_rect):
            self.x = player_rect.right  # prevent sticking/tunneling
            self.velocity_x = abs(self.velocity_x)
            if self.snd_paddle_hit: self.snd_paddle_hit.play()

        elif ball_rect.colliderect(ai_rect):
            self.x = ai_rect.left - self.width
            self.velocity_x = -abs(self.velocity_x)
            if self.snd_paddle_hit: self.snd_paddle_hit.play()



    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if self.snd_score:
            self.snd_score.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
