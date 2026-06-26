#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

try:
    from faster_whisper import WhisperModel
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency faster-whisper. Run scripts/run_local_subtitles.sh first."
    ) from exc


STRONG_BREAKS = set("。！？!?；;")


@dataclass
class Caption:
    start: float
    end: float
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert local video or audio files into timecoded SRT subtitles."
    )
    parser.add_argument("input", help="Input media path, for example ./demo.mp4")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for generated subtitles. Default: ./output",
    )
    parser.add_argument(
        "--model",
        default="small",
        help="Whisper model name. Default: small",
    )
    parser.add_argument(
        "--language",
        default="zh",
        help="Language code. Use auto for mixed or unknown audio. Default: zh",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Inference device. Default: cpu",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="Inference precision. CPU default: int8",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Decoder beam size. Default: 5",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=22,
        help="Maximum characters per subtitle cue. Default: 22",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=4.0,
        help="Maximum duration per subtitle cue. Default: 4.0",
    )
    parser.add_argument(
        "--copy-next-to-input",
        action="store_true",
        help="Copy the generated SRT next to the source media file.",
    )
    parser.add_argument(
        "--no-vad",
        action="store_true",
        help="Disable VAD filtering.",
    )
    return parser.parse_args()


def ensure_input(path_str: str) -> Path:
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Input file not found: {path}")
    return path


def ensure_output_dir(path_str: str) -> Path:
    path = Path(path_str).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_timestamp(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def normalize_text(text: str) -> str:
    collapsed = " ".join(text.strip().split())
    for token in (" 。", " ，", " ？", " ！", " ：", " ；", " 、"):
        collapsed = collapsed.replace(token, token.strip())
    return collapsed


def flush_caption(
    captions: List[Caption],
    pieces: List[str],
    start: Optional[float],
    end: Optional[float],
) -> None:
    if not pieces or start is None or end is None or end <= start:
        return
    text = normalize_text("".join(pieces))
    if text:
        captions.append(Caption(start=start, end=end, text=text))


def split_segment(segment: object, max_chars: int, max_seconds: float) -> List[Caption]:
    words = list(getattr(segment, "words", []) or [])
    if not words:
        text = normalize_text(getattr(segment, "text", ""))
        if not text:
            return []
        return [Caption(start=float(segment.start), end=float(segment.end), text=text)]

    captions: List[Caption] = []
    pieces: List[str] = []
    chunk_start: Optional[float] = None
    chunk_end: Optional[float] = None

    for word in words:
        token = getattr(word, "word", "")
        token_start = getattr(word, "start", None)
        token_end = getattr(word, "end", None)

        if token_start is None:
            token_start = chunk_end if chunk_end is not None else float(segment.start)
        if token_end is None:
            token_end = token_start

        if chunk_start is None:
            chunk_start = float(token_start)

        candidate = normalize_text("".join(pieces) + token)
        candidate_duration = float(token_end) - float(chunk_start)
        should_break = bool(
            pieces and (len(candidate) > max_chars or candidate_duration > max_seconds)
        )

        if should_break:
            flush_caption(captions, pieces, chunk_start, chunk_end)
            pieces = []
            chunk_start = float(token_start)

        pieces.append(token)
        chunk_end = float(token_end)
        current = normalize_text("".join(pieces))

        if current and current[-1] in STRONG_BREAKS:
            flush_caption(captions, pieces, chunk_start, chunk_end)
            pieces = []
            chunk_start = None
            chunk_end = None

    flush_caption(captions, pieces, chunk_start, chunk_end)
    return captions


def build_captions(
    segments: Iterable[object],
    max_chars: int,
    max_seconds: float,
) -> List[Caption]:
    captions: List[Caption] = []
    for segment in segments:
        captions.extend(
            split_segment(segment, max_chars=max_chars, max_seconds=max_seconds)
        )
    return captions


def write_srt(captions: List[Caption], output_path: Path) -> None:
    lines: List[str] = []
    for index, caption in enumerate(captions, start=1):
        lines.append(str(index))
        lines.append(
            f"{format_timestamp(caption.start)} --> {format_timestamp(caption.end)}"
        )
        lines.append(caption.text)
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def maybe_copy_next_to_input(output_path: Path, input_path: Path) -> Optional[Path]:
    target_path = input_path.with_suffix(".srt")
    shutil.copy2(output_path, target_path)
    return target_path


def main() -> int:
    args = parse_args()
    input_path = ensure_input(args.input)
    output_dir = ensure_output_dir(args.output_dir)
    output_path = output_dir / f"{input_path.stem}.srt"
    language = None if args.language.lower() == "auto" else args.language

    print(f"Loading model: {args.model}")
    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
    )

    print(f"Transcribing: {input_path}")
    segments, info = model.transcribe(
        str(input_path),
        language=language,
        beam_size=args.beam_size,
        word_timestamps=True,
        vad_filter=not args.no_vad,
    )

    captions = build_captions(
        list(segments),
        max_chars=args.max_chars,
        max_seconds=args.max_seconds,
    )

    if not captions:
        raise SystemExit("No subtitles were generated.")

    write_srt(captions, output_path)
    print(f"Detected language: {info.language} (prob={info.language_probability:.3f})")
    print(f"Subtitle cues: {len(captions)}")
    print(f"SRT written: {output_path}")

    if args.copy_next_to_input:
        copied_path = maybe_copy_next_to_input(output_path, input_path)
        print(f"Copied next to input: {copied_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
