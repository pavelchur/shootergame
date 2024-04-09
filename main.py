from pygame import *
import random
font.init()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        global finish
        hits = sprite.groupcollide(p,monsters,False,False)
        for hit in hits:
            finish = False
        if ship.rect.x <= win_width - 80 and ship.x_speed > 0 or ship.rect.x >= 0 and ship.x_speed < 0:
            self.rect.x += self.x_speed

    def fire(self):
        bullet = Bullet('laser.png', self.rect.x+self.size_x/2-8, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)
        mixer.init()
        mixer.music.load('blaster.wav')
        mixer.music.play()

def draw_text(surf, text, size, x, y):
    font1 = font.Font(font.match_font('vernada'), size)
    text_surface = font1.render(text,True,(0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = y_speed
    
    def update(self):
        global score
        self.rect.y+=self.speed
        hits = sprite.groupcollide(monsters,bullets,True,True)
        for hit in hits:
            monster = Enemy('asteroid.png', random.randint(80,win_width - 80), random.randint(-1000,-80), 80, 80, 2)
            monsters.add(monster)
            mixer.init()
            mixer.music.load('collision.wav')
            mixer.music.play()
            score+=1
        if self.rect.y+self.size_y >= win_height:
            global finish
            self.rect.y = random.randint(-300,0-self.size_y)
            finish = False
        


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = y_speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("starwars")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)  
score = 0
bullets = sprite.Group()
monsters = sprite.Group()

ship = Player('rocket.png', win_width//2-40, win_height - 80, 80, 80, 0, 0)
p = sprite.Group()
p.add(ship)
for f in range(8):
    monster = Enemy('asteroid.png', random.randint(80,win_width - 80), random.randint(-1000,-80), 80, 80, 2)
    monsters.add(monster)


finish = True

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                ship.x_speed = -5
            elif e.key == K_RIGHT:
                ship.x_speed = 5
            elif e.key == K_SPACE:
                ship.fire()
            elif e.key == K_r and over == True:
                score = 0
                bullets = sprite.Group()
                monsters = sprite.Group()

                ship = Player('rocket.png', win_width//2-40, win_height - 80, 80, 80, 0, 0)
                p = sprite.Group()
                p.add(ship)
                for f in range(8):
                    monster = Enemy('asteroid.png', random.randint(80,win_width - 80), random.randint(-1000,-80), 80, 80, 2)
                    monsters.add(monster)
                    finish = True
                    over = False     
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                ship.x_speed = 0
            elif e.key == K_RIGHT:
                ship.x_speed = 0
            elif e.key == K_UP:
                ship.y_speed = 0
            elif e.key == K_DOWN:
                ship.y_speed = 0
    if finish != False:
        window.fill(back)  
        bullets.draw(window)
        monsters.draw(window)

        ship.reset()
        ship.update()
        monsters.update()
        bullets.update()
        draw_text(window,str(score),40,win_width/2,10)
    else:
        window.fill(back)
        draw_text(window,'Final score: '+str(score),40,win_width/2,win_height//3)
        draw_text(window,'Press R to restart',40,win_width/2,win_height//3+60)
        over = True
        


        

    time.delay(20)
    display.update()
