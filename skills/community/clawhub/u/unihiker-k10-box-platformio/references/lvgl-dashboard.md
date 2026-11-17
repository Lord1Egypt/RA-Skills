# LVGL Dashboard and Actuator Patterns

## Recommended pages

Use a compact four-page dashboard:

1. K10 temperature, humidity, ambient light, microphone, and A/B state plus box
   QMI8658 acceleration X/Y/Z and vector magnitude.
2. Box knob, sound, IR code, ultrasonic distance, left/right keys,
   conductance, and infrared obstacle state.
3. Box QMI8658 gyroscope X/Y/Z plus five-channel line raw values, thresholds,
   and digital status.
4. Explicitly triggered actuator self-test with current stage, supported output
   list, motor power, start instructions, and emergency-stop instructions.

This layout keeps source identity visible. Label QMI8658 values as box data;
never label them as the K10-native SC7A20H.

## LVGL initialization

Initialize the display only through the K10 BSP:

```cpp
k10.begin();
k10.initScreen(2);
```

Create LVGL objects after this call. Do not initialize a second LCD driver and
do not mix repeated Canvas redraws with the same LVGL screen.

Update label text or other changed widgets only. Full-screen clearing in the
sensor loop causes visible flicker.

## Safe formatting

The K10 BSP's LVGL configuration sets `LV_SPRINTF_USE_FLOAT` to `0`. Format
floating-point values through the ESP32 C library:

```cpp
char text[384];
snprintf(text, sizeof(text),
         "Temperature %5.1f C\nHumidity %5.1f %%\nACC X %7.1f mg",
         temperatureC, humidityRh, boxAccXmg);
lv_label_set_text(contentLabel, text);
```

Do not use `lv_label_set_text_fmt` for floats. A large variadic call mixing
multiple floats and `String::c_str()` arguments can crash in `_vsnprintf` via
`lv_vsnprintf` and `_lv_txt_set_text_vfmt`.

## Button and thread boundary

K10 button callbacks run in button tasks. Queue intent only:

```cpp
std::atomic<int> pendingPageDelta{0};

void requestNextPage() {
  pendingPageDelta.fetch_add(1, std::memory_order_relaxed);
}
```

Consume the flag and perform every LVGL call from `loop()`. The same rule
applies to an A+B actuator-test callback.

Wire the callbacks explicitly after `k10.begin()`:

```cpp
std::atomic<bool> pendingActuatorStart{false};
std::atomic<bool> pendingActuatorStop{false};

void requestActuatorTest() {
  pendingActuatorStart.store(true, std::memory_order_relaxed);
}

k10.buttonA->setPressedCallback(requestPreviousPage);
k10.buttonB->setPressedCallback(requestNextPage);
k10.buttonAB->setPressedCallback(requestActuatorTest);
```

When A+B is held, suppress the individual A/B navigation requests so the
combined gesture cannot start a test and immediately navigate away. Apply page
changes and actuator flags in `loop()`, then sample sensors and render:

```cpp
void loop() {
  handleSerialCommands();
  applyPendingPageChange();
  updateActuatorTest();
  sampleAndRenderWhenDue();
  lv_timer_handler();
  delay(5);
}
```

For diagnostics, accept serial commands such as:

- `n` / `p`: next or previous page.
- `t`: start actuator test.
- `x`: emergency stop.

## Knob-controlled motors

Map the box angle knob to both DC motors only on an explicit motor-control
screen. Use a left dead zone and preserve enough duty to overcome geared-motor
starting friction:

```cpp
constexpr uint16_t kDeadZone = 64;
constexpr uint16_t kKnobMax = 4095;
constexpr uint8_t kMinimumRunningSpeed = 90;

uint8_t knobToMotorSpeed(uint16_t knob) {
  if (knob <= kDeadZone) return 0;
  if (knob >= kKnobMax) return 255;
  return kMinimumRunningSpeed +
         (static_cast<uint32_t>(knob - kDeadZone) *
          (255 - kMinimumRunningSpeed)) /
             (kKnobMax - kDeadZone);
}
```

Initialize M1 before M2 because the upstream driver shares PWM setup across the
two paths. Update around every 100 ms, skip unchanged PWM values, and stop both
motors when leaving the control screen, pressing the stop control, or handling
an error. Do not start knob motor control automatically at boot.

## Sensor sampling

- Sample sensors around every 500 ms and print a concise serial summary around
  every 1 s.
- Use the base `DFRobot_AHT20` synchronously if the K10 convenience wrapper's
  background task causes shared-`Wire` contention.
- Read QMI8658 once, then convert all six raw fields.
- Treat ultrasonic `0xFFFF` as invalid and display `--`, not `65535 cm`.

## Actuator state machine

Never run a motor self-test automatically on boot. Require A+B or a serial `t`
command and provide `x` as an emergency stop.

A safe, observable sequence is:

1. Box red, yellow, and green LEDs, 500 ms each.
2. K10 RGB red, green, and blue, 500 ms each.
3. Box buzzer, then a short K10 speaker tone.
4. M1 forward, stop, reverse.
5. M2 forward, stop, reverse.
6. Shut down every output and report completion.

Use a non-blocking `millis()` state machine for the sequence. The official box
test uses motor speed `255`; use `255` for 800 ms per direction when a lower
short pulse cannot start the geared motors. Insert a 400 ms stop interval before
reversal. Warn the user to lift the wheels or clear the area first.

Centralize shutdown:

```cpp
void stopAllActuators() {
  music.stopPlayTone();
  k10.rgb->brightness(0);
  k10.rgb->write(-1, 0x000000);
  if (boxIoAvailable) {
    box.red_digital(0);
    box.yellow_digital(0);
    box.green_digital(0);
    box.stopBuzzer();
    box.setMotor1Run(0, 0);
    box.setMotor2Run(0, 0);
  }
}
```

Call it at startup, completion, cancellation, and when leaving the test page.
