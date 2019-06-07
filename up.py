# !/usr/bin/python
# -*- coding: utf-8 -*-
from sense_hat import SenseHat
import time

from time import sleep
sense = SenseHat()

import threading, queue
import random
import inputs

def drawBox(a, b, x, y):
  for dbX in range(x - a):
    for dbY in range(y - b):
      sense.set_pixel(a + dbX, b + dbY, red)
      
def get_input(user_input, inputs):
  while True:
      try:
        events = inputs.get_gamepad()
      except:
        sense.show_message(".")
        
      if len(events) > 0:
        for event in events:
          if event.ev_type == "Key" and event.state == 1:
            if event.code == "BTN_THUMB":
              user_input.put("Red 1")
            if event.code == "BTN_PINKIE":
              user_input.put("Green 2")
            if event.code == "BTN_BASE2":
              user_input.put("Blue 3")
            if event.code == "BTN_TRIGGER":
              user_input.put("Yellow 4")
            if event.code == "BTN_TOP2":
              user_input.put("Pink 5")
            if event.code == "BTN_BASE":
              user_input.put("Purple 6")
            if event.code == "BTN_THUMB2":
              user_input.put("Left side")
            if event.code == "BTN_BASE3":
              user_input.put("Right side")
            if event.code == "BTN_TOP":
              user_input.put("Front")

          elif event.ev_type == "Absolute" and event.state == 0 or event.state == 255:
            if event.code == "ABS_Y":
              if event.state == 0:
                user_input.put("Up")
              else:
                user_input.put("Down")
            elif event.code == "ABS_X":
              if event.state == 0:
                user_input.put("Left")
              else:
                user_input.put("Right")

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
purple = (255,0, 255)
colours = [red,blue,green,white,yellow,purple]
numbers = [1,2,3,4,5,6]
text = ".d.a.t.a."

def play(user_input, inputs):
  
  state = "Startup"
# state = "Ready"
# state = "Set"
# state = "Go"
# state = "Counting"
# state = "Showing"
# state = "Maze"
  state = "Maze End"
