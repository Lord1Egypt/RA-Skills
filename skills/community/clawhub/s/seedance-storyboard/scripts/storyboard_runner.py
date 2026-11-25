#!/usr/bin/env python3
"""End-to-end Asset-First storyboard runner for HotAPI (Seedream 5.0 + Seedance 2.5/2.0).

Uses Python 3 standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import http.client
import json
import math
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "https://api.hotapi.ai"
DEFAULT_POLL_INTERVAL = 3.0
DEFAULT_POLL_TIMEOUT = 900.0
UPLOAD_REFRESH_MARGIN_SECONDS = 300
TERMINAL_STATUSES = {"succeeded", "failed", "cancelled", "expired"}

IMAGE_MODELS: dict[str, dict[str, Any]] = {
    "seedream-5.0-pro-spicy": {
        "sizes": ("2K",),
        "credits_per_image": 120,
    },
    "seedream-5.0-lite-spicy": {
        "sizes": ("2K", "3K", "4K"),
        "credits_per_image": 60,
    },
}

VIDEO_MODELS: dict[str, dict[str, Any]] = {
    "seedance-2.5-spicy": {
        "max_ref_images": 30,
        "max_ref_audio": 10,
        "max_ref_video": 10,
        "min_duration": 4,
        "max_duration": 30,
        "supports_draft": True,
        "supports_output_format": True,
        "audio_requires_visual_ref": False,
        "resolutions": ("480p", "720p", "1080p"),
        "credits_per_sec": {"480p": 206, "720p": 463, "1080p": 1137},
    },
    "seedance-2.5-flash-spicy": {
        "max_ref_images": 10,
        "max_ref_audio": 5,
        "max_ref_video": 5,
        "min_duration": 4,
        "max_duration": 30,
        "supports_draft": False,
        "supports_output_format": True,
        "audio_requires_visual_ref": False,
        "resolutions": ("480p", "720p"),
        "credits_per_sec": {"480p": 136, "720p": 304},
    },
    "seedance-2.0-spicy": {
        "max_ref_images": 9,
        "max_ref_audio": 3,
        "max_ref_video": 3,
        "min_duration": 4,
        "max_duration": 15,
        "supports_draft": False,
        "supports_output_format": False,
        "audio_requires_visual_ref": True,
        "resolutions": ("480p", "720p", "1080p", "4k"),
        "credits_per_sec": {"480p": 140, "720p": 304, "1080p": 748, "4k": 1556},
    },
    "seedance-2.0-fast-spicy": {
        "max_ref_images": 9,
        "max_ref_audio": 3,
        "max_ref_video": 3,
        "min_duration": 4,
        "max_duration": 15,
        "supports_draft": False,
        "supports_output_format": False,
        "audio_requires_visual_ref": True,
        "resolutions": ("480p", "720p"),
        "credits_per_sec": {"480p": 53, "720p": 113},
    },
    "seedance-2.0-mini-spicy": {
        "max_ref_images": 9,
        "max_ref_audio": 3,
        "max_ref_video": 3,
        "min_duration": 4,
        "max_duration": 15,
        "supports_draft": False,
        "supports_output_format": False,
        "audio_requires_visual_ref": True,
        "resolutions": ("480p", "720p"),
        "credits_per_sec": {"480p": 30, "720p": 60},
    },
}

VIDEO_RATIOS = {"21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "adaptive"}
IMAGE_RATIOS = {"1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9"}
OUTPUT_FORMATS = {"mp4", "mov"}

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")
ALNUM_RE = re.compile(r"[A-Za-z0-9]")


class RunnerError(RuntimeError):
    """Actionable failure raised by runner operations."""


def load_json(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise RunnerError(f"Failed to read {path}: {exc}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RunnerError(f"Invalid JSON in {path}: {exc}") from exc


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex[:8]}.tmp")
    content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    try:
        tmp_path.write_text(content, encoding="utf-8")
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def estimate_speech_seconds(text: str) -> float:
    cjk_count = len(CJK_RE.findall(text))
    latin_count = len(ALNUM_RE.findall(text))
    return (cjk_count / 4.5) + (latin_count / 14.0) + 0.3


def unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def collect_segment_asset_refs(seg: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    if isinstance(seg.get("asset_refs"), list):
        refs.extend(str(r) for r in seg["asset_refs"])
    if isinstance(seg.get("shots"), list):
        for shot in seg["shots"]:
            if isinstance(shot, dict) and isinstance(shot.get("asset_refs"), list):
                refs.extend(str(r) for r in shot["asset_refs"])
    return unique_ordered(refs)


def compile_segment_prompt(seg: dict[str, Any]) -> str:
    explicit = seg.get("prompt")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()

    shots = seg.get("shots")
    if not isinstance(shots, list) or not shots:
        return ""

    parts: list[str] = []
    transition = seg.get("transition")
    if isinstance(transition, str) and transition.strip():
        parts.append(f"Transition in: {transition.strip()}.")

    entry_state = seg.get("entry_state")
    if isinstance(entry_state, str) and entry_state.strip():
        parts.append(f"Opening state: {entry_state.strip()}.")

    for idx, shot in enumerate(shots, start=1):
        if not isinstance(shot, dict):
            continue
        shot_id = shot.get("id") or f"shot_{idx}"
        start = shot.get("start", 0)
        end = shot.get("end", 0)
        camera = str(shot.get("camera", "")).strip()
        action = str(shot.get("action", "")).strip()
        line_parts = [f"[{start}s-{end}s | {shot_id}]"]
        if camera:
            line_parts.append(f"Camera: {camera}.")
        if action:
            line_parts.append(action)
        dialogues = shot.get("dialogues")
        if isinstance(dialogues, list) and dialogues:
            spoken = []
            for d in dialogues:
                if isinstance(d, dict):
                    cid = str(d.get("character_id", "")).strip()
                    txt = str(d.get("text", "")).strip()
                    if txt:
                        spoken.append(f'{cid}: "{txt}"' if cid else f'"{txt}"')
            if spoken:
                line_parts.append("Dialogue: " + "; ".join(spoken))
        parts.append(" ".join(line_parts))

    exit_state = seg.get("exit_state")
    if isinstance(exit_state, str) and exit_state.strip():
        parts.append(f"Closing state: {exit_state.strip()}.")

    return "\n".join(parts).strip()


def validate_storyboard(data: Any) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    def add_err(code: str, path: str, msg: str) -> None:
        errors.append({"level": "error", "code": code, "path": path, "message": msg})

    def add_warn(code: str, path: str, msg: str) -> None:
        warnings.append({"level": "warn", "code": code, "path": path, "message": msg})

    if not isinstance(data, dict):
        add_err("SCHEMA", "$", "Root document must be a JSON object.")
        return {"valid": False, "errors": errors, "warnings": warnings, "estimate": {}}

    project = data.get("project")
    assets = data.get("assets")
    segments = data.get("segments")
    characters = data.get("characters", [])

    if not isinstance(project, dict):
        add_err("SCHEMA", "$.project", "`project` must be an object.")
        project = {}
    if not isinstance(assets, list):
        add_err("SCHEMA", "$.assets", "`assets` must be an array.")
        assets = []
    if not isinstance(segments, list) or not segments:
        add_err("SCHEMA", "$.segments", "`segments` must be a non-empty array.")
        segments = []
    if not isinstance(characters, list):
        add_err("SCHEMA", "$.characters", "`characters` must be an array when present.")
        characters = []

    video_model = project.get("video_model", "seedance-2.5-spicy")
    image_model = project.get("image_model", "seedream-5.0-pro-spicy")
    video_aspect = project.get("video_aspect", "16:9")
    asset_aspect = project.get("asset_aspect", "16:9")
    output_format = project.get("output_format")

    if video_model not in VIDEO_MODELS:
        add_err(
            "UNSUPPORTED_MODEL",
            "$.project.video_model",
            f"Unsupported video_model {video_model!r}. Expected one of: {', '.join(sorted(VIDEO_MODELS))}.",
        )
    if image_model not in IMAGE_MODELS:
        add_err(
            "UNSUPPORTED_MODEL",
            "$.project.image_model",
            f"Unsupported image_model {image_model!r}. Expected one of: {', '.join(sorted(IMAGE_MODELS))}.",
        )
    if video_aspect not in VIDEO_RATIOS:
        add_err(
            "INVALID_ASPECT",
            "$.project.video_aspect",
            f"Unsupported video_aspect {video_aspect!r}. Expected one of: {', '.join(sorted(VIDEO_RATIOS))}.",
        )
    if asset_aspect not in IMAGE_RATIOS:
        add_err(
            "INVALID_ASPECT",
            "$.project.asset_aspect",
            f"Unsupported asset_aspect {asset_aspect!r}. Expected one of: {', '.join(sorted(IMAGE_RATIOS))}.",
        )
    if output_format is not None:
        if output_format not in OUTPUT_FORMATS:
            add_err("INVALID_FORMAT", "$.project.output_format", f"Unsupported output_format {output_format!r}.")
        elif video_model in VIDEO_MODELS and not VIDEO_MODELS[video_model]["supports_output_format"]:
            add_err(
                "INVALID_FORMAT",
                "$.project.output_format",
                f"Model {video_model} does not accept `output_format`.",
            )

    seen_ids: dict[str, str] = {}
    character_ids: set[str] = set()
    asset_ids: set[str] = set()

    def register_id(raw_id: Any, path: str) -> str | None:
        if not isinstance(raw_id, str) or not raw_id.strip():
            add_err("SCHEMA", path, "ID must be a non-empty string.")
            return None
        if raw_id in seen_ids:
            add_err("DUPLICATE_ID", path, f"Duplicate ID {raw_id!r} (already used at {seen_ids[raw_id]}).")
            return None
        seen_ids[raw_id] = path
        return raw_id

    for idx, ch in enumerate(characters):
        p = f"$.characters[{idx}]"
        if not isinstance(ch, dict):
            add_err("SCHEMA", p, "Character entry must be an object.")
            continue
        cid = register_id(ch.get("id"), f"{p}.id")
        if cid:
            character_ids.add(cid)

    img_spec = IMAGE_MODELS.get(image_model, IMAGE_MODELS["seedream-5.0-pro-spicy"])
    generated_asset_count = 0

    for idx, asset in enumerate(assets):
        p = f"$.assets[{idx}]"
        if not isinstance(asset, dict):
            add_err("SCHEMA", p, "Asset entry must be an object.")
            continue
        aid = register_id(asset.get("id"), f"{p}.id")
        if aid:
            asset_ids.add(aid)
        has_prompt = isinstance(asset.get("prompt"), str) and bool(asset["prompt"].strip())
        has_local = isinstance(asset.get("local_file"), str) and bool(asset["local_file"].strip())
        has_url = isinstance(asset.get("url"), str) and bool(asset["url"].strip())
        if not (has_prompt or has_local or has_url):
            add_err("ASSET_SOURCE", p, "Asset must define at least one of `prompt`, `local_file`, or `url`.")
        if not has_local and not has_url:
            generated_asset_count += 1
        ar = asset.get("aspect_ratio")
        if ar is not None and ar not in IMAGE_RATIOS:
            add_err("INVALID_ASPECT", f"{p}.aspect_ratio", f"Unsupported aspect_ratio {ar!r}.")
        sz = asset.get("size")
        if sz is not None and sz not in img_spec["sizes"]:
            add_err(
                "INVALID_SIZE",
                f"{p}.size",
                f"Size {sz!r} not supported by {image_model}; allowed: {', '.join(img_spec['sizes'])}.",
            )

    vid_spec = VIDEO_MODELS.get(video_model, VIDEO_MODELS["seedance-2.5-spicy"])
    total_duration = 0

    for idx, seg in enumerate(segments):
        p = f"$.segments[{idx}]"
        if not isinstance(seg, dict):
            add_err("SCHEMA", p, "Segment entry must be an object.")
            continue
        register_id(seg.get("id"), f"{p}.id")

        dur = seg.get("duration_seconds")
        if isinstance(dur, bool) or not isinstance(dur, int):
            add_err("INVALID_DURATION", f"{p}.duration_seconds", "`duration_seconds` must be an integer.")
        else:
            if dur < vid_spec["min_duration"] or dur > vid_spec["max_duration"]:
                add_err(
                    "INVALID_DURATION",
                    f"{p}.duration_seconds",
                    f"Duration {dur}s out of range [{vid_spec['min_duration']}, {vid_spec['max_duration']}] for {video_model}.",
                )
            total_duration += dur

        seg_refs = collect_segment_asset_refs(seg)
        for ref in seg_refs:
            if ref not in asset_ids:
                add_err("DANGLING_REF", f"{p}.asset_refs", f"Referenced asset ID {ref!r} does not exist in `assets`.")

        if len(seg_refs) > vid_spec["max_ref_images"]:
            add_err(
                "REF_IMAGE_CAP",
                f"{p}.asset_refs",
                f"Segment references {len(seg_refs)} image assets, exceeding {video_model} limit of {vid_spec['max_ref_images']}.",
            )

        audio_refs = seg.get("audio_refs", [])
        video_refs = seg.get("video_refs", [])
        if not isinstance(audio_refs, list):
            add_err("SCHEMA", f"{p}.audio_refs", "`audio_refs` must be an array.")
            audio_refs = []
        if not isinstance(video_refs, list):
            add_err("SCHEMA", f"{p}.video_refs", "`video_refs` must be an array.")
            video_refs = []

        if len(audio_refs) > vid_spec["max_ref_audio"]:
            add_err(
                "REF_AUDIO_CAP",
                f"{p}.audio_refs",
                f"Segment has {len(audio_refs)} audio refs, exceeding {video_model} limit of {vid_spec['max_ref_audio']}.",
            )
        if len(video_refs) > vid_spec["max_ref_video"]:
            add_err(
                "REF_VIDEO_CAP",
                f"{p}.video_refs",
                f"Segment has {len(video_refs)} video refs, exceeding {video_model} limit of {vid_spec['max_ref_video']}.",
            )
        if vid_spec["audio_requires_visual_ref"] and audio_refs and not seg_refs and not video_refs:
            add_err(
                "AUDIO_NEEDS_VISUAL_REF",
                p,
                f"{video_model} requires at least one image or video reference alongside `audio_refs`.",
            )

        shots = seg.get("shots")
        if shots is not None:
            if not isinstance(shots, list) or not shots:
                add_err("SCHEMA", f"{p}.shots", "`shots` must be a non-empty array when provided.")
            else:
                cursor = 0.0
                for s_idx, shot in enumerate(shots):
                    sp = f"{p}.shots[{s_idx}]"
                    if not isinstance(shot, dict):
                        add_err("SCHEMA", sp, "Shot must be an object.")
                        continue
                    register_id(shot.get("id"), f"{sp}.id")
                    if not isinstance(shot.get("action"), str) or not shot["action"].strip():
                        add_err("SCHEMA", f"{sp}.action", "Shot `action` must be a non-empty string.")
                    if not isinstance(shot.get("camera"), str) or not shot["camera"].strip():
                        add_err("SCHEMA", f"{sp}.camera", "Shot `camera` must be a non-empty string.")
                    start = shot.get("start")
                    end = shot.get("end")
                    if (
                        isinstance(start, bool)
                        or isinstance(end, bool)
                        or not isinstance(start, (int, float))
                        or not isinstance(end, (int, float))
                        or not math.isfinite(start)
                        or not math.isfinite(end)
                    ):
                        add_err("SHOT_COVERAGE", sp, "Shot `start` and `end` must be finite numbers.")
                    else:
                        if start < 0 or end <= start:
                            add_err("SHOT_COVERAGE", sp, f"Invalid shot span [{start}, {end}].")
                        if abs(start - cursor) > 1e-6:
                            add_err(
                                "SHOT_COVERAGE",
                                sp,
                                f"Shot start {start}s does not match previous cursor {cursor}s (no gaps or overlaps).",
                            )
                        cursor = float(end)
                        dialogues = shot.get("dialogues", [])
                        if isinstance(dialogues, list) and dialogues:
                            speech_est = 0.0
                            for d_idx, dlg in enumerate(dialogues):
                                if not isinstance(dlg, dict):
                                    add_err("SCHEMA", f"{sp}.dialogues[{d_idx}]", "Dialogue entry must be an object.")
                                    continue
                                cid = dlg.get("character_id")
                                if character_ids and isinstance(cid, str) and cid and cid not in character_ids:
                                    add_warn(
                                        "UNKNOWN_CHARACTER",
                                        f"{sp}.dialogues[{d_idx}].character_id",
                                        f"Dialogue character_id {cid!r} is not listed in `characters`.",
                                    )
                                txt = dlg.get("text", "")
                                if not isinstance(txt, str) or not txt.strip():
                                    add_err("SCHEMA", f"{sp}.dialogues[{d_idx}].text", "Dialogue `text` cannot be empty.")
                                else:
                                    speech_est += estimate_speech_seconds(txt)
                            shot_dur = float(end) - float(start)
                            if shot_dur > 0 and speech_est > shot_dur:
                                add_warn(
                                    "DIALOGUE_PACING",
                                    f"{sp}.dialogues",
                                    f"Estimated dialogue duration ({speech_est:.1f}s) exceeds shot window ({shot_dur:.1f}s).",
                                )
                if isinstance(dur, int) and not isinstance(dur, bool) and abs(cursor - float(dur)) > 1e-6:
                    add_err(
                        "SHOT_COVERAGE",
                        f"{p}.shots",
                        f"Shots end at {cursor}s, which does not equal segment duration {dur}s.",
                    )

        if not compile_segment_prompt(seg):
            add_err("EMPTY_PROMPT", p, "Segment must provide a non-empty `prompt` or `shots`.")

    asset_credits = generated_asset_count * img_spec["credits_per_image"]
    video_credits_by_res: dict[str, int] = {}
    for res, rate in vid_spec["credits_per_sec"].items():
        video_credits_by_res[res] = total_duration * rate

    recommended_res = "480p" if vid_spec["supports_draft"] else ("720p" if "720p" in video_credits_by_res else "480p")
    total_est_credits = asset_credits + video_credits_by_res.get(recommended_res, 0)
    estimate = {
        "generated_assets": generated_asset_count,
        "asset_credits": asset_credits,
        "segment_count": len(segments),
        "total_duration_seconds": total_duration,
        "video_credits_by_resolution": video_credits_by_res,
        "recommended_initial_credits": total_est_credits,
        "recommended_initial_usd": round(total_est_credits / 1000.0, 3),
    }

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "estimate": estimate,
    }


def map_bundle_model(raw_model: str) -> str:
    lowered = raw_model.strip().lower()
    if lowered in VIDEO_MODELS:
        return lowered
    if "2.5" in lowered:
        return "seedance-2.5-flash-spicy" if "flash" in lowered else "seedance-2.5-spicy"
    if "2.0" in lowered:
        if "fast" in lowered:
            return "seedance-2.0-fast-spicy"
        if "mini" in lowered:
            return "seedance-2.0-mini-spicy"
        return "seedance-2.0-spicy"
    return "seedance-2.5-spicy"


def import_project_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(bundle, dict):
        raise RunnerError("project_bundle.json root must be a JSON object.")

    proj = bundle.get("project")
    if not isinstance(proj, dict):
        raise RunnerError("project_bundle.json missing `project` object.")

    raw_chars = bundle.get("characters") or []
    raw_assets = bundle.get("assets") or []
    raw_segments = bundle.get("segments") or []

    char_map: dict[str, dict[str, Any]] = {}
    characters: list[dict[str, Any]] = []
    for ch in raw_chars:
        if isinstance(ch, dict) and isinstance(ch.get("id"), str):
            char_map[ch["id"]] = ch
            characters.append(
                {
                    "id": ch["id"],
                    "visual_age": ch.get("visual_age"),
                    "description": ch.get("description", ""),
                }
            )

    asset_aspect_default = proj.get("asset_aspect", "16:9")
    assets: list[dict[str, Any]] = []
    for a in raw_assets:
        if not isinstance(a, dict):
            continue
        prompt = str(a.get("prompt", "")).strip()
        refs = [str(r) for r in (a.get("refs") or []) if isinstance(r, str)]
        char_notes: list[str] = []
        for ref in refs:
            if ref in char_map:
                ch = char_map[ref]
                desc = str(ch.get("description", "")).strip()
                age = ch.get("visual_age")
                if desc and desc not in prompt:
                    age_part = f", visual age {age}" if age is not None else ""
                    char_notes.append(f"{ref}{age_part}: {desc}")
        if char_notes:
            prompt = f"{prompt}\nSubject details — " + "; ".join(char_notes)
        entry: dict[str, Any] = {
            "id": a.get("id", ""),
            "type": a.get("type", "asset"),
            "aspect_ratio": a.get("aspect", asset_aspect_default),
            "prompt": prompt,
        }
        if refs:
            entry["refs"] = refs
        assets.append(entry)

    segments: list[dict[str, Any]] = []
    for seg in raw_segments:
        if not isinstance(seg, dict):
            continue
        raw_dur = seg.get("duration")
        if isinstance(raw_dur, bool) or not isinstance(raw_dur, (int, float)):
            raise RunnerError(f"Segment {seg.get('id')!r} missing numeric `duration`.")
        dur_int = int(round(float(raw_dur)))
        seg_out: dict[str, Any] = {
            "id": seg.get("id", ""),
            "duration_seconds": dur_int,
            "entry_state": seg.get("entry_state", ""),
            "exit_state": seg.get("exit_state", ""),
            "shots": seg.get("shots", []),
        }
        if isinstance(seg.get("transition"), str) and seg["transition"].strip():
            seg_out["transition"] = seg["transition"].strip()
        seg_out["asset_refs"] = collect_segment_asset_refs(seg_out)
        seg_out["prompt"] = compile_segment_prompt(seg_out)
        segments.append(seg_out)

    video_model = map_bundle_model(str(proj.get("model", "2.5")))
    video_aspect = proj.get("video_aspect", "16:9")

    return {
        "project": {
            "title": str(proj.get("title") or "Imported Storyboard"),
            "video_model": video_model,
            "image_model": "seedream-5.0-pro-spicy",
            "video_aspect": video_aspect,
            "asset_aspect": asset_aspect_default,
            "generate_audio": True,
            **({"output_format": "mp4"} if VIDEO_MODELS[video_model]["supports_output_format"] else {}),
        },
        "characters": characters,
        "assets": assets,
        "segments": segments,
    }


class HotAPIClient:
    """Minimal HotAPI HTTP client using stdlib urllib + http.client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        poll_timeout: float = DEFAULT_POLL_TIMEOUT,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": "hotapi-seedance-storyboard/1.0",
        }
        if extra:
            headers.update(extra)
        return headers

    def _request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        body = None
        extra_headers: dict[str, str] = {}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            extra_headers["Content-Type"] = "application/json"
        if idempotency_key:
            extra_headers["Idempotency-Key"] = idempotency_key

        req = urllib.request.Request(url, data=body, headers=self._headers(extra_headers), method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raw_err = exc.read().decode("utf-8", errors="replace")
            try:
                err_obj = json.loads(raw_err)
                err_info = err_obj.get("error", err_obj)
                raise RunnerError(f"HotAPI HTTP {exc.code} on {method} {path}: {json.dumps(err_info)}") from exc
            except json.JSONDecodeError:
                raise RunnerError(f"HotAPI HTTP {exc.code} on {method} {path}: {raw_err}") from exc
        except urllib.error.URLError as exc:
            raise RunnerError(f"Network error calling {method} {path}: {exc.reason}") from exc

    def post_task(self, path: str, payload: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
        return self._request_json("POST", path, payload=payload, idempotency_key=idempotency_key)

    def get_task(self, task_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/v1/tasks/{urllib.parse.quote(task_id, safe='')}")

    def poll_task(self, task_id: str) -> dict[str, Any]:
        deadline = time.monotonic() + self.poll_timeout
        while True:
            task = self.get_task(task_id)
            status = str(task.get("status", "")).lower()
            if status in TERMINAL_STATUSES:
                return task
            if time.monotonic() >= deadline:
                raise RunnerError(f"Timed out waiting for task {task_id} (last status: {status or 'unknown'}).")
            time.sleep(self.poll_interval)

    def upload_file(self, file_path: Path) -> dict[str, Any]:
        if not file_path.is_file():
            raise RunnerError(f"Local asset file not found: {file_path}")
        mime, _ = mimetypes.guess_type(file_path.name)
        content_type = mime or "application/octet-stream"
        boundary = f"----HotAPIUpload{uuid.uuid4().hex}"
        file_bytes = file_path.read_bytes()
        safe_name = file_path.name.replace('"', "_")

        head = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{safe_name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
        tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
        body = head + file_bytes + tail

        parsed = urllib.parse.urlparse(self.base_url)
        conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        base_path = parsed.path.rstrip("/")
        conn = conn_cls(parsed.hostname, port, timeout=120)
        try:
            headers = self._headers({"Content-Type": f"multipart/form-data; boundary={boundary}"})
            conn.request("POST", f"{base_path}/v1/uploads", body=body, headers=headers)
            resp = conn.getresponse()
            raw = resp.read().decode("utf-8", errors="replace")
            if resp.status >= 400:
                raise RunnerError(f"HotAPI upload HTTP {resp.status}: {raw}")
            return json.loads(raw)
        except OSError as exc:
            raise RunnerError(f"Failed uploading {file_path}: {exc}") from exc
        finally:
            conn.close()

    def download_file(self, url: str, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "hotapi-seedance-storyboard/1.0"})
        tmp_path = dest.with_name(f".{dest.name}.{os.getpid()}.{uuid.uuid4().hex[:8]}.tmp")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            tmp_path.write_bytes(data)
            os.replace(tmp_path, dest)
            return dest
        except (urllib.error.URLError, OSError) as exc:
            raise RunnerError(f"Failed downloading {url} to {dest}: {exc}") from exc
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass


def extract_first_asset_url(task: dict[str, Any]) -> str:
    output = task.get("output")
    if isinstance(output, dict):
        assets = output.get("assets")
        if isinstance(assets, list) and assets:
            first = assets[0]
            if isinstance(first, dict) and isinstance(first.get("url"), str) and first["url"]:
                return first["url"]
        if isinstance(output.get("url"), str) and output["url"]:
            return output["url"]
    raise RunnerError(f"Succeeded task {task.get('id')} contains no asset URL in output.")


def extension_from_url(url: str, fallback: str) -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix and len(suffix) <= 6:
        return suffix
    return fallback


def load_state(out_dir: Path) -> dict[str, Any]:
    state_path = out_dir / "state.json"
    if state_path.exists():
        data = load_json(state_path)
        if isinstance(data, dict):
            data.setdefault("assets", {})
            data.setdefault("segments", {})
            return data
    return {"assets": {}, "segments": {}}


def save_state(out_dir: Path, state: dict[str, Any]) -> None:
    write_json_atomic(out_dir / "state.json", state)


def require_client(args: argparse.Namespace) -> HotAPIClient:
    api_key = os.environ.get("HOTAPI_KEY", "").strip()
    if not api_key:
        raise RunnerError("HOTAPI_KEY environment variable is required (or pass --dry-run).")
    base_url = os.environ.get("HOTAPI_BASE_URL", DEFAULT_BASE_URL)
    return HotAPIClient(
        api_key=api_key,
        base_url=base_url,
        poll_interval=getattr(args, "poll_interval", DEFAULT_POLL_INTERVAL),
        poll_timeout=getattr(args, "poll_timeout", DEFAULT_POLL_TIMEOUT),
    )


def parse_only_filter(only_arg: str | None) -> set[str] | None:
    if not only_arg:
        return None
    items = {x.strip() for x in only_arg.split(",") if x.strip()}
    return items or None


def make_idempotency_key(action: str, item_id: str, payload: Any, attempt: int) -> str:
    return f"{action}-{item_id}-{canonical_hash({'payload': payload, 'attempt': attempt})}"


def resolve_attempt(existing: dict[str, Any], force: bool) -> int:
    prev = int(existing.get("attempt", 0))
    if force or existing.get("status") in {"failed", "cancelled", "expired"}:
        return prev + 1
    return prev or 1


def ensure_valid_storyboard(data: dict[str, Any]) -> None:
    report = validate_storyboard(data)
    if not report["valid"]:
        lines = [f"  - [{e['code']}] {e['path']}: {e['message']}" for e in report["errors"]]
        raise RunnerError("Storyboard validation failed:\n" + "\n".join(lines))


def run_validate(args: argparse.Namespace) -> int:
    data = load_json(Path(args.storyboard))
    report = validate_storyboard(data)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        status_label = "VALID" if report["valid"] else "INVALID"
        print(f"Validation: {status_label} ({len(report['errors'])} errors, {len(report['warnings'])} warnings)")
        for err in report["errors"]:
            print(f"  ERROR [{err['code']}] {err['path']}: {err['message']}")
        for warn in report["warnings"]:
            print(f"  WARN  [{warn['code']}] {warn['path']}: {warn['message']}")
        est = report.get("estimate", {})
        if est:
            print(
                f"Estimate: {est.get('generated_assets', 0)} generated assets "
                f"({est.get('asset_credits', 0)} credits), "
                f"{est.get('segment_count', 0)} segments / {est.get('total_duration_seconds', 0)}s video"
            )
            by_res = est.get("video_credits_by_resolution", {})
            if by_res:
                res_str = ", ".join(f"{r}: {c} cr (${c / 1000.0:.2f})" for r, c in by_res.items())
                print(f"  Video credits by resolution: {res_str}")
            print(
                f"  Recommended initial run: ~{est.get('recommended_initial_credits', 0)} credits "
                f"(${est.get('recommended_initial_usd', 0):.3f})"
            )
    return 0 if report["valid"] else 1


def run_import_bundle(args: argparse.Namespace) -> int:
    bundle = load_json(Path(args.bundle))
    storyboard = import_project_bundle(bundle)
    report = validate_storyboard(storyboard)
    out_path = Path(args.output)
    write_json_atomic(out_path, storyboard)
    print(
        f"Imported {len(storyboard['assets'])} assets and {len(storyboard['segments'])} segments "
        f"into {out_path} (valid={report['valid']}, errors={len(report['errors'])}, warnings={len(report['warnings'])})"
    )
    return 0 if report["valid"] else 1


def run_assets(args: argparse.Namespace) -> int:
    storyboard_path = Path(args.storyboard).resolve()
    data = load_json(storyboard_path)
    ensure_valid_storyboard(data)

    out_dir = Path(args.out_dir)
    only = parse_only_filter(args.only)
    project = data["project"]
    image_model = project.get("image_model", "seedream-5.0-pro-spicy")
    default_aspect = project.get("asset_aspect", "16:9")

    state = load_state(out_dir)
    client = None if args.dry_run else require_client(args)
    base_dir = storyboard_path.parent

    for asset in data.get("assets", []):
        aid = asset["id"]
        if only is not None and aid not in only:
            continue

        existing = state["assets"].get(aid, {})

        if isinstance(asset.get("url"), str) and asset["url"].strip():
            ext_url = asset["url"].strip()
            print(f"[asset {aid}] Using external URL: {ext_url}")
            if not args.dry_run:
                state["assets"][aid] = {
                    "mode": "external_url",
                    "status": "succeeded",
                    "remote_url": ext_url,
                }
                save_state(out_dir, state)
            continue

        if isinstance(asset.get("local_file"), str) and asset["local_file"].strip():
            local_p = Path(asset["local_file"])
            if not local_p.is_absolute():
                local_p = (base_dir / local_p).resolve()
            now = time.time()
            cached_exp = existing.get("upload_expires_at", 0)
            if (
                not args.force
                and existing.get("upload_url")
                and isinstance(cached_exp, (int, float))
                and cached_exp - now > UPLOAD_REFRESH_MARGIN_SECONDS
            ):
                print(f"[asset {aid}] Skipping already-uploaded local file ({local_p})")
                continue
            if args.dry_run:
                print(f"[dry-run] POST /v1/uploads file={local_p}")
                continue
            assert client is not None
            up = client.upload_file(local_p)
            state["assets"][aid] = {
                "mode": "upload",
                "status": "succeeded",
                "local_path": str(local_p),
                "upload_url": up["url"],
                "upload_expires_at": up.get("expires_at", 0),
                "content_type": up.get("content_type"),
            }
            save_state(out_dir, state)
            print(f"[asset {aid}] Uploaded {local_p} -> {up['url']}")
            continue

        local_saved = existing.get("local_path")
        if (
            not args.force
            and existing.get("status") == "succeeded"
            and isinstance(local_saved, str)
            and Path(local_saved).is_file()
        ):
            print(f"[asset {aid}] Already locked at {local_saved} (skipping)")
            continue

        endpoint = f"/v1/{image_model}/text-to-image"
        payload: dict[str, Any] = {
            "prompt": asset["prompt"],
            "size": asset.get("size", "2K"),
            "aspect_ratio": asset.get("aspect_ratio", default_aspect),
        }
        attempt = resolve_attempt(existing, args.force)
        idem_key = make_idempotency_key("asset", aid, payload, attempt)

        if args.dry_run:
            print(f"[dry-run] POST {endpoint} Idempotency-Key={idem_key} payload={json.dumps(payload, ensure_ascii=False)}")
            continue

        assert client is not None
        task_id = existing.get("task_id")
        resumable = (
            not args.force
            and isinstance(task_id, str)
            and existing.get("status") in {"pending", "queued", "processing"}
            and existing.get("payload_hash") == canonical_hash(payload)
        )

        if resumable:
            print(f"[asset {aid}] Resuming existing task {task_id}...")
        else:
            created = client.post_task(endpoint, payload, idempotency_key=idem_key)
            task_id = created["id"]
            state["assets"][aid] = {
                "mode": "generated",
                "model": image_model,
                "task_id": task_id,
                "status": created.get("status", "queued"),
                "attempt": attempt,
                "payload_hash": canonical_hash(payload),
                "idempotency_key": idem_key,
                "estimated_credits_cost": created.get("estimated_credits_cost"),
            }
            save_state(out_dir, state)
            print(f"[asset {aid}] Queued task {task_id}, polling...")

        final_task = client.poll_task(str(task_id))
        status = str(final_task.get("status", "")).lower()
        entry = state["assets"][aid]
        entry["status"] = status
        entry["expires_at"] = final_task.get("expires_at")
        entry["actual_credits_cost"] = final_task.get("actual_credits_cost") or final_task.get("estimated_credits_cost")

        if status != "succeeded":
            save_state(out_dir, state)
            raise RunnerError(f"Asset {aid} task {task_id} ended with status={status}: {final_task.get('error')}")

        remote_url = extract_first_asset_url(final_task)
        ext = extension_from_url(remote_url, ".png")
        dest = out_dir / "assets" / f"{aid}{ext}"
        client.download_file(remote_url, dest)
        entry["remote_url"] = remote_url
        entry["local_path"] = str(dest)
        save_state(out_dir, state)
        print(f"[asset {aid}] Locked -> {dest}")

    return 0


def resolve_asset_reference_url(
    asset_id: str,
    asset_defs: dict[str, dict[str, Any]],
    state: dict[str, Any],
    out_dir: Path,
    base_dir: Path,
    client: HotAPIClient | None,
    dry_run: bool,
) -> str:
    if dry_run:
        entry = state["assets"].get(asset_id, {})
        for key in ("upload_url", "remote_url"):
            if isinstance(entry.get(key), str) and entry[key]:
                return entry[key]
        adef = asset_defs.get(asset_id, {})
        if isinstance(adef.get("url"), str) and adef["url"].strip():
            return adef["url"].strip()
        return f"https://example.invalid/assets/{asset_id}.png"

    assert client is not None
    now = time.time()
    entry = state["assets"].get(asset_id, {})
    adef = asset_defs.get(asset_id, {})

    if isinstance(adef.get("url"), str) and adef["url"].strip():
        return adef["url"].strip()

    up_url = entry.get("upload_url")
    up_exp = entry.get("upload_expires_at", 0)
    if isinstance(up_url, str) and up_url and isinstance(up_exp, (int, float)) and up_exp - now > UPLOAD_REFRESH_MARGIN_SECONDS:
        return up_url

    rem_url = entry.get("remote_url")
    rem_exp = entry.get("expires_at", 0)
    if isinstance(rem_url, str) and rem_url and isinstance(rem_exp, (int, float)) and rem_exp - now > UPLOAD_REFRESH_MARGIN_SECONDS:
        return rem_url

    local_candidate: Path | None = None
    if isinstance(entry.get("local_path"), str) and entry["local_path"]:
        p = Path(entry["local_path"])
        if p.is_file():
            local_candidate = p
    elif isinstance(adef.get("local_file"), str) and adef["local_file"].strip():
        p = Path(adef["local_file"].strip())
        if not p.is_absolute():
            p = (base_dir / p).resolve()
        if p.is_file():
            local_candidate = p

    if local_candidate is not None:
        up = client.upload_file(local_candidate)
        entry = dict(entry)
        entry["local_path"] = str(local_candidate)
        entry["upload_url"] = up["url"]
        entry["upload_expires_at"] = up.get("expires_at", 0)
        entry.setdefault("status", "succeeded")
        state["assets"][asset_id] = entry
        save_state(out_dir, state)
        return up["url"]

    raise RunnerError(
        f"Asset {asset_id!r} has no fresh URL or local file. Run `assets` first before rendering."
    )


def run_render(args: argparse.Namespace) -> int:
    storyboard_path = Path(args.storyboard).resolve()
    data = load_json(storyboard_path)
    ensure_valid_storyboard(data)

    project = data["project"]
    video_model = project.get("video_model", "seedance-2.5-spicy")
    vid_spec = VIDEO_MODELS[video_model]
    ratio = project.get("video_aspect", "16:9")
    generate_audio = bool(project.get("generate_audio", True))
    output_format = project.get("output_format")

    if args.draft:
        if not vid_spec["supports_draft"]:
            raise RunnerError(f"--draft is only supported on seedance-2.5-spicy, not {video_model}.")
        if args.resolution and args.resolution != "480p":
            raise RunnerError("--draft requires resolution 480p (cannot be combined with 720p or 1080p).")
        resolution = "480p"
    else:
        resolution = args.resolution or ("720p" if "720p" in vid_spec["resolutions"] else "480p")
        if resolution not in vid_spec["resolutions"]:
            raise RunnerError(
                f"Resolution {resolution!r} is not supported by {video_model}; allowed: {', '.join(vid_spec['resolutions'])}."
            )

    out_dir = Path(args.out_dir)
    only = parse_only_filter(args.only)
    state = load_state(out_dir)
    client = None if args.dry_run else require_client(args)
    asset_defs = {a["id"]: a for a in data.get("assets", []) if isinstance(a, dict) and "id" in a}
    slot_name = "draft" if args.draft else "render"

    for seg in data.get("segments", []):
        sid = seg["id"]
        if only is not None and sid not in only:
            continue

        seg_state = state["segments"].setdefault(sid, {})
        existing = seg_state.get(slot_name, {})
        local_saved = existing.get("local_path")
        if (
            not args.force
            and existing.get("status") == "succeeded"
            and isinstance(local_saved, str)
            and Path(local_saved).is_file()
        ):
            print(f"[segment {sid}/{slot_name}] Already rendered at {local_saved} (skipping)")
            continue

        ref_ids = collect_segment_asset_refs(seg)
        ref_image_urls = [
            resolve_asset_reference_url(
                aid, asset_defs, state, out_dir, storyboard_path.parent, client, args.dry_run
            )
            for aid in ref_ids
        ]
        audio_urls = [str(u) for u in seg.get("audio_refs", []) if isinstance(u, str) and u.strip()]
        video_urls = [str(u) for u in seg.get("video_refs", []) if isinstance(u, str) and u.strip()]

        has_refs = bool(ref_image_urls or audio_urls or video_urls)
        endpoint = f"/v1/{video_model}/{'reference-to-video' if has_refs else 'text-to-video'}"

        payload: dict[str, Any] = {
            "prompt": compile_segment_prompt(seg),
            "duration_seconds": seg["duration_seconds"],
            "resolution": resolution,
            "ratio": ratio,
            "generate_audio": generate_audio,
        }
        if ref_image_urls:
            payload["reference_image_urls"] = ref_image_urls
        if audio_urls:
            payload["reference_audio_urls"] = audio_urls
        if video_urls:
            payload["reference_video_urls"] = video_urls
        if args.draft:
            payload["draft"] = True
        if vid_spec["supports_output_format"] and output_format:
            payload["output_format"] = output_format

        attempt = resolve_attempt(existing, args.force)
        idem_key = make_idempotency_key(f"render-{slot_name}", sid, payload, attempt)

        if args.dry_run:
            print(f"[dry-run] POST {endpoint} Idempotency-Key={idem_key} payload={json.dumps(payload, ensure_ascii=False)}")
            continue

        assert client is not None
        task_id = existing.get("task_id")
        resumable = (
            not args.force
            and isinstance(task_id, str)
            and existing.get("status") in {"pending", "queued", "processing"}
            and existing.get("payload_hash") == canonical_hash(payload)
        )

        if resumable:
            print(f"[segment {sid}/{slot_name}] Resuming existing task {task_id}...")
        else:
            created = client.post_task(endpoint, payload, idempotency_key=idem_key)
            task_id = created["id"]
            seg_state[slot_name] = {
                "model": video_model,
                "resolution": resolution,
                "draft": bool(args.draft),
                "task_id": task_id,
                "status": created.get("status", "queued"),
                "attempt": attempt,
                "payload_hash": canonical_hash(payload),
                "idempotency_key": idem_key,
                "estimated_credits_cost": created.get("estimated_credits_cost"),
            }
            save_state(out_dir, state)
            print(f"[segment {sid}/{slot_name}] Queued task {task_id}, polling...")

        final_task = client.poll_task(str(task_id))
        status = str(final_task.get("status", "")).lower()
        entry = seg_state[slot_name]
        entry["status"] = status
        entry["expires_at"] = final_task.get("expires_at")
        entry["actual_credits_cost"] = final_task.get("actual_credits_cost") or final_task.get("estimated_credits_cost")

        if status != "succeeded":
            save_state(out_dir, state)
            raise RunnerError(f"Segment {sid} task {task_id} ended with status={status}: {final_task.get('error')}")

        remote_url = extract_first_asset_url(final_task)
        default_ext = f".{output_format}" if output_format else ".mp4"
        ext = extension_from_url(remote_url, default_ext)
        filename = f"{sid}.draft{ext}" if args.draft else f"{sid}{ext}"
        dest = out_dir / "segments" / filename
        client.download_file(remote_url, dest)
        entry["remote_url"] = remote_url
        entry["local_path"] = str(dest)
        save_state(out_dir, state)
        print(f"[segment {sid}/{slot_name}] Saved -> {dest}")

    return 0


def run_finalize(args: argparse.Namespace) -> int:
    storyboard_path = Path(args.storyboard).resolve()
    data = load_json(storyboard_path)
    ensure_valid_storyboard(data)

    project = data["project"]
    video_model = project.get("video_model", "seedance-2.5-spicy")
    if video_model != "seedance-2.5-spicy":
        raise RunnerError(f"`finalize` only applies to `seedance-2.5-spicy` drafts (found {video_model}).")

    output_format = args.output_format or project.get("output_format")
    if output_format is not None and output_format not in OUTPUT_FORMATS:
        raise RunnerError(f"Unsupported output_format {output_format!r}.")

    out_dir = Path(args.out_dir)
    only = parse_only_filter(args.only)
    state = load_state(out_dir)
    client = None if args.dry_run else require_client(args)
    endpoint = "/v1/seedance-2.5-spicy/draft-to-video"

    for seg in data.get("segments", []):
        sid = seg["id"]
        if only is not None and sid not in only:
            continue

        seg_state = state["segments"].setdefault(sid, {})
        draft_entry = seg_state.get("draft", {})
        draft_task_id = draft_entry.get("task_id")

        if not args.dry_run and (draft_entry.get("status") != "succeeded" or not draft_task_id):
            raise RunnerError(
                f"Segment {sid!r} has no succeeded draft task in {out_dir / 'state.json'}. Run `render --draft` first."
            )

        existing = seg_state.get("final", {})
        local_saved = existing.get("local_path")
        if (
            not args.force
            and existing.get("status") == "succeeded"
            and isinstance(local_saved, str)
            and Path(local_saved).is_file()
        ):
            print(f"[segment {sid}/final] Already finalized at {local_saved} (skipping)")
            continue

        payload: dict[str, Any] = {"draft_task_id": draft_task_id or f"<draft_task_id:{sid}>"}
        if output_format:
            payload["output_format"] = output_format

        attempt = resolve_attempt(existing, args.force)
        idem_key = make_idempotency_key("finalize", sid, payload, attempt)

        if args.dry_run:
            print(f"[dry-run] POST {endpoint} Idempotency-Key={idem_key} payload={json.dumps(payload, ensure_ascii=False)}")
            continue

        assert client is not None
        task_id = existing.get("task_id")
        resumable = (
            not args.force
            and isinstance(task_id, str)
            and existing.get("status") in {"pending", "queued", "processing"}
            and existing.get("payload_hash") == canonical_hash(payload)
        )

        if resumable:
            print(f"[segment {sid}/final] Resuming finalize task {task_id}...")
        else:
            created = client.post_task(endpoint, payload, idempotency_key=idem_key)
            task_id = created["id"]
            seg_state["final"] = {
                "model": video_model,
                "resolution": "1080p",
                "draft_task_id": draft_task_id,
                "task_id": task_id,
                "status": created.get("status", "queued"),
                "attempt": attempt,
                "payload_hash": canonical_hash(payload),
                "idempotency_key": idem_key,
                "estimated_credits_cost": created.get("estimated_credits_cost"),
            }
            save_state(out_dir, state)
            print(f"[segment {sid}/final] Queued 1080p finalize task {task_id}, polling...")

        final_task = client.poll_task(str(task_id))
        status = str(final_task.get("status", "")).lower()
        entry = seg_state["final"]
        entry["status"] = status
        entry["expires_at"] = final_task.get("expires_at")
        entry["actual_credits_cost"] = final_task.get("actual_credits_cost") or final_task.get("estimated_credits_cost")

        if status != "succeeded":
            save_state(out_dir, state)
            raise RunnerError(f"Finalize for {sid} task {task_id} ended with status={status}: {final_task.get('error')}")

        remote_url = extract_first_asset_url(final_task)
        default_ext = f".{output_format}" if output_format else ".mp4"
        ext = extension_from_url(remote_url, default_ext)
        dest = out_dir / "finals" / f"{sid}{ext}"
        client.download_file(remote_url, dest)
        entry["remote_url"] = remote_url
        entry["local_path"] = str(dest)
        save_state(out_dir, state)
        print(f"[segment {sid}/final] Finalized 1080p -> {dest}")

    return 0


def rel_media_href(local_path: str | None, out_dir: Path) -> str | None:
    if not local_path:
        return None
    p = Path(local_path)
    try:
        return "./" + p.resolve().relative_to(out_dir.resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def sum_state_credits(state: dict[str, Any]) -> int:
    total = 0
    for entry in state.get("assets", {}).values():
        if isinstance(entry, dict):
            c = entry.get("actual_credits_cost") or entry.get("estimated_credits_cost") or 0
            if isinstance(c, (int, float)):
                total += int(c)
    for seg_slots in state.get("segments", {}).values():
        if isinstance(seg_slots, dict):
            for slot in seg_slots.values():
                if isinstance(slot, dict):
                    c = slot.get("actual_credits_cost") or slot.get("estimated_credits_cost") or 0
                    if isinstance(c, (int, float)):
                        total += int(c)
    return total


def build_board_html(data: dict[str, Any], state: dict[str, Any], out_dir: Path) -> str:
    project = data.get("project", {})
    title = html.escape(str(project.get("title") or "Seedance Storyboard"))
    video_model = html.escape(str(project.get("video_model", "seedance-2.5-spicy")))
    image_model = html.escape(str(project.get("image_model", "seedream-5.0-pro-spicy")))
    video_aspect = html.escape(str(project.get("video_aspect", "16:9")))
    segments = data.get("segments", [])
    assets = data.get("assets", [])
    total_dur = sum(int(s.get("duration_seconds", 0)) for s in segments if isinstance(s, dict))
    credits_spent = sum_state_credits(state)
    usd_spent = credits_spent / 1000.0

    asset_cards: list[str] = []
    for asset in assets:
        aid = str(asset.get("id", ""))
        atype = html.escape(str(asset.get("type", "asset")))
        aprompt = html.escape(str(asset.get("prompt", asset.get("local_file", asset.get("url", "")))))
        entry = state.get("assets", {}).get(aid, {})
        status = str(entry.get("status", "pending"))
        src = rel_media_href(entry.get("local_path"), out_dir) or entry.get("remote_url") or asset.get("url")
        media_html = (
            f'<img src="{html.escape(str(src))}" alt="{html.escape(aid)}" loading="lazy">'
            if src
            else '<div class="empty">Not generated yet</div>'
        )
        task_meta = html.escape(str(entry.get("task_id") or entry.get("mode") or "unrun"))
        credits = entry.get("actual_credits_cost") or entry.get("estimated_credits_cost") or 0
        asset_cards.append(
            f'<article class="card">'
            f'<div class="media">{media_html}</div>'
            f'<div class="body">'
            f'<div class="row"><strong>{html.escape(aid)}</strong><span class="badge">{atype}</span>'
            f'<span class="status status-{html.escape(status)}">{html.escape(status)}</span></div>'
            f'<p class="prompt">{aprompt}</p>'
            f'<div class="meta">Ref: {task_meta} · {int(credits)} cr</div>'
            f"</div></article>"
        )

    seg_cards: list[str] = []
    for seg in segments:
        sid = str(seg.get("id", ""))
        dur = int(seg.get("duration_seconds", 0))
        seg_slots = state.get("segments", {}).get(sid, {})
        final_entry = seg_slots.get("final", {})
        render_entry = seg_slots.get("render", {})
        draft_entry = seg_slots.get("draft", {})

        players: list[str] = []
        for label, slot in (("1080p Final", final_entry), ("Render", render_entry), ("480p Draft", draft_entry)):
            vsrc = rel_media_href(slot.get("local_path"), out_dir) or slot.get("remote_url")
            if vsrc:
                vstatus = html.escape(str(slot.get("status", "unknown")))
                vcredits = int(slot.get("actual_credits_cost") or slot.get("estimated_credits_cost") or 0)
                players.append(
                    f'<div class="video-slot">'
                    f'<div class="slot-head"><span>{label}</span><span class="status status-{vstatus}">{vstatus}</span>'
                    f'<span class="meta">{vcredits} cr</span></div>'
                    f'<video controls preload="metadata" src="{html.escape(str(vsrc))}"></video>'
                    f"</div>"
                )
        if not players:
            players.append('<div class="empty">No clips rendered yet</div>')

        ref_badges = "".join(
            f'<span class="chip">{html.escape(r)}</span>' for r in collect_segment_asset_refs(seg)
        ) or '<span class="muted">None</span>'

        shots_rows = ""
        if isinstance(seg.get("shots"), list) and seg["shots"]:
            row_items = []
            for sh in seg["shots"]:
                dlg_text = "; ".join(
                    f'{d.get("character_id", "")}: "{d.get("text", "")}"'
                    for d in (sh.get("dialogues") or [])
                    if isinstance(d, dict)
                )
                row_items.append(
                    "<tr>"
                    f"<td><code>{html.escape(str(sh.get('id', '')))}</code></td>"
                    f"<td>{html.escape(str(sh.get('start', 0)))}–{html.escape(str(sh.get('end', 0)))}s</td>"
                    f"<td>{html.escape(str(sh.get('camera', '')))}</td>"
                    f"<td>{html.escape(str(sh.get('action', '')))}</td>"
                    f"<td>{html.escape(dlg_text) or '—'}</td>"
                    "</tr>"
                )
            shots_rows = (
                '<table><thead><tr><th>Shot</th><th>Span</th><th>Camera</th><th>Action</th><th>Dialogue</th></tr></thead>'
                f"<tbody>{''.join(row_items)}</tbody></table>"
            )

        compiled = html.escape(compile_segment_prompt(seg))
        seg_cards.append(
            f'<article class="seg-card">'
            f'<div class="seg-head"><div><h3>{html.escape(sid)}</h3>'
            f'<span class="meta">{dur}s · Refs: {ref_badges}</span></div></div>'
            f'<div class="players">{"".join(players)}</div>'
            f'<details><summary>Compiled Prompt</summary><pre>{compiled}</pre></details>'
            f"{shots_rows}"
            f"</article>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — HotAPI Storyboard Board</title>
<style>
  :root {{ color-scheme: dark; --bg:#0b0c10; --card:#141720; --line:#252a38; --fg:#eef1f7; --muted:#939cb0; --accent:#ff6363; --ok:#38d399; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 28px; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background: var(--bg); color: var(--fg); line-height: 1.5; }}
  header {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 16px; border-bottom: 1px solid var(--line); padding-bottom: 18px; margin-bottom: 28px; }}
  .kicker {{ font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); font-weight: 700; }}
  h1 {{ margin: 4px 0 6px; font-size: 24px; }}
  h2 {{ margin: 28px 0 14px; font-size: 17px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }}
  .stats {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .stat {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 14px; font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }}
  .card, .seg-card {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }}
  .media img {{ display: block; width: 100%; aspect-ratio: 16/9; object-fit: cover; background: #06070a; }}
  .body {{ padding: 14px; }}
  .row {{ display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }}
  .badge, .chip, .status {{ font-size: 11px; padding: 2px 8px; border-radius: 999px; border: 1px solid var(--line); background: #1c202c; }}
  .status-succeeded {{ color: var(--ok); border-color: #1f5c47; }}
  .status-failed, .status-expired {{ color: var(--accent); border-color: #6b2626; }}
  .prompt {{ font-size: 12.5px; color: var(--muted); margin: 0 0 10px; }}
  .meta {{ font-size: 12px; color: var(--muted); }}
  .segments {{ display: flex; flex-direction: column; gap: 18px; }}
  .seg-card {{ padding: 18px; }}
  .seg-head h3 {{ margin: 0 0 4px; font-size: 18px; }}
  .players {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin: 14px 0; }}
  .video-slot {{ background: #0e1017; border: 1px solid var(--line); border-radius: 10px; padding: 10px; }}
  .slot-head {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12.5px; font-weight: 600; }}
  video {{ width: 100%; border-radius: 8px; background: #000; }}
  .empty {{ padding: 28px; text-align: center; color: var(--muted); font-size: 13px; border: 1px dashed var(--line); border-radius: 8px; }}
  details {{ margin: 10px 0; }}
  summary {{ cursor: pointer; font-size: 13px; color: var(--muted); }}
  pre {{ white-space: pre-wrap; background: #0b0d13; border: 1px solid var(--line); border-radius: 8px; padding: 12px; font-size: 12px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 12.5px; }}
  th, td {{ text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 600; }}
</style>
</head>
<body>
<header>
  <div>
    <div class="kicker">HotAPI · Seedance Storyboard Board</div>
    <h1>{title}</h1>
    <div class="meta">Video: <code>{video_model}</code> · Assets: <code>{image_model}</code> · Aspect: <code>{video_aspect}</code></div>
  </div>
  <div class="stats">
    <div class="stat">Assets: <strong>{len(assets)}</strong></div>
    <div class="stat">Segments: <strong>{len(segments)}</strong> ({total_dur}s)</div>
    <div class="stat">Credits Spent: <strong>{credits_spent}</strong> (${usd_spent:.3f})</div>
  </div>
</header>
<h2>Locked Assets</h2>
<section class="grid">{"".join(asset_cards)}</section>
<h2>Timeline Segments</h2>
<section class="segments">{"".join(seg_cards)}</section>
</body>
</html>
"""


def run_board(args: argparse.Namespace) -> int:
    storyboard_path = Path(args.storyboard).resolve()
    data = load_json(storyboard_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    state = load_state(out_dir)
    html_text = build_board_html(data, state, out_dir)
    board_path = out_dir / "board.html"
    board_path.write_text(html_text, encoding="utf-8")
    print(f"Wrote offline storyboard review board -> {board_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="storyboard_runner.py",
        description="End-to-end Asset-First storyboard runner for HotAPI (Seedream 5.0 + Seedance 2.5/2.0).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="Validate storyboard.json and estimate credit cost.")
    p_val.add_argument("storyboard", help="Path to storyboard.json")
    p_val.add_argument("--json", action="store_true", help="Print machine-readable JSON validation report")
    p_val.set_defaults(func=run_validate)

    p_imp = sub.add_parser("import-bundle", help="Convert project_bundle.json into storyboard.json.")
    p_imp.add_argument("bundle", help="Path to project_bundle.json")
    p_imp.add_argument("-o", "--output", required=True, help="Output path for storyboard.json")
    p_imp.set_defaults(func=run_import_bundle)

    p_assets = sub.add_parser("assets", help="Generate or upload locked character/scene/prop reference assets.")
    p_assets.add_argument("storyboard", help="Path to storyboard.json")
    p_assets.add_argument("--out-dir", default="./out", help="Output workspace directory (default: ./out)")
    p_assets.add_argument("--only", help="Comma-separated asset IDs to process")
    p_assets.add_argument("--force", action="store_true", help="Regenerate or re-upload already-locked assets")
    p_assets.add_argument("--dry-run", action="store_true", help="Print API calls without spending credits")
    p_assets.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL)
    p_assets.add_argument("--poll-timeout", type=float, default=DEFAULT_POLL_TIMEOUT)
    p_assets.set_defaults(func=run_assets)

    p_ren = sub.add_parser("render", help="Render storyboard segments via Seedance reference-to-video.")
    p_ren.add_argument("storyboard", help="Path to storyboard.json")
    p_ren.add_argument("--out-dir", default="./out", help="Output workspace directory (default: ./out)")
    p_ren.add_argument("--draft", action="store_true", help="Render 480p draft previews (seedance-2.5-spicy only)")
    p_ren.add_argument("--resolution", choices=["480p", "720p", "1080p", "4k"], help="Target resolution")
    p_ren.add_argument("--only", help="Comma-separated segment IDs to render")
    p_ren.add_argument("--force", action="store_true", help="Re-render segments that already succeeded")
    p_ren.add_argument("--dry-run", action="store_true", help="Print API calls without spending credits")
    p_ren.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL)
    p_ren.add_argument("--poll-timeout", type=float, default=DEFAULT_POLL_TIMEOUT)
    p_ren.set_defaults(func=run_render)

    p_fin = sub.add_parser("finalize", help="Promote succeeded Seedance 2.5 draft previews to 1080p.")
    p_fin.add_argument("storyboard", help="Path to storyboard.json")
    p_fin.add_argument("--out-dir", default="./out", help="Output workspace directory (default: ./out)")
    p_fin.add_argument("--only", help="Comma-separated segment IDs to finalize")
    p_fin.add_argument("--output-format", choices=["mp4", "mov"], help="Container format override")
    p_fin.add_argument("--force", action="store_true", help="Re-finalize segments that already succeeded")
    p_fin.add_argument("--dry-run", action="store_true", help="Print API calls without spending credits")
    p_fin.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL)
    p_fin.add_argument("--poll-timeout", type=float, default=DEFAULT_POLL_TIMEOUT)
    p_fin.set_defaults(func=run_finalize)

    p_board = sub.add_parser("board", help="Generate self-contained offline HTML review board.")
    p_board.add_argument("storyboard", help="Path to storyboard.json")
    p_board.add_argument("--out-dir", default="./out", help="Output workspace directory (default: ./out)")
    p_board.set_defaults(func=run_board)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RunnerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
