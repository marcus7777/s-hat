from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
dx = 0
dy = 0
x = 0
looper = True
while looper:
    acceleration = sense.get_accelerometer_raw()
    if x != 0:
        dx = x - acceleration['x']
        dy = y - acceleration['y']
        print(dx,dy)
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    r = int((x * 255) + 128)
    g = int((y * 255) + 128)
    b = int((z * 255) + 128)
    if r < 0   : r = 0
    if g < 0   : g = 0
    if b < 0   : b = 0
    if r > 255 : r = 255
    if g > 255 : g = 255
    if b > 255 : b = 255

    j = int((x * 7) + 4)
    q = int((y * 7) + 4)

    if j >= 0 and q >= 0 and j < 6 and q < 6:
        print(q, j, (255-r,255-g,255-b))
        sense.clear((r, g, b))
        sense.set_pixel(q, j, (255-r,255-g,255-b))
        sense.set_pixel(q+1, j, (255-r,255-g,255-b))
        sense.set_pixel(q, j+1, (255-r,255-g,255-b))
        sense.set_pixel(q+1, j+1, (255-r,255-g,255-b))
    else:
        sense.clear((255, 0, 0))
        sleep(0.5)
    for event in sense.stick.get_events():
    # Check if the joystick was pressed
        if event.action == "pressed":
            # Check which direction
            if event.direction == "up":
                sense.show_letter("U")      # Up arrow
            elif event.direction == "down":
                sense.show_letter("D")      # Down arrow
            elif event.direction == "left": 
                sense.show_letter("L")      # Left arrow
            elif event.direction == "right":
                sense.show_letter("R")      # Right arrow
            elif event.direction == "middle":
                sense.show_letter("M")      # Enter key
                looper = False
        # Wait a while and then clear the screen
        sleep(0.5)
        sense.clear()

# Random Maze Generator using Depth-first Search
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# FB - 20121214
import random
mx = 8; my = 8 # width and height of the maze
maze = [[0 for x in range(mx)] for y in range(my)]
dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
color = [(125,125,125), (0, 0, 0)] # RGB colors of the maze

rodX = 0
rodY = 0
rodn = 0
saveX = 0
saveY = 0
mazelooper = True
while mazelooper:
    if rodX == saveX and rodY == saveY:
        rodX = 0
        rodY = 0
        rodn += 1
        sense.show_message("Save rod" + str(rodn) +  ":")
        # start the maze from a random cell
        stack = [(random.randint(0, mx - 1), random.randint(0, my - 1))]
        maze = [[0 for x in range(mx)] for y in range(my)]
        (rodX, rodY) = stack[-1]

        (saveX, saveY) = (7,7)
        while len(stack) > 0:
            print(stack[-1])
            (cx, cy) = stack[-1]
            maze[cy][cx] = 1
            # find a new cell to add
            nlst = [] # list of available neighbors
            for i in range(4):
                nx = cx + dx[i]; ny = cy + dy[i]
                if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                    if maze[ny][nx] == 0:
                        # of occupied neighbors must be 1
                        ctr = 0
                        for j in range(4):
                            ex = nx + dx[j]; ey = ny + dy[j]
                            if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                                if maze[ey][ex] == 1: ctr += 1
                        if ctr == 1: nlst.append(i)
            # if 1 or more neighbors available then randomly select one and move
            if len(nlst) > 0:
                ir = nlst[random.randint(0, len(nlst) - 1)]
                cx += dx[ir]; cy += dy[ir]
                stack.append((cx, cy))
            else:
                if (saveX, saveY) == (7,7): 
                    (saveX, saveY) = stack.pop()
                else:
                    stack.pop()
                    

    sleep(0.3)
    for ky in range(my):
        for kx in range(mx):
            if rodX == kx and rodY == ky:
                sense.set_pixel(rodX,  rodY,  (125,0,0))
            elif saveX == kx and saveY == ky:
                sense.set_pixel(saveX, saveY, (0,125,0))
            else:
                sense.set_pixel(kx, ky, color[maze[ky][kx]])

    sleep(0.1)
    sense.set_pixel(rodX,  rodY,  (94, 55, 0))
    sleep(0.1)
    sense.set_pixel(rodX,  rodY,  (0, 55, 94))
    sleep(0.1)
    sense.set_pixel(rodX,  rodY,  (0, 0, 125))
    sleep(0.1)
    sense.set_pixel(rodX,  rodY,  (0, 55, 94))
    sleep(0.1)
    sense.set_pixel(rodX,  rodY,  (94, 55, 0))

    for event in sense.stick.get_events():
    # Check if the joystick was pressed
        if event.action == "pressed":
            # Check which direction
            if event.direction == "up":
                if rodY >= 1:
                    if maze[rodY-1][rodX] == 1: 
                        rodY -= 1
            elif event.direction == "down":
                if rodY <= 6:
                    if maze[rodY+1][rodX] == 1:
                        rodY += 1
            elif event.direction == "left": 
                if rodX >= 1:
                    if maze[rodY][rodX - 1] == 1: 
                        rodX -= 1
            elif event.direction == "right":
                if rodX <= 6:
                    if maze[rodY][rodX + 1] == 1: 
                        rodX += 1
    if rodX == saveX and rodY == saveY:
        if rodn == 6:
            sense.show_message("Yippy!! safe", text_colour=[0,100,0])
            mazelooper= False
