from pygame import *
from math import *
from pygame import mixer

display.set_caption("Shape Run") #names the window

width,height=1200,800
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)

mixer.init() #initialize mixer

def drawScene(p,blocks,spikes,lev):
    'this function does all the drawing in the levels'
   
    #this set of "ifs" are to change the background if it is a different level
    if lev=="lev1":
        screen.fill(BLUE)
    elif lev=="lev2":
        screen.fill((255,0,255))
   
    draw.rect(screen,BLACK,(0,650,1200,5)) #draws the floor
    screen.blit(playerSkin,p) #draws the player

    #this is too see if the blocks and or the spikes are on the screen
    #and if they are it will be put on the screen
    for b in blocks:
        if b[0]-distance<1200 and b[0]-distance>-b[2]:
            draw.rect(screen,BLACK,(b[0]-distance,b[1],b[2],b[3]))
    for s in spikes:
        if s[0]-distance<1200 and s[0]-distance>-s[2]:
            screen.blit(spikePic,(s[0]-distance,s[1]))

def move(p,blocks):
    'this function is to move the player AKA let the player jump'
   
    global fromMenu #sees if you go into a level from a menu screen
    vy=p[1]-170 #this is the vertical jump/ Y valocity
    gravity=2 #this is the graviy to let the player fall back down
   
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()

    #this check if you have clicked the space bar or left click
    #it also checks if you just came from a menu, it check if you are
    #over the pause button and if the pixel below is black then yets you jump
    if ((mb[0] and fromMenu==False and pauseButton.collidepoint(mx,my)==False) or keys[K_SPACE]) and (screen.get_at((p[0],p[1]+51))==BLACK or screen.get_at((p[0]+p[2]-1,p[1]+51))==BLACK):
        p[1]=vy

    if p[1]<=598: #this makes it so you keep falling until you are at a Y position of 598 or lower
        p[1]+=gravity

    for b in blocks:
        if b[0]-distance<1200 and (b[0]+b[2])-distance>=p[0]: #this checks if the block is on the screen
            if p[0]+p[2]>=b[0]-distance and p[1]+p[3]>=b[1] and p[1]<b[1]+b[3]: #this lets you jump on top of the block
                p[1]=b[1]-p[3]

def hit(blocks,spikes,p,skin,triangle):
    'this function is to detect if you hit something'
   
    global distance #this lets you use distance any where
   
    for b in blocks: #going through each block
        if b[0]-distance<1200 and (b[0]+b[2])-distance>=p[0]: #this checks if the block is on the screen
            if p[0]+p[2]>=b[0]-distance and p[1]+p[3]>b[1] and p[1]<b[1]+b[3]:#then this check for if the player hits the sides of the box
                distance=0#resets the level
                p[1]=600#returns player to the start
   
    for s in spikes: #going through each spike
            if s[0]-distance<1200 and s[0]-distance>-s[2]: #this checks if the spike is on the screen
                #what masking does is let you get pixel perfect collision with images
                triangle_mask=mask.from_surface(triangle) #this mask the image of the triangle
                triangle_rect=triangle.get_rect() #get the rect of the triangle
                tx=s[0]-distance #x location
                ty=s[1] #y location
                skin_mask=mask.from_surface(skin) #mask the image of the player
                skin_rect=skin.get_rect() #gets the rect of the player
                offset=(int(p[0]-tx),int(p[1]-ty)) #check the offset of the player and triangle
                result=triangle_mask.overlap(skin_mask,offset) #check to see if the player hits the triangle
                if result: #if yes
                    distance=0 #resets the level
                    p[1]=600 #returns to the start of the level

def music(file):
    'this function lets you load music'
    mixer.music.load(file) #load the music file
    mixer.music.play(-1) #puts it on repeat

def menu(action):
    'this function is the menu for our game'
   
    music("Sounds/SR_menu.mp3") #adds music to the menu
   
    screen.blit(menuBackground,(0,0)) #adding a background picture
    screen.blit(title,(150,100)) #adding the name of our game

    while action=="menu": #this will run when while the action equals menu
       
        click=False
       
        for evt in event.get():
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
               
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
       
        for b in range(3):
            if buttons[b].collidepoint(mx,my): #this is to check if the mouse is over the buttons
                screen.blit(menuOptionsHover[b],buttons[b]) #this turns the button a little gray when you are hovering
                if click: #chekcs if you left click over the button
                    if b==0: #this sends you to the levels screen
                        action=levels("levs")
                    elif b==1: #sends you to the setting screen
                        global fromGame
                        fromGame=False #this sets fromGame to false so you dont go to level1 or 2 when you hit the back button
                        action=settings("set","menu")
                    else: #sends you to the credits screen
                        action=credits("cr")
            else: #this is for when you aren't hovering so it won't be gray
                screen.blit(menuOptions[b],buttons[b])
       
        display.flip()

