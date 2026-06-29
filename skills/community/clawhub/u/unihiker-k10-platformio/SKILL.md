---
name: unihiker-k10-platformio
description: Use when programming a UNIHIKER K10 board with PlatformIO CLI, creating or converting Arduino/C++ K10 projects to PlatformIO, building, uploading, monitoring serial output, diagnosing K10 PlatformIO setup, or preparing/installing offline PlatformIO support bundles for workshops where many students should not download toolchains at the same time.
---

# UNIHIKER K10 - PlatformIO

## Overview

Use PlatformIO Core CLI for UNIHIKER K10 Arduino/C++ development. Prefer this skill when the user wants a PlatformIO-based workflow instead of `arduino-cli`, especially for workshops that need predownloaded support files.

Core PlatformIO environment:

```ini
[env:unihiker]
platform = https://github.com/DFRobot/platform-unihiker.git
board = unihiker_k10
framework = arduino
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=None
```

K10 uses DFRobot's PlatformIO platform and Arduino framework package. First build downloads a large framework and toolchains; avoid doing this from every student machine during a workshop.

If a project uses K10 AI, voice recognition, TTS, face recognition, or OTA partitions, preserve the factory model-data offsets. Read the repository reference `references/k10-ai-model-flash.md` when available, or follow the model rules below.

Screen refresh policy: generated K10 display code must prefer partial redraws. Full-screen clearing or full-background redraw causes visible flicker and is uncomfortable; use it only for initialization, page switches, exit cleanup, or when measured full-screen refresh is above 30 fps.

## Quick Workflow

Before writing K10 application code, read the relevant local references:

- `references/k10-arduino-api.md` for K10 C++ API signatures.
- `references/k10-arduino-examples.md` for working examples, including display, RGB, sensors, audio, AI, TTS, and ASR.

1. Check PlatformIO:

```bash
pio --version
```

If missing, install PlatformIO Core using the official installer script or package manager. Do not use sudo/admin unless the user explicitly needs a system-wide install.

2. Create or normalize a K10 project:

```bash
bash path/to/unihiker-k10-platformio/scripts/init-k10-platformio-project.sh my-k10-project
```

3. Put code in `src/main.cpp`. For `.ino` sketches, preserve the same Arduino code but make sure function prototypes/includes are valid C++.

4. Build:

```bash
pio run -d my-k10-project
```

5. Upload:

```bash
pio run -d my-k10-project -t upload --upload-port /dev/cu.usbmodemXXXX
```

If no port is provided, PlatformIO may auto-detect. Use `pio device list` when upload fails or multiple boards are connected.

6. Monitor serial:

```bash
pio device monitor -d my-k10-project --port /dev/cu.usbmodemXXXX
```

## Bundled Scripts

- `scripts/init-k10-platformio-project.sh`: create a minimal K10 PlatformIO project with sample screen code.
- `scripts/k10-pio.sh`: convenience wrapper for `doctor`, `ports`, `build`, `upload`, and `monitor`.
- `scripts/prepare-offline-bundle.sh`: build once, collect K10 PlatformIO support files, and create a distributable `.tgz`.
- `scripts/install-offline-bundle.sh`: install a prepared bundle into a user's PlatformIO core directory.
- `scripts/doctor-offline.sh`: verify that the required K10 PlatformIO packages are present before class.
- `scripts/k10-pio.ps1` and `scripts/install-offline-bundle.ps1`: Windows PowerShell helpers for common operations and bundle installation.

Prefer scripts for repeated workshop setup. Read `references/platformio-workshop.md` before changing offline bundle behavior.

## Workshop Offline Bundle

Use an offline bundle when many learners will build K10 projects in the same room.

Expected support-file sizes after first successful build vary by OS/CPU, but the important K10 pieces are roughly:

| Directory | Purpose | Typical uncompressed size |
| --- | --- | --- |
| `platforms/unihiker` | DFRobot PlatformIO platform | <1 MB |
| `packages/framework-arduinounihiker` | K10 Arduino framework, SDK, libraries | ~500 MB |
| `packages/toolchain-xtensa-esp32s3` | ESP32-S3 compiler toolchain | ~250-300 MB |
| `packages/toolchain-riscv32-esp` | RISC-V helper toolchain used by the K10 build | varies, often large |
| `packages/toolchain-xtensa-esp32` | Base ESP32 toolchain declared by platform; include when present for conservative bundles | ~350-400 MB |
| `packages/tool-esptoolpy` | Upload tool | a few MB |
| `packages/tool-scons` | Build tool | a few MB |
| `packages/tool-mkfatfs`, `tool-mklittlefs`, `tool-mkspiffs` | Filesystem image tools used by some upload targets | a few MB |

