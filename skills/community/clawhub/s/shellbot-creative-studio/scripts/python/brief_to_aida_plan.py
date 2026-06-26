#!/usr/bin/env python3
"""
Turn a product brief JSON file into an AIDA scene plan JSON.

Usage:
  python3 scripts/brief_to_aida_plan.py --in brief.json --out plan.json --duration-sec 45 --fps 30
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "product_name",
    "audience",
    "problem",
    "solution",
    "use_cases",
    "cta",
    "incentive",
)


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object.")
    return data


def _validate_brief(brief: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in brief]
    if missing:
        raise ValueError(f"Missing required brief fields: {', '.join(missing)}")

    use_cases = brief.get("use_cases")
    if not isinstance(use_cases, list) or len(use_cases) == 0:
        raise ValueError("`use_cases` must be a non-empty array.")

    if len(use_cases) > 4:
        raise ValueError("Use 1 to 4 use cases for product-video pacing.")

    for idx, item in enumerate(use_cases):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"`use_cases[{idx}]` must be a non-empty string.")

    features = brief.get("features", [])
    if isinstance(features, list) and features and not use_cases:
        raise ValueError(
            "Detected features with no use cases. Rewrite feature points as real use cases."
        )


def _frames(seconds: float, fps: int) -> int:
    return max(1, int(round(seconds * fps)))


def _build_plan(brief: dict[str, Any], duration_sec: int, fps: int) -> dict[str, Any]:
    total_frames = _frames(duration_sec, fps)

    attention_frames = max(1, math.floor(total_frames * 0.20))
    interest_frames = max(1, math.floor(total_frames * 0.25))
    desire_frames = max(1, math.floor(total_frames * 0.35))
    action_frames = max(1, total_frames - (attention_frames + interest_frames + desire_frames))

    use_cases: list[str] = brief["use_cases"]
    per_use_case = max(1, desire_frames // len(use_cases))
    desire_allocations = [per_use_case for _ in use_cases]
    remainder = desire_frames - sum(desire_allocations)
    if remainder > 0:
        desire_allocations[-1] += remainder

    scenes = []
    cursor = 0

    scenes.append(
        {
            "id": "attention-problem",
            "stage": "attention",
            "from": cursor,
            "duration_in_frames": attention_frames,
            "objective": f"Establish the pain: {brief['problem']}",
            "voiceover": f"{brief['audience']} face this every day: {brief['problem']}",
        }
    )
    cursor += attention_frames

    scenes.append(
        {
            "id": "interest-solution",
            "stage": "interest",
            "from": cursor,
            "duration_in_frames": interest_frames,
            "objective": f"Introduce solution: {brief['solution']}",
            "voiceover": f"Meet {brief['product_name']}: {brief['solution']}",
        }
    )
    cursor += interest_frames

    for index, use_case in enumerate(use_cases, start=1):
        duration = desire_allocations[index - 1]
        scenes.append(
            {
                "id": f"desire-use-case-{index}",
                "stage": "desire",
                "from": cursor,
                "duration_in_frames": duration,
                "objective": f"Show use case {index}: {use_case}",
                "voiceover": use_case,
            }
        )
        cursor += duration

    scenes.append(
        {
            "id": "action-cta",
            "stage": "action",
            "from": cursor,
            "duration_in_frames": action_frames,
            "objective": f"Deliver CTA with incentive: {brief['cta']} ({brief['incentive']})",
            "voiceover": f"{brief['cta']}. {brief['incentive']}.",
        }
    )

    return {
        "meta": {
            "product_name": brief["product_name"],
            "audience": brief["audience"],
            "fps": fps,
            "duration_sec": duration_sec,
            "duration_in_frames": total_frames,
            "framework": "AIDA",
        },
        "rules": [
            "Show use cases, not feature bullets.",
            "Keep Remotion as timeline authority.",
            "End with CTA plus incentive.",
        ],
        "scenes": scenes,
        "assets": {
            "attention": ["hero-still"],
            "interest": ["product-context-still-or-clip"],
            "desire": ["use-case-visuals"],
            "action": ["cta-card", "optional-subtle-bg-motion"],
        },
    }


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an AIDA scene plan from a product brief.")
    parser.add_argument("--in", dest="input_path", required=True, help="Path to brief JSON")
    parser.add_argument("--out", dest="output_path", required=True, help="Path to output plan JSON")
    parser.add_argument(
        "--duration-sec",
        type=int,
        default=45,
        help="Final video duration in seconds (default: 45)",
    )
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    return parser


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.duration_sec < 15 or args.duration_sec > 180:
        raise ValueError("--duration-sec must be between 15 and 180.")
    if args.fps < 1 or args.fps > 120:
        raise ValueError("--fps must be between 1 and 120.")

    input_path = Path(args.input_path).resolve()
    output_path = Path(args.output_path).resolve()

    brief = _load_json(input_path)
    _validate_brief(brief)
    plan = _build_plan(brief, duration_sec=args.duration_sec, fps=args.fps)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
