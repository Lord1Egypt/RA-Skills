#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import ensure_dir, resolve_api_key, trim_string
from story_artifacts import refresh_story_artifact_manifest
from step_tts_client import StepTTSClient, StepTTSError
from tts_requests_runtime import (
    get_segment_artifact_dir,
    load_tts_requests_artifact,
    merge_instruction_into_input,
    parse_user_facing_segment_spec,
    resolve_segment_audio_path,
    save_tts_requests_artifact,
    segment_number_to_index,
    select_target_indices,
    upsert_segment,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthesize replayable segment artifacts from audiobook tts-requests.json."
    )
    parser.add_argument("--input", required=True, help="tts-requests artifact path")
    parser.add_argument(
        "--segments",
        help="User-facing 1-based segment selection, e.g. 1,2,5-8",
    )
    parser.add_argument("--start-segment", dest="start_segment", type=int, help="User-facing 1-based start segment")
    parser.add_argument("--end-segment", dest="end_segment", type=int, help="User-facing 1-based end segment")
    parser.add_argument("--only-failed", action="store_true", help="Only synthesize segments currently marked failed")
    parser.add_argument("--force", action="store_true", help="Re-synthesize even if audio artifact already exists")
    parser.add_argument("--dry-run", action="store_true", help="Preview selected segments without calling TTS")
    parser.add_argument(
        "--request-mode",
        choices=["auto", "split_instruction", "inline_prefixed"],
        default="auto",
        help="How to send instruction to Step TTS",
    )
    parser.add_argument("--api-key-env", dest="api_key_env", default="STEP_API_KEY")
    parser.add_argument("--base-url", dest="base_url", default="https://api.stepfun.com/v1")
    parser.add_argument("--model", help="Optional model override; defaults to tts-requests.common_request.model")
    parser.add_argument("--request-interval-ms", dest="request_interval_ms", type=int, default=6500)
    parser.add_argument("--max-retries", dest="max_retries", type=int, default=3)
    parser.add_argument("--timeout-sec", dest="timeout_sec", type=int, default=60)
    parser.add_argument("--speed", type=float, help="Optional TTS speed override")
    return parser.parse_args()


