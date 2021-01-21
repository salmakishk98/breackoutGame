from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame import mixer

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init(44100)

checks = []
FROM_RIGHT = 2
FROM_LEFT = 3
FROM_TOP = 4
FROM_BOTTOM = 5

win_width = 600
win_height = 700

deltaX = 4
deltaY = 4
mouse_x = 0
time_interval = 1
clock = pygame.time.Clock()
fps = 20


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, win_width, 0, win_height, 0, 1)
    glMatrixMode(GL_MODELVIEW)


class rect:
    def __init__(self, left, bottom, right, top, state, color=-1,score=1):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.state = state
        self.score = score
        self.color = color


blocks = []
ball = rect(100, 120, 110, 130, 1)
wall = rect(0, 0, win_width, win_height, 1)
player = rect(0, 48, 60, 63, 1,10)
blue_bar = rect(0, 45, win_width, 60, 1,10)
blue_l = rect(0, 40, 10, 65, 1,10)
blue_r = rect(win_width - 10, 40, win_width, 65, 1,10)
color_list = [r1,r2,r3,r4] = [(1, 1,0),(0, 1, 0), (1, 0.7, 0),(0, 0, 1)]
score_list = [s1,s2,s3,s4]=[10,10,10,10]


def draw_rect(rect):
    if (rect.color == -1):
        glColor(1, 1, 1)
    elif (rect.color == 10):
        glColor(0, 0, 1)
    else:
        glColor(color_list[rect.color])
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex2d(rect.left, rect.bottom)
    glVertex2d(rect.right, rect.bottom)
    glVertex2d(rect.right, rect.top)
    glVertex2d(rect.left, rect.top)
    glEnd()


def draw_text(string, x, y):
    glLineWidth(3)
    glColor(1, 1, 1)
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(0.2, 0.2, 0.2)
    string = string.encode()
    for char in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, char)


def draw_frame():
    side_left = rect(0, 0, 10, win_height, 1)
    draw_rect(side_left)
    side_right = rect(win_width - 10, 0, win_width, win_height, 1)
    draw_rect(side_right)
    top = rect(0, win_height - 10, win_width, win_height, 1)
    top.color=3
    draw_rect(top)


def block_coll_ded(blocks, ball, deltay):
    global deltaX
    global deltaY
    global score
    if (not start):
        return
    for block in blocks:
        if block.state:
            if ((ball.left >= block.left and ball.left <= block.right) or (
                    ball.right >= block.left and ball.right <= block.right)) \
                    and ((ball.bottom >= block.bottom and ball.bottom <= block.top) or (
                    ball.top >= block.bottom and ball.top <= block.top)):
                block.state = 0
                score+=block.score

                if block.bottom >= ball.bottom and block.top >= ball.top:
                    deltaY = -4
                    bricks_hit = pygame.mixer.Sound('bricks.ogg')
                    bricks_hit.play()
                if block.bottom <= ball.bottom and block.top <= ball.top:
                    deltaY = 4
                    bricks_hit = pygame.mixer.Sound('bricks.ogg')
                    bricks_hit.play()
                if block.left >= ball.left and block.right >= ball.right:
                    deltaX = -4
                    bricks_hit = pygame.mixer.Sound('bricks.ogg')
                    bricks_hit.play()
                if block.left <= ball.left and block.right <= ball.right:
                    deltaX = 4
                    bricks_hit = pygame.mixer.Sound('bricks.ogg')
                    bricks_hit.play()


def creat_blocks(blocks):
    l = 0
    b = 390
    r = 41
    t = 403
    block = rect(l, b, r, t, 1)
    for i in range(10) :
        for k in range(4):
            block.left = l
            block.right = r
            for j in range(14):
                block1 = rect(block.left, block.bottom, block.right, block.top, 1)
                block1.score = score_list[k]
                blocks.append(block1)
                block.left += 43
                block.right += 43
            block.bottom += 15
            block.top += 15
        block.bottom+=46
        block.top+=46



def draw_blocks(blocks, ball):
    for block in blocks:
        if block.state:
            draw_rect(block)

def intial_blocks(blocks):
    global intite
    for block in blocks :
        block.state=1
        block.bottom+=(intite*15)
        block.top+=(intite*15)
def you_win (blocks):
    count=0
    for block in blocks:
        if block.state==1:
            count+=1
    return count
def Test_Ball_Wall(ball, wall):
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM

    if ball.right >= wall.right - 10:
        return FROM_RIGHT
    if ball.left <= wall.left + 10:
        return FROM_LEFT
    if ball.top >= wall.top - 10:
        return FROM_TOP
    if ball.bottom <= wall.bottom + 63:
        return FROM_BOTTOM
    player.left = mouse_x - 30
    player.right = mouse_x + 30

def Test_Ball_Player(ball, player):
    if ball.bottom <= player.top and ball.left >= player.left and ball.right <= player.right:
        return True
    return False


def keyboard(key, x, y):
    global start
    if key == b"s":
        start = True
    if key == b"q":
        sys.exit()


def MouseMotion(x, y):
    global mouse_x
    mouse_x = x


def Timer(v):
    draw()
    glutTimerFunc(time_interval, Timer, 1)

