import pygame
import random
import time
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
    def get(self):
        return [self.x, self.y]
    def dot(self, other):
        return self.x * other.x + self.y * other.y
     

class Color:
    def __init__(self, r=0, g=0, b=0):
        self.rgb = [r,b,g]
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
    def __init__(self, posvec=None, velo=None, mass=1):
        self.posvec = posvec
        self.velo = velo 
        if posvec == None:
            self.posvec = Vector2( random.randint(10,  SCREEN_SIZE[0]-10), random.randint(10, SCREEN_SIZE[1]-10) )
        if velo == None:
            self.velo = Vector2(1, random.randint(-1, 1))
        self.mass = mass 
        self.color = Color()
        self.freez = False
        self.size = 10
        self.color.set(500)

    def update(self):
        newpos = self.posvec + self.velo
        if newpos.x > SCREEN_SIZE[0] - self.size or newpos.x < self.size:
            self.velo.x = -self.velo.x
        if newpos.y > SCREEN_SIZE[1] - self.size or newpos.y < self.size:
            self.velo.y = -self.velo.y
        if not self.freez:
            self.posvec = self.posvec + self.velo


def collition22(ball1, ball2):
    pos_dif = ball1.posvec - ball2.posvec
    velo_diff = ball1.velo - ball2.velo
    dist_sq = pos_dif.dot(pos_dif)
    factor = 2 * velo_diff.dot(pos_dif) / dist_sq
    ball1.velo = ball1.velo - pos_dif.scale((factor * ball2.mass) / (ball1.mass + ball2.mass))
    ball2.velo = ball2.velo + pos_dif.scale((factor * ball1.mass) / (ball1.mass + ball2.mass))

def reac(ball1, ball2):
    nv =  ball1.velo * (ball1.mass - ball2.mass) + ball2.velo  * ball2.mass * 2
    print(nv)
    return nv


def (ball1, ball2):
    m1 = ball1.mass
    m2 = ball2.mass
    v1 = ball1.velo
    v2 = ball2.velo

    v1_final = (m1 - m2) / (m1 + m2) * v1 + 2 * m2 / (m1 + m2) * v2
    v2_final = (m2 - m1) / (m1 + m2) * v2 + 2 * m1 / (m1 + m2) * v1

def collition(ball1, ball2):
def calculate_final_velocity(ball1, ball2):
    m1 = ball1.mass
    m2 = ball2.mass
    v1 = ball1.velo
    v2 = ball2.velo

    v1_final = (m1 - m2) / (m1 + m2) * v1 + 2 * m2 / (m1 + m2) * v2
    v2_final = (m2 - m1) / (m1 + m2) * v2 + 2 * m1 / (m1 + m2) * v1
    ball2.velo = v2

def drawball(ball):
    print(ball.posvec.get())
    pygame.draw.circle(screen , ball.color.get(), ball.posvec.get(), ball.size)



class Balls:
    def __init__(self):
        self.balls = []
        self.freez = False

    def update(self):
        self.checkcollition()
        for ball in self.balls:
            ball.update()
            drawball(ball)
        
    def newball(self):
        self.balls.append(Ball())

    def checkcollition(self):
        for i in range(len(self.balls) - 1):
            if (self.balls[i].posvec.x - self.balls[i+1].posvec.x) < 1 and (self.balls[i].posvec.y - self.balls[i+1].posvec.y) < 1:
                collition(self.balls[i], self.balls[i+1])

screen = pygame.display.set_mode(SCREEN_SIZE)
balls = Balls()
for i in range(10):
    balls.newball()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
    balls.update()
    pygame.display.flip()
    screen.fill(0)
    time.sleep(.01)
    