def levels(action):
    'this function is the screen for selecting levels'
   
    screen.blit(menuBackground,(0,0)) #adds a background image for this screen
    screen.blit(levelSelect,(338,100)) #adds the title to this screen
     
    while action=="levs": #runs while action equals levs
       
        click=False

        escape=False
       
        for evt in event.get():
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
       
        for l in range(2):
            if levelOptions[l].collidepoint(mx,my): #this checks if your mouse is over the level buttons
                screen.blit(levelOptionsPicsHover[l],levelOptions[l]) #this turns the level button gray when over it to show what you are selecting
                if click: #checks if you left click over the levelOptions button
                    if l==0: #if you click on the first one it brings you to level 1
                        action=level1("lev1")
                    elif l==1: #if you click on the second one it brings you to level 2
                        action=level2("lev2")
            else: #this displays the original level option buttons
                screen.blit(levelOptionsPics[l],levelOptions[l])
       
        if escape: #if you press escape it will bring you back to the menu for this screen
            action=menu("menu")
        if back.collidepoint(mx,my): #checks if your mouse is over the back button
            screen.blit(backPicHover,back) #turns the button gray when over it
            if click: #if you left click the back button it will bring you back to the menu screen
                action=menu("menu")
        else: #the original image for the back button
            screen.blit(backPic,back)

        display.flip()

def level1(action):
    'this funtion is the first level in our game'

    #this adds a different background music for this level
    music("Sounds/SR_level1.mp3")

   
    player[1]=600 #the y value for the player at the start
    global distance #lets you use distance anywhere
    distance=0 #the starting value for distance
   
    global fromMenu #to let you use fromMenu anywhere
    fromMenu=True #fromMenu starts off as true
   
    while action=="lev1": #while the action is lev1
       
        click=False
       
        escape=False
       
        for evt in event.get():            
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
                    fromMenu=False
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
       
        distance+=1.5 #constantly adds 1.5 to the distance
       
        drawScene(player,blocks1,spikes1,action) #this add our draw scene function with it's parameters
        hit(blocks1,spikes1,player,playerSkin,spikePic) #this adds our hit function with it's parameters
        move(player,blocks1) #this adds our move funtion with it's parameters
       
        if distance>=5000: #when the distance it greater or equal to 5000 it will go to the win screen
            action=win("W")
       
        if escape: #if you press escape it will go to our pause screen and pause the game
            action=pause("pau",action)
        if pauseButton.collidepoint(mx,my): #checks if your mouse is over the pause button
            screen.blit(pauseButtonPicHover,pauseButton) #turns the pause button gray
            if click: #checks if you click
                fromMenu=True #turns the fromMenu to true
                action=pause("pau",action) #brings you to the pause screen
        else: #the original pause button
            screen.blit(pauseButtonPic,pauseButton)

        time.Clock().tick(220) #changes the speed
       
        display.flip()

def level2(action):
    'this funtion is the second level in our game'

    #this adds a different background music for this level
    music("Sounds/SR_level2.mp3")

   
    player[1]=600 #the y value for the player at the start
    global distance #to let you use distance any where
    distance=0 #the starting value for distance
   
    global fromMenu  #to let you use fromMenu any where
    fromMenu=True #fromMenu starts off as true
   
    while action=="lev2": #while the action is lev2
       
        click=False
       
        escape=False
       
        for evt in event.get():            
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
                    fromMenu=False
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
       
        distance+=1.5 #constantly adds 1.5 to the distance
       
        drawScene(player,blocks2,spikes2,action) #this adds our draw scene function with it's parameters
        hit(blocks2,spikes2,player,playerSkin,spikePic) #this adds our hit function with it's parameters
        move(player,blocks2) #this adds our move funtion with it's parameters
       
        if distance>=6500: #when the distance it greater or equal to 5000 it will go to the win screen
            action=win("W")
       
        if escape: #if you press escape it will go to our pause screen and pause the game
            action=pause("pau",action)
        if pauseButton.collidepoint(mx,my): #chekcs if your mouse is over the pause button
            screen.blit(pauseButtonPicHover,pauseButton) #turns the pause button gray
            if click: #checks if you click
                fromMenu=True #turns the fromMenu to true
                action=pause("pau",action) #brings you to the pause screen
        else: #the original pause button
            screen.blit(pauseButtonPic,pauseButton)

        time.Clock().tick(220) #changes the speed
       
        display.flip()
   

