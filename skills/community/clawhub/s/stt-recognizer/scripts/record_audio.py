#!/usr/bin/env python3
"""
Audio Recording Script - Record audio from microphone.
Cross-platform: Linux (ALSA/PulseAudio), Windows (WASAPI), macOS (AVFoundation).
Outputs WAV files for Whisper transcription.
"""
import argparse
import os
import sys
import time
import wave
import struct
import threading
import shutil
import subprocess

# Try to import audio libraries
try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False

try:
    import sounddevice as sd
    import soundfile as sf
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

IS_WINDOWS = sys.platform == "win32" or sys.platform == "cygwin"
IS_LINUX = sys.platform.startswith("linux")
IS_MACOS = sys.platform == "darwin"


def get_default_output_dir():
    """Get default output directory in workspace projects folder."""
    workspace = os.environ.get("OPENCLAW_WORKSPACE",
                              os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
    return os.path.join(workspace, "projects", "stt-recognizer", "recordings")


def get_skill_dir():
    """Get the skill directory based on this script's location."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Recording with PyAudio ───────────────────────────────────────────────────
def record_with_pyaudio(duration, output_path, sample_rate=16000, channels=1):
    """Record audio using PyAudio."""
    p = pyaudio.PyAudio()

    # Auto-detect input device
    device_count = p.get_device_count()
    input_device_index = None
    for i in range(device_count):
        dev_info = p.get_device_info_by_index(i)
        if dev_info['maxInputChannels'] > 0:
            input_device_index = i
            break

    if input_device_index is None:
        print("ERROR: No input audio device found", file=sys.stderr)
        p.terminate()
        sys.exit(1)

    print(f"  Using device: {p.get_device_info_by_index(input_device_index)['name']}")

    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        input_device_index=input_device_index,
        frames_per_buffer=1024
    )

    print(f"  Recording {duration}s...")
    frames = []
    num_chunks = int(sample_rate / 1024 * duration)

    for i in range(num_chunks):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Write WAV file
    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"  Saved: {output_path}")


# ── Recording with SoundDevice ───────────────────────────────────────────────
def record_with_sounddevice(duration, output_path, sample_rate=16000, channels=1):
    """Record audio using sounddevice."""
    print(f"  Recording {duration}s...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                       channels=channels, dtype='int16')
    sd.wait()
    sf.write(output_path, recording, sample_rate)
    print(f"  Saved: {output_path}")


# ── Fallback: usingarecord (Linux) ──────────────────────────────────────────
def record_with_arecord(duration, output_path, sample_rate=16000):
    """Fallback recording using aplay/arecord command line tools on Linux."""
    print(f"  Using arecord (fallback) for {duration}s...")
    # Record as WAV using arecord
    cmd = [
        'arecord',
        '-f', 'cd',          # CD quality: 16-bit, 44100 Hz, stereo
        '-r', str(sample_rate),
        '-c', '1',           # Mono
        '-d', str(duration), # Duration
        '-t', 'wav',
        output_path
    ]
    # Use subprocess.run with shell=False to prevent shell injection via output_path
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  Saved: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: arecord failed with code {e.returncode}", file=sys.stderr)
        sys.exit(1)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Record audio from microphone and save as WAV for STT transcription."
    )
    parser.add_argument("--duration", type=float, default=10.0,
                        help="Recording duration in seconds (default: 10)")
    parser.add_argument("--sample-rate", type=int, default=16000,
                        help="Audio sample rate in Hz (default: 16000, recommended for Whisper)")
    parser.add_argument("--channels", type=int, default=1,
                        help="Number of audio channels, 1=mono (default: 1)")
    parser.add_argument("--output-dir", default=None,
                        help=f"Output directory (default: ~/.../projects/stt-recognizer/recordings)")
    parser.add_argument("--filename", default=None,
                        help="Output filename (default: auto-generated with timestamp)")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available audio input devices")
    args = parser.parse_args()

    # Setup output
    output_dir = args.output_dir or get_default_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    if args.filename:
        filename = args.filename if args.filename.endswith('.wav') else args.filename + '.wav'
    else:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
    output_path = os.path.join(output_dir, filename)

    print("[Audio Recording] Starting...")
    print(f"  Duration:    {args.duration}s")
    print(f"  Sample Rate: {args.sample_rate} Hz")
    print(f"  Channels:    {args.channels}")
    print(f"  Output:     {output_path}")
    print()

    # List devices if requested
    if args.list_devices:
        print("Available input devices:")
        if HAS_PYAUDIO:
            p = pyaudio.PyAudio()
            for i in range(p.get_device_count()):
                dev = p.get_device_info_by_index(i)
                if dev['maxInputChannels'] > 0:
                    print(f"  [{i}] {dev['name']} (inputs: {dev['maxInputChannels']})")
            p.terminate()
        elif HAS_SOUNDDEVICE:
            print(sd.query_devices())
        else:
            # Try using arecord -l
            result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
            if result.returncode != 0:
                print('No arecord available')
            else:
                print(result.stdout)
        print()
        if len(sys.argv) == 2:  # Only --list-devices was passed
            sys.exit(0)

    # Choose recording method
    if HAS_PYAUDIO:
        record_with_pyaudio(args.duration, output_path, args.sample_rate, args.channels)
    elif HAS_SOUNDDEVICE:
        record_with_sounddevice(args.duration, output_path, args.sample_rate, args.channels)
    elif IS_LINUX:
        record_with_arecord(args.duration, output_path, args.sample_rate)
    else:
        print("ERROR: No audio recording library available.", file=sys.stderr)
        print("Please install pyaudio or sounddevice:", file=sys.stderr)
        print("  pip install pyaudio", file=sys.stderr)
        print("  or", file=sys.stderr)
        print("  pip install sounddevice soundfile", file=sys.stderr)
        sys.exit(1)

    # Verify file
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print()
        print(f"Done! Recording saved: {output_path}")
        print(f"  Size: {size / 1024:.1f} KB")
    else:
        print("ERROR: Output file was not created", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
