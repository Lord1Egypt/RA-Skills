#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import ensure_dir, trim_string
from story_artifacts import refresh_story_artifact_manifest
from tts_requests_runtime import (
    collect_segment_audio_entries,
    get_default_final_output_path,
    get_requests_base_name,
    load_tts_requests_artifact,
    parse_user_facing_segment_spec,
    save_tts_requests_artifact,
    segment_number_to_index,
    select_target_indices,
)


ENCODERS = {
    "mp3": "libmp3lame",
    "wav": "pcm_s16le",
    "flac": "flac",
    "opus": "libopus",
    "pcm": "pcm_s16le",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Concatenate audiobook segment artifacts into a final audio file."
    )
    parser.add_argument("--input", required=True, help="tts-requests artifact path")
    parser.add_argument("--output", help="Optional final audio output path")
    parser.add_argument("--segments", help="Optional 1-based segment selection for excerpt export")
    parser.add_argument("--start-segment", dest="start_segment", type=int, help="1-based start segment")
    parser.add_argument("--end-segment", dest="end_segment", type=int, help="1-based end segment")
    parser.add_argument("--normalize", action="store_true", help="Apply ffmpeg loudnorm during export")
    parser.add_argument("--target-level-db", dest="target_level_db", type=float, default=-1.0)
    parser.add_argument("--ffmpeg-path", dest="ffmpeg_path", default="ffmpeg")
    parser.add_argument("--ffprobe-path", dest="ffprobe_path", default="ffprobe")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it already exists")
    parser.add_argument("--dry-run", action="store_true", help="Preview export inputs without running ffmpeg")
    return parser.parse_args()


def build_encoder(response_format: str) -> str:
    if response_format not in ENCODERS:
        raise RuntimeError(f"当前不支持导出格式: {response_format}")
    return ENCODERS[response_format]


def compress_segment_numbers(indices: list[int]) -> str:
    if not indices:
        return "empty"

    ordered = sorted(indices)
    ranges: list[str] = []
    start = ordered[0]
    end = ordered[0]
    for index in ordered[1:]:
        if index == end + 1:
            end = index
            continue
        ranges.append(f"{start + 1}" if start == end else f"{start + 1}-{end + 1}")
        start = end = index
    ranges.append(f"{start + 1}" if start == end else f"{start + 1}-{end + 1}")
    return "_".join(ranges)


def resolve_output_path(
    request_path: Path,
    artifact: dict[str, Any],
    *,
    selected_indices: list[int],
    explicit_output: str | None,
) -> Path:
    if trim_string(explicit_output):
        return Path(str(explicit_output)).resolve()

    all_indices = sorted(int(segment.get("index") or 0) for segment in artifact.get("segments") or [])
    is_full_export = selected_indices == all_indices
    default_output = get_default_final_output_path(request_path, artifact)
    if is_full_export:
        return default_output

    label = compress_segment_numbers(selected_indices)
    response_format = trim_string((artifact.get("common_request") or {}).get("response_format")).lower() or "wav"
    return request_path.parent / f"{get_requests_base_name(request_path)}.preview-{label}.{response_format}"


def ensure_ffmpeg_available(ffmpeg_path: str) -> None:
    try:
        subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True, check=True)
    except Exception as error:
        raise RuntimeError(f"ffmpeg 不可用: {ffmpeg_path} ({error})") from error