def pause(action,lev):
    'this funnction is use to pause the game'
   
    screen.blit(menuBackground,(0,0)) #adds the background image
    screen.blit(paused,(110,200)) #adds the title image
   
    while action=="pau": #while the action equals to pause
       
        click=False
       
        escape=False
       
        for evt in event.get():
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        for b in range(3): #this is for the list of buttons
            if buttons[b].collidepoint(mx,my): #checks if your mouse is over the button
                screen.blit(pauseOptionsHover[b],buttons[b]) #turn the button gray
                if click: #check to see if you click the button
                    if b==0: #if you click the first button
                        global fromMenu #lets you use our menu variable
                        fromMenu=True #this sets fromMenu to true
                        return lev #returns you back to where you were
                    elif b==1: #brings you back to the menu
                        return menu("menu")
                    else: #this check if you opened the setting from the game so that if you go back it won't go back to the menu
                        global fromGame
                        fromGame=True
                        return settings("set",lev)
            else: #the original buttons for the pause screen
                screen.blit(pauseOptions[b],buttons[b])
       
        display.flip()

def win(action):
    'this function is used for when the player wins the game it will bring up the win screen'
    #sound for the win screen
    music("Sounds/SR_menu.mp3")
       
    screen.blit(menuBackground,(0,0)) #adds the background for the win screen
    screen.blit(winPic,(400,100)) #adds the title for the win screen
   
    while action=="W": #while the action equals w
       
        click=False
       
        escape=False
       
        for evt in event.get():
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        for w in range(2): #for the list of buttons
            if winOptions[w].collidepoint(mx,my):#checks if your mouse is over the button
                screen.blit(winOptionsPicsHover[w],winOptions[w])#turns the button gray
                if click: #checks if you left click
                    if w==0: #brings you to the menu
                        action=menu("menu")
                    else: #brings you back to the level screen
                        action=levels("levs")
            else: #the original button for the winOptions
                screen.blit(winOptionsPics[w],winOptions[w])
       
        display.flip()

def settings(action,lev):
    'this function is for when you open the setting menus'
   
    screen.blit(menuBackground,(0,0)) #adds the background

    global playerSkin #lets you use the playerSkin veriable
   
    global fromGame #lets you use the fromGame veriable
   
    while action=="set": #while the action equals set
       
        click=False
       
        escape=False
       
        for evt in event.get():
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        draw.rect(screen,BLACK,(200,100,800,600)) #draws a black rectangle
        screen.blit(changeIcon,(300,125)) #adds the different icons
       
        for s in range(3): #goes through each of the skins
            if playerSkin==playerSkins[s]: #this checks for which skin is selected
                draw.rect(screen,WHITE,(skins[s][0]-1,skins[s][1]-1,skins[s][2]+2,skins[s][3]+2),1) #adds a whilte ring around the selected skin
            if skins[s].collidepoint(mx,my): #this checks if you mouse is over one of the skins
                screen.blit(playerSkinsHover[s],skins[s]) #turns the button/skinn darker
                if click: #checks if you left click
                    playerSkin=playerSkins[s] #the playerSkin equals the skin you selected
            else: #original image for the skins
                screen.blit(playerSkins[s],skins[s])
       
        if escape:#checks for if you pressed escape
            if fromGame:#this check if you came for the game/pause menu
                return pause("pau",lev)#this is so you can go back the the pause menu/go back to the pause menu
            else:#else you came from the menu
                action=menu("menu")#returns you the the menu
        if back.collidepoint(mx,my):#checks for if your mouse is over the back button
            screen.blit(backPicHover,back) #turns it gray
            if click: #checks for if you left click
                if fromGame: #checks if you came from game/pause menu
                    return pause("pau",lev) #brings you back to the pause menu
                else: #this means you came from the main menu
                    action=menu("menu") #returns you to the menu
        else: #the original picture for the back button
            screen.blit(backPic,back)
       
        if instructionsButton.collidepoint(mx,my): #check if you're hovering the instruction button
            screen.blit(instructionsButtonPicHover,instructionsButton) #turns the button draker
            if click: #checks for if you left click
                return instructions("ins",lev) #brings you to the instruction screen
        else: #original picture for the instructionsButton
            screen.blit(instructionsButtonPic,instructionsButton)
       
        display.flip()

