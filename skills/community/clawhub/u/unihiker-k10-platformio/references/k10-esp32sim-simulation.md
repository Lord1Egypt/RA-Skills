# Simulating UNIHIKER K10 firmware with esp32sim

[esp32sim](https://github.com/mikroverk/esp32sim) is a cycle-approximate ESP32-S3 emulator
written in Rust: it boots the **real** firmware images produced by `pio run`, runs the ESP32-S3
mask ROM and the Arduino/LVGL code on top, and renders the SPI display to a PNG. Nothing is
reimplemented as a mock — what you see is what the firmware drew.

Use it to check layout, colours, animation timing, and button handling without plugging in a
board, which makes it a good fit for classroom prep and for iterating on screen code.

## What is simulated, what is not

| Works | Does not work |
| --- | --- |
| Boot, app start, `setup()`/`loop()` | Camera, microphone, IMU (SC7A20H), light sensor (LTR303ALS) |
| Display: ILI9341 240×320 over SPI, full LVGL/canvas output | ASR wake words, TTS, built-in AI models (no voice model flash contents) |
| Buttons A and B (through the I2C expander) | RGB LED strip beyond the modelled GPIO writes |
| `millis()`, timers, I2C, SPI, UART/`printf` | Wi-Fi-dependent behaviour, OTA in detail |
| Scripted host input (`press`, `gpio`, `stop`) | Real-world electrical edge cases |

Library initialisation for missing devices prints `not found` and continues, so code that
touches several peripherals still reaches the drawing calls. Expect ASR/TTS/face-recognition
projects to verify only their UI in the simulator.

## Prerequisites

- Rust (`cargo`) — Windows also needs the MSVC build tools because cargo links with `link.exe`.
  In China, install Rust through <https://rsproxy.cn>.
- `python3` (or `python`), `curl`, `tar`, and a working PlatformIO K10 build.
- The K10 mask ROM ELF, already shipped inside PlatformIO:
  `~/.platformio/packages/tool-esp-rom-elfs/esp32s3_rev0_rom.elf`. Nothing to download.

There is no official Windows binary; building locally is the supported path (about 4 minutes,
~150 MB in `target/`). The upstream release binaries are macOS/Linux only.

## One-time setup

```bash
bash scripts/k10-sim-setup.sh                  # installs to ~/.k10-esp32sim
bash scripts/k10-sim-setup.sh /opt/esp32sim    # custom location
```

The script downloads the source, drops in the K10 board model
(`references/esp32sim/unihiker_k10.rs`), applies three small source edits, and builds.

- Direct GitHub access is often very slow from CN networks; the script tries `ghfast.top` and
  `gh-proxy.com` mirrors first and falls back to `github.com`. Force one path with
  `K10_SIM_MIRROR=direct`.
- It also points cargo at the `rsproxy.cn` crates mirror unless `.cargo/config.toml` already
  exists. `K10_SIM_CRATES_MIRROR=off` disables that.
- Re-running is safe: an existing source tree is reused and every patch is idempotent.

## Running firmware

```bash
cd my-k10-project && pio run                  # 1. build, as usual
bash /path/to/skill/scripts/k10-sim.sh . 3.0  # 2. run 3 emulated seconds, save one PNG
```

Or verify the setup end to end with the bundled probe project:

```bash
bash scripts/k10-sim.sh --demo     # builds examples/smiley, writes 3 frames to its sim/
```

`k10-sim.sh` finds `.pio/build/*/firmware.bin` automatically, passes the K10 memory geometry
(16 MB flash, 8 MB PSRAM), and saves the final frame to `sim/sim-<seconds>s.png`. Options:
`--out PNG`, `--script FILE`, `--env NAME`, `--console uart0|usb|both|none`, `--show-console`
(print the whole firmware console instead of just the verdict). Environment overrides:
`ESP32SIM`, `ESP32SIM_ROM`.

To drive the firmware, write a script file and pass `--script`:

```text
1.2 press btnA 200     # hold A for 200 ms starting at t = 1.2 s
0.05 gpio 5 1          # drive pad 5 high directly
3.0 stop
```

## Board model facts (hardware behaviour worth remembering)

These are the details that make the firmware behave correctly in the emulator, and they are
also handy when debugging on real hardware.

| Item | Value |
| --- | --- |
| Panel | ILI9341, 240×320, `TFT_eSPI ILI9341_DRIVER` |
| SPI pins | SCLK 12, MOSI 21, CS 14, DC 13 (no MISO) |
| Memory | 16 MB flash, 8 MB PSRAM |
| Buttons | **not on GPIO pads** — I2C GPIO expander PCA9555 at address `0x20` |

The button finding matters: `digital_read()` in the K10 library addresses the expander, never a
pad. If the expander is absent the read returns all zeros, the firmware concludes that A and B
are held down from the first instruction, and any `if (button->isPressed())` branch fires
immediately. That is why the board model does three things:

1. `input_levels()` reports the two button lines high at reset, so nothing reads as pressed.
2. `gpio_input()` maps a scripted `press btnA` onto the expander's input bits.
3. `i2c_devices()` serves `0x20` with input ports defaulting to `0xff`.

## Status line

Each run ends with two report lines:

```text
[emu] stop: Halted — core0 10189964 + core1 44848519 insns in 1.9s wall = 28.9 Minsn/s; emulated 3.000s (720000000 cycles)
[emu] k10 tft: 3 RAMWR, 230400 pixels, madctl=0x88 colmod=0x55 inverted=false on=true bbox=Some((0, 0, 239, 319)) top colours [(efbf, bc94), (fe66, 4e44), (3123, 126c), (d9c9, 334), (fd16, 2c8)]; gpio events 258
```

`RAMWR` counts pushes to the panel, `bbox` is the bounding box of everything written, and
`top colours` gives the dominant RGB565 values — enough to confirm that a redraw really was
partial (a small `bbox` change) rather than a full-screen flash.

## Speed

Roughly 27 M instructions per emulated second on a desktop CPU: three seconds of firmware time
take about two seconds of wall clock. Faster than flashing hardware for pure UI iteration.

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| `cargo not found` | Install Rust; the setup script adds `~/.cargo/bin` to `PATH` itself |
| `link.exe not found` | Install VS 2022 Build Tools with the C++ workload |
| Download stalls near 20 KB/s | Keep the default mirror order, or set `K10_SIM_MIRROR=direct` if GitHub is fast for you |
| Screen stays black | Firmware ran but wrote nothing — check `Serial`/`printf` output, and that `initScreen()`/`creatCanvas()` were called |
| Buttons act pressed at boot | Something reads the expander before the model answers; confirm the board in use is `unihiker-k10`, not `none` |
| Garbage colours or shifted image | Rotation/`madctl` mismatch — the model already undoes MADCTL, so a shift means the firmware set an orientation the panel does not support |
| Empty PNG but a full report line | `--max-seconds` ended before the first draw; raise it |
| `Serial.printf` prints nothing | `Serial` goes to USB CDC: use `--console usb`, or switch the debug line to `printf()` on uart0 |

## CI and clean-up

The emulator is a single executable plus the ROM ELF, so it can be cached between runs
(`~/.k10-esp32sim`). Delete that directory to reclaim ~150 MB; rebuilding takes a few minutes.

Verified on 2026-11 with esp32sim `main`, Rust 1.100, Windows 11 + VS 2022 Build Tools, and a
K10 PlatformIO build (`framework-arduinounihiker`): smiley rendering, 3.2 s blink timing, and
A-button expression switching all matched the source code.
