# UNIHIKER and PinPong API Reference

These signatures were inspected on an M10 running Python 3.12.7. Use the PinPong board name `UNIHIKER`.

## Initialization

```python
from pinpong.board import Board, Pin
from pinpong.extension.unihiker import *
from unihiker import GUI, Audio, UNIConfig

Board("UNIHIKER").begin()
```

## `unihiker.GUI` on the 240x320 display

| Method | Purpose |
|---|---|
| `draw_text(text, x, y, color, font_size, font_family)` | Draw text |
| `draw_digit(text, x, y, color, font_size)` | Draw large digits |
| `draw_rect` / `fill_rect` | Draw or fill a rectangle |
| `draw_circle` / `fill_circle` | Draw or fill a circle |
| `draw_line(x0, y0, x1, y1, color, width)` | Draw a line |
| `draw_point(x, y, color)` | Draw a point |
| `draw_image(x, y, w, h, image)` | Draw an image from a path |
| `draw_emoji(x, y, w, h, emoji, duration)` | Draw an emoji |
| `draw_qr_code(x, y, w, h, text)` | Draw a QR code |
| `clear()` | Clear the display |
| `update()` | Refresh the display |

Widgets: `add_button(...)`, `add_text_box(...)`, and `add_list_box(...)`.

Input: `on_a_click(fn)`, `on_b_click(fn)`, `on_key_click(event, fn)`, `wait_a_click()`, `wait_b_click()`, and `wait_key_click(event)`.

Threads: `start_thread(callback)` and `stop_thread(thread)`.

## `unihiker.Audio`

| Method | Purpose |
|---|---|
| `record(file, duration, target_volume=-20)` | Synchronous recording |
| `start_record(file)` / `stop_record()` | Asynchronous recording |
| `play(file_path)` | Play a file |
| `start_play` / `stop_play` / `pause_play` / `resume_play` | Playback control |
| `sound_level()` / `sound_dBFS()` | Measure sound level |

## `unihiker.UNIConfig`

- `set_brightness(brightness)` sets display brightness from 0 to 100.

## `pinpong.board.Pin`

```python
p = Pin(Pin.P0, Pin.OUT)  # or Pin.IN / Pin.ANALOG
p.write_digital(1)
p.read_digital()
p.write_analog(duty)
p.read_analog()
p.on()
p.off()
p.irq(trigger, handler)
```

## Onboard `pinpong.extension.unihiker` objects

- Light: `light.read()`, `light.read_and_average(num_reads=5)`.
- Accelerometer: `get_x()`, `get_y()`, `get_z()`, `get_alldata()`, `get_strength()`.
- Gyroscope: `get_x()`, `get_y()`, `get_z()`.
- Buttons: `button_a.is_pressed()`, `button_b.value()`, `irq(trigger, handler)`.
- Buzzer: `pitch(freq, beat=None)`, `play(index, options)`, `stop()`, `set_tempo(ticks, bpm)`, `redirect(pin)`.

## Board helpers

```python
Board("UNIHIKER").begin()
Board.get_i2c_master(bus_num=0)
Board.get_spi_master(...)
Board.disconnect()
```