def instructions(action,lev):
    'function for the instructions'
    
    screen.blit(menuBackground,(0,0)) #displaying the background
    screen.blit(instructionsPic,(37.5,50)) #displaying the image for the instructions
   
    while action=="ins": #while action equals ins
       
        click=False
       
        escape=False
       
        for evt in event.get():            
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
       
        if escape: #checks for if you pressed escape
            return settings("set",lev) #going back to settings
        if back.collidepoint(mx,my): #if the mouse if hovering over the back button
            screen.blit(backPicHover,back) #turns the button gray when over it
            if click: #checks for if you left click
                return settings("set",lev) #going back to settings
        else: #if the mouse isn't hovered over the back button
            screen.blit(backPic,back) #displayying the normal back button
       
        display.flip()

def credits(action):
    'function for the credits'
    
    screen.blit(menuBackground,(0,0)) #displaying the background
    draw.rect(screen,BLACK,(0,650,1200,150)) #drawing the floor
    screen.blit(creditsPic,(100,400)) #displaying the picture for the credits
    screen.blit(playerSkins[0],(200,350)) #displaying the first skin
    screen.blit(playerSkins[1],(800,300)) #displaying the second skin
    screen.blit(playerSkins[2],(1100,600)) #displaying the third skin
   
    while action=="cr": #while action equals cr
       
        click=False
       
        escape=False
       
        for evt in event.get():            
            if evt.type==QUIT:
                return "end"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    click=True
            if evt.type==KEYDOWN:
                if evt.key==K_ESCAPE:
                    escape=True
       
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
       
        if escape: #checks for if you pressed escape
            action=menu("menu") #going back to the main menu
        if back.collidepoint(mx,my): #checking if the mouse is hovering over the back button
            screen.blit(backPicHover,back) #turns the button gray when over it
            if click: #checks for if you left click
                action=menu("menu") #going back to the main menu
        else: #this means the mouse isn't hovering over the back button
            screen.blit(backPic,back) #displaying the original back button
       
        display.flip()

#MAIN PROGRAM
#this is to load all the images
#the convert_alpha() turns the image to the same pixel format as the one the screen uses
title=image.load("Images/title.png")
menuBackground=image.load("Images/menuBackground.png")
backPic=image.load("Images/back.png")
backPicHover=image.load("Images/backHover.png")
levelSelect=image.load("Images/levelSelect.png")
spikePic=image.load("Images/redTri.png").convert_alpha()
pauseButtonPic=image.load("Images/pauseButton.png")
pauseButtonPicHover=image.load("Images/pauseButtonHover.png")
paused=image.load("Images/paused.png")
winPic=image.load("Images/win.png")
changeIcon=image.load("Images/changeIcon.png")
instructionsButtonPic=image.load("Images/instructionsButton.png")
instructionsButtonPicHover=image.load("Images/instructionsButtonHover.png")
instructionsPic=image.load("Images/instructions.png")
creditsPic=image.load("Images/credits.png")

#these are all the lists for the button placements and lists for pictures
buttons=[Rect(220+x*260,600,240,75) for x in range(3)]
menuOptions=[image.load("Images/levels.png"),image.load("Images/settings.png"),image.load("Images/creditsButton.png")]
menuOptionsHover=[image.load("Images/levelsHover.png"),image.load("Images/settingsHover.png"),image.load("Images/creditsButtonHover.png")]
back=Rect(25,25,150,37)
levelOptions=[Rect(220+x*520,500,240,75) for x in range(2)]
levelOptionsPics=[image.load("Images/level1.png"),image.load("Images/level2.png")]
levelOptionsPicsHover=[image.load("Images/level1Hover.png"),image.load("Images/level2Hover.png")]
pauseButton=Rect(10,10,75,75)
pauseOptions=[image.load("Images/resume.png"),image.load("Images/menu.png"),image.load("Images/settings.png")]
pauseOptionsHover=[image.load("Images/resumeHover.png"),image.load("Images/menuHover.png"),image.load("Images/settingsHover.png")]
winOptions=[Rect(220+x*520,500,240,75) for x in range(2)]
winOptionsPics=[image.load("Images/menu.png"),image.load("Images/levels.png")]
winOptionsPicsHover=[image.load("Images/menuHover.png"),image.load("Images/levelsHover.png")]
instructionsButton=Rect(400,600,400,61)
skins=[Rect(475+x*100,250,50,50) for x in range(3)]
playerSkins=[image.load("Images/playerSkin1.png").convert_alpha(),image.load("Images/playerSkin2.png").convert_alpha(),image.load("Images/playerSkin3.png").convert_alpha()]
playerSkinsHover=[image.load("Images/playerSkin1Hover.png"),image.load("Images/playerSkin2Hover.png"),image.load("Images/playerSkin3Hover.png")]