def move_blocks (blocks):
    global time
    global intite
    if time ==1000:
        intite+=1
        time =0
        for block in blocks:
            block.bottom-=15
            block.top-=15

def colorized_blocks(blocks):
    for block in blocks:
        if block.bottom >=390 and block.bottom<=465:
            block.color=0
        elif block.bottom >=465 and block.bottom<=540:
            block.color=1
        elif block.bottom >= 540 and block.bottom <= 615:
            block.color =2
        elif block.bottom >= 615 and block.bottom <= 690:
            block.color = 3
        else:
            block.color=-1
def color_frame ():
    left=rect(0,390,10,465,1,0)
    draw_rect(left)
    left1 = rect(0, 465, 10, 540, 1, 1)
    draw_rect(left1)
    left2 = rect(0, 540, 10, 615, 1, 2)
    draw_rect(left2)
    left3 = rect(0, 615, 10,  690,1, 3)
    draw_rect(left3)
    right0 = rect(win_width-10, 390, win_width, 465, 1, 0)
    draw_rect(right0)
    right1 = rect(win_width-10, 465, win_width, 540, 1, 1)
    draw_rect(right1)
    right2 = rect(win_width-10, 540, win_width, 615, 1, 2)
    draw_rect(right2)
    right3 = rect(win_width-10, 615, win_width, 690,1, 3)
    draw_rect(right3)
def colorized_ball(ball):
    if ball.bottom >= 390 and ball.bottom <= 465:
        ball.color = 0
    elif ball.bottom >= 465 and ball.bottom <= 540:
        ball.color = 1
    elif ball.bottom >= 540 and ball.bottom <= 615:
        ball.color = 2
    elif ball.bottom >= 615 and ball.bottom <= 690:
        ball.color = 3
    else:
        ball.color = -1




chances = 0
score = 000
global inite
intite=0
global time
time = 0
global start
start = False
again =False
your_score = 0
creat_blocks(blocks)



def draw():
    global chances
    global score
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM
    global deltaX
    global deltaY
    global start
    global blocks
    global time
    global intite
    global again
    global your_score
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glColor(1, 1, 1)
    block_coll_ded(blocks, ball, deltaY)
    draw_blocks(blocks, ball)
    colorized_blocks(blocks)
    draw_frame()
    color_frame()
    if start == False:
        score = 0
        draw_rect(blue_bar)
        wall.bottom = 0
        if Test_Ball_Wall(ball, wall) == FROM_BOTTOM:
            deltaY = 4
        if again:
            draw_text(" you con try again , your score =", 0, 280)
            draw_text(str(your_score), 500, 280)

        draw_text(" PRESS ' S ' TO START ", 0, 240)
        if ball.top == 390:
            deltaY = -4
    draw_rect(blue_l)
    draw_rect(blue_r)
    glColor(1, 1, 1)
    colorized_ball(ball)
    draw_rect(ball)
    glColor(1, 1, 1)
    string = "score:" +str(score)
    draw_text(string, 30, 10)
    string ="chances:" + str(chances)
    draw_text(string, 400, 10)
    glLoadIdentity()
    ball.left = ball.left + deltaX
    ball.right = ball.right + deltaX
    ball.top = ball.top + deltaY
    ball.bottom = ball.bottom + deltaY
    if Test_Ball_Wall(ball, wall) == FROM_RIGHT:
        deltaX = -4
    if Test_Ball_Wall(ball, wall) == FROM_LEFT:
        deltaX = 4
    if Test_Ball_Wall(ball, wall) == FROM_TOP:
        deltaY = -4
    if start:
        player.left = mouse_x - 30
        player.right = mouse_x + 30
        if Test_Ball_Player(ball, player):
            deltaY = 4
            bat_hit = pygame.mixer.Sound('bat.ogg')
            bat_hit.play()
        wall.bottom = -30
        if Test_Ball_Wall(ball, wall) == FROM_RIGHT:
           wall_hit = pygame.mixer.Sound('wall.ogg')
           wall_hit.play()
        if Test_Ball_Wall(ball, wall) == FROM_LEFT:
           wall_hit = pygame.mixer.Sound('wall.ogg')
           wall_hit.play()
        if Test_Ball_Wall(ball, wall) == FROM_TOP:
           wall_hit = pygame.mixer.Sound('wall.ogg')
           wall_hit.play()
        if Test_Ball_Wall(ball, wall) == FROM_BOTTOM:
            ball.left = 300
            ball.right = 310
            ball.bottom = 320
            ball.top = 330
            chances = chances + 1
            game_over = pygame.mixer.Sound('gameOver.ogg')
            game_over.play()
        if player.left < 0:
            player.left = 0
        if player.right > win_width:
            player.right = win_width
        draw_rect(player)
        time+=1
    count = you_win(blocks)
    if chances == 3 or count==0:
        again=True
        start = False
        your_score = score
        chances = 0
        intial_blocks(blocks)

    move_blocks(blocks)
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(600, 700)
glutInitWindowPosition(0, 0)
glutCreateWindow(b" BREAKOUT GAME ")
glutDisplayFunc(draw)
glutKeyboardFunc(keyboard)
glutTimerFunc(time_interval, Timer, 1)
glutPassiveMotionFunc(MouseMotion)
init()
glutMainLoop()