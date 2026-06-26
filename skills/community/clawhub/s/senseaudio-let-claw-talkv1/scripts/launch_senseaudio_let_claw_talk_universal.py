#!/usr/bin/env python3
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
START_PY = SCRIPT_DIR / "start_senseaudio_let_claw_talk_universal.py"
DISPLAY_NAME = "SenseAudio-Let-Claw-Talk-Universal"


def resolve_python_command() -> list[str]:
    env_python = os.getenv("VOICECLAW_PYTHON_BIN", "").strip()
    if env_python:
        return [env_python]

    executable = sys.executable or ""
    if executable and "WindowsApps" not in executable:
        return [executable]

    if platform.system().lower() == "windows":
        py = shutil.which("py.exe") or shutil.which("py")
        if py:
            return [py, "-3"]

    python3 = shutil.which("python3")
    if python3:
        return [python3]
    python = shutil.which("python")
    if python:
        return [python]
    return [sys.executable] if sys.executable else ["python3"]


def launch_macos(args: list[str]) -> None:
    python_command = resolve_python_command()
    command = " ".join(shlex.quote(part) for part in [*python_command, str(START_PY), *args])
    script = [
        'tell application "Terminal"',
        "activate",
        f"do script {json.dumps(command)}",
        "end tell",
    ]
    subprocess.run(["osascript", *sum([["-e", line] for line in script], [])], check=True)


def launch_windows(args: list[str]) -> None:
    command = [*resolve_python_command(), str(START_PY), *args]
    creationflags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    subprocess.Popen(command, cwd=str(SCRIPT_DIR), creationflags=creationflags)


def launch_linux(args: list[str]) -> None:
    command = [*resolve_python_command(), str(START_PY), *args]
    candidates = [
        ("x-terminal-emulator", ["-e", *command]),
        ("gnome-terminal", ["--", *command]),
        ("konsole", ["-e", *command]),
        ("xterm", ["-e", *command]),
    ]
    for binary, extra in candidates:
        found = shutil.which(binary)
        if found:
            subprocess.Popen([found, *extra])
            return
    raise RuntimeError("No supported terminal launcher found on this platform.")


def main() -> int:
    args = sys.argv[1:]
    system_name = platform.system().lower()
    if system_name == "darwin":
        launch_macos(args)
    elif system_name == "windows":
        launch_windows(args)
    else:
        launch_linux(args)
    print("opened_terminal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
