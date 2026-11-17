"""Display a persistent hello message on the M10 screen."""
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()
gui.clear()
gui.draw_text(
    text="Hello, UNIHIKER!",
    x=35,
    y=150,
    color="#00FF00",
    font_size=24,
)

print("The hello message is visible on the M10 display.")

while True:
    time.sleep(0.05)
