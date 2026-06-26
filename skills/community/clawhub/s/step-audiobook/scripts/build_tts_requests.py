#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    ensure_dir,
    get_story_base_name,
    load_yaml,
    normalize_string_array,
    resolve_story_workspace_dir,
    save_json,
    trim_string,
)
from instruction_builder import InstructionBuilder
from script_runtime import load_normalized_script
from story_artifacts import refresh_story_artifact_manifest


VALID_RESPONSE_FORMATS = {"wav", "mp3", "flac", "opus"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build replayable tts-requests from a structured audiobook script plus casting-plan."
    )
    parser.add_argument("--input", required=True, help="Structured script path (.yaml/.yml/.json)")
    parser.add_argument("--casting", help="Casting plan path; defaults to <input>.casting-plan.yaml")
    parser.add_argument(
        "--output",
        help="Output tts-requests artifact path; defaults to sibling .audiobook/<input>.tts-requests.json",
    )
    parser.add_argument("--model", default="stepaudio-2.5-tts")
    parser.add_argument("--sample-rate", dest="sample_rate", type=int, default=48000)
    parser.add_argument(
        "--response-format",
        dest="response_format",
        default="wav",
        help="Audio response format: wav/mp3/flac/opus",
    )
    parser.add_argument(
        "--volume",
        type=float,
        help="Optional TTS volume passthrough; written to common_request.extra_body.volume",
    )
    parser.add_argument(
        "--tone-map",
        dest="tone_map",
        action="append",
        default=[],
        help="Repeatable pronunciation_map.tone entry, for example: 阿胶/e1胶",
    )
    parser.add_argument(
        "--pronunciation-map-file",
        dest="pronunciation_map_file",
        help="Optional JSON/YAML file for pronunciation_map; accepts either a raw map object or {pronunciation_map: {...}}",
    )
    return parser.parse_args()


def resolve_default_casting_plan_path(input_path: Path) -> Path:
    return resolve_story_workspace_dir(input_path) / f"{get_story_base_name(input_path)}.casting-plan.yaml"


def resolve_default_output_path(input_path: Path) -> Path:
    return resolve_story_workspace_dir(input_path) / f"{get_story_base_name(input_path)}.tts-requests.json"


def resolve_default_audio_output_path(input_path: Path, response_format: str) -> Path:
    return resolve_story_workspace_dir(input_path) / f"{get_story_base_name(input_path)}.audiobook.{response_format}"


def get_requests_base_name(output_path: Path) -> str:
    base = output_path.stem
    return base[: -len(".tts-requests")] if base.endswith(".tts-requests") else base


def get_runtime_script_artifact_path(output_path: Path) -> Path:
    return output_path.parent / f"{get_requests_base_name(output_path)}.script-runtime.json"


def derive_quality_profile(sample_rate: int, response_format: str) -> str:
    if sample_rate >= 48000 and response_format == "wav":
        return "max"
    if sample_rate >= 24000 and response_format in {"wav", "flac"}:
        return "balanced"
    return "compact"


def load_pronunciation_map_file(file_path: Path) -> dict[str, Any]:
    parsed = load_yaml(file_path)
    if isinstance(parsed, dict) and isinstance(parsed.get("pronunciation_map"), dict):
        parsed = parsed["pronunciation_map"]
    if not isinstance(parsed, dict):
        raise RuntimeError(f"pronunciation_map 文件必须是对象: {file_path}")

    normalized = dict(parsed)
    if "tone" in normalized:
        tone_entries = normalize_string_array(normalized.get("tone"))
        if tone_entries:
            normalized["tone"] = tone_entries
        else:
            normalized.pop("tone", None)
    return normalized


def build_common_extra_body(args: argparse.Namespace) -> dict[str, Any]:
    extra_body: dict[str, Any] = {}
    if args.volume is not None:
        if args.volume < 0:
            raise RuntimeError("--volume 不能是负数")
        extra_body["volume"] = float(args.volume)

    pronunciation_map: dict[str, Any] = {}
    if args.pronunciation_map_file:
        pronunciation_map = load_pronunciation_map_file(Path(args.pronunciation_map_file).resolve())

    tone_entries = normalize_string_array(args.tone_map)
    if tone_entries:
        merged_tones = normalize_string_array([*(pronunciation_map.get("tone") or []), *tone_entries])
        if merged_tones:
            pronunciation_map["tone"] = merged_tones

    if pronunciation_map:
        extra_body["pronunciation_map"] = pronunciation_map
    return extra_body


def load_casting_plan(casting_path: Path) -> dict[str, Any]:
    parsed = load_yaml(casting_path)
    if not isinstance(parsed, dict):
        raise RuntimeError(f"casting-plan 不是合法对象: {casting_path}")
    if not isinstance(parsed.get("roles"), list) or not parsed.get("roles"):
        raise RuntimeError(f"casting-plan 缺少 roles，无法生成 tts-requests: {casting_path}")
    return parsed


