# M10 Code Templates

## 1. Persistent static display

Drawing and immediately exiting makes the content disappear. Keep the process alive.

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()
gui.clear()
gui.draw_text(text="M10 Ready", x=40, y=150, color="#00FF00", font_size=20)

while True:
    time.sleep(0.05)
```

## 2. Button or GUI event loop

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()

def on_a():
    buzzer.pitch(440, 0.2)
    gui.draw_text(text="A!", x=100, y=150, color="#FF0000")

gui.on_a_click(on_a)
while True:
    time.sleep(0.05)
```

## 3. Sensor polling

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()

while True:
    ax = accelerometer.get_x()
    ay = accelerometer.get_y()
    az = accelerometer.get_z()
    gui.clear()
    gui.draw_text(text=f"X:{ax} Y:{ay} Z:{az}", x=10, y=140, color="#FFFFFF", font_size=16)
    time.sleep(0.2)
```

## 4. GPIO output

```python
from pinpong.board import Board, Pin
import time

Board("UNIHIKER").begin()
led = Pin(Pin.P21, Pin.OUT)

for _ in range(5):
    led.write_digital(1)
    time.sleep(0.3)
    led.write_digital(0)
    time.sleep(0.3)
```

## 5. Audio

```python
from pinpong.board import Board
from unihiker import Audio

Board("UNIHIKER").begin()
audio = Audio()
audio.record("/tmp/rec.wav", 3)
audio.play("/tmp/rec.wav")
```

## 6. Network API structure

Ask which service the user selected, obtain any required API key through a safe credential mechanism, and confirm that the M10 has internet access. Do not place credentials directly in generated source.

```python
from unihiker import GUI, Audio
import os
import requests

api_key = os.environ["SERVICE_API_KEY"]
# 1. Record audio -> 2. ASR -> 3. LLM -> 4. TTS -> 5. display/playback
```
