from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont
import random
import time
import threading
from ping3 import ping

'''
Description: This program creates a system tray icon that displays the ping time to a host.

Todo:
1. Add a ping host input
2. Add a ping interval input
3. Add GUI for the above inputs
4. Add addtional menu options
5. Add a ping status indicator (red, yellow, green)
'''
#Globals
pingHost = "www.google.com"
pingInterval = 1

def createIconText(text, size):
    image = Image.new('RGBA', (size, size), (255,255,255,1))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype('arial.ttf', size//1.3)
    except IOError:
        font = ImageFont.load_default()

    textbbox = draw.textbbox((0,0), text, font=font)
    textWidth, textHeight = textbbox[2] - textbbox[0], textbbox[3] - textbbox[1] + 20
    textPos = (size//2 - textWidth//2, size//2 - textHeight//2)
    draw.text(textPos, text, font=font, fill="white", align="center")

    return image

def onExit(icon):
    icon.stop()

def pingingMode(icon, host, timeInterval):
    while True:
        pingMs = ping(host, unit="ms")
        icon.icon = createIconText(str(int(pingMs)), 64)
        print(pingMs)
        time.sleep(timeInterval)

initText = "0"
textIcon = createIconText(initText, 64)
menu = Menu(MenuItem('Exit', onExit))
icon = Icon("Test Icon", textIcon, menu=menu)

rngThread = threading.Thread(target=pingingMode, args=(icon, pingHost, pingInterval ), daemon=True)  
rngThread.start()

icon.run()

'''
For rng code testing

def rng(icon):
    while True:
        randnum = random.randint(0, 100)
        icon.icon = createIconText(str(randnum), 64)
        time.sleep(1)

initText = "0"
textIcon = createIconText(initText, 64)
menu = Menu(MenuItem('Exit', onExit))
icon = Icon("Test Icon", textIcon, menu=menu)

rngThread = threading.Thread(target=rng, args=(icon, ), daemon=True)  
rngThread.start()

icon.run()
'''