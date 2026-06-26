#!/usr/bin/env python3
"""
One-command WhisperX subtitle generation and translation pipeline.
Cross-platform runner that chains transcribe.py and translate.py together.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"

# Windows cmd.exe does not support ANSI by default; disable colors there.
if sys.platform == "win32" and "WT_SESSION" not in os.environ:
    try:
        os.system("")  # enable ANSI on Windows 10+
    except Exception:
        GREEN = YELLOW = RED = NC = ""


def cprint(msg, color=NC):
    print(f"{color}{msg}{NC}")


def check_dependency(name, install_hint):
    if not shutil.which(name):
        cprint(f"{name} not found", RED)
        print(f"   Install with: {install_hint}")
        sys.exit(1)


def run_cmd(args):
    result = subprocess.run(args)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    script_dir = Path(__file__).resolve().parent

    video_dir = os.environ.get("VIDEO_DIR", "./videos")
    output_dir = os.environ.get("OUTPUT_DIR", "./output")
    translated_dir = os.environ.get("TRANSLATED_DIR", "./translated")
    target_lang = os.environ.get("TARGET_LANG", "zh")
    model_size = os.environ.get("WHISPER_MODEL", "medium")

    cprint("=================================", GREEN)
    cprint("  WhisperX Subtitle Generation + Translation Tool", GREEN)
    cprint("=================================", GREEN)
    print()

    # Check dependencies
    python_cmd = sys.executable
    check_dependency("ffmpeg",
                     "brew install ffmpeg (macOS) / apt install ffmpeg (Linux) / choco install ffmpeg (Windows)")

    # Create output directories
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(translated_dir).mkdir(parents=True, exist_ok=True)

    # Step 1: transcription
    cprint("Step 1: Transcribe video audio into subtitles", YELLOW)
    print()

    run_cmd([python_cmd, str(script_dir / "transcribe.py"),
             video_dir, "-o", output_dir, "-m", model_size])

    print()
    cprint("Transcription completed", GREEN)
    print()

    # Step 2: translation (optional)
    cprint(f"Step 2: Translate subtitles into target language ({target_lang})", YELLOW)
    print()

    if not os.environ.get("OPENAI_API_KEY"):
        cprint("OPENAI_API_KEY is not set, skipping translation", YELLOW)
        print("   To enable translation, set the OPENAI_API_KEY environment variable")
        print()
    else:
        run_cmd([python_cmd, str(script_dir / "translate.py"),
                 output_dir, "-o", translated_dir,
                 "-t", target_lang, "--bilingual", "--target-only"])
        print()
        cprint("Translation completed", GREEN)

    print()
    cprint("=================================", GREEN)
    cprint("  All tasks completed", GREEN)
    cprint("=================================", GREEN)
    print()
    print("Output files:")
    print(f"  - Source subtitles:    {output_dir}/*.{{lang}}.srt")
    print(f"  - Bilingual subtitles: {translated_dir}/*.bilingual.srt")
    print(f"  - Target subtitles:    {translated_dir}/*.{target_lang}.srt")
    print()


if __name__ == "__main__":
    main()
