#!/usr/bin/env python3
"""Offline, bounded contact sheets and full-dimension frames from local video."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MAX_FRAMES = 240
MAX_PAGES = 12
MAX_FULL_FRAMES = 24


class ReviewError(Exception):
    pass


def positive_float(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("expected a finite positive number")
    return number


def nonnegative_float(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("expected a finite nonnegative number")
    return number


def dense_interval(value: str) -> tuple[float, float, float]:
    parts = value.split(":")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("use START:END:STEP in seconds")
    try:
        start, end, step = map(float, parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("use numeric START:END:STEP") from exc
    if not all(map(math.isfinite, (start, end, step))) or start < 0 or end <= start or step <= 0:
        raise argparse.ArgumentTypeError("require finite 0 <= START < END and STEP > 0")
    return start, end, step


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="local video file")
    parser.add_argument("--output", type=Path, required=True, help="new output directory; existing paths are rejected")
    parser.add_argument("--interval", type=positive_float, default=2.0, help="regular sampling interval in seconds (default: 2)")
    parser.add_argument("--start", type=nonnegative_float, default=0.0, help="coverage start in seconds")
    parser.add_argument("--end", type=positive_float, help="exclusive coverage end in seconds (default: duration)")
    parser.add_argument("--dense", type=dense_interval, action="append", default=[], metavar="START:END:STEP", help="add a densely sampled interval; repeatable")
    parser.add_argument("--full", type=nonnegative_float, action="append", default=[], metavar="SECONDS", help="save full-dimension frame at/after this time; repeatable")
    parser.add_argument("--page-size", type=int, default=20, help="frames per contact sheet, 1-40 (default: 20)")
    parser.add_argument("--max-frames", type=int, default=MAX_FRAMES, help="maximum requested sample times, up to 240")
    parser.add_argument("--thumb-width", type=int, default=320, help="thumbnail width in pixels, 240-640")
    return parser.parse_args()


def run(command: list[str]) -> str:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()[-1200:]
        raise ReviewError(f"{command[0]} failed (exit {result.returncode}): {detail}")
    return result.stdout


def dependencies():
    for name in ("ffprobe", "ffmpeg"):
        if not shutil.which(name):
            raise ReviewError(f"{name} is not available on PATH; install/configure it in this runtime. No host fallback is attempted")
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError as exc:
        raise ReviewError("Pillow is unavailable in this Python runtime; no automatic installation or host fallback is attempted") from exc
    return Image, ImageDraw, ImageOps


def probe(path: Path) -> tuple[float, int, int, bool]:
    raw = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=index,codec_type,width,height", "-of", "json", str(path)])
    data = json.loads(raw)
    video = next((stream for stream in data.get("streams", []) if stream.get("codec_type") == "video"), None)
    if not video:
        raise ReviewError("input has no video stream")
    try:
        duration = float(data["format"]["duration"])
        width, height = int(video["width"]), int(video["height"])
    except (KeyError, ValueError, TypeError) as exc:
        raise ReviewError("video duration or dimensions are unavailable") from exc
    if not math.isfinite(duration) or duration <= 0 or width <= 0 or height <= 0:
        raise ReviewError("video duration or dimensions are invalid")
    has_audio = any(stream.get("codec_type") == "audio" for stream in data.get("streams", []))
    return duration, width, height, has_audio


def times(start: float, end: float, step: float) -> list[float]:
    count = math.ceil((end - start) / step - 1e-10)
    if count > MAX_FRAMES:
        raise ReviewError(f"a single sampling interval requests {count} frames; hard limit is {MAX_FRAMES}")
    return [start + i * step for i in range(max(0, count))]


def targets(args: argparse.Namespace, duration: float) -> tuple[float, list[dict]]:
    end = args.end if args.end is not None else duration
    if not 0 <= args.start < end <= duration + 1e-6:
        raise ReviewError(f"require 0 <= start < end <= video duration ({duration:.3f}s)")
    if not 1 <= args.max_frames <= MAX_FRAMES or not 1 <= args.page_size <= 40 or not 240 <= args.thumb_width <= 640:
        raise ReviewError("require max-frames 1-240, page-size 1-40, thumb-width 240-640")
    requested: dict[float, set[str]] = {}

    def add(time: float, reason: str) -> None:
        requested.setdefault(round(time, 6), set()).add(reason)

    for time in times(args.start, end, args.interval):
        add(time, "regular")
    for start, stop, step in args.dense:
        if start < args.start or stop > end + 1e-6:
            raise ReviewError("dense interval must be inside the requested coverage window")
        for time in times(start, stop, step):
            add(time, "dense")
    for time in args.full:
        if not args.start <= time < end:
            raise ReviewError("full-frame time must be inside the requested coverage window")
        add(time, "full")
    if len(set(args.full)) > MAX_FULL_FRAMES:
        raise ReviewError(f"at most {MAX_FULL_FRAMES} selected full-dimension frames may be requested")
    if len(requested) > args.max_frames:
        raise ReviewError(f"{len(requested)} requested times exceed --max-frames {args.max_frames}; narrow coverage or increase interval")
    if math.ceil(len(requested) / args.page_size) > MAX_PAGES:
        raise ReviewError(f"{len(requested)} requested times need more than {MAX_PAGES} pages; increase page-size or narrow coverage")
    return end, [{"requested_seconds": t, "reasons": sorted(reasons)} for t, reasons in sorted(requested.items())]


def locate_frames(path: Path, requested: list[dict]) -> list[dict]:
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries", "frame=best_effort_timestamp_time", "-of", "csv=p=0", str(path)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert process.stdout is not None and process.stderr is not None
    next_target = 0
    last = None
    frame_index = 0
    for line in process.stdout:
        value = line.strip().split(",", 1)[0]
        if not value:
            continue
        try:
            pts = float(value)
        except ValueError:
            if value != "N/A":
                process.kill()
                process.wait()
                raise ReviewError(f"unexpected ffprobe frame timestamp record: {value[:100]}")
            frame_index += 1
            continue
        if math.isfinite(pts):
            last = (frame_index, pts)
            while next_target < len(requested) and requested[next_target]["requested_seconds"] <= pts + 1e-6:
                requested[next_target]["frame_index"] = frame_index
                requested[next_target]["pts_seconds"] = pts
                next_target += 1
        frame_index += 1
    stderr = process.stderr.read()
    if process.wait():
        raise ReviewError(f"ffprobe frame scan failed: {stderr.strip()[-1200:]}")
    if last is None:
        raise ReviewError("no video frames with presentation timestamps found")
    for target in requested[next_target:]:
        target["frame_index"], target["pts_seconds"] = last
        target["note"] = "last available frame precedes requested time"
    return requested


def extract(path: Path, indices: list[int], directory: Path) -> None:
    # Escaped commas are required inside FFmpeg filter expressions.
    expression = "+".join(f"eq(n\\,{index})" for index in indices)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(path), "-map", "0:v:0", "-vf", f"select={expression}", "-fps_mode", "passthrough", "-frames:v", str(len(indices)), "-start_number", "0", str(directory / "%06d.png")])
    actual = sorted(directory.glob("*.png"))
    if len(actual) != len(indices):
        raise ReviewError(f"expected {len(indices)} extracted frames, found {len(actual)}; inspect FFmpeg stream/filter compatibility")


def stamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def render(args, output: Path, requested: list[dict], frames: dict[int, Path], size: tuple[int, int], pil) -> tuple[list[dict], list[dict]]:
    Image, ImageDraw, ImageOps = pil
    cells = []
    thumb_height = max(1, round(args.thumb_width * size[1] / size[0]))
    cell_height = thumb_height + 44
    for target in requested:
        index = target["frame_index"]
        with Image.open(frames[index]) as source:
            if source.size != size:
                raise ReviewError(f"frame {index} dimensions {source.size} differ from probed {size}")
            thumb = ImageOps.contain(source.convert("RGB"), (args.thumb_width, thumb_height))
        cells.append((target, thumb))
    sheets = []
    for page_index, offset in enumerate(range(0, len(cells), args.page_size), 1):
        page = cells[offset:offset + args.page_size]
        columns = min(4, len(page))
        rows = math.ceil(len(page) / columns)
        sheet = Image.new("RGB", (columns * args.thumb_width, rows * cell_height), "#151515")
        draw = ImageDraw.Draw(sheet)
        for position, (target, thumb) in enumerate(page):
            x = (position % columns) * args.thumb_width
            y = (position // columns) * cell_height
            sheet.paste(thumb, (x + (args.thumb_width - thumb.width) // 2, y))
            draw.text((x + 5, y + thumb_height + 4), f"PTS {stamp(target['pts_seconds'])}  frame {target['frame_index']}", fill="white")
            draw.text((x + 5, y + thumb_height + 22), f"asked {stamp(target['requested_seconds'])}  {','.join(target['reasons'])}", fill="#cccccc")
        name = f"sheet-{page_index:02d}.jpg"
        sheet.save(output / name, quality=90)
        sheets.append({"file": name, "requested_times": [item["requested_seconds"] for item, _ in page]})
    full_targets = [target for target in requested if "full" in target["reasons"]]
    if not full_targets:
        full_targets = requested[:1]
    full = []
    full_dir = output / "full"
    full_dir.mkdir()
    for number, target in enumerate(full_targets, 1):
        name = f"full-{number:03d}-frame-{target['frame_index']:06d}.png"
        shutil.copyfile(frames[target["frame_index"]], full_dir / name)
        full.append({"file": f"full/{name}", "requested_seconds": target["requested_seconds"], "pts_seconds": target["pts_seconds"], "frame_index": target["frame_index"], "dimensions": list(size)})
    return sheets, full


def main() -> int:
    args = cli()
    try:
        pil = dependencies()
        input_path = args.input.expanduser().resolve(strict=True)
        if not input_path.is_file():
            raise ReviewError("input must be a local file")
        output = args.output.expanduser().resolve()
        if output.exists():
            raise ReviewError(f"output already exists: {output}; choose a new directory")
        if output == input_path or input_path in output.parents:
            raise ReviewError("output cannot contain the input file")
        duration, width, height, has_audio = probe(input_path)
        end, requested = targets(args, duration)
        requested = locate_frames(input_path, requested)
        unique_indices = sorted({target["frame_index"] for target in requested})
        output.mkdir(parents=True, exist_ok=False)
        with tempfile.TemporaryDirectory(prefix=".extracted-", dir=output) as scratch:
            scratch_path = Path(scratch)
            extract(input_path, unique_indices, scratch_path)
            frames = {index: scratch_path / f"{position:06d}.png" for position, index in enumerate(unique_indices)}
            with pil[0].open(frames[unique_indices[0]]) as first_frame:
                displayed_size = first_frame.size
            sheets, full = render(args, output, requested, frames, displayed_size, pil)
        manifest = {
            "input": str(input_path), "duration_seconds": duration, "video_dimensions": list(displayed_size),
            "probed_stream_dimensions": [width, height],
            "coverage": {"start_seconds": args.start, "end_seconds_exclusive": end, "regular_interval_seconds": args.interval, "dense_intervals": [{"start_seconds": a, "end_seconds_exclusive": b, "step_seconds": c} for a, b, c in args.dense]},
            "audio_stream_present": has_audio, "audio_reviewed": False,
            "limits": {"max_frames": args.max_frames, "page_size": args.page_size, "max_pages": MAX_PAGES, "max_full_frames": MAX_FULL_FRAMES},
            "samples": requested, "contact_sheets": sheets, "full_frames": full,
            "limitations": ["Visual samples do not prove events between frames or outside the coverage window.", "Timestamps are decoded-frame presentation timestamps; requested times may map to later frames or the last available frame.", "Audio was not analyzed; use a separate authorized audio workflow if needed.", "Full frames preserve decoded pixel dimensions, not the source's compressed bitstream or exact color metadata."],
        }
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {len(sheets)} sheet(s), {len(full)} full-dimension frame(s), and manifest: {output}")
        return 0
    except (ReviewError, OSError, json.JSONDecodeError) as exc:
        print(f"video-frame-review: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
