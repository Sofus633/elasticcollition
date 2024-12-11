import pygame
import random
import time
import math
SCREEN_SIZE = [1000, 800]
running = True

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    def __add__(self, other):
        if type(other) == list or type(other) == tuple:
            return [self.x + other[0], self.y + other[1]]
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    def get(self):
        return [self.x, self.y]
    def dot(self, other):
        return self.x * other.x + self.y * other.y
     
G = Vector2(0, 9.81/10)

class Color:
    def __init__(self, r=0, g=0, b=0):
        self.rgb = [r + random.randint(0, 255),b+ random.randint(0, 255),g+ random.randint(0, 255)]
    def get(self):
        return self.rgb
    def add(self, number):
        for i in range(len(self.rgb)):
            if number > 0:
                if self.rgb[i] < 255:
                    if self.rgb[i] + number <= 255:
                        self.rgb[i] += number
                        number = 0
                    else:
                        number -= 255 - self.rgb[i]
                        self.rgb[i] += 255 - self.rgb[i]
    def set(self, number):
        self.rgb = [0, 0, 0]
        self.add(number)


class Ball:
    def __init__(self,num, posvec=None, velo=None, mass=1):
        self.posvec = posvec
        self.velo = velo 
        self.forces = [G]
        self.num = num
        if posvec == None:
            self.posvec = Vector2( random.randint(10,  SCREEN_SIZE[0]-10), random.randint(10, SCREEN_SIZE[1]-10) )
        if velo == None:
            self.velo = Vector2(1, random.randint(-1, 1))
        self.mass = mass 
        self.color = Color()
        self.freez = False
        self.size = 10

    def update(self):
        self.color.set(math.sqrt(self.velo.x**2 + self.velo.y**2) * 100)
        for force in self.forces:
            self.velo += force

        newpos = self.posvec + self.velo
        if newpos.x > SCREEN_SIZE[0] - self.size or newpos.x < self.size:
            self.velo.x = -self.velo.x * .8
        if newpos.y > SCREEN_SIZE[1] - self.size or newpos.y < self.size:
            self.velo.y = -self.velo.y * .8

        if not self.freez:
            self.posvec = self.posvec + self.velo




def display_inf(balls):
    print('\033[F\033[K' * (len(balls) + 1), end='')
    a = ""
    for ball in balls:
        a += f"{ball.num}, pos:{ball.posvec} velo:{ball.velo} \n"
    print(a)



def collition(ball1, ball2):
    m1 = ball1.mass
    m2 = ball2.mass
    v1 = ball1.velo
    v2 = ball2.velo
    
    v1_final = v1 * (m1 - m2) / (m1 + m2) +  v2 * 2 * m2 / (m1 + m2) 
    v2_final = v2 * (m2 - m1) / (m1 + m2) + v1 * 2 * m1 / (m1 + m2) 

    
    min_distance = (ball1.size / 2) + (ball2.size / 2)
    dx, dy = ball1.posvec.x- ball2.posvec.x, ball1.posvec.y - ball2.posvec.y
    angle = math.atan2(dy, dx)
    distance = math.sqrt(dx**2 + dy**2)
    print(distance , min_distance)

    overlap = min_distance - distance + 10
    if distance == 0:  
        distance = 0.01
    dx /= distance
    dy /= distance

    ball1.posvec += Vector2(dx * overlap / 2, dy * overlap / 2)
    ball2.posvec -= Vector2(dx * overlap / 2, dy * overlap / 2)
    print('aoerifuy oaizuyhgrpiuzehpfgiumhzMI')
        

    
    
    ball2.velo = v2_final
    ball1.velo = v1_final
    
    

    
def drawball(ball):
    pygame.draw.circle(screen , ball.color.get(), ball.posvec.get(), ball.size)



class Balls:
    def __init__(self):
        self.balls = []
        self.freez = False

    def update(self):
        if self.freez == False:
            self.checkcollition()
        for ball in self.balls:
            if self.freez == False:
                ball.update()
            drawball(ball)
        
    def newball(self, num):
        self.balls.append(Ball(num, velo=Vector2(random.randint(-5, 5), random.randint(-5, 5))))

    def createball(self, num , pos=Vector2(), velo=Vector2(), mass=1):
        self.balls.append(Ball(num, pos, velo, mass))
    
    def checkcollition(self):
        for i in range(len(self.balls)):
            for y in range(i+1, len(self.balls)):
                distance = math.sqrt(
                    (self.balls[i].posvec.x - self.balls[y].posvec.x)**2 +
                    (self.balls[i].posvec.y - self.balls[y].posvec.y)**2
                )
                if distance < self.balls[i].size +  self.balls[y].size:
                    collition(self.balls[i], self.balls[y])
    
    def tellwitchball(self, pos):
        for i in range(len(self.balls)):
            distance = math.sqrt(
                (self.balls[i].posvec.x - pos[0])**2 +
                (self.balls[i].posvec.y - pos[1])**2
            )
            if distance < self.balls[i].size:
                ball = self.balls[i]
                print(f"{ball.num}, {ball.velo}, {ball.posvec}")
                time.sleep(1)

screen = pygame.display.set_mode(SCREEN_SIZE)

balls = Balls()
for i in range(200):
    balls.newball(i)
timer = 0
clock = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and clock < timer:
        balls.freez = True if  balls.freez == False else False
        clock = timer + 100
    
    if True in pygame.mouse.get_pressed() and clock < timer:
        
        mousepos = pygame.mouse.get_pos()
        balls.tellwitchball(pygame.mouse.get_pos())
        
        
        #balls.createball(10, Vector2(mousepos[0], mousepos[1]))
        #clock = timer + 10
    
    balls.update()
    #display_inf(balls.balls)
    pygame.display.flip()
    screen.fill((200, 200, 200))
    time.sleep(.001)
    timer+=1