import glfw
from OpenGL.GL import *
from math import cos, sin, sqrt, pi

alpha = 0.1
speed = 0.15
fill = True

class Dot:
    x, y, z = 0.0, 0.0, 0.0
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def rotate_dot(self, phi, z):
        x_new = cos(phi)*self.x - sin(phi)*self.y
        y_new = sin(phi)*self.x + cos(phi)*self.y
        z_new = self.z + z
        return Dot(x_new, y_new, z_new)

class Square:
    dots = []
    def __init__(self, dots):
        self.dots = dots

    def draw_square(self):
        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 1.0)
        for i in range(len(self.dots)):
            glVertex3f(self.dots[i].x, self.dots[i].y, self.dots[i].z)
        glEnd()

    def rotate_square(self, phi, z):
        rotated_dots = []
        for j in range(4):
            rotated_dots.append(self.dots[j].rotate_dot(phi, z))

        return Square(rotated_dots)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab 3", None, None)
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
    glMultMatrixf([
        cos(alpha), sin(alpha), 0, 0,
        -sin(alpha), cos(alpha), 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1,
    ])

def cube_redraw(current_square, next_square):
    # левая
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    for j in range(2):
        glVertex3f(current_square.dots[j].x, current_square.dots[j].y, current_square.dots[j].z)
    for j in reversed(range(2)):
        glVertex3f(next_square.dots[j].x, next_square.dots[j].y, next_square.dots[j].z)
    glEnd()

    # правая
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 0.0)
    for j in range(2, 4):
        glVertex3f(current_square.dots[j].x, current_square.dots[j].y, current_square.dots[j].z)
    for j in reversed(range(2, 4)):
        glVertex3f(next_square.dots[j].x, next_square.dots[j].y, next_square.dots[j].z)
    glEnd()

    # передняя
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.0, 0.4)
    for j in range(0, 4, 3):
        glVertex3f(current_square.dots[j].x, current_square.dots[j].y, current_square.dots[j].z)
    for j in reversed(range(0, 4, 3)):
        glVertex3f(next_square.dots[j].x, next_square.dots[j].y, next_square.dots[j].z)
    glEnd()

    # задняя
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.4, 0.4)
    for j in range(1, 3):
        glVertex3f(current_square.dots[j].x, current_square.dots[j].y, current_square.dots[j].z)
    for j in reversed(range(1, 3)):
        glVertex3f(next_square.dots[j].x, next_square.dots[j].y, next_square.dots[j].z)
    glEnd()

def display(window):
    global alpha
    global speed

    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)

    rotate(sqrt(2)/2 + alpha)

    current_square = Square([
        Dot(-0.15, -0.15, -0.4),
        Dot(-0.15, 0.15, -0.4),
        Dot(0.15, 0.15, -0.4),
        Dot(0.15, -0.15, -0.4),
    ])

    current_square.draw_square()

    n = 100
    for i in range(1, n+1):
        next_square = current_square.rotate_square(i*pi/(n*n), 0.8/n)
        next_square.draw_square()
        cube_redraw(current_square, next_square)
        current_square = next_square

    glLoadIdentity()

    alpha += speed / 16

    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global alpha
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_F:
            global speed
            if speed > 0:
                speed = 0
            else:
                speed = 0.15
        elif key == glfw.KEY_E:
            global fill
            fill = not fill
            if fill:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

if __name__ == "__main__":
    main()
