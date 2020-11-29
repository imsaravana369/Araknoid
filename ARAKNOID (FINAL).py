import pygame
from pygame.locals import *
from stack import   *
import time 
import random
#COLORS
BLACK=[0,0,0]
RED2=[255, 0, 0]
WHITE=[255,255,255]
GREY=[128,128,128]
RED=[0, 0, 255]
SILVER=[192,192,192]
PINK=(255, 0, 102)
YELLOW=(255,255,0)
BLUE=(0,0,0)
GREEN=(0,255,0)
VIOLET=( 115, 0, 230)
ORANGE=(255, 117, 26)
GREEN2= [ 102, 255, 51]
PINK2=[144, 12, 63]
def reset():
#stack
    global s,emptystr,highscore,show_score,launched,Start,win,speedvar,change_speed,changespeedinterval,bar,lostlife
    global total_score,Level_Score,block_list,all_sprites_list,player_sprite,sprited_block_rect,iron_block_list,hs,level,run
    global counterval0,counterval1,counterval2,counter0,counter1,counter2
    counter0=False
    counter1=False
    counter2=False

    counterval0=counterval1=counterval2=0
    s=Stack()

    emptystr=str()
    highscore=int()
    show_score=bool()
    launched=bool()
    Start=bool()
    win=bool()             
    speedvar=int()            #speedchange for each changespeedinterval
    change_speed=bool()           # whether the speed change at the instant
    changespeedinterval=int()   # for no.of.Level_Score increase, the speed will increase
    bar=0
    lostlife=0
    
    total_score=0      # total Level_Score 
    Level_Score=0               # Level_Score of each level 

      #Group
    block_list=pygame.sprite.Group()
    all_sprites_list=pygame.sprite.Group()
    player_sprite=pygame.sprite.Group()

     #List
    sprited_block_rect=list()
    iron_block_list=list()
    power_block_list=list()
    hs=0            
    with open("HighScore.txt",'r') as f:
                            hs=f.read()

    clock=pygame.time.Clock()
    level=1
    run=True

     
# self.life=3
           
class Block(pygame.sprite.Sprite):
    def  __init__(self,color,w,h):
          super().__init__()
          self.color=color
          self.image=pygame.Surface([w,h])
          self.image.fill(self.color)

          self.rect=self.image.get_rect()
          self.health= 200 if color == [128,128,128] else 100

    def update(self):
          self.rect.y+=10
    

class Bar(pygame.sprite.Sprite):
    def __init__(self,color,w,h):
          super().__init__()
          self.length=w
          self.height=h
          self.color=color
          self.image=pygame.Surface([self.length,self.height])
          self.image.fill(self.color)

          self.rect=self.image.get_rect()
          
          self.rect.x= screen_width//2
          self.rect.y= screen_height - (self.height-1)   # (h is the bar's length)
    
        

