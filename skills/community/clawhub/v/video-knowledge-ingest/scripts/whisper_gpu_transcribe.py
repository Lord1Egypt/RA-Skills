#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel


def format_timestamp_srt(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def write_txt(path: Path, segments: list[dict]) -> None:
    text = "\n".join(seg["text"].strip() for seg in segments if seg["text"].strip())
    path.write_text(text + ("\n" if text else ""), encoding="utf-8")


def write_srt(path: Path, segments: list[dict]) -> None:
    lines: list[str] = []
    for idx, seg in enumerate(segments, 1):
        text = seg["text"].strip()
        if not text:
            continue
        lines.extend([
            str(idx),
            f"{format_timestamp_srt(seg['start'])} --> {format_timestamp_srt(seg['end'])}",
            text,
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_vtt(path: Path, segments: list[dict]) -> None:
    lines = ["WEBVTT", ""]
    for seg in segments:
        text = seg["text"].strip()
        if not text:
            continue
        lines.extend([
            f"{format_timestamp_vtt(seg['start'])} --> {format_timestamp_vtt(seg['end'])}",
            text,
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def normalize_to_wav(src: Path, dst: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-ar",
        "16000",
        "-ac",
        "1",
        "-c:a",
        "pcm_s16le",
        str(dst),
        "-loglevel",
        "error",
    ]
    subprocess.run(cmd, check=True)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Stable GPU Whisper wrapper (faster-whisper on GTX 1060)")
    p.add_argument("input", help="Audio or video file to transcribe")
    p.add_argument("--model", default="small", help="Model name (default: small)")
    p.add_argument("--language", default=None, help="Language code, e.g. zh/en. Omit for auto-detect.")
    p.add_argument("--output-dir", default=".", help="Where to write transcript files")
    p.add_argument("--output-format", default="txt", choices=["txt", "srt", "vtt", "json", "all"], help="Output format")
    p.add_argument("--beam-size", type=int, default=5, help="Beam size (default: 5)")
    p.add_argument("--compute-type", default="int8_float32", help="faster-whisper compute type")
    p.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Prefer cuda; cpu is fallback")
    p.add_argument("--vad-filter", action="store_true", help="Enable VAD filter")
    p.add_argument("--print-info", action="store_true", help="Print model/language info to stderr")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    src = Path(args.input).expanduser().resolve()
    if not src.exists():
        print(f"Input not found: {src}", file=sys.stderr)
        return 2

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem

    with tempfile.TemporaryDirectory(prefix="whisper-gpu-") as td:
        wav_path = Path(td) / f"{stem}.wav"
        normalize_to_wav(src, wav_path)

        model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
        segments_iter, info = model.transcribe(
            str(wav_path),
            language=args.language,
            beam_size=args.beam_size,
            vad_filter=args.vad_filter,
            condition_on_previous_text=False,
        )
        segments = [
            {"start": float(seg.start), "end": float(seg.end), "text": seg.text}
            for seg in segments_iter
        ]

    if args.print_info:
        detected = getattr(info, "language", None)
        prob = getattr(info, "language_probability", None)
        print(
            json.dumps(
                {
                    "model": args.model,
                    "device": args.device,
                    "compute_type": args.compute_type,
                    "detected_language": detected,
                    "language_probability": prob,
                    "segments": len(segments),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )

    formats = ["txt", "srt", "vtt", "json"] if args.output_format == "all" else [args.output_format]

    for fmt in formats:
        path = out_dir / f"{stem}.{fmt}"
        if fmt == "txt":
            write_txt(path, segments)
        elif fmt == "srt":
            write_srt(path, segments)
        elif fmt == "vtt":
            write_vtt(path, segments)
        elif fmt == "json":
            payload = {
                "input": str(src),
                "model": args.model,
                "device": args.device,
                "compute_type": args.compute_type,
                "language": getattr(info, "language", args.language),
                "language_probability": getattr(info, "language_probability", None),
                "segments": segments,
                "text": "\n".join(seg["text"].strip() for seg in segments if seg["text"].strip()),
            }
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    full_text = "\n".join(seg["text"].strip() for seg in segments if seg["text"].strip())
    if full_text:
        print(full_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
