#!/usr/bin/env python3
"""Validate a generic frame-based timeline and optional measured media times."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


class TimelineError(ValueError):
    pass


def load_timeline(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TimelineError(f"cannot read timeline JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise TimelineError("timeline root must be a JSON object")
    return data


def parse_srt(path: Path) -> list[tuple[float, float]]:
    try:
        content = path.read_text(encoding="utf-8-sig").strip()
    except (OSError, UnicodeError) as exc:
        raise TimelineError(f"cannot read SRT: {exc}") from exc
    pattern = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
    cues: list[tuple[float, float]] = []
    for block in re.split(r"\n\s*\n", content):
        lines = block.splitlines()
        if len(lines) < 3:
            raise TimelineError("each SRT cue needs an index, time range, and text")
        match = pattern.match(lines[1].strip())
        if not match or not any(line.strip() for line in lines[2:]):
            raise TimelineError("SRT contains an invalid time range or empty cue")
        n = [int(x) for x in match.groups()]
        start = n[0] * 3600 + n[1] * 60 + n[2] + n[3] / 1000
        end = n[4] * 3600 + n[5] * 60 + n[6] + n[7] / 1000
        if end <= start:
            raise TimelineError("SRT cue end must be after cue start")
        if cues and start < cues[-1][1]:
            raise TimelineError("SRT cues must be ordered and must not overlap")
        cues.append((start, end))
    if not cues:
        raise TimelineError("SRT must contain at least one cue")
    return cues


def _positive_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise TimelineError(f"{name} must be a finite positive number")
    return float(value)


def validate(data: dict[str, Any], *, voiceover_duration: float | None = None,
             preview_duration: float | None = None, captions: Path | None = None) -> None:
    schema_version = data.get("schema_version")
    if isinstance(schema_version, bool) or schema_version != 1:
        raise TimelineError("schema_version must be 1")
    composition = data.get("composition_id")
    if not isinstance(composition, str) or not composition.strip():
        raise TimelineError("composition_id must be a non-empty string")
    fps = _positive_number(data.get("fps"), "fps")
    total_frames = data.get("duration_frames")
    if isinstance(total_frames, bool) or not isinstance(total_frames, int) or total_frames <= 0:
        raise TimelineError("duration_frames must be a positive integer")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise TimelineError("scenes must be a non-empty list")

    seen: set[str] = set()
    cursor = 0
    for i, scene in enumerate(scenes):
        label = f"scenes[{i}]"
        if not isinstance(scene, dict):
            raise TimelineError(f"{label} must be an object")
        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not scene_id.strip():
            raise TimelineError(f"{label}.id must be a non-empty string")
        if scene_id in seen:
            raise TimelineError(f"duplicate scene id: {scene_id}")
        seen.add(scene_id)
        start = scene.get("start_frame")
        end = scene.get("end_frame")
        if isinstance(start, bool) or not isinstance(start, int) or isinstance(end, bool) or not isinstance(end, int):
            raise TimelineError(f"{label} frame bounds must be integers")
        if start != cursor:
            raise TimelineError(f"{label} must start at frame {cursor} for a continuous timeline; got {start}")
        if end <= start:
            raise TimelineError(f"{label}.end_frame must be after start_frame")
        if end > total_frames:
            raise TimelineError(f"{label} extends beyond duration_frames")
        cursor = end
    if cursor != total_frames:
        raise TimelineError(f"last scene ends at frame {cursor}, but duration_frames is {total_frames}")

    duration = total_frames / fps
    tolerance = max(1 / fps, 0.05)
    if voiceover_duration is not None:
        measured_voiceover = _positive_number(voiceover_duration, "voiceover duration")
        if measured_voiceover > duration + tolerance:
            raise TimelineError(f"voiceover duration {measured_voiceover:.3f}s exceeds timeline duration {duration:.3f}s")
    if preview_duration is not None:
        measured_preview = _positive_number(preview_duration, "preview duration")
        if abs(measured_preview - duration) > tolerance:
            raise TimelineError(f"preview duration {measured_preview:.3f}s does not match timeline duration {duration:.3f}s")
    if captions is not None:
        cues = parse_srt(captions)
        if cues[-1][1] > duration + tolerance:
            raise TimelineError(f"final subtitle ends at {cues[-1][1]:.3f}s after timeline duration {duration:.3f}s")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", type=Path)
    parser.add_argument("--voiceover-duration", type=float)
    parser.add_argument("--preview-duration", type=float)
    parser.add_argument("--captions", type=Path)
    args = parser.parse_args(argv[1:])
    try:
        validate(load_timeline(args.timeline), voiceover_duration=args.voiceover_duration,
                 preview_duration=args.preview_duration, captions=args.captions)
    except TimelineError as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 1
    print("valid: continuous frame intervals and supplied media times")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
