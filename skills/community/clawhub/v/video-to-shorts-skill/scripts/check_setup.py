#!/usr/bin/env python3
"""Check what this machine can do before making shorts, and say how to fix what's missing.

    python3 scripts/check_setup.py

Required: ffmpeg and Pillow. Transcription needs one of: an existing transcript file,
GROQ_API_KEY or OPENAI_API_KEY, or faster-whisper. OpenCV is optional (face framing).
"""
import importlib.util, os, platform, shutil, subprocess, sys

system = platform.system()
INSTALL_FFMPEG = {"Darwin": "brew install ffmpeg", "Windows": "winget install ffmpeg",
                  "Linux": "sudo apt install ffmpeg   (or your distro's package manager)"}.get(system, "install ffmpeg")
ok = True


def line(status, name, detail):
    print(f"[{status}] {name}: {detail}")


if sys.version_info < (3, 8):
    ok = False
    line("missing", "Python", f"{platform.python_version()}; needs 3.8 or newer")
else:
    line("ok", "Python", platform.python_version())

if shutil.which("ffmpeg") and shutil.which("ffprobe"):
    v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0]
    line("ok", "ffmpeg", v.replace("ffmpeg version ", "")[:60])
else:
    ok = False
    line("missing", "ffmpeg", INSTALL_FFMPEG)

if importlib.util.find_spec("PIL"):
    line("ok", "Pillow", "captions")
else:
    ok = False
    line("missing", "Pillow", "pip install pillow")

routes = []
if os.environ.get("GROQ_API_KEY"):
    routes.append("Groq API (GROQ_API_KEY)")
if os.environ.get("OPENAI_API_KEY"):
    routes.append("OpenAI API (OPENAI_API_KEY)")
if importlib.util.find_spec("faster_whisper"):
    routes.append("local faster-whisper")
if routes:
    line("ok", "Transcription", ", ".join(routes))
else:
    line("choose", "Transcription",
         "use an existing .srt/.vtt (--from), or pip install faster-whisper (free, local, slower), "
         "or set GROQ_API_KEY / OPENAI_API_KEY (fast, paid per hour of audio)")

try:
    import cv2
    cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    line("ok", "OpenCV", "face framing on")
except Exception:
    line("optional", "OpenCV", "pip install opencv-python-headless  (keeps the speaker centred; without it clips use a centre or full-frame layout)")

py = "py" if system == "Windows" else "python3"
print(f"\nReady. Run the scripts with: {py} scripts/transcribe.py ..." if ok else "\nInstall the missing items above, then run this again.")
sys.exit(0 if ok else 1)
