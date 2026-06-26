#!/usr/bin/env python3
"""
Record and Transcribe - One-shot audio recording and transcription.
Convenience script that records audio and immediately transcribes it.
"""
import argparse
import os
import sys
import time
import shutil

# Import recording and transcription functions
from record_audio import record_with_pyaudio, record_with_sounddevice, record_with_arecord, \
    get_default_output_dir, get_skill_dir, HAS_PYAUDIO, HAS_SOUNDDEVICE, IS_LINUX
from transcribe import transcribe_with_faster_whisper, transcribe_with_faster_whisper, \
    get_default_output_dir as get_transcribe_output_dir

IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"


def get_combined_output_dir():
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                              os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "stt-recognizer")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Record audio from microphone and automatically transcribe it."
    )
    parser.add_argument("--duration", type=float, default=10.0,
                        help="Recording duration in seconds (default: 10)")
    parser.add_argument("--sample-rate", type=int, default=16000,
                        help="Audio sample rate in Hz (default: 16000)")
    parser.add_argument("--model", default="base",
                        help="Whisper model size (default: base)")
    parser.add_argument("--language", default=None,
                        help="Language code (e.g., 'zh', 'en'). Auto-detect if not specified.")
    parser.add_argument("--task", default="transcribe", choices=["transcribe", "translate"],
                        help="Task: 'transcribe' or 'translate' to English")
    parser.add_argument("--engine", default="faster-whisper",
                        help="Transcription engine (default: faster-whisper)")
    parser.add_argument("--keep-recording", action="store_true",
                        help="Keep the recording file after transcription")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory for both recordings and transcriptions")
    args = parser.parse_args()

    output_dir = args.output_dir or get_combined_output_dir()
    recordings_dir = os.path.join(output_dir, "recordings")
    transcriptions_dir = os.path.join(output_dir, "transcriptions")
    os.makedirs(recordings_dir, exist_ok=True)
    os.makedirs(transcriptions_dir, exist_ok=True)

    # Generate filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    recording_path = os.path.join(recordings_dir, f"recording_{timestamp}.wav")
    transcription_path = os.path.join(transcriptions_dir, f"recording_{timestamp}.txt")

    print("[Record & Transcribe] Starting...")
    print(f"  Duration:    {args.duration}s")
    print(f"  Sample Rate: {args.sample_rate} Hz")
    print(f"  Model:       {args.model}")
    print(f"  Language:    {args.language or 'auto-detect'}")
    print(f"  Engine:      {args.engine}")
    print(f"  Output:      {output_dir}")
    print()

    # ── Recording ────────────────────────────────────────────────────────
    print("=" * 60)
    print("STEP 1: Recording")
    print("=" * 60)

    if HAS_PYAUDIO:
        record_with_pyaudio(args.duration, recording_path, args.sample_rate, 1)
    elif HAS_SOUNDDEVICE:
        record_with_sounddevice(args.duration, recording_path, args.sample_rate, 1)
    elif IS_LINUX:
        record_with_arecord(args.duration, recording_path, args.sample_rate)
    else:
        print("ERROR: No audio recording library available.", file=sys.stderr)
        sys.exit(1)

    print()

    # ── Transcription ────────────────────────────────────────────────────
    print("=" * 60)
    print("STEP 2: Transcription")
    print("=" * 60)

    try:
        text = transcribe_with_faster_whisper(
            recording_path,
            args.model,
            args.language,
            transcription_path,
            args.task
        )
    except Exception as e:
        print(f"ERROR: Transcription failed: {e}", file=sys.stderr)
        print("Recording was saved, you can try transcribing later:", file=sys.stderr)
        print(f"  python3 scripts/transcribe.py {recording_path}", file=sys.stderr)
        sys.exit(1)

    # ── Cleanup ───────────────────────────────────────────────────────────
    if not args.keep_recording:
        try:
            os.remove(recording_path)
            print(f"\n(Cleaned up recording file)")
        except:
            pass

    print()
    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    print(text)
    print("=" * 60)
    print(f"\nTranscription saved: {transcription_path}")


if __name__ == "__main__":
    main()
