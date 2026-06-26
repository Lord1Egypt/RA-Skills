#!/usr/bin/env python3
import os
import platform
import shlex
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RUN_SCRIPT = SCRIPT_DIR / "run_continuous_voice_assistant.py"
IS_WINDOWS = platform.system().lower() == "windows"


def default_wespeaker_python() -> str:
    home = Path.home()
    if IS_WINDOWS:
        return str((home / ".audioclaw" / "workspace" / "tools" / "wespeaker" / ".venv" / "Scripts" / "python.exe").resolve())
    return str((home / ".audioclaw" / "workspace" / "tools" / "wespeaker" / ".venv" / "bin" / "python").resolve())


def apply_defaults() -> None:
    defaults = {
        "VOICECLAW_TTS_MODE": "senseaudio",
        "VOICECLAW_CAPTURE_BACKEND": "auto",
        "VOICECLAW_VOICE_ID": "male_0004_a",
        "VOICECLAW_EMOTION": "calm",
        "VOICECLAW_TTS_SPEED": "1.25",
        "VOICECLAW_SENSEAUDIO_STREAMING_TTS": "0",
        "VOICECLAW_SENSEAUDIO_STREAMING_BACKEND": "auto",
        "VOICECLAW_WAKE_PHRASE": "贾维斯",
        "VOICECLAW_SLEEP_PHRASE": "贾维斯休息",
        "VOICECLAW_STATUS_SOUNDS": "0",
        "VOICECLAW_SPEAKER_BACKEND": "none",
        "VOICECLAW_WESPEAKER_THRESHOLD": "0.72",
        "VOICECLAW_WESPEAKER_PORT": "18567",
        "VOICECLAW_WESPEAKER_PYTHON": default_wespeaker_python(),
        "VOICECLAW_EXTRA_ARGS": "",
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)
    os.environ.setdefault("VOICECLAW_PYTHON_BIN", sys.executable)


def main() -> int:
    apply_defaults()
    command = [
        sys.executable,
        "-u",
        str(RUN_SCRIPT),
        "--tts-mode",
        os.environ["VOICECLAW_TTS_MODE"],
        "--capture-backend",
        os.environ["VOICECLAW_CAPTURE_BACKEND"],
        "--voice-id",
        os.environ["VOICECLAW_VOICE_ID"],
        "--emotion",
        os.environ["VOICECLAW_EMOTION"],
        "--tts-speed",
        os.environ["VOICECLAW_TTS_SPEED"],
        "--speaker-verification-backend",
        os.environ["VOICECLAW_SPEAKER_BACKEND"],
        "--wespeaker-threshold",
        os.environ["VOICECLAW_WESPEAKER_THRESHOLD"],
        "--wespeaker-port",
        os.environ["VOICECLAW_WESPEAKER_PORT"],
        "--wespeaker-python",
        os.environ["VOICECLAW_WESPEAKER_PYTHON"],
    ]

    if os.environ.get("VOICECLAW_STATUS_SOUNDS", "0").strip().lower() in {"1", "true", "yes", "on"}:
        command.append("--status-sounds")
    else:
        command.append("--no-status-sounds")

    command.extend(sys.argv[1:])

    extra = os.environ.get("VOICECLAW_EXTRA_ARGS", "").strip()
    if extra:
        command.extend(shlex.split(extra, posix=not IS_WINDOWS))

    os.execv(sys.executable, command)


if __name__ == "__main__":
    raise SystemExit(main())