class Ball(pygame.sprite.Sprite):
    def __init__(self,color,radius,speed,speedvar):
        global lostlife
        super().__init__()
        self.color=color
        self.radius=radius
        self.x_speed=self.y_speed=speed
        self.speedvar=speedvar
        self.life=3-lostlife
        
        self.image=pygame.Surface([self.radius,self.radius],pygame.SRCALPHA)  #SCRALPHA for TRANSOARENCY
        self.image.fill(BLUE)
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()
    
        pygame.draw.ellipse(self.image,self.color,self.rect)    

    def update(self):
       global Start
       global changespeedinterval
       global changespeed
       global win
       global launched
       global bar
       global lostlife
       global fall_list
       global counterval0,counterval1,counterval2
       global counter0,counter1,counter2
       global ball
       global specialcondition
       index=0
       if self.rect.x+self.radius > screen_width or self.rect.x < 0 :
           self.x_speed*=-1
       
       #index=self.rect.collidelistall(all_block_rect)
       hit=True if len(sprited_block_rect) >0 else False
       # hit become True if the ball collides with any blocks
       if hit :
             self.rect.y+=10
             self.y_speed*=-1

       if self.rect.y< 0 or self.rect.colliderect(bar.rect) :
             self.y_speed*=-1
             if bar.rect.x<= self.rect.x <= bar.rect.x + bar.length//3 :
                if self.x_speed > 0 :
                 self.x_speed*=-1

             elif bar.rect.x+bar.length//2 <= self.rect.x <= bar.rect.x + bar.length :
                 if self.x_speed < 0 :
                   self.x_speed*=-1
                   
                   
       if self.rect.y> screen_height and self.life >0.5 and launched :
            big_ball_launch=0
            self.life-=1
            lostlife+=1
            time.sleep(0.5)
            if counter0==True:
                big_ball_launch=10
                    
            self.rect.x=bar.rect.x+self.radius
            self.rect.y=bar.rect.y-(self.radius+big_ball_launch)
            launched=False
            
       if self.rect.y+self.radius > screen_height and self.life <=1:
           Start=False
           win=False
        
       for block in fall_list:
                if block.rect.y<screen_height:
                   block.update()
                
                   
                if block.rect.y>=screen_height:
                     block.rect.y+=screen_height
                     fall_list.remove(block)
                     
                     
                if block.rect.colliderect(bar.rect):
                   for block in fall_list:
                       block.rect.y+=screen_height
                       fall_list.clear()
                   if block.color==PINK2:
                       if counter1==True:
                           counterval1=0
                           break
                       counter1=True
                       colorb=bar.color
                       heightb=bar.height
                       lenghtb=bar.length
                       xpot=bar.rect.x
                       ypot=bar.rect.y
                       all_sprites_list.remove(bar)
                       bar=Bar(PINK2,lenghtb+18,20)
                       all_sprites_list.add(bar)
                       bar.rect.x=xpot
                       bar.rect.y=ypot
                       specialcondition=True
                       break
                   elif block.color==RED2: #slow ball
                       if counter2==True:
                           counterval2=0
                           break
                       counter2=True
                       
                       self.x_speed*=0.80
                       self.y_speed*=0.80
                       break
                   elif block.color==WHITE:
                       if counter0==True:
                           counterval0=0
                           break
                           
                       counter0=True
                       
                       self.radius+=30
                       xpo=self.rect.x
                       ypo=self.rect.y
                       all_sprites_list.remove(ball)
                       player_sprite.remove(ball)
                       ball=Ball(GREEN,self.radius,self.x_speed,self.speedvar)
                       ball.rect.x=xpo
                       ball.rect.y=ypo
                       all_sprites_list.add(ball)
                       player_sprite.add(ball)
                       self.update()
                       break
                   if self.life > 0.5:
                    big_ball_launch=0
                    self.life-=0.25
                    lostlife+=0.25
                    self.rect.x=bar.rect.x+self.radius
                    if counter0==True:
                         big_ball_launch=10
                         
                    self.rect.y=bar.rect.y-(self.radius+big_ball_launch)
                    launched=False
                   else:
                     Start=False
                     win=False
                     break
       
       if counter0 or counter1 or counter2:
           
        if counterval0>=1000:#reverse condition for bigball
            counterval0=0
            counter0=False
            self.radius-=30
            xpo=self.rect.x
            ypo=self.rect.y
            all_sprites_list.remove(ball)
            player_sprite.remove(ball)
            ball=Ball(GREEN,self.radius,self.x_speed,self.speedvar)
            ball.rect.x=xpo
            ball.rect.y=ypo
            all_sprites_list.add(ball)
            player_sprite.add(ball)
            self.update()
        elif counterval1>=1000:
            counter1=False
            counterval1=0
            
            xpot=bar.rect.x
            ypot=bar.rect.y
            all_sprites_list.remove(bar)
            bar=Bar(SILVER,bar_length,20)
            all_sprites_list.add(bar)
            bar.rect.x=xpot
            bar.rect.y=ypot
            specialcondition=False
        elif counterval2>=1000:
            counterval2=0
            counter2=False
            self.x_speed*=1.25
            self.y_speed*=1.25
                          
                 
       if len(block_list) <= 0 :   #when all the blocks are demolished, finish the level 
               Start=False
               win=True
               
       if Level_Score == changespeedinterval :   #for every changespeedinterval value  increment the speed of the ball
             changespeed=True
             
       if Level_Score%10== 0 and Level_Score>=10 and changespeed:  #Level_Score>=10 is not to increment the speed for values less than zero since mod 10 of every value below 11 is 0
           self.x_speed*=self.speedvar
           self.y_speed*=self.speedvar
           changespeed=False
           changespeedinterval+=10

       # finally increment x and y speed   
       self.rect.x+=self.x_speed
       self.rect.y-=self.y_speed


