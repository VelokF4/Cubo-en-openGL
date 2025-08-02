import pygame
from pygame.locals import *
from OpenGL.GL import *
import os

## Configuraciones de la ventana
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 1000

## Propiedades del cubo
# Colores (RGB)
RED = (1.0, 0.0, 0.0)
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)

# angulo inicial
rotacion_x = 0
rotacion_y = 0

# Cara actual visible
current_face = 0

texture_files = [
    "cara1.png",
    "cara2.png",
    "cara3.png",
    "cara4.png",
    "cara5.png",
    "cara6.png"
]

cube_textures = []

# Definición del cubo (vértices más simples)
vertices = [
    # Cara frontal
    [-1, -1, 1],  # 0
    [1, -1, 1],  # 1
    [1, 1, 1],  # 2
    [-1, 1, 1],  # 3
    # Cara trasera
    [-1, -1, -1],  # 4
    [1, -1, -1],  # 5
    [1, 1, -1],  # 6
    [-1, 1, -1]  # 7
]

# Caras del cubo (cada cara es un conjunto de 4 vértices)
faces = [
    [0, 1, 2, 3],  # Frontal
    [1, 5, 6, 2],  # Derecha
    [5, 4, 7, 6],  # Trasera
    [4, 0, 3, 7],  # Izquierda
    [3, 2, 6, 7],  # Superior
    [4, 5, 1, 0]  # Inferior
]

# Colores de cada cara
face_colors = [
    (1.0, 0.0, 0.0),  # Frontal (Rojo)
    (0.0, 1.0, 0.0),  # Derecha (Verde)
    (0.0, 0.0, 1.0),  # Trasera (Azul)
    (1.0, 1.0, 0.0),  # Izquierda (Amarillo)
    (1.0, 0.0, 1.0),  # Superior (Magenta)
    (0.0, 1.0, 1.0)  # Inferior (Cian)
]

face_rotations = [
    (0, 0),  # Cara Frontal
    (0, -90),  # Cara Derecha
    (0, 180),  # Cara Trasera
    (0, 90),  # Cara Izquierda
    (-90, 0),  # Cara Superior
    (90, 0)  # Cara Inferior
]

# Coordenadas de textura
tex_coords = [
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0]
]


def cargar_textura(filename):
    # Carga los archivos de texturas
    if not os.path.exists(filename):
        print(f"Archivo de textura no encontrado: {filename}")
        return None

    try:
        image = pygame.image.load(filename).convert_alpha()
        print(f"Textura cargada exitosamente: {filename}")
    except pygame.error as message:
        print(f"No se pudo cargar la imagen: {filename}")
        print(f"Error: {message}")
        return None

    # Voltear la imagen verticalmente
    image_width, image_height = image.get_size()
    img_data = pygame.image.tostring(image, "RGBA", True)

    # Generar ID de textura
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # Configurar parámetros de textura
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    # Cargar datos de textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return textura_id


def crear_textura_color(color):
    #Crear una textura de color sólido
    textura_id = glGenTextures(1)
    r, g, b = [int(c * 255) for c in color]
    pixel_data = bytes([r, g, b, 255])

    glBindTexture(GL_TEXTURE_2D, textura_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixel_data)

    return textura_id


def draw_cube():
    # Dibujar el cubo con texturas
    for i, face in enumerate(faces):

        if i < len(cube_textures) and cube_textures[i] is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, cube_textures[i])
            glColor3f(1.0, 1.0, 1.0)

            glBegin(GL_QUADS)
            for j, vertex_index in enumerate(face):
                glTexCoord2f(*tex_coords[j])
                glVertex3f(*vertices[vertex_index])
            glEnd()


def setup_projection(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = width / height
    size = 3.0
    glOrtho(-size * aspect, size * aspect, -size, size, -10, 10)

    glMatrixMode(GL_MODELVIEW)


def main():
    global rotacion_x, rotacion_y, current_face

    pygame.init()
    display = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cubo 3D con Texturas")

    # Configurar proyección
    setup_projection(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    # Configurar OpenGL
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # Habilitar blending para transparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearColor(0.3, 0.3, 0.3, 1.0)  # Fondo gris

    # Cargar texturas
    texturas_cargadas = 0
    for i, filename in enumerate(texture_files):
        texture_id = cargar_textura(filename)
        if texture_id is not None:
            cube_textures.append(texture_id)
            texturas_cargadas += 1
        else:
            # Crear textura de color sólido como fallback
            # o debugging nose
            texture_id = crear_textura_color(face_colors[i])
            cube_textures.append(texture_id)

    print(f"Texturas cargadas: {texturas_cargadas}/{len(texture_files)}")

    clock = pygame.time.Clock()
    running = True
    auto_rotate = False
    rotation_angle = 0

    print("Controles:")
    print("- Flecha derecha: siguiente cara")
    print("- Flecha izquierda: cara anterior")
    print("- R: rotar automáticamente")
    print("- ESC: salir")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    current_face = (current_face + 1) % len(face_rotations)
                    print(f"Mostrando cara: {current_face}")
                elif event.key == pygame.K_LEFT:
                    current_face = (current_face - 1) % len(face_rotations)
                    if current_face < 0:
                        current_face = len(face_rotations) - 1
                    print(f"Mostrando cara: {current_face}")
                elif event.key == pygame.K_r:
                    auto_rotate = not auto_rotate
                    print(f"Rotación automática: {'activada' if auto_rotate else 'desactivada'}")

        # Limpiar pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Resetear transformaciones
        glLoadIdentity()

        if auto_rotate:
            # Rotación automática continua
            rotation_angle += 1
            glRotatef(rotation_angle, 1, 1, 0)
        else:
            # Rotación basada en la cara actual
            target_rotation_x, target_rotation_y = face_rotations[current_face]
            lerp_factor = 0.1

            rotacion_x = rotacion_x * (1 - lerp_factor) + target_rotation_x * lerp_factor
            rotacion_y = rotacion_y * (1 - lerp_factor) + target_rotation_y * lerp_factor

            glRotatef(rotacion_x, 1, 0, 0)
            glRotatef(rotacion_y, 0, 1, 0)

        draw_cube()

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    # Limpiar texturas
    if cube_textures:
        glDeleteTextures(cube_textures)

    pygame.quit()


if __name__ == '__main__':
    main()