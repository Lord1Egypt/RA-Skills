"""Blink LED on P24 five times."""
from pinpong.board import Board, Pin
from pinpong.extension.unihiker import *
import time

Board("UNIHIKER").begin()
led = Pin(Pin.P24, Pin.OUT)

for i in range(5):
    led.write_digital(1)
    time.sleep(0.5)
    led.write_digital(0)
    time.sleep(0.5)
    print(f"blink {i + 1}/5")

print("done")