def normalize_role_entry(role: Any) -> dict[str, Any]:
    if not isinstance(role, dict):
        raise RuntimeError("casting-plan.roles[] 每一项都必须是对象")
    role_id = trim_string(role.get("role_id"))
    if not role_id:
        raise RuntimeError("casting-plan.roles[].role_id 不能为空")

    selected_source = trim_string(role.get("selected_source"))
    selected_asset_id = trim_string(role.get("selected_asset_id"))
    selected_voice_id = trim_string(role.get("selected_voice_id"))
    if not selected_voice_id and selected_source == "official":
        selected_voice_id = selected_asset_id

    return {
        "role_id": role_id,
        "role_name": trim_string(role.get("role_name")) or role_id,
        "selected_source": selected_source,
        "selected_asset_id": selected_asset_id,
        "selected_display_name": trim_string(role.get("selected_display_name")) or selected_asset_id or role_id,
        "selected_status": trim_string(role.get("selected_status")),
        "selected_voice_id": selected_voice_id,
        "selected_reason": trim_string(role.get("selected_reason")),
        "stable_instruction": trim_string(role.get("stable_instruction")),
        "current_instruction": trim_string(role.get("current_instruction")),
        "review_status": trim_string(role.get("review_status")),
        "notes": trim_string(role.get("notes")),
    }