A minimal compressed bundle is typically hundreds of MB. Prepare one bundle per OS/architecture: macOS arm64, macOS Intel, Windows, and Linux are not interchangeable.

Bundle preparation flow:

```bash
# On a prepared teacher machine
bash scripts/init-k10-platformio-project.sh /tmp/k10-pio-probe
pio run -d /tmp/k10-pio-probe
bash scripts/prepare-offline-bundle.sh /tmp/k10-platformio-bundle.tgz
```

Student installation flow:

```bash
bash scripts/install-offline-bundle.sh /path/to/k10-platformio-bundle.tgz
bash scripts/doctor-offline.sh
pio run -d my-k10-project
```

If the student machine still tries to download packages, check that the bundle was built on the same OS/CPU architecture and that it was extracted into the same PlatformIO core directory used by `pio`.

If build fails with `ModuleNotFoundError: No module named 'intelhex'` from `tool-esptoolpy`, repair the local PlatformIO Python environment or reinstall PlatformIO Core. This indicates an incomplete PlatformIO tool dependency, not a K10 source-code error.

## Project Conventions

- Use `platformio.ini` at the project root.
- Use `src/main.cpp` for code.
- Keep assets/data files in `data/` only when using filesystem upload features.
- Use `lib/` for private libraries that belong to the project.
- Do not mix `arduino-cli` FQBN settings with PlatformIO project configuration.
- Keep K10 USB serial flags in `build_flags`; they are required for expected USB CDC behavior.
- Treat the PlatformIO skill as self-contained. Do not rely on sibling skills or repository-relative paths for API details after installation from ClawHub.

## K10 API Notes

- Include K10 board APIs with `#include "unihiker_k10.h"`.
- Include speech recognition with `#include "asr.h"`.
- For animations, dashboards, sensor readouts, voice status, OTA status, and other repeated updates, erase and redraw only the changed region. Do not use `canvasClear()` or redraw the full background in a loop unless the measured full-screen refresh rate is above 30 fps.
- For ASR command registration, prefer mutable `char[]` command buffers:

```cpp
char cmdLightOn[] = "kai deng";
asr.addASRCommand(1, cmdLightOn);
```

Avoid `asr.addASRCommand(id, String("..."))` unless the upstream library has been verified fixed. Some K10 ASR library versions recurse in the `String` overload and can trigger a `loopTask` stack canary reset.

## OTA Notes

PlatformIO's DFRobot platform supports normal USB upload with `pio run -t upload`. For OTA-style HTTP uploads used by existing K10 Arduino examples, continue using the existing OTA helper pattern only when the firmware exposes the expected `/ota` endpoint.

For native PlatformIO OTA via ESP OTA, set `upload_protocol = espota` and `upload_port = <ip>` only after confirming the firmware and platform support that route.

When combining OTA with K10 built-in AI features, use a partition table that keeps these regions at the factory offsets:

- `model` at `0x510000`, size `4563K`
- `voice_data` at `0x985000`, size `2542K`
- `fr` at `0xC01000`, size `100K`

Use 2.5 MB OTA app slots ending exactly before `0x510000`. Do not use generic 6 MB OTA slots for AI projects, because they overlap the model region.

For model recovery or first initialization, add separate USB-only environments:

```ini
[env:unihiker]
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=None

[env:unihiker-init-cn]
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=CN

[env:unihiker-init-en]
build_flags =
    -DARDUINO_USB_CDC_ON_BOOT=1
    -DARDUINO_USB_MODE=1
    -DModel=EN
```

Use `unihiker-init-cn` for the Chinese model and `unihiker-init-en` for the English model only when model data may be missing or damaged. Use `unihiker` for normal app uploads and OTA builds.

## References

- Read `references/platformio-workshop.md` for offline bundle preparation, installation, and troubleshooting.
- Read `references/k10-ai-model-flash.md` for AI model partitions, OTA compatibility, and recovery workflow.
- Read `references/k10-arduino-api.md` for K10 API signatures.
- Read `references/k10-arduino-examples.md` for complete K10 Arduino examples. The C++ APIs are the same as Arduino mode; only the build/upload toolchain changes.
