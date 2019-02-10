import pygame
import math
import time

pygame.init()

#window dimensions
display_width = 1000
display_height = 600

#colors used
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
light_green = (0,200,0)
light_blue = (0,0,200)
white = (255,255,255)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Obstacle Avoiding')
clock = pygame.time.Clock()
mouse = pygame.image.load('mouse.png') #picture of a mouse for the instructions page

start = [0,0] #default start position of the bot
end = [1000,600] #default destination of the bot
robotcoords = [0,0] #current coordinates of the bot
obst = [] #list containing all the obstacles drawn by the user
steps = [] #list having all the steps taken by the bot

class sensor:
    
    def __init__(self,start,ang,senscoords,end,obst):
        self.start = start
        self.ang = ang
        self.senscoords = senscoords
        self.end = end
        self.obst = obst
        self.obst_range = []
        #Making a new list containing all obstacles within a certain range of the bot 
        for i in self.obst:
            if ((i[0]-self.start[0])**2 + (i[1]-self.start[1])**2)**0.5 <=75:
                self.obst_range.append(i)
           
    def printer(self):
        pygame.draw.line(screen,red,(self.start[0],self.start[1]), (self.end[0],self.end[1]))
        
#There are 3 types of sensors-
#Primary -10 units long (7) ; Secondary - 8 units long (2) ; Tertiary - 5 units long (4)
#This was done as the bot was over-correcting (when all the sensors were 10 units long) its path
#when it was almost past the obstacle as the trailing edge sensors were being triggered. 

    def retvalues_prim(self):
        ret_list = []
        if not self.obst_range:
            return 10
        else:
            for j in self.obst_range:
                ret_amount = 10
                for i in self.senscoords:
                    a = abs(((i[0]-j[0])**2 + (i[1]-j[1])**2)**0.5)
                    if a<=20 :
                        ret_amount = self.senscoords.index(i)
                        break
                ret_list.append(ret_amount)
            return min(ret_list)

    def retvalues_sec(self):
        ret_list = []
        if not self.obst_range :
            return 8
        else:
            for j in self.obst_range:
                ret_amount = 8
                for i in self.senscoords:
                    a = abs(((i[0]-j[0])**2 + (i[1]-j[1])**2)**0.5)
                    if a <=18:
                        ret_amount = self.senscoords.index(i)
                        break
                ret_list.append(ret_amount)
            return min(ret_list)
        
    def retvalues_ter(self):
        ret_list = []
        if not self.obst_range :
            return 5
        else:
            for j in self.obst_range:
                ret_amount = 5
                for i in self.senscoords:
                    a = abs(((i[0]-j[0])**2 + (i[1]-j[1])**2)**0.5)
                    if a <=15:
                        ret_amount = self.senscoords.index(i)
                        break
                ret_list.append(ret_amount)
            return min(ret_list)

