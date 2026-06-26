#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from common import (
    DEFAULT_LIBRARY_PATH,
    ensure_dir,
    load_json_if_exists,
    load_yaml,
    resolve_path,
    resolve_step_api_key,
    save_yaml,
    sha256_file,
)
from sync_voice_library import (
    build_effective_library,
    build_voice_candidate_pool,
    load_bundled_official_voices,
    load_review_store,
    load_voice_registry,
    save_voice_registry,
    write_sample_preview,
)


def trim_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"


def detect_mime_type(file_path: str | Path) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".wav":
        return "audio/wav"
    if ext == ".mp3":
        return "audio/mpeg"
    if ext == ".m4a":
        return "audio/mp4"
    if ext == ".flac":
        return "audio/flac"
    if ext in {".ogg", ".opus"}:
        return "audio/ogg"
    return "application/octet-stream"


def normalize_base_url(value: Any) -> str:
    return str(value or "https://api.stepfun.com/v1").rstrip("/")


def build_asset_selection(library: dict[str, Any], requested_asset_id: str | None) -> list[str]:
    clones = library.get("clones") or {}
    requested = trim_string(requested_asset_id)
    if requested:
        clone_meta = clones.get(requested)
        if not isinstance(clone_meta, dict):
            raise RuntimeError(f"未找到 clone 资产: {requested}")
        if clone_meta.get("enabled") is False:
            raise RuntimeError(f"clone 资产未启用: {requested}")
        if clone_meta.get("selected_for_clone") is not True:
            raise RuntimeError(
                f"clone 资产尚未确认付费克隆，请先把 selected_for_clone 设为 true: {requested}"
            )
        return [requested]

    selected: list[str] = []
    for asset_id, clone_meta in clones.items():
        if not isinstance(clone_meta, dict):
            continue
        if clone_meta.get("enabled") is False:
            continue
        if clone_meta.get("selected_for_clone") is True:
            selected.append(asset_id)
    return selected


def build_multipart_form_data(
    fields: dict[str, str],
    files: list[tuple[str, str, str, bytes]],
) -> tuple[str, bytes]:
    boundary = f"----CodexBoundary{uuid.uuid4().hex}"
    body = bytearray()

    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8")
        )
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    for field_name, file_name, content_type, content in files:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            (
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{file_name}"\r\n'
            ).encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return f"multipart/form-data; boundary={boundary}", bytes(body)


