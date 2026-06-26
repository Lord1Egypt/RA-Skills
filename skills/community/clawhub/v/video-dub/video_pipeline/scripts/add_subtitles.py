import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCTURED_DIR = PROJECT_ROOT / "data" / "structured"
RETIME_PLAN_DIR = PROJECT_ROOT / "data" / "state" / "retime_plans"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
SUBTITLE_DIR = PROJECT_ROOT / "data" / "subtitles"


def ensure_directories() -> None:
    SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_subtitle_text(text: str) -> str:
    return " ".join(str(text).strip().split())


def format_srt_timestamp(seconds: float) -> str:
    total_ms = max(int(round(seconds * 1000)), 0)
    hours = total_ms // 3_600_000
    minutes = (total_ms % 3_600_000) // 60_000
    secs = (total_ms % 60_000) // 1000
    millis = total_ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def build_normal_entries(structured_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for item in structured_items:
        text = normalize_subtitle_text(item.get("zh") or item.get("en", ""))
        start = float(item.get("start", 0.0) or 0.0)
        end = float(item.get("end", 0.0) or 0.0)
        if not text or end <= start:
            continue
        entries.append({"start": start, "end": end, "text": text})
    return entries


def build_retimed_entries(plan_payload: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for segment in plan_payload.get("segments", []):
        if segment.get("kind") != "speech":
            continue
        text = normalize_subtitle_text(segment.get("zh") or segment.get("en", ""))
        start = float(segment.get("output_start", 0.0) or 0.0)
        end = float(segment.get("output_end", 0.0) or 0.0)
        if not text or end <= start:
            continue
        entries.append({"start": start, "end": end, "text": text})
    return entries


def write_srt(entries: list[dict[str, Any]], output_path: Path) -> Path:
    lines: list[str] = []
    for index, entry in enumerate(entries, start=1):
        lines.extend(
            [
                str(index),
                f"{format_srt_timestamp(entry['start'])} --> {format_srt_timestamp(entry['end'])}",
                entry["text"],
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8-sig")
    print(f"[INFO] Subtitle file saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def ffmpeg_subtitle_path(path: Path) -> str:
    as_posix = path.resolve().as_posix()
    return as_posix.replace(":", "\\:")


def burn_subtitles(video_path: Path, subtitle_path: Path, output_path: Path) -> Path:
    subtitle_filter = (
        f"subtitles='{ffmpeg_subtitle_path(subtitle_path)}':charenc=UTF-8:"
        "force_style='FontName=Microsoft YaHei,FontSize=20,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,"
        "MarginV=24'"
    )
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        subtitle_filter,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "copy",
        str(output_path),
    ]
    print(f"[INFO] Burning subtitles into: {video_path.relative_to(PROJECT_ROOT)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed to burn subtitles")
    print(f"[INFO] Subtitled video saved to: {output_path.relative_to(PROJECT_ROOT)}")
    return output_path


def process_file(structured_path: Path, only_srt: bool) -> None:
    structured_items = load_json(structured_path)
    if not isinstance(structured_items, list):
        raise ValueError(f"Structured JSON must be a list: {structured_path}")

    base_name = structured_path.stem
    normal_entries = build_normal_entries(structured_items)
    normal_srt_path = SUBTITLE_DIR / f"{base_name}_zh.srt"
    write_srt(normal_entries, normal_srt_path)

    if not only_srt:
        normal_video_path = OUTPUT_DIR / f"{base_name}_zh_male.mp4"
        if normal_video_path.exists():
            normal_output_path = OUTPUT_DIR / f"{base_name}_zh_male_subtitled.mp4"
            burn_subtitles(normal_video_path, normal_srt_path, normal_output_path)

    plan_path = RETIME_PLAN_DIR / f"{base_name}.json"
    retimed_video_path = OUTPUT_DIR / f"{base_name}_zh_retimed_v4.mp4"
    if plan_path.exists() and retimed_video_path.exists():
        plan_payload = load_json(plan_path)
        retimed_entries = build_retimed_entries(plan_payload)
        retimed_srt_path = SUBTITLE_DIR / f"{base_name}_zh_retimed_v4.srt"
        write_srt(retimed_entries, retimed_srt_path)
        if not only_srt:
            retimed_output_path = OUTPUT_DIR / f"{base_name}_zh_retimed_v4_subtitled.mp4"
            burn_subtitles(retimed_video_path, retimed_srt_path, retimed_output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Chinese subtitle files and burn them into output videos.")
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Optional single structured JSON path. If omitted, scan data/structured/*.json.",
    )
    parser.add_argument(
        "--only-srt",
        action="store_true",
        help="Only generate SRT files and skip burning subtitles into videos.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_directories()

    if args.input_path:
        structured_files = [Path(args.input_path).resolve()]
    else:
        structured_files = [path.resolve() for path in sorted(STRUCTURED_DIR.glob("*.json"))]

    if not structured_files:
        print("[WARN] No structured JSON files found. Nothing to process.")
        return 0

    had_error = False
    for structured_path in structured_files:
        try:
            process_file(structured_path, args.only_srt)
        except Exception as exc:
            had_error = True
            print(f"[ERROR] Failed to add subtitles for: {structured_path}", file=sys.stderr)
            print(f"[ERROR] Reason: {exc}", file=sys.stderr)

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
