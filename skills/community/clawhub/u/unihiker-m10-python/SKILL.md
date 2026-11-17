---
name: unihiker-m10-python
description: Develop, run, and troubleshoot Python programs for the UNIHIKER M10 from Windows or macOS with the unihiker and PinPong APIs. Use when a user wants to control the display, buttons, onboard sensors, buzzer, GPIO, PWM/ADC, or audio, needs help connecting and deploying over SSH with pyenv, uv, or system Python, or needs missing Python dependencies installed when the M10 has no Internet access.
metadata:
  openclaw:
    requires:
      bins:
        - ping
        - ssh
        - scp
    os:
      - win32
      - darwin
    emoji: "🧩"
    homepage: https://github.com/Nick-ccq/unihiker-m10-python
---

# UNIHIKER M10 Python

Build and deploy Python projects for the UNIHIKER M10 from plain-language requirements.

## Host platform

- On Windows, run the `.ps1` scripts with Windows PowerShell.
- On macOS, run the matching `.sh` scripts with `bash`. Do not require PowerShell on macOS.
- Keep environment selection, dependency installation, and execution in the same M10 Python environment on both platforms.

## Safety and interaction rules

- Confirm the board connection before generating or deploying code.
- Use the host platform's structured question tool when available; otherwise ask in chat.
- Never assume `10.1.2.3` is reachable.
- Do not continue after a failed connection check.
- Treat SSH upload, execution, dependency installation, and process termination as device-changing actions. Explain the intended action before running it when the host requires confirmation.
- Never expose or store a user-supplied password. The documented `dfrobot` value is only the factory default.

## 1. Confirm and verify the connection

Ask whether the M10 is connected:

- **USB Type-C:** use the default host `10.1.2.3`.
- **Wi-Fi:** obtain the board's LAN IP if the user has not provided it.
- **Not connected:** stop and show [connection-guide.md](references/connection-guide.md).

Run the matching check from the skill root:

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check_connection.ps1
powershell -ExecutionPolicy Bypass -File scripts/check_connection.ps1 -M10Host 192.168.x.x
```

macOS:

```bash
bash scripts/check_connection.sh
bash scripts/check_connection.sh --host 192.168.x.x
```

- Exit code `0`: continue to environment detection.
- Exit code `1`: report the failure, summarize the connection guide, and stop.

You may skip the initial question only when the same user message states that the board is connected, identifies USB or a usable IP, and includes a concrete programming request. Still run the connection check.

## 2. Detect and select Python

Run:

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/detect_python_env.ps1
powershell -ExecutionPolicy Bypass -File scripts/detect_python_env.ps1 -M10Host 192.168.x.x
```

macOS:

```bash
bash scripts/detect_python_env.sh
bash scripts/detect_python_env.sh --host 192.168.x.x --save-env-file .m10-env.json
```

Offer only detected environments, plus system Python as a fallback:

- `pyenv 3.12.7` when detected; recommend it because current images normally install `unihiker` and `pinpong` there.
- Other detected pyenv versions.
- `uv` when detected.
- System `python3` as the fallback.

Write the choice to `.m10-env.json` in the current project or skill root. Follow the schema in [m10-env.example.json](references/m10-env.example.json) and the rules in [m10-python-env.md](references/m10-python-env.md).

## 3. Generate the program

Choose the API layer:

- Use `unihiker` for the display, touch UI, button callbacks, audio, and brightness.
- Use `pinpong.extension.unihiker` for onboard sensors, the buzzer, GPIO, PWM, and ADC.

Start hardware programs with the required initialization:

```python
from pinpong.board import Board
from pinpong.extension.unihiker import *
from unihiker import GUI
import time

Board("UNIHIKER").begin()
gui = GUI()
```

Use [code-templates.md](references/code-templates.md) for common structures and [unihiker-pinpong-api.md](references/unihiker-pinpong-api.md) for API details.

### Display lifetime requirement

Any program that draws to the display must remain alive long enough for the user to see it. Choose one pattern:

- Static display: `while True: time.sleep(0.05)`.
- Live sensor display: clear, redraw, and sleep inside a loop.
- Button interaction: wait for a button or keep an event loop alive.
- Timed demonstration: sleep for a clearly stated duration, normally at least five seconds.

Deploy long-running display programs with `-Background` on Windows or `--background` on macOS.

### Required correctness rules

- Use `Board("UNIHIKER")`, never `Board("M10")`.
- Use Linux Python, not MicroPython syntax.
- Import every module used by the generated program.
- Do not let a display program immediately return or exit.
- Prefer a small, direct program that matches the request.
- Explain wiring assumptions for external components before deployment.

