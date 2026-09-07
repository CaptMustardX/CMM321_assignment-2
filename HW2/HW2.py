from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

PI = 3.14159265
RADIUS = 1.5
orthoLeft = -10.0
orthoRight = 10.0
orthoBottom = -7.5
orthoTop = 7.5
posX = 0.0
posY = 0.0
speedX = 0.05
speedY = 0.04
angle = 0.0
speedAngle = 2.0 

def draw_emoji(x, y, radius):
    glColor3f(1.0, 1.0, 0.0) 
    glBegin(GL_POLYGON)
    for i in range(0, 365, 5):
        radian = math.radians(i)
        vx = x + (radius * math.cos(radian))
        vy = y + (radius * math.sin(radian))
        glVertex2f(vx, vy)
    glEnd()

    glColor3f(0.0, 0.0, 0.0) # สีดำ
    glLineWidth(3.0)
    
    glBegin(GL_LINES)
    glVertex2f(x - 0.5, y + 0.5)
    glVertex2f(x - 0.5, y + 0.1)
    
    glVertex2f(x + 0.5, y + 0.5)
    glVertex2f(x + 0.5, y + 0.1)

    glVertex2f(x - 0.5, y - 0.5)
    glVertex2f(x + 0.5, y - 0.5)
    glEnd()

def update_physics(value):
    global posX, posY, speedX, speedY, angle, speedAngle

    posX += speedX
    posY += speedY
    
    angle += speedAngle
    if angle >= 360.0:
        angle -= 360.0

    if posX + RADIUS >= orthoRight or posX - RADIUS <= orthoLeft:
        speedX = -speedX
    
    if posY + RADIUS >= orthoTop or posY - RADIUS <= orthoBottom:
        speedY = -speedY

    glutPostRedisplay()
    
    glutTimerFunc(16, update_physics, 0)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glPushMatrix() 
    
    glTranslatef(posX, posY, 0.0)
    
    glRotatef(angle, 0.0, 0.0, 1.0)
    
    draw_emoji(0.0, 0.0, RADIUS)
    
    glPopMatrix()
    
    glutSwapBuffers()

def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(orthoLeft, orthoRight, orthoBottom, orthoTop) # ตั้งค่ามุมมอง 2 มิติ
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600) 
    glutCreateWindow(b"Bouncing and Rotating Emoji")

    init_gl()
    glutDisplayFunc(render)
    glutTimerFunc(0, update_physics, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()