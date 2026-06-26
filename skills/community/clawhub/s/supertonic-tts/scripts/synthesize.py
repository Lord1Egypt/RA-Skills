#!/usr/bin/env python3
"""Quick CLI for Supertonic TTS synthesis.

Usage:
    python3 synthesize.py "Your text here" --voice M1 --output speech.wav
    python3 synthesize.py "<happy>Hello!</happy>" --voice F2 --total-steps 10 --speed 0.9
    python3 synthesize.py "こんにちは" --voice F3 --lang ja

Voices: M1–M5, F1–F5
"""
import argparse
import sys
from pathlib import Path

# Auto-activate venv
_VENV = Path.home() / ".openclaw/workspace/.browser-use-venv"
if _VENV.is_dir():
    sp = _VENV / f"lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
    if not sp.is_dir():
        for v in [(3,14), (3,13), (3,12), (3,11)]:
            sp = _VENV / f"lib/python{v[0]}.{v[1]}/site-packages"
            if sp.is_dir():
                break
    if str(sp) not in sys.path and sp.is_dir():
        sys.path.insert(0, str(sp))

try:
    from supertonic import TTS
except ImportError:
    print("ERROR: supertonic not installed. Run: pip install supertonic", file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Supertonic TTS CLI")
    parser.add_argument("text", help="Text to synthesize (supports expression tags)")
    parser.add_argument("--voice", "-v", default="M1", help="Voice name (M1–M5, F1–F5)")
    parser.add_argument("--custom-style", "-c", help="Path to custom voice style JSON (from Voice Builder)")
    parser.add_argument("--lang", "-l", default="en", help="Language code (en, ja, ko, hi, etc.) or 'na'")
    parser.add_argument("--total-steps", "-s", type=int, default=8, help="Quality: 5 (low) to 12 (high)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech rate: 0.7 (slow) to 2.0 (fast)")
    parser.add_argument("--output", "-o", default="output.wav", help="Output WAV file path")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.custom_style and args.voice != "M1":
        print("WARNING: --voice is ignored when --custom-style is used", file=sys.stderr)

    print(f"Loading TTS (may auto-download on first run)...")
    tts = TTS(auto_download=True)

    if args.custom_style:
        style_path = Path(args.custom_style).expanduser()
        if not style_path.exists():
            print(f"ERROR: Custom voice style not found: {style_path}", file=sys.stderr)
            sys.exit(1)
        style = tts.get_voice_style_from_path(str(style_path))
        voice_label = f"custom:{style_path.name}"
    else:
        if args.voice not in tts.voice_style_names:
            print(f"ERROR: Unknown voice '{args.voice}'. Available: {', '.join(tts.voice_style_names)}", file=sys.stderr)
            sys.exit(1)
        style = tts.get_voice_style(voice_name=args.voice)
        voice_label = args.voice

    print(f"Synthesizing with voice={voice_label}, lang={args.lang}, steps={args.total_steps}, speed={args.speed}")
    print(f"Text: {args.text[:80]}{'...' if len(args.text) > 80 else ''}")

    wav, duration = tts.synthesize(
        text=args.text,
        lang=args.lang,
        voice_style=style,
        total_steps=args.total_steps,
        speed=args.speed,
    )

    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    tts.save_audio(wav, str(output))

    print(f"\nSaved: {output}")
    print(f"Duration: {duration[0]:.2f}s | Sample rate: {tts.sample_rate} Hz")


if __name__ == "__main__":
    main()