# state = "End Game"

  mx = 8  # width and height of the maze
  my = 8
  maze = [[0 for x in range(mx)] for y in range(my)]
  dx = [0, 1, 0, -1]  # 4 directions to move in the maze
  dy = [-1, 0, 1, 0]
  color = [(125, 125, 125), (0, 0, 0)]  # RGB colors of the maze

  (rodX, rodY) = (0, 0)
  rodn = 1
  (saveX, saveY) = (0, 0)
  size = 2
  (offsetX, offsetY) = (0, 0)

  CountingStartedAt = 0
  
  code = [5, 6, 4, 2]
  theSequence = []
  while True:
    if user_input.empty():
      inputed = ""
    else:
      inputed = user_input.get()
      if inputed == "Red 1":
        print(1)
        if state == "End Game" and theSequence[0][1] == 1:
          sense.show_message(text[0] , text_colour=theSequence[0][3], scroll_speed=0.05)
          theSequence = theSequence[1:]
          text = text[1:]
        if state == "Go":
          state = "Counting"
          CountingStartedAt = time.time()
      elif inputed == "Green 2":
        print(2)
        if state == "End Game" and theSequence[0][1] == 2:
          sense.show_message(text[0] , text_colour=theSequence[0][3], scroll_speed=0.05)
          theSequence = theSequence[1:]
          text = text[1:]
        if state == "Set":
          state = "Go"
        elif state == "Counting" and len(code) == 1:
          code = []
        else:
          code = [5, 6, 4, 2]
          
      elif inputed == "Blue 3":
        print(3)
        if state == "End Game" and theSequence[0][1] == 3:
          sense.show_message(text[0] , text_colour=theSequence[0][3], scroll_speed=0.05)
          theSequence = theSequence[1:]
          text = text[1:]
        
        if state == "Maze End":
          state = "End Game"
          text = ".d.a.t.a."
          for i in range(9):
            b = random.choice(numbers)
            theSequence.append([colours[b-1], b, random.choice([0,1]), random.choice(colours)])
          print(theSequence)
      elif inputed == "Yellow 4" :
        if state == "End Game" and theSequence[0][1] == 4:
          sense.show_message(text[0] , text_colour=theSequence[0][3], scroll_speed=0.05)
          theSequence = theSequence[1:]
          text = text[1:]
        if state == "Counting" and len(code) == 2:
          code = [2]
        else:
          code = [5, 6, 4, 2]
        print(4)
      elif inputed == "Pink 5" :
        print(5)
        if state == "End Game" and theSequence[0][1] == 5:
          sense.show_message(text[0] , text_colour=theSequence[0][3], scroll_speed=0.05)
          theSequence = theSequence[1:]
          text = text[1:]
        if state == "Counting" and len(code) == 4:
          code = [6, 4, 2]
        else:
          code = [5, 6, 4, 2]
  

      elif inputed == "Purple 6" :
        print(6)
        if state == "End Game" and theSequence[0][1] == 6:
          sense.show_message(text[0] , text_colour=theSequence[0][3], scroll_speed=0.05)
          theSequence = theSequence[1:]
          text = text[1:]
        if state == "Counting" and len(code) == 3:
          code = [4, 2]
        else:
          code = [5, 6, 4, 2]
          
        if state == "Showing":
          state = "Maze"
          rodX = 0
          rodY = 0
          
      elif inputed == "Left side" :
        print('l')
        if state == "Startup" :
          state = "Ready"
      elif inputed == "Right side" :
        print('r')
        if state == "Ready" :
          state = "Set"
          sense.clear(green)

      elif inputed == "Front" :
        print('f')
        if state.endswith('~'):
          state = state[:-1]
        else:
          state = state + "~"
      elif inputed == "Up" :
          if rodY >= 1:
            if maze[rodY - 1][rodX] == 1:
              rodY -= 1
      elif inputed == "Down" :
          if rodY <= 6:
            if maze[rodY + 1][rodX] == 1:
              rodY += 1
      elif inputed == "Left" :
          if rodX >= 1:
            if maze[rodY][rodX - 1] == 1:
              rodX -= 1
      elif inputed == "Right" :
          if rodX <= 6:
            if maze[rodY][rodX + 1] == 1:
              rodX += 1
      
      if (rodX > 0 or rodY > 0) and state == "Maze" and rodX == saveX and rodY == saveY:
        state = "Maze End"
      print(state)
    if state == 'Startup':
      sleep(.2)
      sense.clear()
      drawBox(0,random.randint(2, 7),7,7)
    else:
      acceleration = sense.get_accelerometer_raw()
      x = acceleration['x'] - offsetX
      y = acceleration['y'] - offsetY

      j = int(x * 7 + 4)
      q = int(y * 7 + 4)
      if j >= 0 and q >= 0 and j < 8 - size and q < 8 - size:
        sense.clear()
        drawBox(j, q, j + size, q + size)
      else:
        sense.clear((255, 0, 0))
        sleep(0.5)
        size += 1
        (offsetX,offsetY) = (x,y)
        if size > 5:
          size = 2
    if state == "Set":
      sense.clear(green)
    elif state == "Go":
      sense.show_letter("1")
    elif state == "Counting":
      i = 2
      if CountingStartedAt + (i * 1) > time.time():
        sense.show_letter("9", red)
      elif CountingStartedAt + (i * 2) > time.time():
        sense.show_letter("8", blue)
      elif CountingStartedAt + (i * 3) > time.time():
        sense.show_letter("7", green)
      elif CountingStartedAt + (i * 4) > time.time():
        sense.show_letter("6", white)
      elif CountingStartedAt + (i * 5) > time.time():
        sense.show_letter("5", yellow)
      elif CountingStartedAt + (i * 6) > time.time():
        sense.show_letter("4", red)
      elif CountingStartedAt + (i * 7) > time.time():
        sense.show_letter("3", blue)
      elif CountingStartedAt + (i * 8) > time.time():
        sense.show_letter("2", green)
      elif CountingStartedAt + (i * 9) > time.time():
        sense.show_letter("1", white)
      elif CountingStartedAt + (i * 10) > time.time():
        sense.show_letter("0", yellow)
      elif CountingStartedAt + (i * 11) > time.time():
        state = "Startup"
      if len(code) == 0:  
        state = "Showing"

    elif state == "Showing":
      sense.clear()
      sense.set_pixel(1,1,green)
      sense.set_pixel(1,2,green)
      sense.set_pixel(1,3,green)
      sense.set_pixel(1,4,green)
      sense.set_pixel(1,5,green)
      sense.set_pixel(1,6,green)
      sense.set_pixel(1,7,green)
      sense.set_pixel(2,2,green)
      sense.set_pixel(2,3,green)
      sense.set_pixel(2,4,green)
      sense.set_pixel(2,5,green)
      sense.set_pixel(2,6,green)
      sense.set_pixel(2,7,green)
      sense.set_pixel(3,3,green)
      sense.set_pixel(3,4,green)
      sense.set_pixel(3,5,green)
      sense.set_pixel(3,6,green)
      sense.set_pixel(3,7,green)
      sense.set_pixel(4,4,green)
      sense.set_pixel(4,5,green)
      sense.set_pixel(4,6,green)
      sense.set_pixel(4,7,green)
      sense.set_pixel(5,5,green)
      sense.set_pixel(5,6,green)
      sense.set_pixel(5,7,green)
      sense.set_pixel(6,6,green)
      sense.set_pixel(6,7,green)
      sense.set_pixel(7,7,green)
    elif state == "Maze":
      # if new maze is needed
      if saveX == 0 or saveY == 0 or saveX == 7 or saveY == 7:

        # start the maze from a random cell

        stack = [(random.randint(0, mx - 1), random.randint(0, my - 1))]
        maze = [[0 for x in range(mx)] for y in range(my)]
        (rodX, rodY) = stack[-1]

        (saveX, saveY) = (7, 7)
        while len(stack) > 0:
          (cx, cy) = stack[-1]
          maze[cy][cx] = 1

          # find a new cell to add

          nlst = []  # list of available neighbors
          for i in range(4):
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
              if maze[ny][nx] == 0:

              # of occupied neighbors must be 1

                ctr = 0
                for j in range(4):
                  ex = nx + dx[j]
                  ey = ny + dy[j]
                  if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                    if maze[ey][ex] == 1:
                      ctr += 1
                if ctr == 1:
                  nlst.append(i)

        # if 1 or more neighbors available then randomly select one and move

          if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]
            cy += dy[ir]
            stack.append((cx, cy))
          else:
            if (saveX, saveY) == (7, 7):
              (saveX, saveY) = stack.pop()
            else:
              stack.pop()

    # draw maze

      for ky in range(my):
        for kx in range(mx):
          if rodX == kx and rodY == ky:
            sense.set_pixel(rodX, rodY, red)
          elif saveX == kx and saveY == ky:
            sense.set_pixel(saveX, saveY, (0, 125, 0))
          else:
            sense.set_pixel(kx, ky, color[maze[ky][kx]])

    elif state == 'End Game':
      if len(theSequence) > 0:
        if theSequence[0][2]:
          sense.show_letter(str(theSequence[0][1]), theSequence[0][3] )
        else:
          sense.clear(theSequence[0][0])
      else:
        sense.show_message("SAFE" , text_colour=green, scroll_speed=0.05)
        state = 'Startup'  
user_input = queue.Queue()
thread1 = threading.Thread(target=get_input,args=(user_input, inputs))
thread2 = threading.Thread(target=play,args=(user_input, inputs))
thread1.start()
thread2.start()
