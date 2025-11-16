import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Rotating Cube")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 8 points of the cube
points = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
])

# make cube bigger
size = 100
points = points * size

# lines between points
lines = [
    [0, 1], [1, 2], [2, 3], [3, 0],  
    [4, 5], [5, 6], [6, 7], [7, 4],  
    [0, 4], [1, 5], [2, 6], [3, 7]   
]

# faces
faces = [
    [0, 1, 2, 3],  # back face
    [4, 5, 6, 7],  # front face
    [0, 1, 5, 4],  # bottom face
    [2, 3, 7, 6],  # top face
    [0, 3, 7, 4],  # left face
    [1, 2, 6, 5],  # right face
]

# color for each face
face_colors = [
    RED,  # back face
    BLUE,  # front face
    GREEN,  # bottom face
    YELLOW,  # top face
    ORANGE,  # left face
    PURPLE,  # right face
]

# numbers for projection
alpha = 1
beta = 1
f = 500

# angles for rotation
rotation_x = 0
rotation_y = 0
rotation_z = 0

def make_rotation_x(angle):
    # matrix to rotate around x
    matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])
    return matrix

def make_rotation_y(angle):
    # matrix to rotate around y
    matrix = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])
    return matrix

def make_rotation_z(angle):
    # matrix to rotate around z
    matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    return matrix

def make_2d_points(points_3d):
    # turn 3d points into 2d points for screen
    x = points_3d[:, 0]
    y = points_3d[:, 1]
    z = points_3d[:, 2]
    
    # stenpe formula
    x_on_screen = (f * x) / (z + f) * alpha + WIDTH / 2
    y_on_screen = (f * y) / (z + f) * beta + HEIGHT / 2
    
    points_2d = np.column_stack((x_on_screen, y_on_screen))
    return points_2d


clock = pygame.time.Clock()
is_running = True

while is_running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    screen.fill(WHITE)
    # make angles bigger so cube rotates
    rotation_x = rotation_x + 0.01
    rotation_y = rotation_y + 0.01
    rotation_z = rotation_z + 0.005

    # get rotation matrices
    matrix_x = make_rotation_x(rotation_x)
    matrix_y = make_rotation_y(rotation_y)
    matrix_z = make_rotation_z(rotation_z)

    # put all rotations together
    final_rotation = matrix_z @ matrix_y @ matrix_x

    # rotate all points
    rotated_points = points @ final_rotation.T

    # make 2d points from 3d points
    points_on_screen = make_2d_points(rotated_points)

    # draw faces with colors
    for i in range(len(faces)):
        face = faces[i]
        color = face_colors[i]

        # get 4 points of the face
        face_points = []
        for point_index in face:
            point_x = int(points_on_screen[point_index][0])
            point_y = int(points_on_screen[point_index][1])
            face_points.append((point_x, point_y))

        pygame.draw.polygon(screen, color, face_points)

    # draw lines between points
    for line in lines:
        point_start = points_on_screen[line[0]]
        point_end = points_on_screen[line[1]]
        start_x = int(point_start[0])
        start_y = int(point_start[1])
        end_x = int(point_end[0])
        end_y = int(point_end[1])
        pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y), 2)

    #  draw red dots on points
    # for point in points_on_screen:
    #     point_x = int(point[0])
    #     point_y = int(point[1])
    #     pygame.draw.circle(screen, RED, (point_x, point_y), 5)

    pygame.display.flip()

pygame.quit()
