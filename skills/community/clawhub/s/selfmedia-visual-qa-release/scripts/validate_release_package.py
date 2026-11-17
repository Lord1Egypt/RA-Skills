#!/usr/bin/env python3
"""Read-only validation of media package membership and declared metadata."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    pass


def probe_media(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise ContractError("ffprobe was not found on PATH")
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ContractError(f"ffprobe failed for {path.name}: {result.stderr.strip() or result.returncode}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ContractError(f"ffprobe returned invalid JSON for {path.name}") from exc


def load_contract(path: Path) -> dict[str, Any]:
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read contract: {exc}") from exc
    if not isinstance(contract, dict):
        raise ContractError("contract root must be an object")
    required = contract.get("required_files")
    if not isinstance(required, list) or not required or any(not isinstance(x, str) or not x for x in required):
        raise ContractError("required_files must be a non-empty list of filenames")
    if any(Path(name).name != name or "/" in name or "\\" in name or name in {".", ".."} for name in required):
        raise ContractError("required_files entries must be simple filenames without directory components")
    if len(set(required)) != len(required):
        raise ContractError("required_files must not contain duplicates")
    video = contract.get("video")
    if not isinstance(video, dict) or video.get("path") not in required:
        raise ContractError("video.path must name one of required_files")
    if not isinstance(contract.get("images", {}), dict):
        raise ContractError("images must be an object")
    for filename, dimensions in contract.get("images", {}).items():
        if filename not in required or not isinstance(dimensions, dict):
            raise ContractError("each images entry must name a required file and contain dimensions")
        if any(isinstance(dimensions.get(k), bool) or not isinstance(dimensions.get(k), int) or dimensions[k] <= 0 for k in ("width", "height")):
            raise ContractError(f"images.{filename} must declare positive integer width and height")
    subtitles = contract.get("subtitles")
    if not isinstance(subtitles, dict) or subtitles.get("path") not in required:
        raise ContractError("subtitles.path must name one of required_files")
    if "allow_gaps" in subtitles and not isinstance(subtitles["allow_gaps"], bool):
        raise ContractError("subtitles.allow_gaps must be a boolean")
    return contract


def parse_srt(path: Path) -> list[tuple[float, float]]:
    text = path.read_text(encoding="utf-8-sig")
    pattern = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
    cues: list[tuple[float, float]] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        if len(lines) < 3:
            raise ContractError("SRT cue must contain an index, time range, and text")
        match = pattern.match(lines[1].strip())
        if not match or not any(line.strip() for line in lines[2:]):
            raise ContractError("SRT contains an invalid cue time or empty cue text")
        nums = [int(x) for x in match.groups()]
        start = nums[0] * 3600 + nums[1] * 60 + nums[2] + nums[3] / 1000
        end = nums[4] * 3600 + nums[5] * 60 + nums[6] + nums[7] / 1000
        if end <= start:
            raise ContractError("SRT cue end must be after cue start")
        if cues and start < cues[-1][1]:
            raise ContractError("SRT cues must be ordered and must not overlap")
        cues.append((start, end))
    if not cues:
        raise ContractError("SRT must contain at least one cue")
    return cues


def validate_package(directory: Path, contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not directory.is_dir():
        return [f"package directory does not exist: {directory}"]
    required = set(contract["required_files"])
    actual = {p.name for p in directory.iterdir()}
    for name in sorted(required - actual):
        errors.append(f"missing required file: {name}")
    for name in sorted(actual - required):
        errors.append(f"unexpected file: {name}")
    for name in required & actual:
        entry = directory / name
        if entry.is_symlink():
            errors.append(f"symbolic links are not accepted as package files: {name}")
        elif not entry.is_file():
            errors.append(f"required package entry is not a regular file: {name}")

    if errors:
        return errors
    probed: dict[str, dict[str, Any]] = {}
    video_spec = contract["video"]
    video_path = video_spec["path"]
    media_files = {video_path, *contract.get("images", {}).keys()}
    for name in media_files:
        try:
            probed[name] = probe_media(directory / name)
        except (ContractError, OSError) as exc:
            errors.append(str(exc))

    video_data = probed.get(video_path)
    duration = 0.0
    if video_data:
        streams = video_data.get("streams", [])
        video_streams = [s for s in streams if s.get("codec_type") == "video"]
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
        if not video_streams:
            errors.append(f"video file has no video stream: {video_path}")
        else:
            stream = video_streams[0]
            if video_spec.get("codec_name") and stream.get("codec_name") != video_spec["codec_name"]:
                errors.append(f"{video_path}: codec expected {video_spec['codec_name']}, got {stream.get('codec_name')}")
            expected_rate = video_spec.get("frame_rate")
            if expected_rate:
                try:
                    expected = Fraction(str(expected_rate))
                    actual_rate = Fraction(str(stream.get("avg_frame_rate", "0/0")))
                except (ValueError, ZeroDivisionError):
                    actual_rate = Fraction(0, 1)
                    expected = Fraction(1, 1)
                if actual_rate != expected:
                    errors.append(f"{video_path}: frame rate expected {expected_rate}, got {stream.get('avg_frame_rate')}")
        audio_rule = video_spec.get("audio_tracks", "any")
        if audio_rule not in {"any", "required", "forbidden"}:
            errors.append("video.audio_tracks must be any, required, or forbidden")
        elif audio_rule == "required" and not audio_streams:
            errors.append(f"{video_path}: audio track required but absent")
        elif audio_rule == "forbidden" and audio_streams:
            errors.append(f"{video_path}: audio track forbidden but present")
        try:
            duration = float(video_data.get("format", {}).get("duration", "nan"))
            if not duration > 0:
                raise ValueError
        except (TypeError, ValueError):
            duration = 0.0
            errors.append(f"{video_path}: duration is missing or invalid")

    for filename, dimensions in contract.get("images", {}).items():
        data = probed.get(filename)
        if not data:
            continue
        stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
        if stream is None:
            errors.append(f"{filename}: no image stream found")
        elif stream.get("width") != dimensions.get("width") or stream.get("height") != dimensions.get("height"):
            errors.append(f"{filename}: expected {dimensions.get('width')}x{dimensions.get('height')}, got {stream.get('width')}x{stream.get('height')}")

    subtitle_path = directory / contract["subtitles"]["path"]
    if subtitle_path.exists():
        try:
            cues = parse_srt(subtitle_path)
            if contract["subtitles"].get("allow_gaps", True) is False:
                if any(cues[i][0] > cues[i - 1][1] + 0.001 for i in range(1, len(cues))):
                    errors.append(f"{subtitle_path.name}: gaps between subtitle cues are not allowed by the contract")
            if video_data and duration > 0 and cues[-1][1] > duration + 0.05:
                errors.append(f"{subtitle_path.name}: final cue ends at {cues[-1][1]:.3f}s after video duration {duration:.3f}s")
        except (ContractError, OSError, UnicodeError) as exc:
            errors.append(f"{subtitle_path.name}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--contract", type=Path, required=True)
    args = parser.parse_args()
    try:
        contract = load_contract(args.contract)
        errors = validate_package(args.package, contract)
    except ContractError as exc:
        print(f"invalid contract: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: package matches contract {contract.get('name', args.contract.name)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
