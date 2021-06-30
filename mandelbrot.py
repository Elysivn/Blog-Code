import pygame
import numpy as np
import colorsys


def calculate(x):
    """
    Receive complex number x, return number of iterations
    that the function stays below 2.
    """
    z = 0
    for i in range(max_iterations+1):
        if abs(z) <= 2:
            z = z**2 + x
        else:
            break
    return i

def plot(re_start, re_end, im_start, im_end):
    """
    Plot the colour for each pixel based on iterations
    """
    pixel_x = np.linspace(re_start, re_end, w) # range of x vals
    pixel_y = np.linspace(im_start, im_end, h) # range of y vals
    hue_range = np.linspace(145, 240, max_iterations+1) # range of hues

    # loop through each pixel on the screen and assign it a colour
    for i in range(w):
        for j in range(h):
            c = complex(pixel_x[i], pixel_y[j]) # complex number of current pixel
            n = calculate(c) # number of iterations

            # HSV vals
            hue = int(hue_range[n]) # assign hue from linspace index
            saturation = 255
            if n < max_iterations:
                value = 255
            else:
                value = 0
            complex_matrix[i][j] = c # update complex matrix

            # assign colour to pixel on screen
            rgb = colorsys.hsv_to_rgb(hue/255, saturation/255, value/255)
            r,g,b = (int(x*255) for x in rgb)
            screen.set_at((i, j), (r, g, b))


def zoom(rect_start, rect_end):
    """
    Receive coordinates drawn on screen, zoom in on those coordinates
    as a rectangle.
    """
    x1 = rect_start[0]
    y1 = rect_start[1]
    x2 = rect_end[0]
    y2 = rect_end[1]
    re_start = complex_matrix[x1][y1].real
    im_start = complex_matrix[x1][y1].imag
    re_end = complex_matrix[x2][y2].real
    im_end = complex_matrix[x2][y2].imag
    return plot(re_start, re_end, im_start, im_end)


# Setting up initial stuff
pygame.init()
screen = pygame.display.set_mode((800, 600))
w, h = pygame.display.get_surface().get_size()
screen.fill((255, 255, 255))
pygame.display.set_caption('The Mandelbrot Set')

complex_matrix = np.zeros((w, h), dtype=complex) # store all values in the complex plane
max_iterations = 100 # higher = better detail, but more intensive

# range of x and y values to plot
x_start = -2
x_end = 1
y_start = -1
y_end = 1

plot(x_start, x_end, y_start, y_end) # inital mandelbrot plot
pygame.display.update()
rect_start = ()
rect_end = ()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # end program if window is closed
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if mouse button is pressed get the position
            rect_start = event.pos
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # if mouse button is released get position and zoom in
            rect_end = event.pos
            zoom(rect_start, rect_end)
            pygame.display.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: # if backspace is pressed, zoom out fully
                plot(x_start, x_end, y_start, y_end)
                pygame.display.update()
            elif event.key == pygame.K_ESCAPE: # if escape is pressed end program
                pygame.quit()
