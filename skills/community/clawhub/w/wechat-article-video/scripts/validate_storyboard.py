#!/usr/bin/env python3
"""Validate the V2 storyboard before TTS or renderer work begins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MODE_SCENE_RANGES = {
    "brief": (3, 5),
    "compact-standard": (6, 8),
    "standard": (4, 8),
    "detail": (6, 12),
}
LAYOUTS = {"cover", "company-profile", "product-hero", "fact-focus", "cta"}
TYPES = {"cover", "company", "product", "fact", "cta"}
RENDERERS = {"hyperframes", "remotion"}


def all_scene_text(scene: dict) -> str:
    values = [
        scene.get("headline", ""),
        scene.get("supporting_text", ""),
        scene.get("disclaimer", ""),
    ]
    values.extend(scene.get("facts") or [])
    return "".join(str(value) for value in values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Resolve and verify storyboard asset paths against this directory",
    )
    parser.add_argument(
        "--content-brief",
        type=Path,
        help="Verify source references, disclaimer, asset readiness, and blocking status",
    )
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    board = json.loads(args.input.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    known_source_refs: set[str] = set()

    content_brief = None
    critical_claim_source_refs: dict[str, str] = {}
    if args.content_brief:
        content_brief = json.loads(args.content_brief.read_text(encoding="utf-8"))
        known_source_refs = {
            section.get("id")
            for section in content_brief.get("source_sections", [])
            if section.get("id")
        }
        known_source_refs.update(
            claim.get("source_ref")
            for claim in content_brief.get("claims", [])
            if claim.get("source_ref")
        )
        status = str(content_brief.get("production_status", "ready")).lower()
        if status != "ready":
            errors.append(f"content brief production_status is not ready: {status!r}")
        for asset in content_brief.get("assets", []):
            asset_status = str(asset.get("status", "")).lower()
            if asset_status not in {"ready", "available", "usable"}:
                errors.append(
                    f"content brief asset is not ready: "
                    f"{asset.get('path') or asset.get('id') or '<unknown>'} ({asset_status})"
                )
        claims_by_id = {
            claim.get("id"): claim
            for claim in content_brief.get("claims", [])
            if claim.get("id")
        }
        for claim_id in content_brief.get("critical_claim_ids", []):
            claim = claims_by_id.get(claim_id)
            if not claim:
                errors.append(f"unknown critical_claim_id: {claim_id!r}")
                continue
            source_ref = claim.get("source_ref")
            if not source_ref:
                errors.append(f"critical claim {claim_id!r} has no source_ref")
                continue
            critical_claim_source_refs[claim_id] = source_ref

    if board.get("version") != 2:
        errors.append("version must be 2")

    mode = board.get("mode")
    if mode not in MODE_SCENE_RANGES:
        errors.append(f"invalid mode: {mode!r}")

    renderer = board.get("renderer")
    if renderer not in RENDERERS:
        errors.append(f"invalid renderer: {renderer!r}")

    canvas = board.get("canvas") or {}
    if (canvas.get("width"), canvas.get("height"), canvas.get("fps")) != (1080, 1920, 30):
        errors.append("canvas must be 1080x1920 at 30 fps")

    voice = board.get("voice") or {}
    if voice.get("provider") != "edge-tts":
        errors.append("voice.provider must default to edge-tts")

    scenes = board.get("scenes") or []
    if mode in MODE_SCENE_RANGES:
        minimum, maximum = MODE_SCENE_RANGES[mode]
        if not minimum <= len(scenes) <= maximum:
            errors.append(
                f"{mode} mode expects {minimum}-{maximum} scenes including cover; "
                f"got {len(scenes)}"
            )

    if scenes:
        if scenes[0].get("type") != "cover" or scenes[0].get("layout") != "cover":
            errors.append("first scene must use type=cover and layout=cover")
        if float(scenes[0].get("first_meaningful_sec", 99)) != 0:
            errors.append("cover first_meaningful_sec must be 0")
    else:
        errors.append("scenes are required")

    ids: set[str] = set()
    caption_entries: list[int] = []
    storyboard_source_refs: set[str] = set()
    for index, scene in enumerate(scenes):
        label = scene.get("id") or f"scene-{index + 1}"
        if not scene.get("id") or label in ids:
            errors.append(f"{label}: missing or duplicate id")
        ids.add(label)

        if scene.get("type") not in TYPES:
            errors.append(f"{label}: invalid type {scene.get('type')!r}")
        if scene.get("layout") not in LAYOUTS:
            errors.append(f"{label}: invalid layout {scene.get('layout')!r}")
        if not str(scene.get("narrative_job", "")).strip():
            errors.append(f"{label}: narrative_job is required")
        source_refs = scene.get("source_refs") or []
        storyboard_source_refs.update(source_refs)
        if not source_refs:
            errors.append(f"{label}: source_refs are required")
        elif known_source_refs:
            unknown = [source_ref for source_ref in source_refs if source_ref not in known_source_refs]
            if unknown:
                errors.append(f"{label}: unknown source_refs {unknown}")
        if not str(scene.get("headline", "")).strip():
            errors.append(f"{label}: headline is required")

        meaningful = float(scene.get("first_meaningful_sec", 99))
        if meaningful > 0.4:
            errors.append(f"{label}: first meaningful visual appears after 0.4s")

        entries = scene.get("caption_entries") or []
        if entries != sorted(entries) or len(entries) != len(set(entries)):
            errors.append(f"{label}: caption_entries must be sorted and unique")
        caption_entries.extend(entries)

        focal_asset = scene.get("focal_asset")
        if scene.get("layout") in {"cover", "company-profile", "product-hero"} and not focal_asset:
            errors.append(f"{label}: {scene.get('layout')} requires focal_asset")
        if focal_asset and not isinstance(focal_asset, str):
            errors.append(f"{label}: focal_asset must be one project-relative path string")
        if isinstance(focal_asset, str) and args.project_root:
            path = (args.project_root / focal_asset).resolve()
            if not path.is_file():
                errors.append(f"{label}: missing focal asset {focal_asset}")
        secondary_assets = scene.get("secondary_assets") or []
        if not isinstance(secondary_assets, list) or any(
            not isinstance(asset, str) for asset in secondary_assets
        ):
            errors.append(f"{label}: secondary_assets must be a list of path strings")
        elif args.project_root:
            for asset in secondary_assets:
                if not (args.project_root / asset).resolve().is_file():
                    errors.append(f"{label}: missing secondary asset {asset}")

        width_pct = float(scene.get("asset_width_pct", 0) or 0)
        if scene.get("layout") == "product-hero" and width_pct < 60:
            errors.append(f"{label}: product asset_width_pct must be at least 60")
        if scene.get("layout") == "cover" and width_pct < 50:
            errors.append(f"{label}: cover asset_width_pct must be at least 50")

        if index and scene.get("layout") == scenes[index - 1].get("layout"):
            warnings.append(
                f"{label}: repeats adjacent layout {scene.get('layout')}; "
                "change composition, focal position, or information structure"
            )

    if caption_entries:
        expected = list(range(1, max(caption_entries) + 1))
        if caption_entries != expected:
            errors.append(
                "caption_entries across narration scenes must be contiguous, ordered, "
                f"and begin at 1; got {caption_entries}"
            )

    if mode in {"compact-standard", "standard", "detail"} and not any(
        scene.get("layout") == "cta" for scene in scenes
    ):
        errors.append(f"{mode} mode requires a cta scene")

    if mode == "compact-standard":
        if content_brief and not content_brief.get("critical_claim_ids"):
            errors.append("compact-standard mode requires content brief critical_claim_ids")
        for claim_id, source_ref in critical_claim_source_refs.items():
            if source_ref not in storyboard_source_refs:
                errors.append(
                    f"critical claim {claim_id!r} is not covered by storyboard "
                    f"source_refs: {source_ref!r}"
                )

    disclaimer = str(board.get("required_disclaimer", "")).strip()
    if content_brief:
        brief_disclaimer = str(content_brief.get("required_disclaimer", "")).strip()
        if disclaimer.rstrip("。") != brief_disclaimer.rstrip("。"):
            errors.append("storyboard required_disclaimer differs from content brief")
    if disclaimer and not any(disclaimer in all_scene_text(scene) for scene in scenes):
        errors.append("required_disclaimer is not present in any scene")

    report = {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "scene_count": len(scenes),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    for warning in warnings:
        print(f"[warning] {warning}")
    for error in errors:
        print(f"[error] {error}")
    if errors:
        return 1
    print(f"storyboard valid: {len(scenes)} scenes, {len(warnings)} warnings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
