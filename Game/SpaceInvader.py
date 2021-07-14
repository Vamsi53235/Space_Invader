import math
import pygame
import random
from pygame import mixer #mixer is a class that helps us to handle music like loading the music , repeating the music etc.,

#initialize pygame
pygame.init()

#Create a screen
screen = pygame.display.set_mode((800,600)) #(800, 600) indicates (wwidth, height) of screen

#Title and Icon
pygame.display.set_caption('My First Game')
icon = pygame.image.load('D:\Vamsi\Documents\Python\Game\GameIcon.png')
pygame.display.set_icon(icon)


#Player
PlayerImage = pygame.image.load("D:\Vamsi\Documents\Python\Game\Fighter-48.png")
PlayerX = 360
PlayerY = 500
PlayerX_Change = 0

def Player(x,y):
    screen.blit(PlayerImage, (PlayerX, PlayerY)) # draws the player image on screen. blit(image, (co-ordinates))

#Enemy 
#List of enemies
no_of_enemies = 5
EnemyImage = []
EnemyX = []
EnemyY = []
EnemyX_Change = []
EnemyY_Change= []
for i in range(no_of_enemies):
    EnemyImage.append(pygame.image.load("D:\Vamsi\Documents\Python\Game\Enemy-48.png"))
    EnemyX.append(random.randint(0, 752)) #752 because the image is 48x48 size and screen is 800x600 size
    EnemyY.append(random.randint(0,100)) #similary 552
    EnemyX_Change.append(0.5)
    EnemyY_Change.append(50)

def Enemy(x,y):
    screen.blit(EnemyImage[i], (EnemyX[i], EnemyY[i])) # draws the Enemy image on screen

#Background
BackgroundImage = pygame.image.load('D:\Vamsi\Documents\Python\Game\Background.jpg')
BackgroundX = 0
BackgroundY = 0

def Background(x,y):
    screen.blit(BackgroundImage, (BackgroundX, BackgroundY))

# Background Music
mixer.music.load("D:\Vamsi\Documents\Python\Game\Background.wav")
mixer.music.play(-1)

#Bullet
#Ready indicates that the bullet is not on the screen and ready to Fire
#Fire indicates that the bullet is fired or currently in motion
BulletImage = pygame.image.load("D:\Vamsi\Documents\Python\Game\Bullet.png")
BulletX = 0
BulletY = PlayerY + 2
BulletY_Change = 1
Bullet_State = "Ready"

def Fire_Bullet(x,y):
    #print("Fire_Bullet is called")
    global Bullet_State
    Bullet_State = "Fire"
    screen.blit(BulletImage, (BulletX + 8, BulletY))

# Collision
def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    #if BulletY == (EnemyY + 48) and (BulletX == (EnemyX + 48) or BulletX == (EnemyX - 48)):
    P = [EnemyX, EnemyY]
    Q = [BulletX, BulletY]
    distance = math.dist(P, Q)#Find distance to check collision
    if distance <= 30 :#30 is less than the size of the enemy
        return True
    return False

#Score
Score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
#text co-ordinates
textX = 10
textY = 10
# First we need to render the font and then blit it
def show_text(x, y):
    Score = font.render('Score :' + str(Score_value), True, (255, 255, 255))
    screen.blit(Score, (x, y))
    
#Game Over Text
def game_over():
    #screen.fill((128, 120, 100))
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300, 250))

#Game loop
Running = True
while Running:

    #Fill screen with color
    screen.fill((255,252,255))
    Background(BackgroundX, BackgroundY)
    pygame.draw.line(screen,((120,0,255)),(0,PlayerY+48),(800,PlayerY+48),3) # A line to indicate the base of the Player

    #Every keystroke is an event and it is recorded and stored in pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        #check the pressed key is UP or DOWN or LEFT or RIGHT
        if event.type == pygame.KEYDOWN : #KEYDOWN indicates the key is down i.e pressed
            if event.key == pygame.K_LEFT:
                PlayerX_Change = -0.3

            if event.key == pygame.K_RIGHT:
                PlayerX_Change = 0.3

            if event.key == pygame.K_SPACE:
                if Bullet_State == "Ready":
                    BulletX = PlayerX
                    Fire_Bullet(BulletX, BulletY)
                    Bullet_Sound = mixer.Sound("D:\Vamsi\Documents\Python\Game\laser.wav")
                    Bullet_Sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_Change = 0.0


    #Checking player boundaries and make sure that the player is inside the boudaries
    #Player Movement
    PlayerX += PlayerX_Change
    if PlayerX >= 754:
        PlayerX = 754
    if PlayerX <= 0:
        PlayerX = 0

    #Enemy Movement
    for i in range(no_of_enemies):
        #Game Over
        if EnemyY[i] >= PlayerY-24:
            for j in range(no_of_enemies):
                EnemyY[j] = 1000
            game_over()
            break

        EnemyX[i] += EnemyX_Change[i]
        if EnemyX[i] >= 752:
            EnemyX_Change[i] = -0.5
            EnemyY[i] += EnemyY_Change[i]
        if EnemyX[i] <= 0:
            EnemyX_Change[i] = 0.5
            EnemyY[i] += EnemyY_Change[i]

        #Collision
        Collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if Collision:
            Collision_Sound = mixer.Sound('D:\Vamsi\Documents\Python\Game\explosion.wav')
            Collision_Sound.play()
            BulletY = PlayerY
            Bullet_State = "Ready"
            Score_value += 1
            EnemyX[i] = random.randint(0, 752)
            EnemyY[i] = random.randint(0,100) 
        
        Enemy(EnemyX[i], EnemyY[i])
    
    
    #Bullet Movement
    if Bullet_State == 'Fire':
        Fire_Bullet(BulletX, BulletY)
        BulletY -= BulletY_Change
        if BulletY <= 0:
            Bullet_State = 'Ready'
            BulletY = PlayerY

    
    Player(PlayerX,PlayerY) #This function should always be after the screen fill because player is always drawn on the screen but not under the screen 
    show_text(textX, textY)
    pygame.display.update() #update the screen every time(loop)