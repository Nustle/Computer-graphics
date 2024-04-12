from itertools import product

import glfw
from OpenGL.GL import *

angle1, angle2, angle3 = 10, 10, 10
size = 0.2
lines = []
e = 0.001


class Point:
    code_len = 6

    def __init__(self, coordinates):
        self.x, self.y, self.z = coordinates
        self.code = [0] * self.code_len
        self.numeric_code = 0
        self.make_code()

    def make_code(self):
        n = self.code_len
        if self.x < -size - e:
            self.code[n - 1] = 1
        if self.x > size + e:
            self.code[n - 2] = 1
        if self.y < -size - e:
            self.code[n - 3] = 1
        if self.y > size + e:
            self.code[n - 4] = 1
        if self.z > size + e:
            self.code[n - 5] = 1
        if self.z < -size - e:
            self.code[n - 6] = 1
        for i in range(n):
            self.numeric_code += self.code[i] * (2 ** (n - i - 1))

    def is_invisible_point(self):
        invisible = True
        if self.numeric_code == 0:
            invisible = False
        return invisible


class ProcessedLine:
    def __init__(self, points, color):
        self.points = points
        self.color = color

    def draw(self):
        glBegin(GL_LINES)
        glColor3f(*self.color)
        point1, point2 = self.points
        glVertex3f(point1.x, point1.y, point1.z)
        glVertex3f(point2.x, point2.y, point2.z)
        glEnd()


def is_invisible_line(point1, point2):
    invisible = False
    if point1.numeric_code & point2.numeric_code != 0:
        invisible = True
    return invisible


def code_measure_error(point2):
    measure_errors = (
        [point2.x + dx, point2.y + dy, point2.z + dz]
        for dx, dy, dz in product([-e / 100, e / 100], repeat=3)
    )
    for coordinates in measure_errors:
        point = Point(coordinates)
        if point.numeric_code == 0:
            return [True, point]
    return [False, None]


def midline_intersection(point1, point2):
    is_visible_point, point = code_measure_error(point2)
    if is_visible_point:
        return point
    point = point2
    if not is_invisible_line(point1, point2):
        point_mid = Point([
            (point1.x + point2.x) / 2,
            (point1.y + point2.y) / 2,
            (point1.z + point2.z) / 2,
        ])
        if is_invisible_line(point_mid, point2):
            point = midline_intersection(point1, point_mid)
        else:
            point = midline_intersection(point_mid, point2)
    return point

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Lab 5", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def cube(size):
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, -size, size)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, -size, -size)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)
    glColor3f(0.8, 0.0, 0.4)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    glEnd()


def display(window):
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()

    glRotatef(angle1, 0, 0, 1)
    glRotatef(angle2, 0, 1, 0)
    glRotatef(angle3, 1, 0, 0)
    cube(size)

    if len(lines) > 0:
        lines[0].draw()
        lines[1].draw()
        lines[2].draw()

    glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global angle1, angle2, angle3, lines
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            angle2 += 10
        elif key == glfw.KEY_UP:
            angle3 += 10
        elif key == glfw.KEY_DOWN:
            angle3 -= 10
        elif key == glfw.KEY_RIGHT:
            angle1 += 10
        elif key == glfw.KEY_ENTER:
            lines = []
            first_coordinates = list(map(float, input("Координаты x1, y1, z1 первой точки: ").split()))
            second_coordinates = list(map(float, input("Координаты x2, y2, z2 второй точки: ").split()))
            line = ProcessedLine(
                [Point(first_coordinates), Point(second_coordinates)],
                [1.0, 0.0, 0.0],
            )
            new_point1 = midline_intersection(line.points[0], line.points[1])
            new_point2 = midline_intersection(line.points[1], line.points[0])
            color = [0.3, 0.7, 0.4]
            if is_invisible_line(new_point1, new_point2):
                color = [1.0, 0.0, 0.0]
            lines.append(
                ProcessedLine([new_point1, new_point2], color)
            )
            lines.append(
                ProcessedLine([new_point1, line.points[1]], [1.0, 0.0, 0.0])
            )
            lines.append(
                ProcessedLine([line.points[0], new_point2], [1.0, 0.0, 0.0])
            )


if __name__ == "__main__":
    main()
