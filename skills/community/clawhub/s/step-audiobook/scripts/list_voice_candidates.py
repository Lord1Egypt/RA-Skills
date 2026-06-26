#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import locale
import sys
from pathlib import Path

from common import (
    DEFAULT_LIBRARY_PATH,
    format_list,
    format_value,
    load_yaml_if_exists,
    normalize_string_array,
    resolve_path,
)


for locale_name in ("zh_CN.UTF-8", "zh_CN", "C.UTF-8"):
    try:
        locale.setlocale(locale.LC_COLLATE, locale_name)
        break
    except locale.Error:
        continue


def compare_source_then_name(voice: dict) -> tuple[int, str]:
    source_rank = 0 if voice.get("source") == "official" else 1
    display_name = str(voice.get("display_name") or voice.get("asset_id") or "")
    ascii_only_rank = 1 if display_name.isascii() else 0
    return (source_rank, ascii_only_rank, locale.strxfrm(display_name))


def build_pretty_output(payload: dict) -> str:
    lines = [
        "Voice candidate pool",
        f"- library: {payload['library_path']}",
        f"- candidate_pool: {payload['candidate_pool_path']}",
        f"- effective_library: {payload['effective_library_path']}",
        f"- official_cache: {payload['official_cache_path']}",
        f"- mode: {payload['mode']}",
        f"- count: {payload['count']}",
    ]

    if not payload["voices"]:
        lines.append("")
        lines.append("没有匹配的候选音色。")
        return "\n".join(lines) + "\n"

    for voice in payload["voices"]:
        lines.append("")
        lines.append(f"* [{voice['source']}] {voice['display_name']} | {voice['asset_id']}")
        lines.append(f"  status: {voice['status']}")
        lines.append(f"  review_status: {voice['review_status']}")
        if voice["source"] == "clone":
            lines.append(f"  selected_for_clone: {'true' if voice['selected_for_clone'] else 'false'}")
            lines.append(f"  voice_id: {format_value(voice['voice_id'])}")
            lines.append(f"  source_file: {format_value(voice['source_file'])}")
        else:
            lines.append(f"  voice_id: {format_value(voice['voice_id'])}")
            lines.append(f"  official_description: {format_value(voice['official_description'])}")
            lines.append(f"  recommended: {format_list(voice['recommended_scenes'])}")
            lines.append(f"  information_quality: {format_value(voice['information_quality'])}")
        lines.append(f"  description: {format_value(voice['description'])}")
        lines.append(f"  tags: {format_list(voice['tags'])}")
        lines.append(f"  suitable: {format_list(voice['suitable_scenes'])}")
        lines.append(f"  avoid: {format_list(voice['avoid_scenes'])}")
        lines.append(f"  selection_summary: {format_value(voice['selection_summary'])}")
        lines.append(f"  instruction: {format_value(voice['stable_instruction'])}")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List the unified audiobook voice candidate pool.")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY_PATH), help="Path to voice-library.yaml")
    parser.add_argument("--source", help="Filter by source: official/clone")
    parser.add_argument("--asset-id", dest="asset_id", help="Filter by asset id")
    parser.add_argument("--status", help="Filter by voice status")
    parser.add_argument("--review-status", dest="review_status", help="Filter by review status")
    parser.add_argument("--selected-for-clone", action="store_true", help="Only show selected clone entries")
    parser.add_argument("--pretty", action="store_true", help="Render pretty text output")
    parser.add_argument("--json", action="store_true", help="Render JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    library_path = Path(args.library).resolve()
    library_dir = library_path.parent
    pretty = args.pretty or (sys.stdout.isatty() and not args.json)

    library = load_yaml_if_exists(library_path, {}) or {}
    paths = library.get("paths") or {}

    candidate_pool_path = resolve_path(
        library_dir,
        paths.get("candidate_pool_file", ".audiobook/voice-candidate-pool.yaml"),
    )
    effective_library_path = resolve_path(
        library_dir,
        paths.get("effective_library_file", ".audiobook/effective-voice-library.yaml"),
    )
    official_cache_path = resolve_path(
        library_dir,
        paths.get("official_cache_file", ".audiobook/official-voices-cache.json"),
    )

    candidate_pool = load_yaml_if_exists(candidate_pool_path, {"voices": []}) or {"voices": []}
    voices = []
    for voice in candidate_pool.get("voices") or []:
        normalized = {
            "asset_id": voice.get("asset_id") or "",
            "source": voice.get("source") or "unknown",
            "status": voice.get("status") or "unknown",
            "review_status": voice.get("review_status") or "unknown",
            "voice_id": voice.get("voice_id") or "",
            "display_name": voice.get("display_name") or voice.get("asset_id") or "",
            "description": voice.get("description") or "",
            "official_description": voice.get("official_description") or "",
            "recommended_scenes": normalize_string_array(voice.get("recommended_scenes")),
            "tags": normalize_string_array(voice.get("tags")),
            "suitable_scenes": normalize_string_array(voice.get("suitable_scenes")),
            "avoid_scenes": normalize_string_array(voice.get("avoid_scenes")),
            "stable_instruction": voice.get("stable_instruction") or "",
            "selection_summary": voice.get("selection_summary") or "",
            "information_quality": voice.get("information_quality") or "",
            "notes": voice.get("notes") or "",
            "selected_for_clone": voice.get("selected_for_clone") is True,
            "clone_model": voice.get("clone_model") or "",
            "source_file": voice.get("source_file") or "",
            "raw_file": voice.get("raw_file") or "",
            "sources": voice.get("sources") or {},
        }
        if args.source and normalized["source"] != args.source:
            continue
        if args.asset_id and normalized["asset_id"] != args.asset_id:
            continue
        if args.status and normalized["status"] != args.status:
            continue
        if args.review_status and normalized["review_status"] != args.review_status:
            continue
        if args.selected_for_clone and not normalized["selected_for_clone"]:
            continue
        voices.append(normalized)

    voices.sort(key=compare_source_then_name)

    payload = {
        "library_path": str(library_path),
        "candidate_pool_path": str(candidate_pool_path),
        "effective_library_path": str(effective_library_path),
        "official_cache_path": str(official_cache_path),
        "mode": "candidate_pool_only",
        "count": len(voices),
        "voices": voices,
    }

    if pretty:
        sys.stdout.write(build_pretty_output(payload))
        return

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # pragma: no cover - CLI error path
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
