"""
Convert a transcription JSON file to plain text.

The JSON is the raw result from the TextOps API:
  {"segments": [...], "diarization": {...}, "params": {...}}

Each segment: {"start": float, "end": float, "text": str, "speaker": str (optional)}

Usage:
  python json_to_text.py <input.json> [--output <output.txt>] [--diarization true|false]
"""

import argparse
import json
import os
import sys


def extract_segments(data):
    """Handle both flat and nested result structures."""
    for candidate in [data, data.get("result", {})]:
        segs = candidate.get("segments") if isinstance(candidate, dict) else None
        if segs is not None:
            return segs
    return []


def has_speaker_info(segments):
    return any(seg.get("speaker") for seg in segments)


def to_plain_text(segments):
    """Join all segment texts with line breaks between them."""
    return "\n\n".join(
        seg.get("text", "").strip()
        for seg in segments
        if seg.get("text", "").strip()
    )


def to_diarized_text(segments):
    """Group segments by speaker, with speaker labels."""
    speaker_map = {}
    counter = 1
    for seg in segments:
        spk = seg.get("speaker", "")
        if spk and spk not in speaker_map:
            speaker_map[spk] = f"Speaker {counter}"
            counter += 1

    lines = []
    current_speaker = None
    for seg in segments:
        spk = seg.get("speaker", "")
        text = seg.get("text", "").strip()
        if not text:
            continue
        name = speaker_map.get(spk, "Speaker") if spk else "Speaker"
        if name != current_speaker:
            lines.append(f"\n{name}:")
            current_speaker = name
        lines.append(text)

    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(description="Convert transcription JSON to text")
    parser.add_argument("input", help="Path to JSON file from transcription")
    parser.add_argument("--output", default=None, help="Output .txt path (default: same name as input)")
    parser.add_argument("--diarization", default="auto",
                        help="Speaker separation: true / false / auto (detect from data)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}", flush=True)
        sys.exit(1)

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    segments = extract_segments(data)

    if not segments:
        print("WARNING: No segments found in JSON file", flush=True)
        print("  Try checking the structure manually", flush=True)
        sys.exit(1)

    # determine diarization mode
    if args.diarization == "auto":
        use_diarization = has_speaker_info(segments)
    else:
        use_diarization = args.diarization.lower() in ("true", "1", "yes")

    content = to_diarized_text(segments) if use_diarization else to_plain_text(segments)

    # output path
    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(args.input)[0]
        output_path = base + ".txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    char_count = len(content)
    mode = "speakers" if use_diarization else "plain text"
    print(f"[FILE] TEXT: {output_path} ({char_count:,} chars, {mode})", flush=True)


if __name__ == "__main__":
    main()