global playerSkin #variable for the player's skin
playerSkin=playerSkins[0] #starting skin
player=Rect(100,600,50,50) #rect for the player's position


#these blocks and spikes are the (x,y) location and size of the blocks and spikes for the levels
blocks1=[Rect(500,600,50,50),Rect(600,550,50,100),Rect(700,500,50,150),Rect(900,550,50,100),Rect(1600,600,50,50),Rect(1700,550,600,100)
        ,Rect(2500,600,50,50),Rect(2600,550,50,100),Rect(2700,500,100,150),Rect(3400,550,50,100),Rect(3500,500,50,150),Rect(3650,450,700,200)
        ,Rect(4450,500,50,150),Rect(4550,550,50,100),Rect(4650,600,50,50)]
spikes1=[Rect(750,600,50,50),Rect(800,600,50,50),Rect(850,600,50,50),Rect(1200,600,50,50),Rect(2800,600,50,50),Rect(2850,600,50,50),Rect(2900,600,50,50)
        ,Rect(3850,400,50,50),Rect(4000,400,50,50),Rect(4150,400,50,50),Rect(4350,600,50,50),Rect(4400,600,50,50),Rect(4500,600,50,50),Rect(4600,600,50,50)
        ,Rect(4700,600,50,50),Rect(4750,600,50,50)]

blocks2=[Rect(500,600,50,50),Rect(650,600,50,50),Rect(800,550,50,100),Rect(900,500,50,150),Rect(1000,600,50,50),Rect(1100,500,50,150),Rect(1200,600,50,50)
        ,Rect(1300,500,50,150),Rect(1400,600,50,50),Rect(1500,500,50,150),Rect(1600,450,700,200),Rect(2800,550,100,100),Rect(3000,600,50,50),Rect(3150,600,50,50)
        ,Rect(3250,500,50,150),Rect(3350,600,50,50),Rect(3450,500,50,150),Rect(3550,600,50,50),Rect(3650,500,50,150),Rect(3750,600,50,50),Rect(3850,500,50,150)
        ,Rect(3950,450,1000,200),Rect(4250,400,50,50),Rect(4400,400,50,50),Rect(4550,400,50,50),Rect(4700,400,50,50),Rect(4850,400,50,50),Rect(5500,600,50,50)
        ,Rect(5600,550,50,100),Rect(5700,500,50,150),Rect(5800,450,50,200),Rect(5900,500,50,150),Rect(5800,550,50,100),Rect(5900,600,50,50),Rect(6050,600,50,50)]
spikes2=[Rect(550,600,50,50),Rect(600,600,50,50),Rect(700,600,50,50),Rect(750,600,50,50),Rect(2300,600,50,50),Rect(2350,600,50,50),Rect(2400,600,50,50)
        ,Rect(2450,600,50,50),Rect(1700,400,50,50),Rect(1850,400,50,50),Rect(2000,400,50,50),Rect(2150,400,50,50),Rect(2900,600,50,50),Rect(2950,600,50,50),Rect(3050,600,50,50),Rect(3100,600,50,50)
        ,Rect(3200,600,50,50),Rect(4200,400,50,50),Rect(4300,400,50,50),Rect(4350,400,50,50),Rect(4450,400,50,50),Rect(4500,400,50,50),Rect(4600,400,50,50),Rect(4650,400,50,50),Rect(4750,400,50,50)
        ,Rect(4800,400,50,50),Rect(4950,600,50,50),Rect(5000,600,50,50),Rect(5050,600,50,50),Rect(5950,600,50,50),Rect(6000,600,50,50)]

menu("menu") #calling menu
quit()
