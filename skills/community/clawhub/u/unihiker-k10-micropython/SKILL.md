---
name: unihiker-k10-micropython
description: Use when programming Unihiker K10 board with MicroPython, uploading code, flashing firmware, or accessing K10 MicroPython APIs (screen, sensors, RGB, audio, AI)
---

# Unihiker K10 - MicroPython

## Overview

CLI toolkit for Unihiker K10 board MicroPython programming. **Core principle:** Follow reference docs exactly—no improvisation.

Screen refresh policy: always design K10 display code around partial redraws. Full-screen clearing or full-background redraw causes obvious flicker and is uncomfortable; use it only for initialization, page switches, exit cleanup, or when you have measured full-screen refresh above 30 fps.

## When to Use

- Uploading MicroPython code to K10
- Flashing MicroPython firmware
- Looking up K10 MicroPython APIs (screen, sensors, RGB, audio, AI)
- Port detection or connectivity issues

## Commands

| Command | Description |
|---------|-------------|
| `k10-micropython upload-mp <file.py>` | Upload MicroPython |
| `k10-micropython flash-mp` | Flash MicroPython firmware |
| `k10-micropython ports` | List serial ports |
| `k10-micropython doctor` | Environment diagnostic |

## Coding

### Basic Template

```python
from unihiker_k10 import screen
screen.init(dir=2)
screen.draw_text(text="Hello", x=10, y=0, font_size=24, color=0xFF0000)
screen.show_draw()
```

**Important:**
- **Auto-execution**: Only `main.py` runs automatically on boot. Other filenames (e.g., `test.py`) must be imported or run via REPL
- **Best practice**: Name your entry file as `main.py` for auto-start
- **Screen refresh**: 默认局部刷新。除初始化、页面切换、退出清理，或实测全屏刷新率超过 30 fps 外，不要在循环里调用 `screen.clear()` 或整屏 `screen.show_bg()`。
- **Reference**: [`references/micropython-api.md`](references/micropython-api.md)

## Common Issues

| Issue | Solution |
|-------|----------|
| **MicroPython code doesn't run** | Only `main.py` runs automatically. Rename your file or use REPL to run it |
| **Flash failed** | Make sure BOOT button is held when connecting USB to enter download mode |
| **mpremote: could not enter raw repl** | K10 is running Arduino, flash MicroPython firmware first |
| Port not found | `k10-micropython ports` or hold BOOT while connecting |
| **AI + WiFi conflict** | Use only one in V0.9.2 |
| **屏幕闪烁** | 使用局部刷新，避免循环中频繁调用 `screen.clear()` 或整屏 `screen.show_bg()`；只有实测全屏刷新超过 30 fps 才可高频全屏刷新 |
| **Windows PowerShell执行策略限制** | 运行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |

## 开发经验教训

### 2025-03-22 实践总结

**与Arduino模式的区别：**
1. **固件互斥**: K10不能同时运行Arduino和MicroPython固件，需要刷写对应固件
2. **入口文件**: MicroPython只有`main.py`会自动运行，其他文件需要手动import
3. **工具链不同**: Arduino使用arduino-cli，MicroPython使用mpremote

**刷写MicroPython固件步骤：**
1. 按住BOOT按钮
2. 按RST按钮重置
3. 释放BOOT按钮
4. 运行刷写命令
5. 等待完成(30-60秒)
6. 按RST重启

**注意事项：**
- V0.9.2固件中AI功能和WiFi不能同时使用，会导致内存溢出
- 首次刷写后建议先上传简单的main.py测试

## Files

```
unihiker-k10-micropython/
├── SKILL.md                 # This file
└── references/            # MicroPython API docs
    └── micropython-api.md # MicroPython API reference
```

**Manual usage without CLI:**
```bash
# Upload MicroPython
bash path/to/unihiker-k10-micropython/scripts/upload-micropython.sh main.py /dev/cu.usbmodem2201

# Flash MicroPython firmware
bash path/to/unihiker-k10-micropython/scripts/flash-micropython.sh /dev/cu.usbmodem2201
```

## MicroPython Code Execution

- **Automatic execution**: Files named `main.py` run automatically after upload and reset
- **Manual execution**: Other filenames require REPL interaction:
  ```bash
  # Connect to REPL
  mpremote connect /dev/cu.usbmodem2201 repl
  
  # Import and run your module
  >>> import test
  ```

**File naming best practice:**
```
your_project/
├── main.py          # Entry point - runs automatically on boot
├── test.py          # Test file - must be imported via REPL
└── heart.py         # Other files - import with `import heart`
```

## Flashing MicroPython Firmware

**Method 1: Manual (Recommended)**
1. Hold BOOT button on K10
2. Press RST button on K10
3. Release BOOT button
4. Run: `k10-micropython flash-mp` or `k10-micropython flash-mp --port /dev/cu.usbmodem2201`
5. Wait for flash to complete (30-60 seconds)
6. Press RST button on K10 to restart
7. Upload Python code with `k10-micropython upload-mp file.py`

**Method 2: Interactive**
1. Run: `k10-micropython flash-mp`
2. Follow on-screen prompts
3. Hold BOOT button, connect USB, release BOOT

