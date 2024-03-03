import glfw
from OpenGL.GL import *
from math import cos, sin, sqrt

alpha = 0.1
speed = 0.2
fill = True

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab 2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

def draw_dividing_lines():
    glLineWidth(4.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(0.0, 1.0)
    glVertex2f(0.0, -1.0)
    glEnd()

def cube(size):
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.4, 0.4)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size,  size, -size)
    glVertex3f(-size,  size,  size)
    glVertex3f(-size, -size,  size)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size,  size)
    glVertex3f(size,  size,  size)
    glVertex3f(size,  size, -size)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size,  size)
    glVertex3f(size, -size,  size)
    glVertex3f(size, -size, -size)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size,  size)
    glVertex3f(size, size,  size)
    glVertex3f(size, size, -size)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-size, -size, -size)
    glVertex3f( size, -size, -size)
    glVertex3f( size,  size, -size)
    glVertex3f(-size,  size, -size)
    glColor3f(0.6, 0.0, 0.0)
    glVertex3f(-size, -size,  size)
    glVertex3f(size, -size,  size)
    glVertex3f(size,  size,  size)
    glVertex3f(-size,  size,  size)
    glEnd()

def rotate(phi):
    glMultMatrixf([
        cos(phi), 0, -sin(phi), 0,
        0, 1, 0, 0,
        sin(phi), 0, cos(phi), 0,
        0, 0, 0, 1,
    ])
    glMultMatrixf([
        1, 0, 0, 0,
        0, cos(phi), sin(phi), 0,
        0, -sin(phi), cos(phi), 0,
        0, 0, 0, 1,
    ])

def shift(x, y, z):
    glMultMatrixf([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        x, y, z, 1
    ])

def display(window):
    global alpha
    global speed

    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    draw_dividing_lines()

    glMatrixMode(GL_PROJECTION)

    # start move for initial pos of cube
    shift(-0.5, 0.5, 0)
    rotate(sqrt(2)/2 + alpha)
    cube(0.15)
    glLoadIdentity()

    shift(0.5, 0.5, 0)
    # Проекция слева 
    glMultMatrixf([
        0, 0, -1, 0,
        0, 1, 0, 0,
        -1, 0, 0, 0,
        0, 0, 0, 1,
    ])
    rotate(sqrt(2)/2 + alpha)
    cube(0.15)
    glLoadIdentity()

    shift(0.5, -0.5, 0)
    # Проекция сзади
    glMultMatrixf([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, -1, 0,
        0, 0, 0, 1,
    ])
    rotate(sqrt(2)/2 + alpha)
    cube(0.15)
    glLoadIdentity()

    shift(-0.5, -0.5, 0)
    # Проекция сверху 
    glMultMatrixf([
        1, 0, 0, 0,
        0, 0, -1, 0,
        0, -1, 0, 0,
        0, 0, 0, 1,
    ])
    rotate(sqrt(2)/2 + alpha)
    cube(0.15)

    alpha += speed / 16

    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global alpha
    global speed
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_F:
            speed = 0
        elif key == glfw.KEY_Y:
            speed = 0.2
        elif key == glfw.KEY_E:
            global fill
            fill = not fill
            if fill:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

if __name__ == "__main__":
    main()
