#!/usr/bin/env python3
"""Transcribe audio using faster-whisper with auto device detection."""
import argparse
import sys
import os


def detect_device():
    """Auto-detect best available compute device."""
    try:
        import coremltools  # noqa: F401
        return "coreml"
    except ImportError:
        pass
    try:
        import torch
        if torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio with faster-whisper")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--language", default=None,
                        help="Language code (e.g. zh, en, ja). Omit for auto-detect.")
    parser.add_argument("--output", default=None, help="Save transcript to file")
    parser.add_argument("--device", default=None,
                        choices=["cpu", "coreml", "mps"],
                        help="Compute device (default: auto-detect)")
    parser.add_argument("--no-vad", action="store_true", help="Disable VAD filter")
    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.audio_path):
        print(f"ERROR: File not found: {args.audio_path}", file=sys.stderr)
        return 1

    device = args.device or detect_device()
    print(f"Device: {device}, Model: {args.model}", file=sys.stderr)

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("ERROR: faster-whisper not installed.", file=sys.stderr)
        print("Run with: uv run --with faster-whisper python3 scripts/transcribe.py ...", file=sys.stderr)
        return 1

    try:
        if device == "coreml":
            model = WhisperModel(args.model, device="cpu", compute_type="int8",
                                 cpu_cores=4)
        elif device == "mps":
            model = WhisperModel(args.model, device="cpu", compute_type="int8")
        else:
            model = WhisperModel(args.model, device="cpu", compute_type="int8")
    except Exception as e:
        print(f"ERROR: Failed to load model '{args.model}': {e}", file=sys.stderr)
        return 1

    try:
        segments, info = model.transcribe(
            args.audio_path,
            language=args.language,
            vad_filter=not args.no_vad,
        )
    except Exception as e:
        print(f"ERROR: Transcription failed: {e}", file=sys.stderr)
        return 1

    print(f"Detected language: {info.language} (p={info.language_probability:.2f})", file=sys.stderr)

    lines = []
    for seg in segments:
        m, s = divmod(int(seg.start), 60)
        h, m = divmod(m, 60)
        if h > 0:
            timestamp = f"[{h:02d}:{m:02d}:{s:02d}]"
        else:
            timestamp = f"[{m:02d}:{s:02d}]"
        line = f"{timestamp} {seg.text.strip()}"
        lines.append(line)
        print(line)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\nSaved to {args.output}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    exit(main())
