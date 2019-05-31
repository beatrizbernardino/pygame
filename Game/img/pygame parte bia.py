
import random
import pygame,time, sys
from pygame.locals import*
from os import path
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
vermelhozinho = (190, 2, 20)
width=900
height=600
win = pygame.display.set_mode((900,600))
pygame.display.set_caption("Missão Polar")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

walkRight = [pygame.image.load('papainoel5.png'), pygame.image.load('papainoel6.png'), pygame.image.load('papainoel7.png')]
walkLeft = [pygame.image.load('papainoel1.png'), pygame.image.load('papainoel3.png'), pygame.image.load('papainoel4.png')]
snd_dir = path.join(path.dirname(__file__))
img_dir=path.join(path.dirname(__file__))
bg = pygame.image.load('snow.png')
char  = pygame.image.load('papain.png')
pew = pygame.image.load("tiro.png").convert_alpha()
som=pygame.mixer.Sound(path.join(snd_dir, 'tiro.wav'))
boom=pygame.mixer.Sound(path.join(snd_dir, 'expl6.wav'))
bgsong=pygame.mixer.Sound(path.join(snd_dir, 'bg.wav'))
inicial=pygame.image.load('bbg.png')
final=pygame.image.load('final.jpg').convert()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Bg=pygame.transform.scale(bg,(900,600))
clock = pygame.time.Clock()
telafinal=pygame.transform.scale(final,(900,600))

vida=pygame.image.load('ra.jpg').convert()
vida.set_colorkey((255,255,255))
vitaoradical0=pygame.transform.scale(vida,(45,40))
vitaoradical1=pygame.transform.scale(vida,(45,40))
vitaoradical2=pygame.transform.scale(vida,(45,40))


player_img = pygame.image.load('pegiga.png') 
all_sprites=pygame.sprite.Group()
playergroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_platforms=pygame.sprite.Group()

class player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)

        self.image= pygame.transform.scale(char,(48,64))
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.invencivel=0
        self.speedx=0
        self.speedy=0
        self.pulo = False
        self.vel = 10
        self.jumpCount = 10
        self.direita = True
        self.esquerda = False
        self.parado = False
        self.radius = 32
        self.sprite_left = 0
        self.sprite_right = 0
        
    def update_sprite(self):
        if self.direita:
            self.sprite_right += 1
            if self.sprite_right == len(walkRight) - 1:
                self.sprite_right = 0
            self.image = pygame.transform.scale(walkRight[self.sprite_right],(48,64))
            
        if self.esquerda:
            self.sprite_left += 1
            if self.sprite_left == len(walkLeft) - 1:
                self.sprite_left = 0
            self.image = pygame.transform.scale(walkLeft[self.sprite_left],(48,64))
            
        if self.pulo or self.parado and self.speedx==0:
            self.image = pygame.transform.scale(char,(48,64))

    def update(self):
     
        self.rect.x += self.speedx
        self.rect.y+=self.speedy
        
        if not self.parado:
            self.speedy += 1 # Gravidade
            
        if self.speedx != 0:
            man.parado = False

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.invencivel > 0:
            self.invencivel -= 1
            
            
            
class enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image= pygame.transform.scale(player_img,(80,80))
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect() 
        self.rect.y = y 
        self.rect.x = x
        self.speedx = 5 
        self.speedy = 5

        self.herox = 0
        self.heroy = 0

        self.visible=True
        self.radius=27
        
    def update(self):
        if self.visible:
            if(self.rect.x - 16 > self.herox):
               self.rect.x -= self.speedx
            
            elif(self.rect.x + 16 < self.herox):
               self.rect.x += self.speedx
           
            if(self.rect.y - 16 > self.heroy):
               self.rect.y -= self.speedy
            
            elif(self.rect.y + 16 < self.heroy):
               self.rect.y += self.speedy
           
    def sethero(self, x, y):
        self.herox = x
        self.heroy = y

