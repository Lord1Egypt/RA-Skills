---
name: unihiker-k10-box-platformio
description: Use when building, uploading, or debugging PlatformIO Arduino/C++ projects for the UNIHIKER K10 information-technology experiment box (K10 试验盒), especially LVGL sensor dashboards or games, QMI8658 six-axis control, microphone FFT visualizers and sound-reactive lights, DFRobot_K10Box integration, knob-controlled motors, actuator tests, or K10-native versus box-hardware conflicts.
---

# UNIHIKER K10 Box - PlatformIO

## Overview

Build and diagnose PlatformIO applications for the K10 experiment box without
confusing K10-native devices with the box's I2C controller, IMU, line tracker,
and actuators. Keep display, sensor, and actuator work non-blocking and safe.

## Required Reading

Before writing hardware code, read `references/hardware-map.md` completely.

Then read only the task-specific reference:

- Read `references/lvgl-dashboard.md` for LVGL pages, live sensor displays,
  button callbacks, knob-controlled motors, or actuator self-tests.
- Read `references/audio-fft.md` for microphone waveforms, FFT spectra,
  dominant-frequency detection, dBFS loudness, or sound-reactive lights.
- Read `references/six-axis-games.md` for QMI8658 tilt/flick controls, motion
  calibration, or an LVGL Snake-style game.
- Read `references/troubleshooting.md` for missing values, crashes, motors that
  do not move, I2C contention, upload failures, or runtime verification.

## Create or Normalize a Project

Use this PlatformIO environment:

```ini
[env:unihiker]
platform = https://github.com/DFRobot/platform-unihiker.git
board = unihiker_k10
framework = arduino
monitor_speed = 115200
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=None
```

Install the pinned experiment-box driver into an existing project:

```bash
bash path/to/unihiker-k10-box-platformio/scripts/install-k10-box-driver.sh /path/to/project
```

The script refuses to replace `lib/DFRobot_K10Box` unless `--force` is passed.
It downloads DFRobot's MIT-licensed driver at a fixed commit and applies three
small ESP32/PlatformIO compatibility fixes.

Include both hardware layers explicitly:

```cpp
#include <lvgl.h>
#include <unihiker_k10.h>
#include "DFRobot_K10Box.h"

UNIHIKER_K10 k10;
DFRobot_K10Box box;
```

Initialize in this order:

```cpp
k10.begin();
k10.initScreen(2);       // Initialize LCD and LVGL exactly once.
box.begin();             // Box I2C bus: SDA 47, SCL 48.

uint8_t qmiChipId = box.readQMI8658CID();
bool boxImuAvailable = qmiChipId == 0x05;
if (boxImuAvailable) {
  box.initQMI8658C();
}
```

Probe box IO address `0x20` before allowing actuator tests. Never divide raw
QMI8658 values by `ssvtA` or `ssvtG` unless chip ID `0x05` was detected and the
IMU was initialized.

## Implementation Rules

- Keep K10-native and box values in separately named fields such as
  `boardAmbientLight` and `boxAccX`.
- Treat K10 SC7A20H `0x19` and box QMI8658 `0x6B` as different sensors. Do not
  present an absent SC7A20H as valid `(0,0,0)` data.
- Read QMI8658 once per refresh with `getQMI8658xyz()`, then convert all six
  public raw fields. Do not trigger six redundant I2C transactions.
- For motion controls, calibrate a neutral pose before accepting input and keep
  accelerometer and gyroscope units explicit (`mg` and `dps`).
- Perform LVGL calls only from Arduino's main loop. Button-task callbacks may
  update atomics or flags, but must not touch LVGL objects.
- Prefer partial widget updates. Do not clear or redraw the whole screen in a
  sensor loop.
- Format floats with `snprintf`, then call `lv_label_set_text`. The bundled
  LVGL build disables float formatting and its variadic formatter can crash on
  mixed float/string argument lists.
- Run actuator tests only after an explicit user action. Stop all motors,
  buzzer, and LEDs on completion, cancellation, page exit, and startup.
- Treat the K10 I2S microphone as K10-native hardware even when its spectrum
  drives box LEDs. Do not confuse box sound-level ADC data with microphone PCM.
- The box driver exposes DC motors, red/yellow/green LEDs, and a buzzer. It does
  not expose a servo API.

## Build, Upload, and Verify

```bash
pio run -d /path/to/project
pio device list
pio run -d /path/to/project -t upload --upload-port /dev/cu.usbmodemXXXX
pio device monitor -d /path/to/project --port /dev/cu.usbmodemXXXX --baud 115200
```

Verification must cover the user's actual failure mode:

- Confirm I2C identities (`0x20`, `0x30`, QMI chip ID `0x05`) in serial logs.
- Navigate every LVGL page and watch for resets or exception backtraces.
- Confirm temperature, humidity, and box acceleration are non-placeholder
  values.
- For motors, do not accept an `ACTUATOR=...` log alone. Confirm physical
  movement or a strong contemporaneous QMI8658 change, then issue the stop
  command and confirm outputs return to idle.

## Upstream Source

The box driver comes from DFRobot's extension repository:

```text
https://gitee.com/zhaoruiz/ext-unihiker-k10-box
```

The installer pins commit `cde0ad33a6c76089b72a8b73fd74ae71213cf1c7`.
