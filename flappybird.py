import pygame,random
pygame.init()
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
dw=600
dh=476
screen=pygame.display.set_mode([dw,dh])
pygame.display.set_caption('Flappy Bird')
pimg=[pygame.image.load(str(i)+'.png') for i in range(1,5)]
clock=pygame.time.Clock()
vec=pygame.math.Vector2
bg=pygame.image.load('bg.png')
bw=bg.get_width()
blist=[[50,310],[60,300],[70,290],[80,280],[90,270],[100,260],[110,250],[120,240],[130,230],[140,220],[150,210],[160,200],[170,190],[180,180],
       [190,170],[200,160],[210,150],[220,140],[230,130],[240,120],[250,110],[260,100],[270,90],[280,80]
       ,[290,70],[300,60],[310,50]]
class Bird(pygame.sprite.Sprite):
   def __init__(self,game):
      super().__init__()
      self.image=pimg[0]
      self.image=pygame.transform.scale(self.image,(100,85))
      self.rect=self.image.get_rect()
      self.vel=vec(0,0)
      self.rect.center=(dw/2,dh/2)
      self.acc=vec(0,0)
      self.pos=vec(self.rect.center)
      self.fc=0
   def update(self):
      self.acc=vec(0,1.5)
      self.vel=vec(0,0)
      keys=pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
         self.acc.y=-1.5
         if self.fc+1<28:
            self.fc+=1
            self.image=pimg[self.fc//7]
            self.image=pygame.transform.scale(self.image,(100,85))
         else:
            self.fc=0
      else:
         self.image=pimg[0]
         self.image=pygame.transform.scale(self.image,(100,85))
      self.vel+=self.acc
      self.pos+=self.vel+0.5*self.acc
      if self.pos.y<=0+self.rect.width/2:
         self.pos.y=0+self.rect.width/2
      if self.pos.y>=dh-self.rect.width/2:
         self.pos.y=dh-self.rect.width/2
      self.rect.center=self.pos
      self.mask=pygame.mask.from_surface(self.image)
class TBlock(pygame.sprite.Sprite):
   def __init__(self,x,h1):
      super().__init__()
      self.image=pygame.image.load('tp.png')
      self.image=pygame.transform.scale(self.image,(80,h1))
      self.rect=self.image.get_rect()
      self.rect.x,self.rect.y=x,0
   def update(self):
      self.rect.x-=2
      self.mask1=pygame.mask.from_surface(self.image)
class BBlock(pygame.sprite.Sprite):
   def __init__(self,x,h2):
      super().__init__()
      self.image=pygame.image.load('bp.png')
      self.image=pygame.transform.scale(self.image,(80,h2))
      self.rect=self.image.get_rect()
      self.rect.x,self.rect.y=x,dh-self.rect.height
   def update(self):
      self.rect.x-=2
      self.mask2=pygame.mask.from_surface(self.image)
class Game:
   def __init__(self):
      self.bgx=0
      self.x=650
      self.h1=180
      self.h2=180
      self.score=0
      self.gover=0
      self.last=pygame.time.get_ticks()
   def blockgen(self):
      x=random.randint(620,650)
      h=random.choice(blist)
      h1=h[0]
      h2=h[1]
      self.tblock=TBlock(x,h1)
      self.tblocks=pygame.sprite.Group()
      self.tblocks.add(self.tblock)
      self.all_sprites.add(self.tblock)
      self.bblock=BBlock(x,h2)
      self.bblocks=pygame.sprite.Group()
      self.bblocks.add(self.bblock)
      self.all_sprites.add(self.bblock)
   def new(self):
      self.bird=Bird(self)
      self.all_sprites=pygame.sprite.Group()
      self.all_sprites.add(self.bird)
      self.tblock=TBlock(self.x,self.h1)
      self.tblocks=pygame.sprite.Group()
      self.tblocks.add(self.tblock)
      self.all_sprites.add(self.tblock)
      self.bblock=BBlock(self.x,self.h2)
      self.bblocks=pygame.sprite.Group()
      self.bblocks.add(self.bblock)
      self.all_sprites.add(self.bblock)
      self.score=0
      self.gover=0
   def msg(self,text,x,y,color,size):
      self.font=pygame.font.SysFont('georgia',size,bold=1)
      msgtxt=self.font.render(text,1,color)
      msgrect=msgtxt.get_rect()
      msgrect.center=x/2,y/2
      screen.blit(msgtxt,(msgrect.center))
   def pause(self):
      wait=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
         self.msg("Paused",dw-100,dh-100,blue,40)
         pygame.display.flip()
   def over(self):
      wait=1
      self.gover=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
         self.msg("Gameover",dw-150,dh-100,red,40)
         self.msg("Press Enter to Play Again",dw-545,dh+200,red,40)
         pygame.display.flip()
      self.new()
   def scores(self):
         self.msg("Score:"+str(self.score),dw-130,200,green,30)
      
   def update(self):
     self.all_sprites.update()
     now=pygame.time.get_ticks()
     hits1=pygame.sprite.spritecollide(self.bird,self.bblocks,False,pygame.sprite.collide_mask)
     hits2=pygame.sprite.spritecollide(self.bird,self.tblocks,False,pygame.sprite.collide_mask)
     if hits1 or hits2:
        self.over()       
     relx=self.bgx%bw+5
     screen.blit(bg,(relx-bw+3,0))
     if relx<dw:
        screen.blit(bg,(relx,0))
     self.bgx-=2
     if self.bblock.rect.x<dw/2 and self.tblock.rect.x<dw/2:
        self.blockgen()
        self.score+=1
     if now-self.last>1500:
         self.last=now
         self.score+=1
     else:
        self.score+=0
         
   def draw(self):
      self.all_sprites.draw(screen)
      self.scores()
   def event(self):
      for event in pygame.event.get():
         clock.tick(60)
         if event.type==pygame.QUIT:
            pygame.quit()
            quit()
         if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  self.pause()
   def run(self):
      while 1:
         self.event()
         self.update()
         self.draw()
         pygame.display.flip()
g=Game()
while g.run:
   g.new()
   g.run()
