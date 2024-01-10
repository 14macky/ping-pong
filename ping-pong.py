from pygame import *
import time as t
from random import *
font.init()
default_font = font.Font(None, 80)

width = 600
height = 500
test = 0
window = display.set_mode((width, height))
background_color = (50, 200, 90)

clock = time.Clock()

game_over = False

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, s):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.speed = s

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_1(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] == True and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] == True and self.rect.bottom < height:
            self.rect.y += self.speed

    def update_2(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] == True and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] == True and self.rect.bottom < height:
            self.rect.y += self.speed

player_1 = Player("racket.png", 0, 200, 50, 150, 4)
player_2 = Player("racket.png", 550, 200, 50, 150, 4)

player_group = sprite.Group()
player_group.add(player_1)
player_group.add(player_2)

class Ball(GameSprite):
    def __init__(self, img, x, y, w, h, s):
        super().__init__(img, x, y, w, h, s)
        self.speed_x = self.speed
        self.speed_y = self.speed

        self.on_bounce_cooldown = False
        self.bounce_cd_start = 0
        
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y <= 0 or self.rect.bottom >= height:
            self.speed_y *= -1
        if self.on_bounce_cooldown == False:
            if len(sprite.spritecollide(self, player_group, False)) != 0:
                self.speed_x *= -1
                self.on_bounce_cooldown = True
                self.bounce_cd_start = t.time()

        if self.on_bounce_cooldown == True:
            if t.time() - self.bounce_cd_start >= 0.5:
                self.on_bounce_cooldown = False

ball = Ball("tensis_ball.png", 200, 200,50, 50, 4)
p1_score = 0
p2_score = 0

paused = False
while game_over == False:
    for e in event.get():
        if e.type == QUIT:
            game_over = True

    if paused == False:
        window.fill(background_color)
        player_group.draw(window)
        ball.draw()
        player_1.update_1()
        player_2.update_2()
        ball.update()
        if ball.rect.x <= 0:
            lose_text = default_font.render("p1 lost hehe", True, (255, 255, 255))
            window.blit(lose_text, (150, 200))
            p2_score += 1
            paused = True
            paused_start = t.time()
        if ball.rect.right >= width:
            lose_text = default_font.render("p2 lost hehe", True, (255, 255, 255))
            window.blit(lose_text, (150, 200))
            p1_score += 1
            paused = True
            paused_start = t.time()

        p1_score_text = default_font.render(str(p1_score), True, (255, 255, 255))
        dash_text = default_font.render(" - ", True, (255, 255, 255))
        p2_score_text = default_font.render(str(p2_score), True, (255, 255, 255))

        window.blit(p1_score_text, (230, 0))
        window.blit(dash_text, (275, 0))
        window.blit(p2_score_text, (340, 0))
    else:
        if t.time() - paused_start >= 1:
            player_1 = Player("racket.png", 0, 200, 50, 150, 4)
            player_2 = Player("racket.png", 550, 200, 50, 150, 4)
            player_group = sprite.Group()
            player_group.add(player_1)
            player_group.add(player_2)
            ball = Ball("tensis_ball.png", 200, 200, 50, 50, 4)
            paused = False

    display.update()
    clock.tick(60)