class projetil(pygame.sprite.Sprite):
    def __init__(self,x,y,pew,facing):
        pygame.sprite.Sprite.__init__(self)
        self.image=pew
        self.image = pygame.transform.scale(pew, (70, 50))
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedx=20 * facing
        self.facing = facing
    def update(self):
        self.rect.centerx += (self.speedx)
        if self.rect.centerx>width or self.rect.centerx<0:
            self.kill()
            
class Platform(pygame.sprite.Sprite):

    def __init__(self,x,y,w,h, tipo):
        pygame.sprite.Sprite.__init__(self)
        filename = ''
        if tipo == 'left':
            filename = 'snow_76.png'
        elif tipo == 'right':
            filename = 'snow_77.png'
        elif tipo== "middle":
           filename='snow_54.png'
           
           
        player_img=pygame.image.load(path.join(img_dir,filename)).convert()
        self.image=player_img 
        self.image=pygame.transform.scale(player_img,(w,h))    
        self.rect=self.image.get_rect()
        self.rect.height = 5
        self.rect.centerx=x
        self.rect.bottom=y
        self.image.set_colorkey((0,0,0))
   

for i in range (4):
    if i==0:
        for i in range (4):
    
            if i==0:
                p1=Platform(width/2-150+i*100,height-120,100,50,'left')
            elif i==3:
                p1=Platform(width/2-150+i*100,height-120,100,50,'right')
            else:
                p1=Platform(width/2-150+i*100,height-120,100,50,'middle')
        
            all_sprites.add(p1)
            all_platforms.add(p1)
        
    if i ==1:
         for i in range (4):
    
            if i==0:
                p1=Platform(width/2-400+i*70,height-300,70,45,'left')
            elif i==3:
                p1=Platform(width/2-400+i*70,height-300,70,45,'right')
            else:
                p1=Platform(width/2-400+i*70,height-300,70,45,'middle')
        
            all_sprites.add(p1)
            all_platforms.add(p1)
    if i ==2:
        
         for i in range (4):
    
            if i==0:
                p1=Platform(width/2+190+i*70,height-300,70,45,'left')
            elif i==3:
                p1=Platform(width/2+190+i*70,height-300,70,45,'right')
            else:
                p1=Platform(width/2+190+i*70,height-300,70,45,'middle')
            all_sprites.add(p1)
            all_platforms.add(p1)

    if i ==3:
        
        p1=Platform(width/2,height,900,30,'middle')
        
        all_sprites.add(p1)
        all_platforms.add(p1)

            
def RestaurarJanela():
    man.update_sprite() 
    all_sprites.update()
    win.blit(Bg, (0,0))
    all_sprites.draw(win)
    placar=font.render("Score: " + str(score), 1, (190,2,20))
    win.blit(placar,(730,70))
    
    if lives==3:
        win.blit(vitaoradical0,(730,10))
        win.blit(vitaoradical1,(785,10))
        win.blit(vitaoradical2,(840,10))
    if lives==2:
        win.blit(vitaoradical0,(730,10))
        win.blit(vitaoradical1,(785,10))
    if lives==1:
         win.blit(vitaoradical0,(730,10))

    pygame.display.update()


   
man=player(1,450,64,64)
playergroup.add(man)
all_sprites.add(man)
projeteis=[]
font = pygame.font.SysFont("comicsana",40,True)
count=0
run = True
font = pygame.font.SysFont("Somic Sans MS", 30)

 
       
high_score_file = open("high_score_file.txt", "r")
high_score = int(high_score_file.read())
high_score_file.close()  

numeroparticulas=100;

neve_list=[]

for i in range(numeroparticulas):
    x = random.randrange(0, 900)
    y = random.randrange(0, 600)
    neve_list.append([x,y])    

end_it=False

while not end_it:
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            end_it=True
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
            
    win.blit(inicial, (0,0))    
    pygame.display.flip()
    
