#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


SRT_TS = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})")
ASS_TS = re.compile(r"Dialogue:[^,]*,([^,]+),([^,]+),([^,]*),[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)")
ASS_OVERRIDE = re.compile(r"\{[^}]*\}")


@dataclass
class Cue:
    start: float
    end: float
    style: str
    text: str


def parse_srt_time(value: str) -> float:
    hh, mm, rest = value.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000


def parse_ass_time(value: str) -> float:
    hh, mm, rest = value.strip().split(":")
    ss, cs = rest.split(".")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(cs) / 100


def clean_text(value: str) -> str:
    value = ASS_OVERRIDE.sub("", value)
    return value.replace("\\N", "\n").replace("\\n", "\n").strip()


def parse_srt(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        ts_index = next((i for i, line in enumerate(lines) if SRT_TS.search(line)), None)
        if ts_index is None:
            continue
        match = SRT_TS.search(lines[ts_index])
        assert match is not None
        text = "\n".join(lines[ts_index + 1 :]).strip()
        if text:
            cues.append(Cue(parse_srt_time(match.group(1)), parse_srt_time(match.group(2)), "Default", text))
    return cues


def parse_ass(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = ASS_TS.match(line)
        if match:
            text = clean_text(match.group(4))
            if text:
                cues.append(Cue(parse_ass_time(match.group(1)), parse_ass_time(match.group(2)), match.group(3).strip() or "Default", text))
    return cues


def parse_subtitle(path: Path) -> list[Cue]:
    if path.suffix.lower() == ".srt":
        return parse_srt(path)
    if path.suffix.lower() == ".ass":
        return parse_ass(path)
    raise SystemExit(f"Unsupported subtitle format: {path.suffix}")


def cue_score(cue: Cue) -> tuple[int, float]:
    lines = len([line for line in cue.text.splitlines() if line.strip()])
    text_len = len(re.sub(r"\s+", "", cue.text))
    return (lines * 1000 + text_len, cue.end - cue.start)


def choose_times(cues: list[Cue], count: int) -> list[float]:
    if not cues:
        return []
    windows: list[Cue] = [cues[0], cues[len(cues) // 2], cues[-1]]
    for cue in sorted(cues, key=cue_score, reverse=True):
        if cue not in windows:
            windows.append(cue)
        if len(windows) >= count * 2:
            break
    candidates: list[float] = []
    for cue in windows:
        duration = max(0.1, cue.end - cue.start)
        candidates.extend(
            [
                cue.start + duration * 0.5,
                cue.start + duration * 0.25,
                cue.start + duration * 0.75,
            ]
        )
    unique: list[float] = []
    seen: set[float] = set()
    for value in candidates:
        rounded = round(value, 3)
        key = round(value, 1)
        if key in seen:
            continue
        seen.add(key)
        unique.append(rounded)
        if len(unique) >= count:
            break
    return sorted(unique)


def format_name(index: int, seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hh = total // 3600
    mm = (total % 3600) // 60
    ss = total % 60
    return f"design-{index:02d}-{hh:02d}-{mm:02d}-{ss:02d}.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract subtitle design confirmation frames from a subtitled preview or output video.")
    parser.add_argument("video", type=Path)
    parser.add_argument("subtitle", type=Path, help="SRT or ASS used for the preview/output")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print("FAIL: ffmpeg is required")
        return 1
    if not args.video.exists():
        print(f"FAIL: missing video {args.video}")
        return 1
    if not args.subtitle.exists():
        print(f"FAIL: missing subtitle {args.subtitle}")
        return 1

    cues = parse_subtitle(args.subtitle)
    times = choose_times(cues, max(3, args.count))
    if not times:
        print("FAIL: no subtitle-bearing times found")
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for index, seconds in enumerate(times, 1):
        output = args.out_dir / format_name(index, seconds)
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{seconds:.3f}",
                "-i",
                str(args.video),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(output),
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print(result.stderr.strip())
            return 1
        print(f"wrote {output}")
    print(f"PASS: extracted {len(times)} design confirmation frame(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
