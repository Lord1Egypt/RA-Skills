# UNIHIKER M10 Hardware Reference

## Architecture

- **CPU:** RK3308 quad-core 1.2 GHz, 512 MB RAM, 16 GB eMMC, Debian 10, Wi-Fi, and Bluetooth.
- **Coprocessor:** GD32VF103 RISC-V, controlled through PinPong for onboard components and external I/O.
- **Display:** 2.8-inch 240x320 color touchscreen controlled through `unihiker.GUI`.

## Onboard components

| Object | Component | Common API |
|---|---|---|
| `light` | Light sensor | `light.read()` |
| `accelerometer` | Three-axis accelerometer | `get_x()`, `get_y()`, `get_z()`, `get_strength()` |
| `gyroscope` | Three-axis gyroscope | `get_x()`, `get_y()`, `get_z()` |
| `button_a`, `button_b` | Physical buttons | `is_pressed()`; GUI callbacks are usually easier |
| `buzzer` | Passive buzzer | `buzzer.pitch(freq, beat)` |

## Interfaces

- USB Type-C for power and the computer connection; the board normally uses `10.1.2.3`.
- USB Type-A for peripherals.
- microSD storage expansion.
- Three 3-pin I/O ports with PWM and ADC support.
- Independent 4-pin I2C port.
- A 19-I/O edge connector compatible with micro:bit pin numbering.

Common edge pins are `P0` through `P20`; some are reserved by onboard hardware. Use `Pin(Pin.Px, Pin.IN/OUT/ANALOG)` for external devices.

## Network and Python defaults

- USB/AP address: `10.1.2.3`.
- Example Wi-Fi DHCP address: `192.168.199.102`.
- Factory-default SSH login: `root` / `dfrobot`.
- Common interpreter: `/root/.pyenv/versions/3.12.7/bin/python3`.
- Common packages: `unihiker==0.0.29.0`, `pinpong==0.6.2`.

Treat these values as known examples and prefer live detection.
