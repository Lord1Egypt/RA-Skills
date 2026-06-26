#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from common import ensure_dir, load_json, save_json, trim_string
from instruction_builder import InstructionBuilder, sanitize_spoken_text


VALID_RESPONSE_FORMATS = {"wav", "mp3", "flac", "opus", "pcm"}


def get_requests_base_name(request_path: Path) -> str:
    base = request_path.stem
    return base[: -len(".tts-requests")] if base.endswith(".tts-requests") else base


def get_segment_artifact_dir(request_path: Path) -> Path:
    return request_path.parent / f"{get_requests_base_name(request_path)}.segments"


def get_default_final_output_path(request_path: Path, artifact: dict[str, Any]) -> Path:
    source = artifact.get("source") or {}
    explicit_output = trim_string(source.get("output_path"))
    if explicit_output:
        return Path(explicit_output).resolve()

    response_format = trim_string((artifact.get("common_request") or {}).get("response_format")).lower() or "wav"
    return request_path.parent / f"{get_requests_base_name(request_path)}.audiobook.{response_format}"


def load_tts_requests_artifact(request_path: str | Path) -> dict[str, Any]:
    path = Path(request_path).resolve()
    parsed = load_json(path)
    if not isinstance(parsed, dict):
        raise RuntimeError(f"tts-requests 不是合法对象: {path}")
    if not isinstance(parsed.get("source"), dict):
        raise RuntimeError(f"tts-requests 缺少 source: {path}")
    if not isinstance(parsed.get("common_request"), dict):
        raise RuntimeError(f"tts-requests 缺少 common_request: {path}")
    if not isinstance(parsed.get("segments"), list):
        raise RuntimeError(f"tts-requests 缺少 segments 数组: {path}")

    response_format = trim_string((parsed.get("common_request") or {}).get("response_format")).lower()
    if response_format and response_format not in VALID_RESPONSE_FORMATS:
        raise RuntimeError(f"tts-requests.response_format 不支持: {response_format}")

    parsed.setdefault("version", "1")
    parsed.setdefault("global_instruction", "")
    parsed.setdefault("updated_at", parsed.get("generated_at") or "")
    common_request = parsed.get("common_request") or {}
    if not isinstance(common_request.get("extra_body"), dict):
        common_request["extra_body"] = {}
    parsed["common_request"] = common_request
    for segment in parsed.get("segments") or []:
        if isinstance(segment, dict) and not isinstance(segment.get("extra_body"), dict):
            segment["extra_body"] = {}
    return parsed


def save_tts_requests_artifact(request_path: str | Path, artifact: dict[str, Any]) -> None:
    save_json(request_path, artifact)


def build_segment_file_name(index: int, speaker_id: str, response_format: str) -> str:
    safe_speaker = re.sub(r"[^0-9A-Za-z\u4e00-\u9fa5_-]+", "-", trim_string(speaker_id) or "speaker").strip("-")
    safe_speaker = safe_speaker or "speaker"
    return f"{index + 1:04d}-{safe_speaker}.{response_format}"


def resolve_segment_audio_path(request_path: str | Path, segment: dict[str, Any], response_format: str) -> Path:
    base_dir = get_segment_artifact_dir(Path(request_path).resolve())
    ensure_dir(base_dir)
    return base_dir / build_segment_file_name(int(segment.get("index") or 0), trim_string(segment.get("speaker_id")), response_format)


def parse_user_facing_segment_spec(raw_value: str | None) -> list[int]:
    if not trim_string(raw_value):
        return []

    selected: set[int] = set()
    for token in [part.strip() for part in str(raw_value).split(",") if part.strip()]:
        if "-" in token:
            left, right = token.split("-", 1)
            start = int(left)
            end = int(right)
            if start <= 0 or end <= 0:
                raise RuntimeError("--segments 使用 1-based 编号，最小值为 1")
            if end < start:
                raise RuntimeError(f"非法段落范围: {token}")
            selected.update(range(start - 1, end))
            continue

        value = int(token)
        if value <= 0:
            raise RuntimeError("--segments 使用 1-based 编号，最小值为 1")
        selected.add(value - 1)

    return sorted(selected)


