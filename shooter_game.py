#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):

        sprite.Sprite.__init__(self)
        
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed 

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 920:
            self.rect.x += self.speed
      
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

goal = 15
lost = 0
score = 0
max_lost = 10
life = 3

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_widght -80)
            self.rect.y = 0 
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 or sprite.groupcollide(bullets, asteroids, True, False):
            self.kill() 


img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_back = 'galaxy.jpg'
img_asteroid = 'asteroid.png'

clock = time.Clock()

FPS = 50

win_widght = 1000
win_height = 700

window = display.set_mode((win_widght, win_height))
display.set_caption('Cyberpunck_2077')
background= transform.scale(image.load(img_back), (win_widght, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

finish = False

rocket = Player('rocket.png', 500, 610, 70, 85, 15) 

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_asteroid, randint(30, win_widght - 30), -40, 80, 50, randint(1, 6)) 
    asteroids.add(asteroid)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_widght - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

rel_time = False
num_fire = 0

run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background, (0,0))
        text = font2.render('Check:' + str(score), 1, (139, 0, 0))
        window.blit(text, (10, 20))
        text_lose = font2.render('Lost:' + str(lost), 1, (139, 0, 0))
        window.blit(text_lose, (10, 50))

        rocket.reset()
        asteroids.update()
        monsters.update()
        rocket.update()
        bullets.update()  
        asteroids.draw(window)   
        monsters.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False 

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_widght - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(rocket, monsters, False) or sprite.spritecollide(rocket, asteroids, False):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life = life - 1
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color= (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        life = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        
        for i in range(5):
            monster = Enemy(img_enemy, randint(80, win_widght - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for j in asteroids:
            j.kill()

        for i in range(3):
            asteroid = Enemy(img_asteroid, randint(30, win_widght - 30), -40, 80, 50, randint(1, 6)) 
            asteroids.add(asteroid)

    clock.tick(FPS)