def probe_audio_duration_ms(audio_path: Path) -> int | None:
    try:
        result = subprocess.run(
            [
                "ffprobe",
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


def build_request_payload(
    *,
    segment: dict[str, Any],
    request_mode: str,
) -> dict[str, str]:
    input_text = trim_string(segment.get("input_text"))
    instruction = trim_string(segment.get("instruction"))

    if request_mode == "inline_prefixed":
        merged = merge_instruction_into_input(input_text, instruction)
        return {
            "api_input_text": merged["api_input_text"],
            "api_instruction": "",
            "request_instruction_mode": merged["request_instruction_mode"],
        }

    return {
        "api_input_text": input_text,
        "api_instruction": instruction,
        "request_instruction_mode": "split_instruction",
    }


def should_attempt_inline_fallback(error: StepTTSError, segment: dict[str, Any], request_mode: str) -> bool:
    if request_mode != "auto":
        return False
    if error.status != 400:
        return False
    if not trim_string(segment.get("instruction")):
        return False
    body = trim_string(error.body).lower()
    return "instruction is not supported" in body


def merge_extra_payload(common_request: dict[str, Any], segment: dict[str, Any], speed: float | None) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    common_extra = common_request.get("extra_body")
    segment_extra = segment.get("extra_body")
    if isinstance(common_extra, dict):
        merged.update(common_extra)
    if isinstance(segment_extra, dict):
        merged.update(segment_extra)
    if speed is not None:
        merged["speed"] = speed
    return merged


def synthesize_segment(
    *,
    client: StepTTSClient,
    segment: dict[str, Any],
    common_request: dict[str, Any],
    model: str,
    sample_rate: int,
    response_format: str,
    request_mode: str,
    speed: float | None,
) -> dict[str, Any]:
    primary_payload = build_request_payload(
        segment=segment,
        request_mode="split_instruction" if request_mode == "auto" else request_mode,
    )
    extra_payload = merge_extra_payload(common_request, segment, speed)

    try:
        result = client.synthesize(
            model=model,
            input_text=primary_payload["api_input_text"],
            instruction=primary_payload["api_instruction"],
            voice_id=trim_string(segment.get("voice_id")),
            sample_rate=sample_rate,
            response_format=response_format,
            extra_payload=extra_payload or None,
        )
        return {
            **result,
            "api_input_text": primary_payload["api_input_text"],
            "api_instruction": primary_payload["api_instruction"],
            "request_instruction_mode": primary_payload["request_instruction_mode"],
            "fallback_used": False,
        }
    except StepTTSError as error:
        if not should_attempt_inline_fallback(error, segment, request_mode):
            raise

        fallback_payload = build_request_payload(segment=segment, request_mode="inline_prefixed")
        result = client.synthesize(
            model=model,
            input_text=fallback_payload["api_input_text"],
            instruction=fallback_payload["api_instruction"],
            voice_id=trim_string(segment.get("voice_id")),
            sample_rate=sample_rate,
            response_format=response_format,
            extra_payload=extra_payload or None,
        )
        return {
            **result,
            "api_input_text": fallback_payload["api_input_text"],
            "api_instruction": fallback_payload["api_instruction"],
            "request_instruction_mode": fallback_payload["request_instruction_mode"],
            "fallback_used": True,
            "fallback_from_error": {
                "status": error.status,
                "body": error.body,
            },
        }


def validate_segment_for_tts(segment: dict[str, Any]) -> None:
    if not trim_string(segment.get("voice_id")):
        raise RuntimeError(
            f"第 {int(segment.get('index') or 0) + 1} 段缺少 voice_id，通常表示 casting-plan 还没 ready"
        )
    if not trim_string(segment.get("input_text")):
        raise RuntimeError(f"第 {int(segment.get('index') or 0) + 1} 段缺少 input_text")


def main() -> None:
    args = parse_args()
    request_path = Path(args.input).resolve()
    if not request_path.exists():
        raise RuntimeError(f"tts-requests 文件不存在: {request_path}")

    artifact = load_tts_requests_artifact(request_path)
    common_request = artifact.get("common_request") or {}
    response_format = trim_string(common_request.get("response_format")).lower()
    sample_rate = int(common_request.get("sample_rate") or 0)
    model = trim_string(args.model) or trim_string(common_request.get("model")) or "stepaudio-2.5-tts"

    selected_indices = select_target_indices(
        artifact,
        segments=parse_user_facing_segment_spec(args.segments) or None,
        start_index=segment_number_to_index(args.start_segment, "--start-segment"),
        end_index=segment_number_to_index(args.end_segment, "--end-segment"),
        only_failed=args.only_failed,
    )
    if not selected_indices:
        raise RuntimeError("当前没有匹配到要合成的段落")

    selected_segments = []
    skipped_existing: list[int] = []
    for segment in artifact.get("segments") or []:
        index = int(segment.get("index") or 0)
        if index not in selected_indices:
            continue
        audio_path = Path(str(segment.get("audio_path") or "")).resolve() if trim_string(segment.get("audio_path")) else None
        if (
            not args.force
            and trim_string(segment.get("status")) in {"success", "restored"}
            and audio_path
            and audio_path.exists()
        ):
            skipped_existing.append(index)
            continue
        selected_segments.append(segment)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "input_path": str(request_path),
                    "selected_indices": selected_indices,
                    "skipped_existing_indices": skipped_existing,
                    "target_count": len(selected_segments),
                "request_mode": args.request_mode,
                "model": model,
                "sample_rate": sample_rate,
                "response_format": response_format,
                "selected_segment_numbers": [index + 1 for index in selected_indices],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    api_key_info = resolve_api_key([Path.cwd(), request_path.parent, Path(__file__).resolve().parent], args.api_key_env)
    if not api_key_info.get("value"):
        raise RuntimeError(f"缺少 {args.api_key_env}，无法调用 Step TTS")

    client = StepTTSClient(
        api_key=str(api_key_info["value"]),
        base_url=args.base_url,
        request_interval_ms=args.request_interval_ms,
        max_retries=args.max_retries,
        timeout_sec=args.timeout_sec,
    )

    artifact.setdefault("updated_at", now_iso())
    ensure_dir(request_path.parent)

    results: list[dict[str, Any]] = []
    failed_count = 0
    success_count = 0

    for segment in sorted(selected_segments, key=lambda item: int(item.get("index") or 0)):
        index = int(segment.get("index") or 0)
        try:
            validate_segment_for_tts(segment)
            synthesized = synthesize_segment(
                client=client,
                segment=segment,
                common_request=common_request,
                model=model,
                sample_rate=sample_rate,
                response_format=response_format,
                request_mode=args.request_mode,
                speed=args.speed,
            )
            audio_path = resolve_segment_audio_path(request_path, segment, response_format)
            ensure_dir(audio_path.parent)
            audio_path.write_bytes(synthesized["audio_bytes"])
            duration_ms = probe_audio_duration_ms(audio_path)

            updated_segment = {
                **segment,
                "status": "success",
                "audio_path": str(audio_path),
                "duration_ms": duration_ms,
                "file_size_bytes": audio_path.stat().st_size,
                "resolved_model": synthesized.get("resolved_model") or model,
                "request_instruction_mode": synthesized.get("request_instruction_mode"),
                "api_input_text": synthesized.get("api_input_text") or "",
                "api_instruction": synthesized.get("api_instruction") or "",
                "response_content_type": synthesized.get("content_type") or "",
                "fallback_used": synthesized.get("fallback_used") is True,
                "fallback_from_error": synthesized.get("fallback_from_error") or None,
                "error": "",
                "updated_at": now_iso(),
            }
            upsert_segment(artifact, updated_segment)
            success_count += 1
            results.append(
                {
                    "index": index,
                    "speaker_id": segment.get("speaker_id"),
                    "status": "success",
                    "audio_path": str(audio_path),
                    "duration_ms": duration_ms,
                    "request_instruction_mode": updated_segment["request_instruction_mode"],
                    "fallback_used": synthesized.get("fallback_used") is True,
                    "fallback_from_error": synthesized.get("fallback_from_error") or None,
                }
            )
        except Exception as error:
            failed_count += 1
            updated_segment = {
                **segment,
                "status": "failed",
                "error": str(error),
                "updated_at": now_iso(),
            }
            upsert_segment(artifact, updated_segment)
            results.append(
                {
                    "index": index,
                    "speaker_id": segment.get("speaker_id"),
                    "status": "failed",
                    "error": str(error),
                }
            )
        finally:
            artifact["updated_at"] = now_iso()
            save_tts_requests_artifact(request_path, artifact)

    refresh_story_artifact_manifest(tts_requests_path=request_path)

    print(
        json.dumps(
            {
                "input_path": str(request_path),
                "api_key_env": args.api_key_env,
                "api_key_source": api_key_info.get("source"),
                "base_url": args.base_url,
                "request_mode": args.request_mode,
                "model": model,
                "sample_rate": sample_rate,
                "response_format": response_format,
                "selected_indices": selected_indices,
                "selected_segment_numbers": [index + 1 for index in selected_indices],
                "skipped_existing_indices": skipped_existing,
                "skipped_existing_segment_numbers": [index + 1 for index in skipped_existing],
                "target_count": len(selected_segments),
                "success_count": success_count,
                "failed_count": failed_count,
                "segment_dir": str(get_segment_artifact_dir(request_path)),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
