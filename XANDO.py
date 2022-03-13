import pygame
from os import system

from datetime import datetime
from random import shuffle
 
def saveData(data):
    saving_time = datetime.now()
    filename = saving_time.strftime("%Y-%m-%d-%H%M%S")
    filename = "Data {}.txt".format(filename)

    shuffle(data)

    with open(filename, 'w') as datafile:
        for expl in data:
            datafile.write("{},{},{}\n".format(*expl))
        pass

system('cls')

pygame.init()

clock = pygame.time.Clock()

# Main variables:

width = 500
height = 500
bar_height = 50
info_height = 30

total_height = height + bar_height + info_height

colors = {"white" : (240, 240, 245),
          "dark" : (30, 30, 35),
          "red" : (250, 40, 40),
          "green": (40, 250, 40)}

data = []

newlabel = 0
mode = "add"

window = pygame.display.set_mode((width, total_height))

pygame.display.set_caption("XANDO - Data Generator")

marksize = (10, 10)

xmark = pygame.image.load("assets/x.png")
xmark = pygame.transform.scale(xmark, marksize)

omark = pygame.image.load("assets/o.png")
omark = pygame.transform.scale(omark, marksize)

count_x = 0
count_o = 0

big_font = pygame.font.SysFont("calibri", 24, bold = True)
small_font = pygame.font.SysFont("calibri", 14, bold = True)

# Main loop
done = False

while not done:
    events = pygame.event.get()
    for event in events:
        # print(event)
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if event.button == 1 and  0 < y - info_height < height:
                data.append((x, height - y, newlabel))

            elif event.button == 3:
                for i in range(len(data)):
                    try:
                        x0, y0, label = data[i]
                        if (x-x0)**2 + (height - y - y0)**2 <= 5**2:
                            data.pop(i)
                            break
                    except IndexError:
                        print("Error : Data list - Index out of range")

            elif event.button == 2:
                newlabel = int(not newlabel)

        elif event.type == pygame.KEYDOWN:
            if event.unicode.lower() == u'r':
                data = []

            elif event.unicode.lower() == u'p':
                newlabel = 1

            elif event.unicode.lower() == u'n':
                newlabel = 0
            
            elif event.unicode.lower() == u's':
                saveData(data)
        
    
    window.fill(colors["white"])

#Show Data points
    count_x = 0
    count_o = 0

    for expl in data:
        x, y, label = expl
        if label:
            count_o += 1
            mark = omark
        else:
            count_x += 1
            mark = xmark

        window.blit(mark, (x - marksize[0] / 2, height - y - marksize[1] / 2))


#Show tutorial
    pygame.draw.rect(window, colors["dark"], [0, 0, width, info_height])
    tut_text = "Mouse : Add / Remove  |  N : Negative  |  P : Positive  |  R : Reset  |  S : Save"

    text_surf_top = small_font.render(tut_text, True, colors["white"])

    window.blit(text_surf_top, (.05 * width, .25 * info_height))


#Show bottom bar
    pygame.draw.rect(window, colors["red"], [0, height + info_height, .5 * width, bar_height])
    pygame.draw.rect(window, colors["green"], [.5 * width, height + info_height, .5 * width, bar_height])

    text_surf_left = big_font.render(str(count_x), True, colors["white"])
    text_surf_right = big_font.render(str(count_o), True, colors["white"])

    window.blit(text_surf_left, (.25 * width, total_height - .75 * bar_height))
    window.blit(text_surf_right, (.75 * width, total_height - .75 * bar_height))


    pygame.display.update()

    clock.tick(60)

pygame.quit()

# pyinstaller main.py --noconsole --name XANDO
