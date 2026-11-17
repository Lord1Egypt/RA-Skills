# K10 Box Troubleshooting

## Third LVGL page crashes or resets

Evidence:

```text
LoadProhibited
_vsnprintf -> lv_vsnprintf -> _lv_txt_set_text_vfmt
-> lv_label_set_text_fmt -> render...
```

Cause: a large LVGL variadic formatting call mixes floats and strings.

Fix: build the complete label in a bounded `char[]` with `snprintf`, then pass
it to `lv_label_set_text`.

## Temperature or humidity is blank

Cause: the bundled LVGL formatter has float support disabled.

Fix: keep the sensor values as floats, but format them with newlib `snprintf`
before updating the LVGL label.

## K10 ACC X/Y/Z stays at zero

Check startup serial output for:

```text
SC7A20H Device not found
```

`k10.getAccelerometerX/Y/Z()` reads K10-native SC7A20H at `0x19`. The box uses
a different QMI8658 at `0x6B`. Do not silently substitute one API for the other
without changing the UI label. Probe QMI8658 chip ID and show box acceleration
when the intended hardware is the experiment box.

## Box QMI8658 has no data

1. Call `box.begin()`.
2. Read chip ID and expect `0x05`.
3. Call `box.initQMI8658C()` only when present.
4. Avoid conversion if `ssvtA` or `ssvtG` was not initialized.
5. Print chip ID and converted values to serial before blaming LVGL.

## Motor stage logs appear, but motors do not move

Do not treat `ACTUATOR=BOX motor...` as proof of physical output.

1. Increase the diagnostic pulse from `90/255` for 300 ms to the upstream
   hardware-test value `255/255`; hold about 800-1000 ms.
2. Stop for about 400 ms before reversing.
3. Confirm the IO controller at `0x20` responds.
4. Look for a large simultaneous QMI8658 change or directly observe the wheel.
5. If full-duty commands still cause no movement, inspect motor power, the box
   power switch, motor connectors, and mechanical binding.
6. Always issue speed `0` after the test.

The upstream driver's M2 path relies on the PWM group initialized by the M1
path. Initialize or stop M1 before testing M2 in isolation, or use the driver's
normal M1-then-M2 sequence.

## Sensors intermittently disappear

All devices share `Wire`. Avoid concurrent background reads where possible.
Use synchronous AHT20 sampling, keep box I2C access in `loop()`, and let button
callbacks change atomics only.

## Ultrasonic always reports 65535

`0xFFFF` is the driver's invalid/no-result sentinel. Check sensor connection and
target range, and render `--` while invalid.

## Upload port is busy

Stop any active `pio device monitor` session before upload. Then re-check:

```bash
pio device list
pio run -t upload --upload-port /dev/cu.usbmodemXXXX
```

## Runtime verification checklist

After the final code change:

```bash
git diff --check
pio run
pio run -t upload --upload-port /dev/cu.usbmodemXXXX
pio device monitor --port /dev/cu.usbmodemXXXX --baud 115200
```

Confirm:

- Build and upload both report `SUCCESS`; flash hashes verify.
- QMI chip ID is `0x05` and acceleration changes with orientation.
- Temperature and humidity are plausible and visible.
- Every page can be selected without a reset.
- Actuator sequence reaches completion and emergency stop returns to idle.
- Motor verification includes physical movement or clear IMU motion evidence.
