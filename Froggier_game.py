from turtle import Turtle, Screen
import random
import time
import pygame

pygame.init()
pygame.mixer.init()

music = pygame.mixer.music.load('Music/bg_music_ambient_sounds.mp3')
thump = pygame.mixer.Sound("Music/thump.mp3") 
ribbit = pygame.mixer.Sound("Music/ribbit.mp3")
crunch = pygame.mixer.Sound("Music/crunch.mp3")
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(-1)

# thump.play(), ribbit.play(), crunch.play()

# Import image library, preload all images
import img_assets


screen = Screen()
screen.colormode(255)
screen.title("Froggy Frogs")
screen.bgpic("background.gif")
screen.bgcolor(255,255,255)
screen.screensize(600,600)
screen.tracer(0)

# Container for lists of objects to keep garbage collection happy
class Data_container():
    def __init__(self):
        self.obj_list = []
        
class Writer(Turtle):
    def __init__(self):
        super().__init__(shape='circle', visible=False)
        self.ht()
        self.pu()
        self.goto(275,275)
        self.style = ('Arial', 8, 'normal')
        self.score = 0
        
class Fly(Turtle):
    def __init__(self):
        super().__init__(shape="Assets/fly/tile005.gif", visible=True)
        self.pu()
        self.goto(random.randrange(-250,250),300)
        self.gravity = random.uniform(1,5)
        self.vel_count = 0
        self.flip = False
        self.count = 0
        self.collision = True
    def move(self):
        if not self.flip:
            self.vel_count += .5
            if self.vel_count > random.randrange(1,3,1):
                self.flip = True
        if self.flip:
            self.vel_count -= .5
            if self.vel_count < random.randrange(1,3,1)*-1:
                self.flip = False
        if self.ycor() > 300:
            self.ht()
            self.goto(-300,-300)
            self.st()
        if self.count > 3:
            self.count = 0
        self.shape(img_assets.fly_img_list[self.count])
        self.goto(self.xcor()+self.vel_count,self.ycor() - self.gravity)
        self.count += 1
        if self.ycor() < -300:
            self.ht()
            self.collision = False
            self.goto(random.randrange(-250,250),300)
            self.collision = True
            self.st()
            
        screen.ontimer(self.move, 150)        

class Frog(Turtle):
    def __init__(self):
        super().__init__(shape='circle', visible=True)
        self.pu()
        self.st()
        self.hop_count = 0
        self.jump = False
        self.steps = 6
        self.shape("Assets/frog/back_sit_1.gif")
        self.goto(0,-225)
        self.direction = "back_sit"
        self.ribbit_counter = 0

    def frog_up(self):
        if self.hop_count > 2:
            self.hop_count = 0    
        self.shape(img_assets.frog_back_sit_list[self.hop_count])
        self.hop_count += 1
        if self.hop_count == 2:
            self.direction = "back_sit"
            self.hop_count = 0


            
    def frog_down(self):
        if self.hop_count > 2:
            self.hop_count = 0
        self.ribbit_counter += 1
        if self.ribbit_counter >= 6:
            ribbit.play()
            self.ribbit_counter = 0
        self.shape(img_assets.frog_front_face_list[self.hop_count])
        self.hop_count += 1
        if self.hop_count == 2:
            self.direction = "face_sit"
            self.hop_count = 0

        
    def frog_left(self):
        if self.hop_count > 2:
            self.hop_count = 0
        if self.hop_count == 0:
            thump.play()
        self.shape(img_assets.frog_left_hop_list[self.hop_count])
        if self.xcor() > -265:
            self.goto(self.xcor()-self.steps,self.ycor())
        self.hop_count += 1

        
    def frog_right(self):
        if self.hop_count > 2:
            self.hop_count = 0
        if self.hop_count == 0:
            thump.play()
        self.shape(img_assets.frog_right_hop_list[self.hop_count])
        if self.xcor() < 265:
            self.goto(self.xcor()+self.steps,self.ycor())
        self.hop_count += 1

        
    def frog_jump(self):
        if self.jump:
            if self.hop_count > 2:
                self.hop_count = 0
            if self.direction == "face_jump":
                self.shape(img_assets.frog_front_hop_list[self.hop_count])
            else:
                self.shape(img_assets.frog_back_hop_list[self.hop_count])
            self.hop_count += 1
            if self.hop_count == 2:
                self.direction = "back_sit"
                self.hop_count = 0
        self.jump = False

        
    def move_frog(self):
        if self.direction == "back_sit": #Up
            self.frog_up()
        elif self.direction == "face_sit": # Down
            self.frog_down()
        elif self.direction == "left": # Left
            self.frog_left()
        elif self.direction == "right": # Right
            self.frog_right()
        elif self.direction == "face_jump":
            self.jump = True
            self.frog_jump()
        elif self.direction == "back_jump":
            self.jump = True
            self.frog_jump()
            
        screen.update()
        screen.ontimer(self.move_frog, 200)
        
container = Data_container()
writer = Writer()
writer.write(writer.score, move=False, align='left', font=writer.style)
for i in range(25):
    container.obj_list.append(Fly())
    
for fly in container.obj_list:
    fly.move()
        
frog = Frog()
frog.move_frog()
def check_collisions():
    for fly in container.obj_list:
        if frog.distance(fly) < 25:
            crunch.play()
            writer.score += 1
            writer.clear()
            writer.write(writer.score, move=False, align='left', font=writer.style)
            fly.ht()
            fly.gravity += 1
            frog.steps += .5
            fly.collision = False
            fly.goto(random.randrange(-250,250),300)
            fly.collision = True
            fly.st()
    screen.update()
    screen.ontimer(check_collisions,25)

check_collisions()    
def player_up():
    frog.direction = "back_sit"
def player_down():
    frog.direction = "face_sit"
def player_right():
    frog.direction = "right"
def player_left():
    frog.direction = "left"
def player_jump():
    if frog.direction == "face_sit":
        frog.direction = "face_jump"
    else:
        frog.direction = "back_jump"

screen.onkey(player_up, "Up")
screen.onkey(player_down, "Down")
screen.onkey(player_right, "Right")
screen.onkey(player_left, "Left")
screen.onkey(player_jump, "space")

screen.listen()

screen.mainloop()
        