def build_role_map(casting_plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    role_map: dict[str, dict[str, Any]] = {}
    for raw_role in casting_plan.get("roles") or []:
        role = normalize_role_entry(raw_role)
        role_map[role["role_id"]] = role
    return role_map


def resolve_role_voice_readiness(role: dict[str, Any]) -> tuple[bool, str]:
    if not role.get("selected_source") or not role.get("selected_asset_id"):
        return False, "缺少 selected_source / selected_asset_id"

    if role.get("selected_source") == "clone" and not role.get("selected_voice_id"):
        return False, "选中了 clone，但尚未拿到 ready voice_id（通常表示还没执行真正付费 clone）"

    if role.get("selected_status") and role.get("selected_status") != "ready":
        return False, f"selected_status={role['selected_status']}"

    if not role.get("selected_voice_id"):
        return False, "缺少 selected_voice_id"

    return True, ""


def build_blocking_errors(
    *,
    script: dict[str, Any],
    role_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    segment_indices_by_speaker: dict[str, list[int]] = {}
    for segment in script.get("segments") or []:
        speaker = trim_string(segment.get("speaker"))
        segment_indices_by_speaker.setdefault(speaker, []).append(int(segment.get("index") or 0))

    issues: list[dict[str, Any]] = []
    for speaker, indices in segment_indices_by_speaker.items():
        role = role_map.get(speaker)
        if not role:
            issues.append(
                {
                    "role_id": speaker,
                    "role_name": speaker,
                    "reason": "casting-plan 里找不到该角色的选角结果",
                    "segments": indices,
                }
            )
            continue

        is_ready, reason = resolve_role_voice_readiness(role)
        if is_ready:
            continue

        issues.append(
            {
                "role_id": role["role_id"],
                "role_name": role["role_name"],
                "selected_source": role.get("selected_source"),
                "selected_asset_id": role.get("selected_asset_id"),
                "selected_status": role.get("selected_status"),
                "selected_voice_id": role.get("selected_voice_id"),
                "reason": reason,
                "segments": indices,
            }
        )
    return issues


def format_blocking_errors(issues: list[dict[str, Any]]) -> str:
    lines = [
        "当前 casting-plan 里仍有角色没有 ready 音色，不能继续生成 tts-requests：",
    ]
    for issue in issues:
        segment_text = ", ".join(f"#{index + 1}" for index in issue.get("segments") or [])
        lines.append(
            "- "
            + " / ".join(
                [
                    trim_string(issue.get("role_id")) or "unknown_role",
                    trim_string(issue.get("role_name")) or "unknown_name",
                ]
            )
            + f": {issue.get('reason')}"
            + (
                f"；selected={issue.get('selected_source')}:{issue.get('selected_asset_id')}"
                if issue.get("selected_asset_id")
                else ""
            )
            + (f"；涉及段落 {segment_text}" if segment_text else "")
        )
    lines.extend(
        [
            "请先完成以下任一动作后再重跑：",
            "1. 在 clone-review 里确认并执行真正 paid clone，让 clone 进入 ready 状态；",
            "2. 或手动把对应角色改选成一个 official ready 音色，再刷新 casting-plan。",
        ]
    )
    return "\n".join(lines)


def build_request_segment(
    *,
    segment: dict[str, Any],
    role: dict[str, Any],
    instruction_builder: InstructionBuilder,
    global_instruction: str,
) -> dict[str, Any]:
    prepared = instruction_builder.build_for_segment(
        segment,
        role_stable_instruction=role.get("stable_instruction") or role.get("current_instruction") or "",
        global_instruction=global_instruction,
    )
    input_text = trim_string(prepared["tts_input_text"])
    if not input_text:
        raise RuntimeError(f"段落 #{int(segment.get('index') or 0) + 1} 清理后没有可送入 TTS 的文本")

    return {
        "index": int(segment.get("index") or 0),
        "speaker_id": segment.get("speaker"),
        "speaker_name": segment.get("character_name") or segment.get("speaker"),
        "status": "pending",
        "delivery_mode": segment.get("delivery_mode") or "dialogue",
        "raw_text": trim_string(segment.get("raw_text")),
        "clean_text": trim_string(prepared["clean_text"]),
        "input_text": input_text,
        "instruction": trim_string(prepared["instruction"]),
        "voice_id": role.get("selected_voice_id"),
        "voice_type": role.get("selected_source"),
        "voice_source": role.get("selected_source"),
        "selected_asset_id": role.get("selected_asset_id"),
        "selected_display_name": role.get("selected_display_name"),
        "selected_status": role.get("selected_status"),
        "selection_reason": role.get("selected_reason"),
        "inline_instruction": trim_string(prepared["inline_instruction"]),
        "scene_instruction": trim_string(prepared["scene_instruction"]),
        "character_instruction": trim_string(prepared["character_instruction"]),
        "role_stable_instruction": trim_string(prepared["role_stable_instruction"]),
        "review_status": role.get("review_status") or "",
        "extra_body": {},
        "metadata": segment.get("metadata") if isinstance(segment.get("metadata"), dict) else {},
        "updated_at": now_iso(),
    }


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise RuntimeError(f"输入脚本不存在: {input_path}")

    response_format = str(args.response_format or "").strip().lower()
    if response_format not in VALID_RESPONSE_FORMATS:
        raise RuntimeError(f"不支持的 response-format: {args.response_format}")
    if args.sample_rate <= 0:
        raise RuntimeError("--sample-rate 必须是正整数")
    common_extra_body = build_common_extra_body(args)

    casting_path = Path(args.casting).resolve() if args.casting else resolve_default_casting_plan_path(input_path)
    if not casting_path.exists():
        raise RuntimeError(f"缺少 casting-plan，请先执行 recommend_casting.py: {casting_path}")

    output_path = Path(args.output).resolve() if args.output else resolve_default_output_path(input_path)
    runtime_script_path = get_runtime_script_artifact_path(output_path)
    ensure_dir(output_path.parent)

    normalized_script = load_normalized_script(input_path)
    save_json(runtime_script_path, normalized_script)

    casting_plan = load_casting_plan(casting_path)
    role_map = build_role_map(casting_plan)
    blocking_issues = build_blocking_errors(script=normalized_script, role_map=role_map)
    if blocking_issues:
        raise RuntimeError(format_blocking_errors(blocking_issues))

    instruction_builder = InstructionBuilder(max_length=200)
    request_segments = [
        build_request_segment(
            segment=segment,
            role=role_map[segment["speaker"]],
            instruction_builder=instruction_builder,
            global_instruction=trim_string(normalized_script.get("global_instruction")),
        )
        for segment in normalized_script.get("segments") or []
    ]

    artifact = {
        "version": "1",
        "generated_at": now_iso(),
        "updated_at": now_iso(),
        "title": trim_string(normalized_script.get("title")) or input_path.stem,
        "source": {
            "input_path": str(input_path),
            "script_path": str(input_path),
            "casting_plan_path": str(casting_path),
            "runtime_script_path": str(runtime_script_path),
            "output_path": str(resolve_default_audio_output_path(input_path, response_format)),
        },
        "common_request": {
            "model": trim_string(args.model) or "stepaudio-2.5-tts",
            "sample_rate": int(args.sample_rate),
            "response_format": response_format,
            "quality_profile": derive_quality_profile(int(args.sample_rate), response_format),
            "extra_body": common_extra_body,
        },
        "global_instruction": trim_string(normalized_script.get("global_instruction")),
        "segments": request_segments,
    }
    save_json(output_path, artifact)
    refresh_story_artifact_manifest(
        effective_story_input_path=input_path,
        casting_output_path=casting_path,
        tts_requests_path=output_path,
    )

    print(
        json.dumps(
            {
                "input_path": str(input_path),
                "casting_plan_path": str(casting_path),
                "runtime_script_path": str(runtime_script_path),
                "output_path": str(output_path),
                "suggested_audio_output_path": artifact["source"]["output_path"],
                "segment_count": len(request_segments),
                "role_count": len(role_map),
                "model": artifact["common_request"]["model"],
                "sample_rate": artifact["common_request"]["sample_rate"],
                "response_format": artifact["common_request"]["response_format"],
                "extra_body": artifact["common_request"]["extra_body"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
