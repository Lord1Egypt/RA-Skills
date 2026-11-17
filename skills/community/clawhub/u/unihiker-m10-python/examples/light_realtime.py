"""Real-time light sensor display on M10 screen."""
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()

while True:
    v = light.read()
    gui.clear()
    gui.draw_text(text=f"Light: {v}", x=20, y=140, color="#FFFF00", font_size=28)
    time.sleep(0.3)