def set_direction(robotcoords,angh,obst,start,end):
    #Lists which contain the return values of the sensors of their respective category.
    retvalues_prim = []
    retvalues_sec = []
    retvalues_ter = []
    
    #List which contains the return values of all the sensors in the right order 
    retvalues_fin = [0]*13

    for a in range(angh-45,angh+46,15):
        senscoords = []
        for i in range (0,51,5):
            x = robotcoords[0]+math.cos(math.radians(a))*i
            y = robotcoords[1]+math.sin(math.radians(a))*i
            senscoords.append([x,y])
        end = [robotcoords[0]+math.cos(math.radians(a))*50,robotcoords[1]+math.sin(math.radians(a))*50]
        sens = sensor(robotcoords,a,senscoords,end,obst)
        sens.printer()
        retvalues_prim.append(sens.retvalues_prim())
        
    for a in [angh-60,angh+60]:
        senscoords = []
        for i in range (0,41,5):
            x = robotcoords[0]+math.cos(math.radians(a))*i
            y = robotcoords[1]+math.sin(math.radians(a))*i
            senscoords.append([x,y])
        end = [robotcoords[0]+math.cos(math.radians(a))*40,robotcoords[1]+math.sin(math.radians(a))*40]
        sens = sensor(robotcoords,a,senscoords,end,obst)
        sens.printer()
        retvalues_sec.append(sens.retvalues_sec())
        
    for a in [angh-90,angh-75,angh+75,angh+90]:
        senscoords = []
        for i in range (0,26,5):
            x = robotcoords[0]+math.cos(math.radians(a))*i
            y = robotcoords[1]+math.sin(math.radians(a))*i
            senscoords.append([x,y])
        end = [robotcoords[0]+math.cos(math.radians(a))*25,robotcoords[1]+math.sin(math.radians(a))*25]
        sens = sensor(robotcoords,a,senscoords,end,obst)
        sens.printer()
        retvalues_ter.append(sens.retvalues_ter())
        
    for i in range(0,2):
        retvalues_fin[i] = retvalues_ter[i]
        retvalues_fin[-(i+1)] = retvalues_ter[-(i+1)]

    retvalues_fin[2] = retvalues_sec[0]
    retvalues_fin[10] = retvalues_sec[1]
    
    for i in range(3,10):
        retvalues_fin[i] = retvalues_prim[i-3]
    
    pygame.display.update()
    return retvalues_fin,angh

def arena_setup(start,end,obst):
    steps = []
    while 1:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        pos = pygame.mouse.get_pos()
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

        if pressed1 == 1:
            obst.append((pos[0],pos[1]))
            
        if pressed2 == 1:
            start[0] = pos[0]
            start[1] = pos[1]
            
        if pressed3 == 1:
            end[0] = pos[0]
            end[1] = pos[1]

        obst = list(set(obst)) #should remove all the duplicate obst coords

        draw_dots(start,end,obst)

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                draw_robot(start,end,obst)

# Function to draw the start, end positions and the obstacles everytime the screen refreshes
def draw_dots(start,end,obst):
    pygame.draw.circle(screen, blue, (start[0],start[1]), 5)
    pygame.draw.circle(screen, green, (end[0],end[1]), 5)
    for i in obst:
        pygame.draw.circle(screen,black,(i[0],i[1]),20,2)
    pygame.display.update()

#Function to draw the steps taken by the robot
def draw_steps(steps):
    for i in steps:
        pygame.draw.circle(screen,light_green, (i[0],i[1]),1)
    pygame.display.update()
     