#################HIGH SCORE IN INTRO SCREEN #####################
hs=0            
with open("HighScore.txt",'r') as f:
                    hs=f.read()
#################################################################
                            
def introscreen():
    global hs
    global Start
    global emptystr
    global show_score
    global level
    
    titlefont=pygame.font.SysFont("Comic sans MS",48)
    font=pygame.font.SysFont(None,48)
    title=titlefont.render("Araknoid",True,BLACK,GREEN)
    title_rect=title.get_rect()
    play_text=font.render("Play",True,BLACK,GREEN)
    play_rect=play_text.get_rect()
    quit_text=font.render("Quit",True,BLACK,GREEN)
    quit_rect=quit_text.get_rect()
    high_score=font.render("High Score",True,BLACK,GREEN)
    high_score_rect=high_score.get_rect()
    show_hscore=font.render(emptystr,True,BLACK)
    show_hscore_rect=show_hscore.get_rect()
    

    title_rect.center=screen.get_rect().center
    title_rect.centery=screen.get_rect().centery - 130
    play_rect.center=screen.get_rect().center
    quit_rect.centerx=screen.get_rect().centerx
    quit_rect.centery=screen.get_rect().centery +60
    high_score_rect.centerx=screen.get_rect().centerx
    high_score_rect.centery=screen.get_rect().centery +120
    show_hscore_rect.centerx=screen.get_rect().centerx
    show_hscore_rect.centery=screen.get_rect().centery +200

    screen.blit(title,title_rect)
    screen.blit(play_text,play_rect)
    screen.blit(quit_text,quit_rect)
    screen.blit(high_score,high_score_rect)
    screen.blit(show_hscore,show_hscore_rect)

    
    for event in pygame.event.get():
        mpos=pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
             pygame.quit()
             quit()
        elif event.type==pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_rect.collidepoint(mpos) :
                    Start=True
                    break
                
            elif quit_rect.collidepoint(mpos):
                    pygame.quit()
                    quit()

            # setting highscore button as ON AND OFF switch
             

            elif high_score_rect.collidepoint(mpos) and not show_score  :
                     
                     emptystr=str(hs)
                     show_score=True  

            elif  high_score_rect.collidepoint(mpos) and show_score  :
                    emptystr=str()
                    
                    show_score=False
                    

               
def Start_Game(iron):
    # iron arguments says number of iron block rows 
    pygame.mouse.set_visible(False)
    posy=0
    colourlist=[RED,SILVER,PINK,YELLOW,VIOLET,GREEN2]
    power_block_list=[]
    powlist=['bigball','longbar','slowball']
    bigball=longbar=slowball=0
    for i in range(5):
        posx=0
        
        for j in range(10):
               
               color= GREY if i<iron else colourlist[random.randint(0,5)]  

               block=Block(color,47,25)
               block.rect.x=posx
               block.rect.y=posy
               #screen.blit(block.image,block.rect)
               block_list.add(block)
               all_sprites_list.add(block)
               if i ==0:
                   iron_block_list.append(block)
               #all_block_rect.append(block.rect)
               rand= random.randint(0,7)    
               if (rand <3) and i!=0 :
                   power_block_list.append(block)
                   
                   if rand==0 and bigball <2 :
                       block.color=WHITE #for larger ball
                       
                       
                   elif rand==1 and longbar < 2:
                       
                       
                       block.color=PINK2 #for longer bar
                   elif rand==2 and slowball < 2 :
                       
                       block.color=RED2 #for slower ball
               posx+=50

        posy+=28

    all_sprites_list.add(bar)