def request_json(request: urllib.request.Request, error_prefix: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{error_prefix}: {error.status} {text}") from error


def upload_storage_file(api_key: str, base_url: str, file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)
    content_type, body = build_multipart_form_data(
        {"purpose": "storage"},
        [("file", path.name, detect_mime_type(path), path.read_bytes())],
    )
    request = urllib.request.Request(
        f"{base_url}/files",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
        method="POST",
    )
    raw = request_json(request, "上传参考音频失败")
    file_id = trim_string(raw.get("id"))
    if not file_id:
        raise RuntimeError("上传文件接口未返回 file_id")
    return {"raw": raw, "file_id": file_id}


def create_cloned_voice(
    api_key: str,
    base_url: str,
    clone_meta: dict[str, Any],
    file_id: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": trim_string(clone_meta.get("clone_model")) or "step-tts-2",
        "file_id": file_id,
    }

    transcript = trim_string(clone_meta.get("transcript"))
    if transcript:
        payload["text"] = transcript

    sample_text = trim_string(clone_meta.get("sample_text"))
    if sample_text:
        payload["sample_text"] = sample_text

    request = urllib.request.Request(
        f"{base_url}/audio/voices",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    raw = request_json(request, "创建克隆音色失败")
    voice_id = trim_string(raw.get("id") or raw.get("voice_id"))
    if not voice_id:
        raise RuntimeError("音色克隆接口未返回 voice_id")

    return {
        "raw": raw,
        "voice_id": voice_id,
        "duplicated": raw.get("duplicated") is True,
        "sample_audio": trim_string(raw.get("sample_audio")),
    }


def upsert_registry_entry(
    *,
    library_dir: Path,
    asset_id: str,
    clone_meta: dict[str, Any],
    reference_path: Path,
    file_id: str,
    voice_id: str,
    duplicated: bool,
    preview_path: str,
    prepared_at: str,
) -> dict[str, Any]:
    return {
        "asset_id": asset_id,
        "source_file": trim_string(clone_meta.get("source_file")),
        "reference_audio_path": os.path.relpath(reference_path, library_dir),
        "reference_audio_sha256": sha256_file(reference_path),
        "clone_model": trim_string(clone_meta.get("clone_model")) or "step-tts-2",
        "transcript": trim_string(clone_meta.get("transcript")),
        "sample_text": trim_string(clone_meta.get("sample_text")),
        "voice_id": voice_id,
        "file_id": trim_string(file_id),
        "duplicated": duplicated is True,
        "preview_wav": os.path.relpath(preview_path, library_dir) if preview_path else "",
        "prepared_at": prepared_at,
    }


def rebuild_derived_files(
    *,
    library: dict[str, Any],
    library_path: Path,
    library_dir: Path,
    review_path: Path,
    registry_path: Path,
    registry: dict[str, Any],
    effective_library_path: Path,
    candidate_pool_path: Path,
    official_cache_path: Path,
) -> None:
    review_store = load_review_store(review_path)
    effective_library = build_effective_library(
        library,
        review_store,
        os.path.relpath(effective_library_path, library_dir),
        registry,
    )
    save_yaml(effective_library_path, effective_library)

    bundled_official_voices_path = (Path(__file__).resolve().parent / "../assets/official-voices.seed.json").resolve()
    official_cache = load_json_if_exists(
        official_cache_path,
        load_bundled_official_voices(bundled_official_voices_path),
    )
    candidate_pool = build_voice_candidate_pool(
        official_cache,
        effective_library,
        {
            "effectiveLibraryFile": os.path.relpath(effective_library_path, library_dir),
            "officialCacheFile": os.path.relpath(official_cache_path, library_dir),
        },
    )
    save_yaml(candidate_pool_path, candidate_pool)

    save_voice_registry(registry_path, registry)
    save_yaml(library_path, library)


def resolve_reference_path(references_dir: Path, source_file: str) -> Path:
    source_path = Path(source_file)
    if source_path.is_absolute():
        return source_path
    return (references_dir / source_path).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clone selected audiobook voices via Step paid cloning API."
    )
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY_PATH), help="Path to voice-library.yaml")
    parser.add_argument("--asset-id", dest="asset_id", help="Clone only one selected asset")
    parser.add_argument("--base-url", dest="base_url", help="Override Step API base URL")
    parser.add_argument("--dry-run", action="store_true", help="Preview paid clone actions without calling Step API")
    parser.add_argument(
        "--confirm-paid-action",
        action="store_true",
        help="Required together with real execution to confirm this may trigger paid Step voice cloning",
    )
    parser.add_argument("--force", action="store_true", help="Re-clone assets even if registry already has ready voice_id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dry_run = args.dry_run is True
    force = args.force is True
    library_path = Path(args.library).resolve()

    if not library_path.exists():
        raise RuntimeError(f"音色库文件不存在: {library_path}")

    library_dir = library_path.parent
    library = load_yaml(library_path)
    library.setdefault("paths", {})

    review_path = resolve_path(library_dir, library["paths"].get("review_file", "voice-reviews.yaml"))
    effective_library_path = resolve_path(
        library_dir,
        library["paths"].get("effective_library_file", ".audiobook/effective-voice-library.yaml"),
    )
    candidate_pool_path = resolve_path(
        library_dir,
        library["paths"].get("candidate_pool_file", ".audiobook/voice-candidate-pool.yaml"),
    )
    preview_dir = resolve_path(
        library_dir,
        library["paths"].get("previews_dir", ".audiobook/voice-previews"),
    )
    references_dir = resolve_path(
        library_dir,
        library["paths"].get("references_dir", "voices/references"),
    )
    registry_path = resolve_path(
        library_dir,
        library["paths"].get("registry_file", ".audiobook/voice-registry.json"),
    )
    official_cache_path = resolve_path(
        library_dir,
        library["paths"].get("official_cache_file", ".audiobook/official-voices-cache.json"),
    )

    ensure_dir(review_path.parent)
    ensure_dir(effective_library_path.parent)
    ensure_dir(candidate_pool_path.parent)
    ensure_dir(registry_path.parent)
    ensure_dir(preview_dir)

    target_asset_ids = build_asset_selection(library, args.asset_id)
    registry = load_voice_registry(registry_path)
    registry.setdefault("assets", {})
    base_url = normalize_base_url(args.base_url)

    if not dry_run and args.confirm_paid_action is not True:
        raise RuntimeError(
            "正式付费 clone 前必须显式确认：请先执行 --dry-run，确认无误后再附加 --confirm-paid-action。"
        )

    if not target_asset_ids:
        print(
            json.dumps(
                {
                    "mode": "dry-run" if dry_run else "execute",
                    "library_path": str(library_path),
                    "registry_path": str(registry_path),
                    "target_count": 0,
                    "message": "没有 selected_for_clone=true 的 clone 条目。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    api_key_info = {"value": "", "source": None}
    if not dry_run:
        api_key_info = resolve_step_api_key(
            [Path.cwd(), library_dir, Path(__file__).resolve().parent]
        )
        if not api_key_info.get("value"):
            raise RuntimeError("缺少 STEP_API_KEY，无法访问 Step 音色克隆接口")

    results: list[dict[str, Any]] = []
    success_count = 0
    skipped_count = 0
    error_count = 0

    for asset_id in target_asset_ids:
        clone_meta = ((library.get("clones") or {}).get(asset_id)) or {}
        source_file = trim_string(clone_meta.get("source_file"))
        reference_path = resolve_reference_path(references_dir, source_file) if source_file else Path()
        existing_entry = ((registry.get("assets") or {}).get(asset_id)) or {}
        already_ready = (
            trim_string(clone_meta.get("status")) == "ready"
            and bool(trim_string(existing_entry.get("voice_id")))
        )

        if not source_file:
            results.append(
                {
                    "asset_id": asset_id,
                    "action": "error",
                    "error": "缺少 source_file，请先执行 sync_voice_library.py 或补齐参考音频路径。",
                }
            )
            error_count += 1
            continue

        if not reference_path.exists():
            results.append(
                {
                    "asset_id": asset_id,
                    "action": "error",
                    "source_path": str(reference_path),
                    "error": "参考音频不存在。",
                }
            )
            error_count += 1
            continue

        if already_ready and not force:
            results.append(
                {
                    "asset_id": asset_id,
                    "action": "skip_existing_ready",
                    "voice_id": trim_string(existing_entry.get("voice_id")),
                    "source_path": str(reference_path),
                }
            )
            skipped_count += 1
            continue

        if dry_run:
            results.append(
                {
                    "asset_id": asset_id,
                    "action": "would_clone",
                    "source_path": str(reference_path),
                    "clone_model": trim_string(clone_meta.get("clone_model")) or "step-tts-2",
                    "transcript_present": bool(trim_string(clone_meta.get("transcript"))),
                    "sample_text_present": bool(trim_string(clone_meta.get("sample_text"))),
                    "previous_voice_id": trim_string(existing_entry.get("voice_id")),
                    "force": force,
                }
            )
            continue

        try:
            uploaded = upload_storage_file(api_key_info["value"], base_url, reference_path)
            cloned = create_cloned_voice(
                api_key_info["value"],
                base_url,
                clone_meta,
                uploaded["file_id"],
            )
            prepared_at = now_iso()
            preview_path = write_sample_preview(preview_dir, asset_id, cloned.get("sample_audio"))

            registry["assets"][asset_id] = upsert_registry_entry(
                library_dir=library_dir,
                asset_id=asset_id,
                clone_meta=clone_meta,
                reference_path=reference_path,
                file_id=uploaded["file_id"],
                voice_id=cloned["voice_id"],
                duplicated=cloned["duplicated"],
                preview_path=preview_path,
                prepared_at=prepared_at,
            )

            library.setdefault("clones", {})[asset_id] = {
                **clone_meta,
                "enabled": clone_meta.get("enabled", True) is not False,
                "status": "ready",
                "selected_for_clone": True,
                "clone_model": trim_string(clone_meta.get("clone_model")) or "step-tts-2",
                "runtime_ref": {
                    "registry_file": os.path.relpath(registry_path, library_dir),
                    "key": asset_id,
                    "last_voice_id": cloned["voice_id"],
                    "last_file_id": uploaded["file_id"],
                    "last_prepared_at": prepared_at,
                },
            }

            save_voice_registry(registry_path, registry)
            save_yaml(library_path, library)

            results.append(
                {
                    "asset_id": asset_id,
                    "action": "cloned",
                    "source_path": str(reference_path),
                    "voice_id": cloned["voice_id"],
                    "file_id": uploaded["file_id"],
                    "duplicated": cloned["duplicated"],
                    "preview_wav": os.path.relpath(preview_path, library_dir) if preview_path else "",
                }
            )
            success_count += 1
        except Exception as error:
            results.append(
                {
                    "asset_id": asset_id,
                    "action": "error",
                    "source_path": str(reference_path),
                    "error": str(error),
                }
            )
            error_count += 1

    if not dry_run:
        rebuild_derived_files(
            library=library,
            library_path=library_path,
            library_dir=library_dir,
            review_path=review_path,
            registry_path=registry_path,
            registry=registry,
            effective_library_path=effective_library_path,
            candidate_pool_path=candidate_pool_path,
            official_cache_path=official_cache_path,
        )

    print(
        json.dumps(
            {
                "mode": "dry-run" if dry_run else "execute",
                "library_path": str(library_path),
                "registry_path": str(registry_path),
                "effective_library_path": str(effective_library_path),
                "candidate_pool_path": str(candidate_pool_path),
                "target_count": len(target_asset_ids),
                "success_count": success_count,
                "skipped_count": skipped_count,
                "error_count": error_count,
                "base_url": base_url,
                "paid_action_confirmed": args.confirm_paid_action is True,
                "api_key_source": api_key_info.get("source"),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # pragma: no cover - CLI error path
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
