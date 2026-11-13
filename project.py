
import math
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

GRID = 20            # board is GRID x GRID cells
STEP_MS = 140        # snake moves every 140 ms

# ---------- cube drawing ----------
# each face = (normal, 4 corners)
FACES = [
    ((0, 0, 1),  [(-.5, -.5, .5), (.5, -.5, .5), (.5, .5, .5), (-.5, .5, .5)]),
    ((0, 0, -1), [(-.5, -.5, -.5), (-.5, .5, -.5), (.5, .5, -.5), (.5, -.5, -.5)]),
    ((0, 1, 0),  [(-.5, .5, -.5), (-.5, .5, .5), (.5, .5, .5), (.5, .5, -.5)]),
    ((0, -1, 0), [(-.5, -.5, -.5), (.5, -.5, -.5), (.5, -.5, .5), (-.5, -.5, .5)]),
    ((1, 0, 0),  [(.5, -.5, -.5), (.5, .5, -.5), (.5, .5, .5), (.5, -.5, .5)]),
    ((-1, 0, 0), [(-.5, -.5, -.5), (-.5, -.5, .5), (-.5, .5, .5), (-.5, .5, -.5)]),
]

def draw_cube(x, y, z, size, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size, size)
    glColor3f(*color)
    glBegin(GL_QUADS)
    for normal, corners in FACES:
        glNormal3f(*normal)
        for c in corners:
            glVertex3f(*c)
    glEnd()
    glPopMatrix()

def cell_to_world(cx, cz):
    return cx - GRID / 2 + 0.5, cz - GRID / 2 + 0.5

# ---------- game state ----------
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]   # head first
        self.dir = (1, 0)
        self.next_dir = (1, 0)
        self.score = 0
        self.over = False
        self.place_food()

    def place_food(self):
        while True:
            f = (random.randrange(GRID), random.randrange(GRID))
            if f not in self.snake:
                self.food = f
                return

    def set_dir(self, d):
        # can't turn back into yourself
        if (d[0] + self.dir[0], d[1] + self.dir[1]) != (0, 0):
            self.next_dir = d

    def step(self):
        if self.over:
            return
        self.dir = self.next_dir
        hx, hz = self.snake[0]
        head = (hx + self.dir[0], hz + self.dir[1])
        # hit wall or yourself?
        if not (0 <= head[0] < GRID and 0 <= head[1] < GRID) or head in self.snake:
            self.over = True
            return
        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

# ---------- drawing the scene ----------
def draw_floor():
    for cx in range(GRID):
        for cz in range(GRID):
            x, z = cell_to_world(cx, cz)
            shade = 0.16 if (cx + cz) % 2 == 0 else 0.22
            draw_cube(x, -0.1, z, 1.0, (shade, shade + 0.04, shade + 0.1))
    # border
    wall = (0.5, 0.5, 0.7)
    for i in range(-1, GRID + 1):
        for (cx, cz) in ((i, -1), (i, GRID), (-1, i), (GRID, i)):
            x, z = cell_to_world(cx, cz)
            draw_cube(x, 0.15, z, 0.9, wall)

def draw_game(game, t):
    draw_floor()
    for i, (cx, cz) in enumerate(game.snake):
        x, z = cell_to_world(cx, cz)
        if game.over:
            color = (0.8, 0.2, 0.2)
        elif i == 0:
            color = (0.6, 1.0, 0.3)       # head
        else:
            color = (0.1, 0.7 - min(i, 20) * 0.015, 0.25)
        draw_cube(x, 0.5, z, 0.9, color)
    fx, fz = cell_to_world(*game.food)
    bob = 0.5 + 0.1 * math.sin(t * 5)
    draw_cube(fx, bob, fz, 0.6, (1.0, 0.15, 0.15))

# ---------- camera-relative controls ----------
def screen_dir(up, right, rot_y):
    """Turn 'up/right' on screen into a world grid direction."""
    a = math.radians(rot_y)
    up_vec = (math.sin(a), -math.cos(a))
    right_vec = (math.cos(a), math.sin(a))
    vx = up * up_vec[0] + right * right_vec[0]
    vz = up * up_vec[1] + right * right_vec[1]
    if abs(vx) > abs(vz):
        return (1 if vx > 0 else -1, 0)
    return (0, 1 if vz > 0 else -1)

# ---------- main ----------
def main():
    pygame.init()
    W, H = 1000, 700
    pygame.display.set_mode((W, H), DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    glClearColor(0.02, 0.02, 0.06, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.45, 0.45, 0.45, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1))

    glMatrixMode(GL_PROJECTION)
    gluPerspective(50, W / H, 0.1, 200)
    glMatrixMode(GL_MODELVIEW)

    game = Game()
    rot_x, rot_y, zoom = 55, 0, -32
    dragging = False
    last_step = pygame.time.get_ticks()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                elif e.key == K_r:
                    game.reset()
                elif e.key in (K_UP, K_w):
                    game.set_dir(screen_dir(1, 0, rot_y))
                elif e.key in (K_DOWN, K_s):
                    game.set_dir(screen_dir(-1, 0, rot_y))
                elif e.key in (K_LEFT, K_a):
                    game.set_dir(screen_dir(0, -1, rot_y))
                elif e.key in (K_RIGHT, K_d):
                    game.set_dir(screen_dir(0, 1, rot_y))
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    dragging = True
                elif e.button == 4:
                    zoom = min(-15, zoom + 2)
                elif e.button == 5:
                    zoom = max(-60, zoom - 2)
            elif e.type == MOUSEBUTTONUP and e.button == 1:
                dragging = False
            elif e.type == MOUSEMOTION and dragging:
                rot_y += e.rel[0] * 0.4
                rot_x = max(20, min(89, rot_x + e.rel[1] * 0.4))

        # move the snake on a timer
        now = pygame.time.get_ticks()
        if now - last_step >= max(70, STEP_MS - game.score * 3):
            game.step()
            last_step = now

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, zoom)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)
        glLightfv(GL_LIGHT0, GL_POSITION, (10, 30, 10, 1))

        draw_game(game, now / 1000)

        status = "GAME OVER - press R" if game.over else "Playing"
        pygame.display.set_caption(f"3D Snake | Score: {game.score} | {status}")
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()