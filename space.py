from pygame import *
from random import *
# from time import *

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x-= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x+= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20, 50,  -20)
        bullets.add(bullet)

class Enemy(Gamesprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(Gamesprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)

        
window = display.set_mode((700, 500))
display.set_caption("Caption")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
player = Player("rocket.png", 5, 400, 60, 100, 6)
bullets = sprite.Group()

asteroids = sprite.Group()

for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, 620), 20, 65, 65, 1.3)
    asteroids.add(asteroid)

monsters = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), 80, 80, 80, 1.3)
    monsters.add(monster)

font.init()

font1 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render("YOU LOSE", True, (255, 215, 0))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()  
fire_sound = mixer.Sound('fire.ogg')
game = True
clock = time.Clock()
FPS = 60
finish = False
score = 0
lost = 0

max_set = 0
gool = 10

rel_time = False
shooted = 0


while game:
    window.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    shooted+=1
                    fire_sound.play()
                    player.fire()
                # if shooted < 5 and rel_time == False:
                #     shooted+=1
                #     fire_sound.play()
                #     player.fire()
        # if shooted >= 5 and rel_time == False:
        #     rel_time = True
        #     last_timer = time()
        # if rel_time == True:
        #     now_timer = time()
        # if now_timer - last_timer <=3:
        #     reload = font.render('Reloading', 1, (150, 0, 21))


    if finish != True:
        text = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        lose = font1.render('Потрачено: ' + str(lost), 1, (255, 255, 255))
        window.blit(lose, (10, 50))
        player.update()
        player.reset()
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        asteroids.update()
        asteroids.draw(window)

        

        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), 80, 80, 80, 1.3)
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= 3 or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))
     
        if score >= gool:
            finish = True
            window.blit(win, (200, 200))
    
    else:
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(80, 620), 80, 80, 80, 1.3)
            monsters.add(monster)


    
    display.update()
    clock.tick(FPS)



