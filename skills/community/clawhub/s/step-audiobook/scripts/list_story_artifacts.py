#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import load_json
from story_artifacts import (
    build_story_artifact_manifest,
    format_manifest_pretty,
    save_story_artifact_manifest,
    select_manifest_items,
)


VALID_LEVELS = ("essential", "review", "debug")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List storyboard / casting / synthesis intermediate artifacts for the audiobook workflow."
    )
    parser.add_argument("--manifest", help="Existing <base>.artifacts.json path")
    parser.add_argument("--story-input", dest="story_input", help="Original story input path")
    parser.add_argument("--effective-story-input", dest="effective_story_input", help="Structured script path")
    parser.add_argument("--structured-script-artifact", dest="structured_script_artifact", help="Structured generation trace path")
    parser.add_argument("--casting-plan", dest="casting_plan", help="Casting plan path")
    parser.add_argument("--casting-review", dest="casting_review", help="Casting review path")
    parser.add_argument("--clone-review", dest="clone_review", help="Clone review path")
    parser.add_argument("--role-profiles", dest="role_profiles", help="Role profiles trace path")
    parser.add_argument("--casting-selection", dest="casting_selection", help="Casting selection trace path")
    parser.add_argument("--tts-requests", dest="tts_requests", help="TTS requests artifact path")
    parser.add_argument("--library", help="voice-library.yaml path")
    parser.add_argument("--level", choices=VALID_LEVELS, default="essential")
    parser.add_argument("--write-manifest", action="store_true", help="Write/update the manifest file before printing")
    parser.add_argument("--pretty", action="store_true", help="Print a human-readable grouped view")
    return parser.parse_args()


def load_or_build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    if args.manifest:
        manifest = load_json(Path(args.manifest).resolve())
        if not isinstance(manifest, dict):
            raise RuntimeError(f"manifest 不是合法对象: {args.manifest}")
        return manifest

    manifest = build_story_artifact_manifest(
        story_input_path=args.story_input,
        effective_story_input_path=args.effective_story_input,
        structured_script_artifact_path=args.structured_script_artifact,
        casting_output_path=args.casting_plan,
        casting_review_path=args.casting_review,
        clone_review_path=args.clone_review,
        role_profiles_path=args.role_profiles,
        casting_selection_path=args.casting_selection,
        tts_requests_path=args.tts_requests,
        library_path=args.library,
    )
    if args.write_manifest:
        save_story_artifact_manifest(manifest)
    return manifest


def main() -> None:
    args = parse_args()
    manifest = load_or_build_manifest(args)
    selected_items = select_manifest_items(manifest, args.level)

    if args.pretty:
        print(format_manifest_pretty(manifest, args.level), end="")
        return

    payload = {
        "level": args.level,
        "manifest_path": manifest.get("manifest_path"),
        "artifact_base_dir": manifest.get("artifact_base_dir"),
        "count": len(selected_items),
        "items": selected_items,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