def GameOver(message,Escape):
    global  highscore
    global total_score
    if Escape:
        score=total_score
    else:
        score=highscore
    basicfont=pygame.font.SysFont('Comic Sans MS',46)
    scorefont=pygame.font.SysFont(None,50)
    text=basicfont.render(message,True,WHITE,BLUE)   # render(text,anti-aliasing,color,background)
    textrect=text.get_rect()
    textrect.centerx=screen.get_rect().centerx
    textrect.centery=screen.get_rect().centery-50
    show_score=scorefont.render(str(score),True,RED,GREEN)
    score_rect=show_score.get_rect()
    score_rect.centerx=screen.get_rect().centerx
    score_rect.centery=screen.get_rect().centery 
    intro=scorefont.render("Press Enter to Play Again",True,BLACK,BLUE)
    introrect=intro.get_rect()
    introrect.centerx=screen.get_rect().centerx
    introrect.centery=screen.get_rect().centery+60
    screen.blit(text,textrect)
    screen.blit(show_score,score_rect)
    screen.blit(intro,introrect)
    for event in pygame.event.get():
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
                                return True 
                      

    

def showscore(ball):
      font=pygame.font.SysFont(None,40)
      levelfont=font.render("LEVEL "+str(level),True,WHITE,BLACK)
      lifefont=font.render("LIFE:"+str(ball.life),True,WHITE,BLACK)
      scorefont=font.render("SCORE:"+str(total_score),True,WHITE,BLACK)

      level_rect=levelfont.get_rect()
      life_rect=lifefont.get_rect()
      score_rect=scorefont.get_rect()


      level_rect.centerx=screen.get_rect().centerx
      level_rect.centery=screen.get_rect().centery
      score_rect.centerx=screen.get_rect().centerx+70
      score_rect.centery=screen.get_rect().centery+40
      life_rect.centerx=screen.get_rect().centerx-60
      life_rect.centery=screen.get_rect().centery+40

      screen.blit(levelfont,level_rect)
      screen.blit(scorefont,score_rect)
      screen.blit(lifefont,life_rect)
    

pygame.init()
screen_width=500
screen_height=500
screen=pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("ARAKNOID")


clock=pygame.time.Clock()
level=1
run=True

fall_list=[]
#is_falling=bool()
#fall_img=pygame.Surface([30,30])
#fall_img.fill(RED)
#fall_rect=fall_img.get_rect()

