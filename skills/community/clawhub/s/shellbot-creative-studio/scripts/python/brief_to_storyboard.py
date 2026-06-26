#!/usr/bin/env python3
"""Convert a creative brief into a timed storyboard JSON."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    return re.sub(r"-+", "-", cleaned).strip("-") or "creative-project"


def phase_library(format_name: str) -> List[Dict[str, str]]:
    libraries: Dict[str, List[Dict[str, str]]] = {
        "product-marketing": [
            {"goal": "Hook", "motion": "dynamic opener with brand color burst"},
            {"goal": "Pain", "motion": "fast cuts of user frustration"},
            {"goal": "Reveal", "motion": "hero product reveal with camera push-in"},
            {"goal": "Features", "motion": "interface zooms and feature callouts"},
            {"goal": "Proof", "motion": "testimonial or metric-driven proof scene"},
            {"goal": "CTA", "motion": "clean end card with strong call to action"},
        ],
        "explainer": [
            {"goal": "Context", "motion": "gentle opener that sets the topic"},
            {"goal": "Problem", "motion": "visualize the pain point clearly"},
            {"goal": "Mechanism", "motion": "step-by-step animated process"},
            {"goal": "Benefits", "motion": "before/after comparison"},
            {"goal": "Next Step", "motion": "simple CTA with confidence"},
        ],
        "social-ad": [
            {"goal": "Scroll Stop", "motion": "high contrast hook in first second"},
            {"goal": "Product", "motion": "snappy hero shot loop"},
            {"goal": "Benefit", "motion": "single-message highlight"},
            {"goal": "Offer", "motion": "price or promo emphasis"},
            {"goal": "CTA", "motion": "tap-oriented close"},
        ],
        "feature-launch": [
            {"goal": "Announcement", "motion": "dramatic reveal of new capability"},
            {"goal": "Why It Matters", "motion": "problem-to-solution contrast"},
            {"goal": "Live Demo", "motion": "guided product walkthrough"},
            {"goal": "Adoption", "motion": "show impact in real use"},
            {"goal": "CTA", "motion": "upgrade or try-now close"},
        ],
    }
    return libraries.get(format_name, libraries["product-marketing"])


def distribute_duration(total_seconds: int, num_scenes: int) -> List[int]:
    base = total_seconds // num_scenes
    remainder = total_seconds % num_scenes
    durations = [base] * num_scenes
    for i in range(remainder):
        durations[i] += 1
    return durations


def build_storyboard(
    brief: str,
    format_name: str,
    total_seconds: int,
    aspect_ratio: str,
    scenes_override: int | None,
    cta: str,
) -> Dict[str, object]:
    default_scenes = clamp(int(round(total_seconds / 6.0)), 4, 8)
    scene_count = scenes_override if scenes_override else default_scenes
    scene_count = clamp(scene_count, 3, 12)

    phases = phase_library(format_name)
    selected_phases = [phases[i % len(phases)] for i in range(scene_count)]
    durations = distribute_duration(total_seconds, scene_count)

    scenes: List[Dict[str, object]] = []
    current_start = 0
    for idx, (phase, duration) in enumerate(zip(selected_phases, durations), start=1):
        scene_name = f"Scene {idx}: {phase['goal']}"
        narration = (
            f"{phase['goal']}: {brief}. Keep this line concise, clear, and benefit-focused."
        )
        on_screen_text = (
            f"{phase['goal']} - {brief[:72].rstrip()}"
            if len(brief) > 10
            else phase["goal"]
        )
        scene = {
            "id": idx,
            "name": scene_name,
            "start_second": current_start,
            "duration_seconds": duration,
            "goal": phase["goal"],
            "visual_prompt": (
                f"{brief}. {phase['goal']} scene, {aspect_ratio}, modern cinematic lighting."
            ),
            "animation_hint": phase["motion"],
            "narration": narration,
            "on_screen_text": on_screen_text,
            "sfx_hint": "subtle transition whoosh and clean UI clicks",
        }
        scenes.append(scene)
        current_start += duration

    scenes[-1]["narration"] = f"{scenes[-1]['narration']} {cta}".strip()
    scenes[-1]["on_screen_text"] = cta

    return {
        "project_name": slugify(brief)[:48],
        "format": format_name,
        "aspect_ratio": aspect_ratio,
        "total_duration_seconds": total_seconds,
        "scene_count": scene_count,
        "creative_brief": brief,
        "cta": cta,
        "scenes": scenes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate storyboard JSON from a creative brief")
    parser.add_argument("--brief", required=True, help="Project brief")
    parser.add_argument(
        "--format",
        default="product-marketing",
        choices=["product-marketing", "explainer", "social-ad", "feature-launch"],
        help="Narrative template",
    )
    parser.add_argument("--duration", type=int, default=30, help="Total duration in seconds")
    parser.add_argument("--aspect-ratio", default="16:9", help="Target output aspect ratio")
    parser.add_argument("--scenes", type=int, help="Override scene count")
    parser.add_argument("--cta", default="Try it today", help="Final call to action text")
    parser.add_argument("--out", help="Output path for JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    duration = clamp(args.duration, 6, 300)
    storyboard = build_storyboard(
        brief=args.brief,
        format_name=args.format,
        total_seconds=duration,
        aspect_ratio=args.aspect_ratio,
        scenes_override=args.scenes,
        cta=args.cta,
    )

    output = json.dumps(storyboard, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