try:
    
    bgsong.play(loops=-1)
    score=0
    lives=3
    time_left = 5
    while run:
      
        clock.tick(30)
        
        hits = pygame.sprite.groupcollide(all_platforms, playergroup, False, False)
        for hit in hits:
            if man.speedy > 0:
                man.rect.bottom = hit.rect.top
                man.speedy = 0
                man.pulo = False
                man.parado = True
            elif man.speedy < 0:
                man.rect.top = hit.rect.bottom
                man.speedy = 0
                man.pulo = False
         

        hits = pygame.sprite.groupcollide(enemygroup, playergroup, True, False, pygame.sprite.collide_circle)
     
        if hits:
             if man.invencivel==0:
                 lives -= 1

            
        if lives == 0:
            if score>high_score:
                high_score_file = open("high_score_file.txt", "w")
                high_score_file.write(str(score))
                high_score_file.close()
                high_score = score
            a= False
            pygame.mouse.get_pressed()
            while not a:
                myfont=pygame.font.SysFont("Britannic Bold", 60)
                vitorlindo=pygame.font.SysFont("Britannic Bold", 100)
                b=myfont.render("Score:"+ str(score),2, vermelhozinho )
                nlabel=vitorlindo.render("Game Over", 1, vermelhozinho)
                sco=myfont.render("HighScore:"+ str(high_score),2, vermelhozinho )
                
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
                    win.blit(telafinal,(0,0))
                    win.blit(nlabel,(width/2,height-550))
                    win.blit(b,(150,height-100))
                    win.blit(sco,(150,height-150))
                    pygame.display.flip()
                    run =False
           
            
                        
        hits =pygame.sprite.groupcollide(enemygroup,bullets , True, False, ) 
        if hits:
             boom.play()
             score+=1
        if man.invencivel > 0:
            total_mins = time_left//60 
            total_sec = time_left-(60*(total_mins)) 
            if time_left>0:
                
                time_left -= 1
                text = font.render(("Time left: "+str(total_mins)+":"+str(total_sec)), True, vermelhozinho)
                win.blit(text, (400, 50))
                pygame.display.flip()
        else:
            text = font.render("Time Over!!", True, vermelhozinho)
            win.blit(text, (400, 50))
#            pygame.display.flip()
            time_left=5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if man.esquerda:
                    facing = -1
                else:
                    facing = 1
            if not(man.pulo):
                if keys[pygame.K_w]:
                    man.pulo = True
                    man.speedy = -20
                    man.parado = False
                    
            if keys[pygame.K_s]:
                 man.invencivel=270
#                 time_left = 10
#                 total_mins = time_left//60 
#                 total_sec = time_left-(60*(total_mins)) 
#                 time_left -= 1
                 
                
    
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    man.speedx -= man.vel
                    man.direita = False
                    man.esquerda= True
                    man.parado = False
                    
                if event.key == pygame.K_d:
                    man.speedx += man.vel
                    man.direita = True
                    man.esquerda = False
                    man.parado = False
                if event.key == pygame.K_SPACE:
                    bullet=projetil(man.rect.centerx,man.rect.bottom,pew,facing)
                    bullet.rect.centerx=man.rect.x +10
                    bullet.rect.bottom=man.rect.y + 40
                    som.play()
                    projeteis.append(bullet)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
             
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    man.speedx = 0
                if event.key == pygame.K_d:
                    man.speedx = 0

                
        if count == 80:
            
            en= enemy(random.randrange(0,width), random.randrange(0,height))



            enemygroup.add(en)
            all_sprites.add(en)
            count=0
        count+=1
                
        RestaurarJanela()
        for en in enemygroup:
            en.sethero(man.rect.x, man.rect.y)
        
        for point in neve_list:
            point[1]+=1
            pygame.draw.circle(win, WHITE, point, 2)

            if(point[1] >= height):
                point[0] = random.randrange(0, 900)
                point[1] = random.randrange(-10, -5)
        pygame.display.flip()
finally:
    pygame.quit()
    sys.exit()
    quit()