def probe_duration_ms(ffprobe_path: str, audio_path: Path) -> int | None:
    try:
        result = subprocess.run(
            [
                ffprobe_path,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(audio_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        seconds = float((result.stdout or "").strip())
        if seconds >= 0:
            return round(seconds * 1000)
    except Exception:
        return None
    return None


def build_concat_list_text(audio_paths: list[Path]) -> str:
    lines = []
    for path in audio_paths:
        escaped = str(path).replace("\\", "\\\\").replace("'", r"'\''")
        lines.append(f"file '{escaped}'")
    return "\n".join(lines) + "\n"


def validate_selected_entries(entries: list[dict[str, Any]], *, full_export: bool) -> None:
    if not entries:
        raise RuntimeError("没有可导出的分段音频")

    missing_status = []
    missing_files = []
    for entry in entries:
        if trim_string(entry.get("status")) not in {"success", "restored"}:
            missing_status.append(entry)
        if not entry.get("exists"):
            missing_files.append(entry)

    if not missing_status and not missing_files:
        return

    lines = ["存在尚未准备好的分段音频，当前不能导出最终音频："]
    for entry in missing_status:
        lines.append(
            f"- 第 {entry['index'] + 1} 段状态为 {entry.get('status') or 'unknown'}，请先执行 synthesize_tts_requests.py"
        )
    for entry in missing_files:
        lines.append(
            f"- 第 {entry['index'] + 1} 段缺少本地音频文件: {entry['audio_path']}"
        )
    if full_export:
        lines.append("如果你暂时只想试听已完成的部分，可以用 --segments 导出局部 preview。")
    raise RuntimeError("\n".join(lines))


def run_ffmpeg_concat(
    *,
    ffmpeg_path: str,
    audio_paths: list[Path],
    output_path: Path,
    response_format: str,
    sample_rate: int,
    normalize: bool,
    target_level_db: float,
) -> subprocess.CompletedProcess[str]:
    ensure_dir(output_path.parent)
    encoder = build_encoder(response_format)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        handle.write(build_concat_list_text(audio_paths))
        list_path = Path(handle.name)

    try:
        command = [
            ffmpeg_path,
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c:a",
            encoder,
            "-ar",
            str(sample_rate),
            "-ac",
            "2",
        ]
        if normalize:
            command.extend(["-filter:a", f"loudnorm=I={target_level_db}:TP=-1.5:LRA=11"])
        command.extend(["-y", str(output_path)])
        return subprocess.run(command, capture_output=True, text=True, check=True)
    finally:
        list_path.unlink(missing_ok=True)


def main() -> None:
    args = parse_args()
    request_path = Path(args.input).resolve()
    if not request_path.exists():
        raise RuntimeError(f"tts-requests 文件不存在: {request_path}")

    artifact = load_tts_requests_artifact(request_path)
    selected_indices = select_target_indices(
        artifact,
        segments=parse_user_facing_segment_spec(args.segments) or None,
        start_index=segment_number_to_index(args.start_segment, "--start-segment"),
        end_index=segment_number_to_index(args.end_segment, "--end-segment"),
        only_failed=False,
    )
    if not selected_indices:
        raise RuntimeError("当前没有匹配到要导出的段落")

    all_indices = sorted(int(segment.get("index") or 0) for segment in artifact.get("segments") or [])
    is_full_export = selected_indices == all_indices
    entries = collect_segment_audio_entries(request_path, artifact, indices=selected_indices)
    validate_selected_entries(entries, full_export=is_full_export)

    response_format = trim_string((artifact.get("common_request") or {}).get("response_format")).lower() or "wav"
    sample_rate = int((artifact.get("common_request") or {}).get("sample_rate") or 48000)
    output_path = resolve_output_path(
        request_path,
        artifact,
        selected_indices=selected_indices,
        explicit_output=args.output,
    )
    if output_path.exists() and not args.force and not args.dry_run:
        raise RuntimeError(f"输出文件已存在，如需覆盖请加 --force: {output_path}")

    if args.dry_run:
        print(
            json_dumps(
                {
                    "mode": "dry-run",
                    "input_path": str(request_path),
                    "output_path": str(output_path),
                    "segment_count": len(entries),
                    "selected_indices": selected_indices,
                    "selected_segment_numbers": [index + 1 for index in selected_indices],
                    "full_export": is_full_export,
                    "normalize": args.normalize,
                    "response_format": response_format,
                    "sample_rate": sample_rate,
                    "audio_paths": [str(entry["audio_path"]) for entry in entries],
                }
            )
        )
        return

    ensure_ffmpeg_available(args.ffmpeg_path)
    audio_paths = [entry["audio_path"] for entry in entries]
    result = run_ffmpeg_concat(
        ffmpeg_path=args.ffmpeg_path,
        audio_paths=audio_paths,
        output_path=output_path,
        response_format=response_format,
        sample_rate=sample_rate,
        normalize=args.normalize,
        target_level_db=args.target_level_db,
    )
    duration_ms = probe_duration_ms(args.ffprobe_path, output_path)
    file_size_bytes = output_path.stat().st_size if output_path.exists() else 0

    artifact["updated_at"] = now_iso()
    artifact["latest_export"] = {
        "output_path": str(output_path),
        "response_format": response_format,
        "sample_rate": sample_rate,
        "segment_count": len(entries),
        "selected_indices": selected_indices,
        "selected_segment_numbers": [index + 1 for index in selected_indices],
        "full_export": is_full_export,
        "normalize": args.normalize,
        "duration_ms": duration_ms,
        "file_size_bytes": file_size_bytes,
        "exported_at": now_iso(),
    }
    if is_full_export:
        artifact["final_output"] = artifact["latest_export"]
    save_tts_requests_artifact(request_path, artifact)
    refresh_story_artifact_manifest(tts_requests_path=request_path)

    print(
        json_dumps(
            {
                "input_path": str(request_path),
                "output_path": str(output_path),
                "segment_count": len(entries),
                "selected_segment_numbers": [index + 1 for index in selected_indices],
                "full_export": is_full_export,
                "normalize": args.normalize,
                "duration_ms": duration_ms,
                "file_size_bytes": file_size_bytes,
                "ffmpeg_stderr_tail": (result.stderr or "").splitlines()[-10:],
            }
        )
    )


def json_dumps(payload: dict[str, Any]) -> str:
    import json

    return json.dumps(payload, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