def segment_number_to_index(value: int | None, flag_name: str) -> int | None:
    if value is None:
        return None
    if value <= 0:
        raise RuntimeError(f"{flag_name} 使用 1-based 编号，最小值为 1")
    return value - 1


def find_segment(artifact: dict[str, Any], index: int) -> dict[str, Any]:
    for segment in artifact.get("segments") or []:
        if int(segment.get("index") or -1) == index:
            return segment
    raise RuntimeError(f"tts-requests 中找不到 index={index} 的 segment")


def upsert_segment(artifact: dict[str, Any], updated_segment: dict[str, Any]) -> None:
    target_index = int(updated_segment.get("index") or -1)
    segments = artifact.get("segments") or []
    for index, segment in enumerate(segments):
        if int(segment.get("index") or -1) == target_index:
            merged = {**segment, **updated_segment}
            segments[index] = merged
            break
    else:
        segments.append(updated_segment)
    segments.sort(key=lambda item: int(item.get("index") or 0))
    artifact["segments"] = segments


def extract_prefix_instruction(text: str) -> tuple[str, str]:
    normalized = sanitize_spoken_text(text)
    if not normalized:
        return "", ""

    pattern = re.compile(r"^[（(]\s*([^（）()]{1,200}?)\s*[）)]\s*(.*)$", re.DOTALL)
    match = pattern.match(normalized)
    if not match:
        return "", normalized

    return trim_string(match.group(1)), sanitize_spoken_text(match.group(2))


def merge_instruction_into_input(input_text: str, instruction: str) -> dict[str, str]:
    safe_input = sanitize_spoken_text(input_text)
    safe_instruction = trim_string(instruction)
    if not safe_instruction:
        return {
            "api_input_text": safe_input,
            "request_instruction_mode": "input_only",
        }

    builder = InstructionBuilder()
    prefix_instruction, remaining_text = extract_prefix_instruction(safe_input)
    merged_instruction = builder.merge_instruction_parts(safe_instruction, prefix_instruction)

    if not remaining_text:
        remaining_text = safe_input

    return {
        "api_input_text": f"（{merged_instruction}）{remaining_text}",
        "request_instruction_mode": "inline_prefixed",
    }


def select_target_indices(
    artifact: dict[str, Any],
    *,
    segments: list[int] | None = None,
    start_index: int | None = None,
    end_index: int | None = None,
    only_failed: bool = False,
) -> list[int]:
    all_indices = [int(segment.get("index") or 0) for segment in artifact.get("segments") or []]
    selected = set(all_indices)

    if segments:
        selected &= set(segments)
    if start_index is not None:
        selected = {index for index in selected if index >= start_index}
    if end_index is not None:
        selected = {index for index in selected if index <= end_index}
    if only_failed:
        failed = {
            int(segment.get("index") or 0)
            for segment in artifact.get("segments") or []
            if trim_string(segment.get("status")) == "failed"
        }
        selected &= failed

    return sorted(selected)


def collect_segment_audio_entries(
    request_path: str | Path,
    artifact: dict[str, Any],
    *,
    indices: list[int] | None = None,
) -> list[dict[str, Any]]:
    request_resolved = Path(request_path).resolve()
    response_format = trim_string((artifact.get("common_request") or {}).get("response_format")).lower() or "wav"
    selected = set(indices) if indices is not None else {
        int(segment.get("index") or 0)
        for segment in artifact.get("segments") or []
    }

    entries: list[dict[str, Any]] = []
    for segment in sorted(artifact.get("segments") or [], key=lambda item: int(item.get("index") or 0)):
        index = int(segment.get("index") or 0)
        if index not in selected:
            continue

        status = trim_string(segment.get("status"))
        raw_audio_path = trim_string(segment.get("audio_path"))
        audio_path = Path(raw_audio_path).resolve() if raw_audio_path else resolve_segment_audio_path(request_resolved, segment, response_format)
        entries.append(
            {
                "index": index,
                "speaker_id": trim_string(segment.get("speaker_id")),
                "status": status,
                "audio_path": audio_path,
                "exists": audio_path.exists(),
                "segment": segment,
            }
        )
    return entries
