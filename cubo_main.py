import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

## Configuraciones de la ventana
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

## Propiedades del cubo
# Colores (RGB)
RED = (1.0, 0.0, 0.0)
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)

# angulo inicial
rotacion_x = 0
rotacion_y = 0

# velocidad de animacion
rotation_speed = 5

# Cara actual visible
current_face = 0 ## 0: Frontal, 1: Derecha, 2: Trasera, 3: Izquierda, 4: Superior, 5: Inferior

face_text = [
    "ASPECTO 1 (DOC 1)"
    "ASPECTO 2 (DOC 2)"
    "ASPECTO 3 (DOC 3)"
    "ASPECTO 4 (DOC 4)"
    "ASPECTO 5 (DOC 5)"
    "ASPECTO 6 (DOC 6)"
]

# definicion del cubo
vertices = (
    (1, -1, -1), # 0
    (1, 1, -1),  # 1
    (-1, 1, -1), # 2
    (-1, -1, -1),# 3
    (1, -1, 1),  # 4
    (1, 1, 1),   # 5
    (-1, -1, 1), # 6
    (-1, 1, 1)   # 7
)

## Edges del cubo
edges = (
    (0,1), (0,3), (0,4),
    (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7),
    (5,1), (5,4), (5,7),
)

# superficies (caras del cubo cochino) - cada tupla representa una cara
surfaces = (
    (0,1,2,3), # Cara Frontal
    (4,5,1,0), # Cara derecha
    (7,6,3,2), # Cara Trasera
    (6,7,5,4), # cara izquierda
    (1,5,7,2), # cara superior
    (0,3,6,4)  # cara inferior
)

# colores de cada cara (Para DEBUG)
face_colors = (
    (1,0,0), # Frontal (Rojo)
    (0,1,0), # Derecha (Verde)
    (0,0,1), # Trasera (Azul)
    (1,1,0), # Izquierda (Amarillo)
    (1,0,1), # Superior (Magenta)
    (0,1,1)  # Inferior (Cian)
)

face_rotations = [
    (0, 0),    # Cara Frontal (sin rotación extra)
    (0, -90),  # Cara Derecha
    (0, 180),  # Cara Trasera
    (0, 90),   # Cara Izquierda
    (-90, 0),  # Cara Superior
    (90, 0)    # Cara Inferior
]

## Funcion para dibujar el cubo

def Cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3f(RED[0], RED[1], RED[2])
        for vertex in surface:
            glVertex3fv(vertices[vertex]) # coordenadas del vertice
    glEnd()

def main():
    global rotacion_x, rotacion_y, current_face

    pygame.init()
    display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Perspectiva de opengl
    # aspect: Relación de aspecto (ancho/alto de la ventana)
    # zNear: Plano de recorte cercano (objetos más cercanos que esto no se ven)
    # zFar: Plano de recorte lejano (objetos más lejanos que esto no se ven)
    #gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect_ratio = float(display[0]) / float(display[1])
    glFrustum(-aspect_ratio, aspect_ratio, -1.0, 1.0, 2.0, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # mueve la camara o los objetos
    glTranslate(0.0, 0.0, -5)

    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    glEnable(GL_DEPTH_TEST)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_face = (current_face + 1) % len(face_rotations)
                elif event.key == pygame.K_LEFT:
                    current_face = (current_face - 1) % len(face_rotations)
                    if current_face < 0:
                        current_face = len(face_rotations) - 1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        target_rotation_x, target_rotation_y = face_rotations[current_face]

        lerp_factor = 0.1

        rotacion_x = rotacion_x * (1 - lerp_factor) + target_rotation_x * lerp_factor
        rotacion_y = rotacion_y * (1 - lerp_factor) + target_rotation_y * lerp_factor

        glPushMatrix()
        glRotate(rotacion_x, 1, 0, 0)
        glRotate(rotacion_y, 0, 1, 0)

        Cube()

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == '__main__':
    main()