def NextStage(speedVar,bar_len,ball_rad,ball_speed):
            global emptystr
            global hs # high score to be stored in file
            global highscore 
            global show_score 
            global Start 
            global win            
            global change_speed         
            global changespeedinterval
            global speedvar
            global bar
            global Level_Score
            global total_score
            global level
            global run
            global launched
            global fall_list
            global counterval0,counter0
            global counterval1,counter1
            global counterval2,counter2
            global ball
            global specialcondition
            global bar_length
            bar_length=bar_len
            
            specialcondition=False
           # global fall_rect


            speedvar=speedVar
            #bar
            bar=Bar(SILVER,bar_len,20)
            emptystr=str()
            show_score=False
            Start=False  if level==1 else True
            win=False

            #execute at the beginning level only
            while not Start and level==1:
                 for event in pygame.event.get():
                     if  event.type == pygame.QUIT :
                          pygame.quit()
                          exit()
                          break
                     
                                                    
                 screen.fill(BLUE)
                 introscreen()
                 pygame.display.flip()

            block_hit_list=[]     
            ball=Ball(GREEN,ball_rad,ball_speed,speedvar)
            ball.rect.x=screen_width//2 + 20
            ball.rect.y=screen_height-45
            all_sprites_list.add(ball)
            player_sprite.add(ball)
            
            #creating blocks
            
            Start_Game(level)
            
            
            launched=False
            while Start:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                          pygame.quit()
                    if event.type== .KEYDOWN and event.key==pygame.K_SPACE and not launched :
                            player_sprite.update()
                            launched=True
                    #for quitting in middle of the running game
                    if   event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                          run=False
                          changeHighscore(total_score,hs)
                          while True:
                                 screen.fill(BLUE)
                                 pygame.mouse.set_visible(True)
                                 if GameOver("You Escaped , Coward !!",True):
                                      return
                                 pygame.display.update()
                if counter0:
                    
                    if counterval0<=1000: counterval0+=1
                elif counter1:
                    
                    if counterval1<=1000: counterval1+=1
                elif counter2:
                    
                    if counterval2<=1000: counterval2+=1
                
                keys=pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and bar.rect.x>0 :
                       if not launched :
                           ball.rect.x-=6  # to move the ball with respect to bar when it is not launched yet
                       bar.rect.x-=7
                if keys[pygame.K_RIGHT] and bar.rect.x<screen_width-bar.length:
                         if not launched :
                            ball.rect.x+=6
                         bar.rect.x+=7

                screen.fill(BLUE)
                
                
                
                remove=bool()
                iron=[block.rect for block in iron_block_list]
                if ball.rect.collidelist(iron)+1 :    # the rect1.collidelist(rect2list) will return the index of the total rectangles of rect2list that collide with rect1
                  for block in iron_block_list:
                     if ball.rect.colliderect(block.rect):
                          remove=False
                          block.image.fill(RED)
                          iron_block_list.remove(block)
                          break
    
                else:
                    remove=True

                block_hit_list=pygame.sprite.spritecollide(ball,block_list,remove)
                    
                for block in block_hit_list:
                      if block.color !=GREY and len(fall_list)<3:
                          block.rect.width-=35
                          block.rect.height-=5
                          fall_list.append(block)
                      if specialcondition==True: block.color=PINK2 

                      if block.color == GREY and block not in iron_block_list :
                          block.color = RED
                            
                      sprited_block_rect.append(block.rect)
                      total_score+=1
                      Level_Score+=1
                
                    
                if launched:
                   player_sprite.update()                       
                   sprited_block_rect.clear()
                   
                all_sprites_list.draw(screen)
                player_sprite.draw(screen)

                for block in fall_list:
                    pygame.draw.rect(screen,block.color,block.rect)
        
                            
                     
                showscore(ball)


                clock.tick(60)
                pygame.display.flip()
                


            while not Start :

                ball.image.fill(BLUE)
                bar.image.fill(BLUE)
                player_sprite.remove(ball)   # del ball   
                pygame.mouse.set_visible(True)
                screen.fill(BLUE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                          pygame.quit()

                highscore=total_score
                if win:
                     if gotonextlevel():
                         break
                else:
                     run=False
                     changeHighscore(highscore,hs)
                     if GameOver('GAME OVER',False):
                               return 
                     
                pygame.display.flip()
            Level_Score=0



    
#NextStage(ch_s,ch_in,bar_len,ball_rad,ball_speed)
def gotonextlevel():
            global level
            if level != 5:
               font=pygame.font.SysFont(None,28)
               nextlev=font.render("Press ENTER to continue",True,BLACK,GREEN)
               nextlev_rect=nextlev.get_rect()
               nextlev_rect.center=screen.get_rect().center
               for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
                             level+=1
                             return True
               screen.blit(nextlev,nextlev_rect)
               pygame.display.update()
           
            else:
                font=pygame.font.SysFont(None,28)
                total_score=400
                nextlev=font.render("You Won !!",True,BLACK,GREEN)
                nextlev_rect=nextlev.get_rect()
                nextlev2=font.render("Score :"+str(total_score),True,BLACK,GREEN)
                nextlev2_rect=nextlev2.get_rect()
                nextlev_rect.center=screen.get_rect().center
                nextlev2_rect.center=screen.get_rect().center
                nextlev2_rect.centery=screen.get_rect().centery+40

                screen.blit(nextlev,nextlev_rect)
                screen.blit(nextlev2,nextlev2_rect)
                pygame.display.update()
                return 

def changeHighscore(highscore,hs):
    if highscore>int(hs):
                with open("HighScore.txt",'w') as f:
                        f.write(str(highscore))

reset()
def Next():
   global run,level,lostlife,s
   
   while run and not s.isEmpty() :
       arg=s.pop()
       if level>1:
         lostlife-=1
       NextStage(arg[0],arg[1],arg[2],arg[3])

try:
 while  True:
     if run :
      Next()
     else:
         reset()
except:
    print("You have to Install PYGAME to run this game")