## Quick Development Workflow

```bash
# 1. Create MicroPython script
echo "from unihiker_k10 import screen
screen.init(dir=2)
screen.draw_text(text='Hello K10', x=10, y=0, font_size=24, color=0xFFFFFF)
screen.show_draw()" > main.py

# 2. Upload as main.py for auto-run
k10-micropython upload-mp main.py

# 3. Or test as test.py and run via REPL
k10-micropython upload-mp test.py
mpremote connect /dev/cu.usbmodem2201 repl
>>> import test
```

## Key Features

**Screen:**
- Screen initialization and direction control
- Text drawing with custom font size and color
- Shape drawing: lines, circles, rectangles, points
- Image display from TF card
- QR code generation and display

**Sensors:**
- Buttons A/B (callback and status check)
- Accelerometer (X, Y, Z axes)
- Temperature & humidity (AHT20)
- Light sensor (ALS)
- Microphone (recording to TF card)

**RGB LED Control:**
- Individual LED control (0, 1, 2)
- All LEDs control (-1)
- Brightness control (0-9)

**Audio:**
- Buzzer control (playTone)
- Microphone recording to TF card

**AI Features (V0.9.2):**
- **Face Detection**: Detect faces, show length, width, center coordinates
- **Face Recognition**: Enroll faces, recognize faces, display ID
- **Cat Recognition**: Detect and classify cats (with TF card images)
- **Movement Detection**: Motion detection with customizable threshold
- **QR Code Scanning**: Scan QR codes and display content
- **Speech Recognition**: Wake-up command and voice commands

**Note on AI:**
- AI functionality is resource-intensive in V0.9.2 firmware
- AI + WiFi conflict: Use only one at a time to avoid memory overflow

## Performance Tips

### Screen Rendering Optimization

K10 的屏幕刷新率有限。循环动画、传感器数值刷新、倒计时、状态提示等场景中，如果每帧都调用 `screen.clear()` 或整屏 `screen.show_bg()`，屏幕容易出现明显闪烁、卡顿，观感很不舒服。默认必须采用**局部刷新**。除初始化、页面切换、退出清理，或实测全屏刷新率超过 30 fps 外，不要使用全局刷新。

**核心原则：**
1. 静态背景只绘制一次
2. 只擦除和重绘发生变化的区域
3. 用背景色覆盖旧内容，再在同一区域绘制新内容
4. 只在完成本轮局部绘制后调用一次 `screen.show_draw()`

**避免：**

```python
while True:
    screen.clear()
    screen.draw_text(text=str(value), x=10, y=20, font_size=24, color=0xFFFFFF)
    screen.show_draw()
```

**推荐：**

```python
last_text = ""

screen.show_bg(color=0x000000)
screen.draw_text(text="Value:", x=10, y=20, font_size=24, color=0xFFFFFF)
screen.show_draw()

while True:
    text = str(value)
    if text != last_text:
        screen.draw_rect(x=100, y=20, w=80, h=28, bcolor=0x000000, fcolor=0x000000)
        screen.draw_text(text=text, x=100, y=20, font_size=24, color=0x00FF00)
        screen.show_draw()
        last_text = text
```

整屏刷新只用于页面切换、初始化、退出清理等低频场景；高频更新必须优先局部刷新。若确实想高频整屏刷新，先实测全屏刷新率，低于或等于 30 fps 时必须改成局部刷新。

## Example: Face Recognition with LED Feedback

```python
import ai
from unihiker_k10 import screen, rgb, button
import time

def callback(data):
    if data == 1:
        screen.draw_text(text="录入中...", x=10, y=90, font_size=24, color=0xFFFF00)
    elif data >= 0:
        screen.draw_text(text=f"人脸ID: {data}", x=10, y=90, font_size=24, color=0x00FF00)
    screen.show_draw()

screen.init(dir=2)
screen.show_bg(color=0x000000)
screen.draw_text(text="A: 录入", x=10, y=50, font_size=18, color=0xFFFF00)
screen.draw_text(text="B: 删除全部", x=10, y=70, font_size=18, color=0xFF0000)
screen.draw_text(text="LED: 红色=未知", x=10, y=110, font_size=18, color=0xFF0000)
screen.draw_text(text="   绿色=已识别", x=10, y=130, font_size=18, color=0x00FF00)
screen.show_draw()

rgb.brightness(9)

ai.init_ai()
ai.camera_start()
ai.face_recognize_start()
ai.send_face_cmd(2)  # Recognition mode
ai.set_asr_callback(callback)

try:
    while True:
        image_data = ai.camera_capture()
        screen.show_camera_img(image_data)
        time.sleep_ms(1)
except KeyboardInterrupt:
    print("Exiting...")
    ai.deinit_ai()
    rgb.brightness(0)
    screen.clear()
```

**Features:**
- **Face Enroll (A button)**: `ai.send_face_cmd(1)` - Green LED
- **Face Recognition (automatic)**: Display ID, Green LED
- **Unknown face**: Red LED
- **Delete all faces (B button)**: `ai.send_face_cmd(3)` - Clear stored faces
- **Camera display**: Show real-time camera feed on screen
