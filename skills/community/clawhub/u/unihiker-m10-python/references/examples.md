# Natural-Language Programming Examples

## Sound the buzzer

Request: “Sound the buzzer at 440 Hz for half a second.”

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *

Board("UNIHIKER").begin()
buzzer.pitch(440, 0.5)
```

## Tilt alarm

Request: “Warn me on the screen and sound the buzzer when the board tilts past a threshold.”

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()
threshold = 8000

while True:
    strength = accelerometer.get_strength()
    gui.clear()
    if strength > threshold:
        gui.draw_text(text="TILT!", x=80, y=150, color="#FF0000", font_size=28)
        buzzer.pitch(880, 0.1)
    else:
        gui.draw_text(text=f"OK {strength}", x=40, y=150, color="#00FF00")
    time.sleep(0.3)
```

## Blink an LED on P21

```python
from pinpong.board import Board, Pin
import time

Board("UNIHIKER").begin()
led = Pin(Pin.P21, Pin.OUT)

while True:
    led.write_digital(1)
    time.sleep(0.5)
    led.write_digital(0)
    time.sleep(0.5)
```

## Count with A and stop with B

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()
count = 0
running = True

def on_a():
    global count
    count += 1

def on_b():
    global running
    running = False

gui.on_a_click(on_a)
gui.on_b_click(on_b)

while running:
    gui.clear()
    gui.draw_text(text=f"Count: {count}", x=60, y=150, font_size=24, color="#FFFFFF")
    time.sleep(0.1)

gui.clear()
gui.draw_text(text="Stopped", x=70, y=150, color="#00FFFF")
time.sleep(5)
```

## Display a Wi-Fi QR code

```python
from pinpong.board import Board
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()
gui.draw_qr_code(x=40, y=40, w=160, h=160, text="WIFI:S:MySSID;T:WPA;P:password;;")

while True:
    time.sleep(0.05)
```
