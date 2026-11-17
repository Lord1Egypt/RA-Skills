# QMI8658 Six-Axis LVGL Games

## Use the box IMU explicitly

For experiment-box motion games, use the box QMI8658 at `0x6B`, not the K10
SC7A20H at `0x19`. Require chip ID `0x05`, call `initQMI8658C()`, then read one
raw sample with `getQMI8658xyz()` and convert all six axes using `ssvtA` and
`ssvtG`.

Sample around every 40 ms. Keep LVGL and game-state mutations in Arduino's
`loop()`; an A+B callback should set only an atomic reset flag.

## Calibrated tilt and flick control

On boot or reset, average about 0.6 seconds of accelerometer X/Y readings while
showing a `KEEP LEVEL... CALIBRATING` status. After calibration, wait for the
first intentional tilt or flick before starting game movement. This prevents a
Snake game from immediately driving into a wall while the user is still
setting the box down.

A tested control mapping is:

```cpp
float horizontal = (accXmg - centerAccXmg) + gyroYdps * 2.5F;
float vertical   = (accYmg - centerAccYmg) - gyroXdps * 2.5F;

if (fabsf(horizontal) >= 180.0F || fabsf(vertical) >= 180.0F) {
  // Choose the axis with the larger absolute value.
}
```

Acceleration provides steady tilt while the cross-axis gyro terms improve
quick flick response. Reject an immediate 180-degree reversal against the
direction used for the current game tick. Use the magnitude of gyro X/Y/Z for
an optional post-game shake restart; about 420 dps is a conservative starting
threshold. Also keep A+B as a deterministic reset and recalibration control.

Treat these values as tested defaults, not universal calibration constants.
Expose them as named constants and tune them against the assembled box
orientation if the axes or sensitivity feel reversed.

## Snake display pattern

An 18 x 18 grid with 12-pixel cells fits a 216 x 216 board on the K10's
240 x 320 display. A true-color LVGL canvas buffer for that board consumes about
91 KiB; the tested firmware used about 35.5% of the K10's 320 KiB RAM.

Redraw the game canvas rather than clearing the full LVGL screen. Keep the
header, score, best score, and control hint as separate widgets. Useful runtime
states are `CALIBRATE`, `WAIT`, `RUN`, and `GAME_OVER`.

Core game rules:

- Store cells in a fixed-size array; avoid heap allocation during play.
- Update direction from IMU samples independently of the slower movement tick.
- Start around 230 ms per cell and decrease toward a 90 ms floor as score rises.
- Check wall and self collision before shifting the body.
- Exclude the departing tail cell from collision when the snake is not growing.
- Place food outside the body and keep a deterministic full-grid fallback.

## Output safety and verification

A motion game does not need box actuators. At startup, explicitly stop both
motors, the buzzer, traffic lights, and K10 RGB LEDs; never reuse their state
from a previously flashed program.

Print the QMI chip ID, six converted values, game state, score, and length about
once per second. Verify on hardware that:

- The chip ID is `0x05` and all six values change with motion.
- A stationary calibrated box remains in `WAIT` without moving the snake.
- Tilting starts `RUN` and changes direction without illegal reversal.
- Eating food increments both score and length.
- A+B resets and recalibrates; shake restart works only after game over.
- Upload logs show flash hash verification and no runtime reset/backtrace.
