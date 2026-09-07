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

emojis = [
    {'x': -5.0, 'y': 2.0, 'vx': 0.05, 'vy': 0.03, 'angle': 0.0, 'v_angle': 2.0, 'is_hurt': False, 'color': (1.0, 1.0, 0.0)},
    {'x': 5.0, 'y': -2.0, 'vx': -0.06, 'vy': 0.05, 'angle': 0.0, 'v_angle': -1.5, 'is_hurt': False, 'color': (0.0, 1.0, 1.0)}
]

def draw_emoji(is_hurt, color):
    glColor3f(color[0], color[1], color[2]) 
    glBegin(GL_POLYGON)
    for i in range(0, 365, 5):
        radian = math.radians(i)
        glVertex2f(RADIUS * math.cos(radian), RADIUS * math.sin(radian))
    glEnd()

    glColor3f(0.0, 0.0, 0.0) 
    glLineWidth(3.0)
    glBegin(GL_LINES)
    
    if not is_hurt:
        glVertex2f(-0.5, 0.5); glVertex2f(-0.5, 0.1)
        glVertex2f(0.5, 0.5); glVertex2f(0.5, 0.1)
        glVertex2f(-0.5, -0.5); glVertex2f(0.5, -0.5)
    else:
        glVertex2f(-0.7, 0.5); glVertex2f(-0.3, 0.3)
        glVertex2f(-0.3, 0.3); glVertex2f(-0.7, 0.1)
        glVertex2f(0.7, 0.5); glVertex2f(0.3, 0.3)
        glVertex2f(0.3, 0.3); glVertex2f(0.7, 0.1)
        glVertex2f(-0.6, -0.4); glVertex2f(-0.2, -0.6)
        glVertex2f(-0.2, -0.6); glVertex2f(0.2, -0.4)
        glVertex2f(0.2, -0.4); glVertex2f(0.6, -0.6)
        
    glEnd()

def update_physics(value):
    for e in emojis:
        e['x'] += e['vx']
        e['y'] += e['vy']
        e['angle'] += e['v_angle']

        if e['x'] + RADIUS >= orthoRight:
            e['x'] = orthoRight - RADIUS
            e['vx'] = -e['vx']
        elif e['x'] - RADIUS <= orthoLeft:
            e['x'] = orthoLeft + RADIUS
            e['vx'] = -e['vx']

        if e['y'] + RADIUS >= orthoTop:
            e['y'] = orthoTop - RADIUS
            e['vy'] = -e['vy']
        elif e['y'] - RADIUS <= orthoBottom:
            e['y'] = orthoBottom + RADIUS
            e['vy'] = -e['vy']

    dx = emojis[0]['x'] - emojis[1]['x']
    dy = emojis[0]['y'] - emojis[1]['y']
    distance = math.sqrt(dx**2 + dy**2)
    
    min_distance = 2 * RADIUS 
    
    if distance <= min_distance:
        emojis[0]['is_hurt'] = True
        emojis[1]['is_hurt'] = True
        
        if distance == 0: distance = 0.01 
        
        overlap = min_distance - distance
        nx, ny = dx / distance, dy / distance 
        
        emojis[0]['x'] += (overlap / 2) * nx
        emojis[0]['y'] += (overlap / 2) * ny
        emojis[1]['x'] -= (overlap / 2) * nx
        emojis[1]['y'] -= (overlap / 2) * ny
        
        dvx = emojis[0]['vx'] - emojis[1]['vx']
        dvy = emojis[0]['vy'] - emojis[1]['vy']
        vel_along_normal = (dvx * nx) + (dvy * ny)
        
        if vel_along_normal < 0:
            speed0 = math.sqrt(emojis[0]['vx']**2 + emojis[0]['vy']**2)
            speed1 = math.sqrt(emojis[1]['vx']**2 + emojis[1]['vy']**2)

            emojis[0]['vx'] -= vel_along_normal * nx
            emojis[0]['vy'] -= vel_along_normal * ny
            emojis[1]['vx'] += vel_along_normal * nx
            emojis[1]['vy'] += vel_along_normal * ny
            
            new_speed0 = math.sqrt(emojis[0]['vx']**2 + emojis[0]['vy']**2)
            new_speed1 = math.sqrt(emojis[1]['vx']**2 + emojis[1]['vy']**2)
            
            if new_speed0 > 0:
                emojis[0]['vx'] = (emojis[0]['vx'] / new_speed0) * speed0
                emojis[0]['vy'] = (emojis[0]['vy'] / new_speed0) * speed0
                
            if new_speed1 > 0:
                emojis[1]['vx'] = (emojis[1]['vx'] / new_speed1) * speed1
                emojis[1]['vy'] = (emojis[1]['vy'] / new_speed1) * speed1
            
    elif distance > min_distance + 1.5:
        emojis[0]['is_hurt'] = False
        emojis[1]['is_hurt'] = False

    glutPostRedisplay()
    glutTimerFunc(16, update_physics, 0)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    
    for e in emojis:
        glPushMatrix()
        glTranslatef(e['x'], e['y'], 0.0)
        glRotatef(e['angle'], 0.0, 0.0, 1.0)
        draw_emoji(e['is_hurt'], e['color']) 
        glPopMatrix()
        
    glutSwapBuffers()

def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(orthoLeft, orthoRight, orthoBottom, orthoTop)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Bouncing Emojis (Constant Speed)")

    init_gl()
    glutDisplayFunc(render)
    glutTimerFunc(0, update_physics, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()