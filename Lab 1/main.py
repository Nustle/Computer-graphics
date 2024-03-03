import glfw
from OpenGL.GL import *
from OpenGL.raw.GLUT import *

delta = 0.4 # скорость поворота
angle = 1.5 # текущий угол
posx = 0.0
posy = 0.0
size = 0.0

def display(window):
    global angle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
   
    glClearColor(0.1, 0.1, 0.1, 0.1)
    glPushMatrix()
    glRotatef(angle, 2, 1, 3)

    glBegin(GL_TRIANGLE_FAN)

    # Точки 6-угольника

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx + size + 0.1, posy + size - 0)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx + size - 0.4, posy + size + 0.4)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx - size + 0.4, posy + size + 0.4)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx - size + 0.6, posy - size + 0)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx + size + 0.4, posy - size + -0.4)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx + size - 0.4, posy - size + -0.4)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx + size - 0.6, posy - size + 0)

    glColor3f(0.9, 0.35, 0.7)
    glVertex2f(posx + size - 0.4, posy + size + 0.4)


    glEnd()
    glPopMatrix()
    angle += delta
    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action,
mods):
    # управляем направлением вращения
    global delta
    global angle
    global stopped
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            delta = -0.4
        if key == 263: # glfw.KEY_LEFT
            delta = 0.4
        if key == glfw.KEY_ENTER:
            delta = 0
        if key == glfw.KEY_E:
            angle = 3.0

def scroll_callback(window, xoffset, yoffset):
    #управляем размером
    global size
    if (xoffset > 0):
        size -= yoffset/10
    else:
        size += yoffset/10

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

main()
