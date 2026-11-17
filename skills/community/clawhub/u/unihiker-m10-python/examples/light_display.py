"""NL demo: show light sensor on screen for 5 seconds."""
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()

for _ in range(10):
    v = light.read()
    gui.clear()
    gui.draw_text(text=f"Light: {v}", x=30, y=150, color="#FFFF00", font_size=22)
    time.sleep(0.5)

print("done")
