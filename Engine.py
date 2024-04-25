import pygame
import numpy as np
import Button as ButtonMaker
from math import *
import re

HEIGHT, WIDTH = 800, 1200
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)

pygame.init()

pygame.display.set_caption("3D PROJECTION ENGINE")
window = pygame.display.set_mode((WIDTH, HEIGHT))
window.fill(WHITE)

cube = np.array([(-1,-1,1),
                  (1,-1,1),
                  (1,1,1),
                  (-1,1,1),
                  (-1,-1,-1),
                  (1,-1,-1),
                  (1,1,-1),
                  (-1,1,-1)]
)
eq_triangle = np.array([(0,0,2), (1,1,0), (1,-1,0), (-1,-1,0), (-1,1,0)])

projectionMatrix = np.matrix([(1,0,0),(0,1,0)])


def connectPoints( start, end, window, color):
    pygame.draw.line(window, color, start ,end)

def rotation(axis: str) -> np.matrix:
    if axis == "x":
      return np.matrix([(1, 0, 0),
            (0, cos(angle), -sin(angle)),
            (0, sin(angle), cos(angle))])
    elif axis == "y":
        return np.matrix([(cos(angle), 0 ,-sin(angle)),
               (0, 1, 0),
               (-sin(angle), 0, cos(angle))])
    elif axis == "z":
        return np.matrix([(cos(angle), -sin(angle), 0),
               (sin(angle), cos(angle), 0),                   
               (0, 0, 1)])
    else:
        raise ValueError("ERROR: invalid axis")
    
def is_valid_number(s):
    return bool(re.match(r'^-?\d+(?:\.\d+)?$', s))


UI_WIDTH = 300
UI_HEIGHT = 800
BUTTON_BOX = (30,30)
main_surface = pygame.Surface((WIDTH-UI_WIDTH, HEIGHT))

scale = 100
angle = 0
clock = pygame.time.Clock()

main_surface.fill(BLACK)


rotation_angle = 0.01
input_text = ""
in_rotation = pygame.Rect((WIDTH-250, 30), (200,50)) #Hard coded locations
font = pygame.font.Font(None, 36) #Font of the texts

inputs = []# all inputs in UI like buttons

text_active = False

X_rotate = False
Y_rotate = False
Z_rotate = False

def action_rX():
    global X_rotate
    X_rotate = not X_rotate
def action_rY():
    global Y_rotate
    Y_rotate = not Y_rotate
def action_rZ():
    global Z_rotate
    Z_rotate = not Z_rotate

buttonX = ButtonMaker.Button(WIDTH-250, 110, 30, 30, "X", font, action_rX) #Hard code location ;(
buttonX.draw(window)
buttonY = ButtonMaker.Button(buttonX.rect.x+60 ,buttonX.rect.y, 30, 30, "Y", font, action_rY)
buttonY.draw(window)
buttonZ = ButtonMaker.Button(buttonY.rect.x+60, buttonY.rect.y, 30, 30, "Z", font, action_rZ)
buttonZ.draw(window)

inputs.append(buttonX)
inputs.append(buttonY)
inputs.append(buttonZ)


running = True
while running:
    clock.tick(60) # 60fps
    window.fill(WHITE)
    window.blit(main_surface, (0,0))
    main_surface.fill(BLACK)

    for but in inputs:
        but.draw(window)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for but in inputs:
                    but.handle_event(event) #MUST IMPLEMENT ACTION IN BUTTON
            if in_rotation.collidepoint(event.pos): # text area pressed
                text_active = not text_active
            else:
                text_active = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if text_active:
                if event.key == pygame.K_RETURN:
                    if is_valid_number(input_text):
                        rotation_angle = float(input_text)
                    else:
                        rotation_angle = 0.01
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            
    

    pygame.draw.rect(window, BLACK, in_rotation,2)
    text_surface = font.render(input_text, True, BLACK)
    window.blit(text_surface, (in_rotation.x+5, in_rotation.y+5))
    

    coordinats = np.zeros((8,), dtype=object) #Coordinats of cube
    angle += rotation_angle

    i = 0
    for point in cube:
        rotation2D_1 = None
        rotation2D_2 = None
        rotation2D_3 = None

        if X_rotate:
            rotation2D_1 = rotation("x").dot(point.reshape((3,1)))
        else:
            rotation2D_1 = point.reshape((3,1))
        if Y_rotate:
            rotation2D_2 = rotation("y").dot(rotation2D_1)
        else:
            rotation2D_2 = rotation2D_1
        if Z_rotate:    
            rotation2D_3 = rotation("z").dot(rotation2D_2)
        else:
            rotation2D_3 = rotation2D_2

        point2D = projectionMatrix.dot(rotation2D_3)
        
        x = int(point2D[0] * scale) + WIDTH/2
        y = int(point2D[1] * scale) + HEIGHT/2
        coordinats[i] = (x,y) 
        i+=1   
        pygame.draw.circle(main_surface, GREEN, (x,y), 5)

    connectPoints(coordinats[0],coordinats[1], main_surface, WHITE)
    connectPoints(coordinats[1],coordinats[2], main_surface, WHITE)
    connectPoints(coordinats[2],coordinats[3], main_surface, WHITE)
    connectPoints(coordinats[3],coordinats[0], main_surface, WHITE)

    connectPoints(coordinats[4],coordinats[5], main_surface, WHITE)
    connectPoints(coordinats[5],coordinats[6], main_surface, WHITE)
    connectPoints(coordinats[6],coordinats[7], main_surface, WHITE)
    connectPoints(coordinats[7],coordinats[4], main_surface, WHITE)

    connectPoints(coordinats[0],coordinats[4], main_surface, WHITE)
    connectPoints(coordinats[1],coordinats[5], main_surface, WHITE)
    connectPoints(coordinats[2],coordinats[6], main_surface, WHITE)
    connectPoints(coordinats[3],coordinats[7], main_surface, WHITE)
    pygame.display.update()
pygame.quit()