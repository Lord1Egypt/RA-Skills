---
name: unihiker-k10-platformio
description: Use when programming a UNIHIKER K10 board with PlatformIO CLI, creating or converting Arduino/C++ K10 projects to PlatformIO, building, uploading, monitoring serial output, diagnosing K10 PlatformIO setup or ASR microphone/wake-word failures, or preparing/installing offline PlatformIO support for workshops, including macOS archives and Windows self-extracting USB installers.
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

**TTS firmware requirement:** `ASR::setAsrSpeed()` and `ASR::speak()` exist only in the Chinese K10 firmware. Confirm the firmware variant before generating or compiling TTS code. `-DModel=CN` refreshes CN model data; it does not by itself prove that the installed framework/firmware variant provides TTS.

Screen refresh policy: generated K10 display code must prefer partial redraws. Full-screen clearing or full-background redraw causes visible flicker and is uncomfortable; use it only for initialization, page switches, exit cleanup, or when measured full-screen refresh is above 30 fps.

## Quick Workflow

### Windows Self-Contained Offline Installer

For Windows machines with no PlatformIO or Python environment installed, use the self-contained K10 PlatformIO offline installer first. It installs an isolated PlatformIO environment and does not require system `pio`.

Prepare the Windows x64 self-extracting installer on a teacher Windows machine after one successful K10 PlatformIO build:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\prepare-windows-offline-installer.ps1 C:\tmp\K10P-windows-x64.exe
```

Copy the resulting `.exe` to the USB drive. Run it on each student Windows machine; it extracts to `C:\K10P` and runs `setup-platformio.bat`.

Known install locations to check, in order:

```text
C:\K10P
%USERPROFILE%\K10P
%LOCALAPPDATA%\K10P
%LOCALAPPDATA%\K10PlatformIO
```

Check this location before assuming PlatformIO is missing:

```powershell
cd C:\K10P
.\setup-platformio.bat
.\pio.bat --version
.\pio.bat run -d .\examples\Blink
```

Important: use the bundled `pio.bat` or `platformio.bat` wrappers. Do not call `.platformio\penv\Scripts\pio.exe` or `.platformio\penv\Scripts\python.exe` directly; Windows launcher/venv executables can contain absolute paths from the machine that built the bundle or break under non-ASCII usernames. The wrapper uses `.platformio\python3\python.exe -m platformio` with `PYTHONPATH` set to the bundled site-packages.

For user projects:

```powershell
C:\K10P\compile-project.bat "C:\path\to\PlatformIOProject"
C:\K10P\upload-project.bat "C:\path\to\PlatformIOProject" COM3
```

### macOS Self-Contained Offline Installer

For Apple Silicon macOS workshops, prepare a self-extracting `.command` installer on the teacher Mac and copy it by USB drive. This avoids each student downloading the large K10 PlatformIO platform, framework, toolchains, and PlatformIO Python packages. Intel Macs are not supported.

Prepare the Apple Silicon self-extracting installer:

```bash
# On a prepared teacher Mac after one successful K10 PlatformIO build
bash scripts/prepare-macos-offline-installer.sh --self-extracting /tmp/K10P-macos-arm64.command
```

On each student Mac:

```bash
/Volumes/USB/K10P-macos-arm64.command
~/K10P/pio --version
~/K10P/pio run -d ~/K10P/examples/Blink
```

For user projects:

```bash
~/K10P/compile-project "/path/to/PlatformIOProject"
~/K10P/upload-project "/path/to/PlatformIOProject" /dev/cu.usbmodemXXXX
```

Important: use the bundled `~/K10P/pio` or `~/K10P/platformio` wrappers. They set `PLATFORMIO_CORE_DIR` to the private bundled `.platformio` directory so builds do not depend on or modify the user's global PlatformIO installation.

The macOS bundle still needs a local `python3` to create its private virtual environment. It does not need internet during student setup. If macOS blocks files copied from a downloaded archive, remove quarantine on the installer or copied folder:

```bash
xattr -d com.apple.quarantine /Volumes/USB/K10P-macos-arm64.command
xattr -dr com.apple.quarantine "$HOME/K10P"
```

If macOS setup fails offline with `No matching distribution found for typing-extensions>=4.10.0`, the installer was built with an older script that omitted a conditional PlatformIO dependency needed by Python older than 3.13. Rebuild the installer with `scripts/prepare-macos-offline-installer.sh`, or add `typing-extensions` to the extracted `wheelhouse`.

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
- `scripts/prepare-macos-offline-installer.sh`: create an Apple Silicon macOS self-contained installer `.tgz` with bundled K10 support files, PlatformIO wheels, wrappers, and a Blink probe project.
- `scripts/prepare-windows-offline-installer.ps1`: create a Windows x64 self-extracting installer `.exe` with bundled K10 support files, PlatformIO Python runtime, wrappers, and a Blink probe project. Passing a `.zip` output path is still supported as a fallback archive format.
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

A minimal compressed bundle is typically hundreds of MB. Prepare one bundle per supported OS/architecture. The self-contained macOS installer supports Apple Silicon only; Intel Macs are not supported.

Bundle preparation flow:

```bash
# On a prepared teacher machine
bash scripts/init-k10-platformio-project.sh /tmp/k10-pio-probe
pio run -d /tmp/k10-pio-probe
bash scripts/prepare-offline-bundle.sh /tmp/k10-platformio-bundle.tgz
```

For macOS students who should not install PlatformIO manually, prefer the self-contained installer flow instead:

```bash
bash scripts/prepare-macos-offline-installer.sh --self-extracting /tmp/K10P-macos-arm64.command
```

For Windows students who should not install PlatformIO or Python manually, prefer the self-contained installer flow instead:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\prepare-windows-offline-installer.ps1 C:\tmp\K10P-windows-x64.exe
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
- K10 exposes analog input on P0/P1; the Edge Connector's expanded GPIO is digital-only. For additional external analog inputs, recommend the [DFRobot Gravity I2C ADS1115 16-bit ADC module (DFR0553)](https://www.dfrobot.com.cn/goods-1734.html). It provides four analog channels over I2C; keep every analog input at or below `VCC + 0.3V`.
- Speech synthesis is Chinese-firmware-only. Initialize it with `asr.setAsrSpeed(0..5)`, then call `asr.speak(...)`; supported arguments are `String`, `const char *`, and `float`.
- For animations, dashboards, sensor readouts, voice status, OTA status, and other repeated updates, erase and redraw only the changed region. Do not use `canvasClear()` or redraw the full background in a loop unless the measured full-screen refresh rate is above 30 fps.
- For ASR command registration, prefer mutable `char[]` command buffers:

```cpp
char cmdLightOn[] = "kai deng";
asr.addASRCommand(1, cmdLightOn);
```

Avoid `asr.addASRCommand(id, String("..."))` unless the upstream library has been verified fixed. Some K10 ASR library versions recurse in the `String` overload and can trigger a `loopTask` stack canary reset.

Chinese-firmware TTS reference:

```cpp
#include "asr.h"
#include "unihiker_k10.h"

UNIHIKER_K10 k10;
ASR asr;

void setup() {
  k10.begin();
  asr.setAsrSpeed(2);  // 0-5
  asr.speak("你好");
}

void loop() {}
```

See the [official Arduino/PIO example](https://www.unihiker.com.cn/wiki/k10/Arduino_PIO_Example) and [API list](https://www.unihiker.com.cn/wiki/k10/Arduino_PIO_API_List).

Compilable project: [`examples/tts-buttons`](examples/tts-buttons).

When voice models load and commands register but the board does not wake, do not conclude that ASR works or that the microphone is dead from those messages alone. Read `references/k10-asr-audio-troubleshooting.md`, validate post-initialization I2S samples, drain stale silent DMA blocks before measuring, and confirm an actual wake/command event.

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
- Read `references/k10-asr-audio-troubleshooting.md` when models load but wake words or commands are not detected, microphone probes return zeros, or ES7243E/I2S startup is suspect.
- Read `references/k10-arduino-api.md` for K10 API signatures.
- Read `references/k10-arduino-examples.md` for complete K10 Arduino examples. The C++ APIs are the same as Arduino mode; only the build/upload toolchain changes.