## 4. Deploy in the selected environment

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_on_m10.ps1 path/to/program.py -EnvFile .m10-env.json
powershell -ExecutionPolicy Bypass -File scripts/run_on_m10.ps1 path/to/program.py -EnvFile .m10-env.json -Background
powershell -ExecutionPolicy Bypass -File scripts/run_on_m10.ps1 path/to/program.py -EnvFile .m10-env.json -PipInstall requests
powershell -ExecutionPolicy Bypass -File scripts/run_on_m10.ps1 path/to/program.py -EnvFile .m10-env.json -PipInstall requests -OfflinePipInstall
```

macOS:

```bash
bash scripts/run_on_m10.sh path/to/program.py --env-file .m10-env.json
bash scripts/run_on_m10.sh path/to/program.py --env-file .m10-env.json --background
bash scripts/run_on_m10.sh path/to/program.py --env-file .m10-env.json --pip-install requests
bash scripts/run_on_m10.sh path/to/program.py --env-file .m10-env.json --pip-install requests --offline-pip-install
```

Environment rules:

- `mode=pyenv`: run with `python_bin`; install with `{python_bin} -m pip install`.
- `mode=uv`: run with `uv run python`; install with `uv pip install`.
- `mode=system`: run with `python3`; install with `python3 -m pip install`.

Review stdout and stderr, make the smallest necessary correction, and rerun. Report whether the program is running in the foreground or background and how to stop it.

## 5. Install missing dependencies

If execution reports `ModuleNotFoundError`, first decide whether the missing name is a project-local module or a third-party distribution. Upload omitted project files; do not install a similarly named PyPI package.

When a third-party distribution is missing and the M10 cannot access the Internet, run:

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_m10_package_offline.ps1 <distribution> -EnvFile .m10-env.json
```

macOS:

```bash
bash scripts/install_m10_package_offline.sh <distribution> --env-file .m10-env.json
```

Then rerun the original program in the same selected environment. Do this without asking again when the import-to-distribution mapping is unambiguous and the user already authorized running the program. Ask before choosing between plausible distributions.

The offline installer must:

- Detect the selected M10 interpreter's Python version, architecture, and glibc version.
- Download the complete binary wheel set on the Internet-connected computer.
- Accept only ARM64-compatible or `py3-none-any` wheels; never upload Windows wheels.
- Upload over SSH and install with `--no-index` so the M10 does not contact PyPI.
- Stop and report the compatibility issue if no binary wheel set exists. Do not silently attempt a source build.

Read [offline-dependencies.md](references/offline-dependencies.md) for package-name mapping and failure handling.

## Quick API map

| Need | API |
|---|---|
| Text | `gui.draw_text(...)` |
| Clear display | `gui.clear()` |
| A/B buttons | `gui.on_a_click(fn)`, `gui.on_b_click(fn)` |
| Light | `light.read()` |
| Accelerometer | `accelerometer.get_x()`, `get_y()`, `get_z()` |
| Gyroscope | `gyroscope.get_x()`, `get_y()`, `get_z()` |
| Buzzer | `buzzer.pitch(freq, beat)` |
| Digital GPIO | `Pin(Pin.P0, Pin.OUT).write_digital(1)` |
| Analog input | `Pin(Pin.P0, Pin.IN).read_analog()` |
| Audio | `Audio().record("a.wav", 3)`, `Audio().play("a.wav")` |
| Brightness | `UNIConfig().set_brightness(80)` |

## Troubleshooting

- SSH timeout: confirm the computer and M10 are on the same network; try `10.1.2.3` for USB.
- PinPong initialization failure: wait for the coprocessor or restart the M10.
- Blank display: check whether a later `gui.clear()` erased the content and keep the process alive.
- Wrong environment: rerun detection and verify that `unihiker` and `pinpong` are installed in the selected interpreter.
- `ModuleNotFoundError`: distinguish a missing project file from a third-party distribution, install it with the offline workflow, and rerun.

## References

- [Connection guide](references/connection-guide.md)
- [Python environments](references/m10-python-env.md)
- [Hardware reference](references/m10-hardware.md)
- [UNIHIKER and PinPong API](references/unihiker-pinpong-api.md)
- [Code templates](references/code-templates.md)
- [Examples](references/examples.md)
- [No-local-Python workflow](references/no-python-workflow.md)
- [Offline dependencies](references/offline-dependencies.md)
- [macOS workflow](references/macos-workflow.md)