def draw_robot(start,end,obst):
    retvalues = [] #list which will contain the return values of all sensors
    angs = [] #list which will contain the angles of the sensors [-90,90]
    weighted = [] #list which will have the element by element product of angs and retvalues
    step = 0
    
    #Initializing the sensor values to an ideal case i.e. no obstacles in range  
    for i in range(0,13):
        weighted.append(0)
        angs.append(-90 + i*15)
        retvalues.append(10) #Primary Sensors
        
    for i in [2,10]:
        retvalues[i] = 8 #Secondary Sensors

    for i in [0,1,11,12]:
        retvalues[i] = 5 #Tertiary Sensors
    
    while 1:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if step == 0:
            robotcoords[0] = start[0]
            robotcoords[1] = start[1]
            step = 1
            
        draw_dots(start,end,obst)

        if ((end[0]-robotcoords[0])**2 + (end[1]-robotcoords[1])**2 )**0.5 >=10:
            #Variable to check if the bot is going head on towards an obstacle.
            #Weighted sum method would not work in a head on collision case 
            headon = True 
            retvalues_sum = 0
            
            #Setting the right heading angle as arctan() returns a value b/w [-pi/2,pi/2]
            if end[0]<robotcoords[0]: 
                angth = int(math.degrees(math.atan((end[1]-robotcoords[1])/(end[0]-robotcoords[0])))) -180
            else:
                angth = int(math.degrees(math.atan((end[1]-robotcoords[1])/(end[0]-robotcoords[0]))))
            
            for i in range(0,len(retvalues)):
                retvalues_sum+=retvalues[i]
                if retvalues[i] != retvalues[-(i+1)]:
                    headon = False

            if retvalues_sum == 106: #106 is the maximum value of sum of the return values
                
                angh = angth
                retvalues,ango = set_direction(robotcoords,angh,obst,start,end)
                #set_direction returns the retvalues list and the angle(ango) at which the bot is currently pointing

            elif retvalues_sum !=106 and headon == True: 
                #If the bot is going headon towards an obstacle, it turns by 15 degrees and resumes its path
                angh = ango - 15
                retvalues,ango = set_direction(robotcoords,angh,obst,start,end)
                
            else:
                #initializing the angs list
                for i in range(0,len(retvalues)):
                    angs[i] = -90 + i*15

                for i in range(0,13):
                    weighted[i] = retvalues[i]*angs[i]

                weighted_sum = sum(weighted)
                ratio = weighted_sum/retvalues_sum #weighted average to find the new angle of heading

                #scaling the ratio
                if abs(ratio)<1:
                    ratio *= 3
                else :
                    ratio*= 1.5
                
                angh = ango+int(ratio) #angh is the angle at which the bot should take its next step
                retvalues,ango = set_direction(robotcoords,angh,obst,start,end)

            #moving the robot in the required direction (5 units at a time)    
            robotcoords[0]+= math.cos(math.radians(angh))*5
            robotcoords[1]+= math.sin(math.radians(angh))*5
            
            #appending the old robot coordinates so as to draw the steps of the bot
            steps.append([int(robotcoords[0]),int(robotcoords[1])]) 
            draw_steps(steps)

        else:
            end_page(len(steps))
        
        time.sleep(0.1)
        pygame.display.update() 
        clock.tick(90)

def end_page(num_steps):
    while 1:
        screen.fill(white)
        font = pygame.font.Font('freesansbold.ttf',40)
        text1 = font.render("Would you like to have another go?", True, black)
        screen.blit(text1,(140,260))
        text2 = font.render("(Click Enter for Yes and Backspace for No)", True, black)
        screen.blit(text2,(100,300))
        text3 = font.render("Number of steps taken : "+str(num_steps), True, red)
        screen.blit(text3,(180,210))
        steps.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                instruct_page()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                pygame.quit()
                quit()
        pygame.display.update()
        
def instruct_page():
    while 1 :
        screen.fill(white)
        screen.blit(mouse, (0,100))
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render("INSTRUCTIONS " , True, black)
        screen.blit(text, (390,0))

        font = pygame.font.Font('freesansbold.ttf',15)
        text1 = font.render("-> USE LEFT CLICK TO DRAW OBSTACLES", True, black)
        screen.blit(text1 ,(200,200))
        text2 = font.render("-> USE RIGHT CLICK TO SET DESTINATION AND SCROLL WHEEL CLICK TO SET START LOCATION", True, black)
        screen.blit(text2 ,(200,225))
        text3 = font.render("(IF YOU DO NOT HAVE A MOUSE, FRET NOT. THE START AND DESTINATION IS PRESET TO THE CORNERS!)",True, black)
        screen.blit(text3 ,(200,250))
        text4 = font.render("->PLEASE DO NOT GO CRAZY WITH THE OBSTACLES. IT WILL MOST DEFINITELY SLOW DOWN...",True, black)
        screen.blit(text4 ,(200,275))
        text5 = font.render("->ONCE YOU HAVE SET UP THE ARENA, PRESS THE ENTER BUTTON TO START THE ROBOT", True, black)
        screen.blit(text5 ,(200,300))
        text6 = font.render("->PRESS ENTER TO BEGIN!", True, black)
        screen.blit(text6 ,(200,325))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                arena_setup(start,end,obst)
        
        pygame.display.update()
instruct_page()
pygame.quit()
quit()
