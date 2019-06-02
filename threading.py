from evdev import InputDevice, categorize, ecodes
import threading, queue

dev = InputDevice('/dev/input/by-id/usb-Monster_Joysticks_MJ2USB_1000-event-joystick')

print(dev)
                  
def joy(dev,q):
  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      q.put(event)
    elif event.type == ecodes.EV_ABS:
      q.put(event)


def play(dev,q):
  var = [] 
  while True:
    if q.empty():
      print(var)
    else:
      var = q.get()



q = queue.Queue()
thread1 = threading.Thread(target=joy,args=(dev,q))
thread2 = threading.Thread(target=play,args=(dev,q))
print('setup')
thread1.start()
thread2.start()
print("Started")
