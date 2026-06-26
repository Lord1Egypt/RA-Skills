#!/usr/bin/env python3
"""Route creative tasks to the best provider/model pair."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Route:
    provider: str
    model_or_endpoint: str
    reason: str
    required_env: List[str]
    command_hint: str


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def route_image(priority: str, consistency: bool, typography: bool, grounding: bool) -> Route:
    if grounding or consistency:
        return Route(
            provider="nano-banana-2",
            model_or_endpoint="google/gemini-3-1-flash-image-preview",
            reason="Best for multi-image consistency and iterative instruction-based editing.",
            required_env=["INFERENCE_API_KEY or infsh login"],
            command_hint=(
                "infsh app run google/gemini-3-1-flash-image-preview --input "
                "'{\"prompt\":\"...\",\"aspect_ratio\":\"16:9\",\"num_images\":2}'"
            ),
        )
    if typography:
        return Route(
            provider="freepik",
            model_or_endpoint="/v1/ai/text-to-image/seedream-v4-5",
            reason="Excellent for typography-heavy posters and ad creatives.",
            required_env=["FREEPIK_API_KEY"],
            command_hint=(
                "curl -s -X POST https://api.freepik.com/v1/ai/text-to-image/seedream-v4-5 "
                "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
                "-d '{\"prompt\":\"...\"}'"
            ),
        )
    if priority == "speed":
        return Route(
            provider="fal",
            model_or_endpoint="fal-ai/flux-2",
            reason="Fast concepting and exploration loops.",
            required_env=["FAL_KEY"],
            command_hint=(
                "curl -s -X POST https://queue.fal.run/fal-ai/flux-2 "
                "-H 'Authorization: Key $FAL_KEY' -H 'Content-Type: application/json' "
                "-d '{\"prompt\":\"...\",\"image_size\":\"landscape_16_9\"}'"
            ),
        )
    return Route(
        provider="freepik",
        model_or_endpoint="/v1/ai/mystic",
        reason="Best default for high-end photoreal product visuals.",
        required_env=["FREEPIK_API_KEY"],
        command_hint=(
            "curl -s -X POST https://api.freepik.com/v1/ai/mystic "
            "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
            "-d '{\"prompt\":\"...\",\"resolution\":\"2k\"}'"
        ),
    )


def route_edit(priority: str, consistency: bool) -> Route:
    if consistency:
        return Route(
            provider="nano-banana-2",
            model_or_endpoint="google/gemini-3-1-flash-image-preview",
            reason="Strong iterative edit quality with multi-reference inputs.",
            required_env=["INFERENCE_API_KEY or infsh login"],
            command_hint=(
                "infsh app run google/gemini-3-1-flash-image-preview --input "
                "'{\"prompt\":\"edit instruction\",\"images\":[\"https://...\"]}'"
            ),
        )
    if priority == "quality":
        return Route(
            provider="freepik",
            model_or_endpoint="/v1/ai/image-upscaler-precision-v2",
            reason="High-fidelity edits and upscale with minimal hallucination.",
            required_env=["FREEPIK_API_KEY"],
            command_hint=(
                "curl -s -X POST https://api.freepik.com/v1/ai/image-upscaler-precision-v2 "
                "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
                "-d '{\"image\":\"https://...\",\"scale\":4}'"
            ),
        )
    return Route(
        provider="freepik",
        model_or_endpoint="/v1/ai/text-to-image/seedream-v4-5-edit",
        reason="Reliable instruction-guided edits for creative revisions.",
        required_env=["FREEPIK_API_KEY"],
        command_hint=(
            "curl -s -X POST https://api.freepik.com/v1/ai/text-to-image/seedream-v4-5-edit "
            "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
            "-d '{\"prompt\":\"...\",\"input_images\":[\"https://...\"]}'"
        ),
    )


def route_video(priority: str) -> Route:
    if priority == "speed":
        return Route(
            provider="fal",
            model_or_endpoint="fal-ai/minimax/video-01/image-to-video",
            reason="Fast fallback for image-to-video scene generation.",
            required_env=["FAL_KEY"],
            command_hint=(
                "curl -s -X POST https://queue.fal.run/fal-ai/minimax/video-01/image-to-video "
                "-H 'Authorization: Key $FAL_KEY' -H 'Content-Type: application/json' "
                "-d '{\"prompt\":\"...\",\"image_url\":\"https://...\"}'"
            ),
        )
    return Route(
        provider="freepik",
        model_or_endpoint="/v1/ai/video/kling-v3-omni-pro",
        reason="Best quality default for cinematic multi-shot outputs.",
        required_env=["FREEPIK_API_KEY"],
        command_hint=(
            "curl -s -X POST https://api.freepik.com/v1/ai/video/kling-v3-omni-pro "
            "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
            "-d '{\"prompt\":\"...\",\"duration\":5}'"
        ),
    )


def route_voice() -> Route:
    return Route(
        provider="freepik",
        model_or_endpoint="/v1/ai/voiceover/elevenlabs-turbo-v2-5",
        reason="Direct ElevenLabs voiceover access with clean integration.",
        required_env=["FREEPIK_API_KEY"],
        command_hint=(
            "curl -s -X POST https://api.freepik.com/v1/ai/voiceover/elevenlabs-turbo-v2-5 "
            "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
            "-d '{\"text\":\"...\",\"voice_id\":\"21m00Tcm4TlvDq8ikWAM\"}'"
        ),
    )


def route_music() -> Route:
    return Route(
        provider="freepik",
        model_or_endpoint="/v1/ai/music-generation",
        reason="Simple text-to-music for short-form marketing and explainer cuts.",
        required_env=["FREEPIK_API_KEY"],
        command_hint=(
            "curl -s -X POST https://api.freepik.com/v1/ai/music-generation "
            "-H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' "
            "-d '{\"prompt\":\"upbeat cinematic\",\"music_length_seconds\":30}'"
        ),
    )


def route(goal: str, priority: str, consistency: bool, typography: bool, grounding: bool) -> Dict[str, object]:
    if goal == "image":
        primary = route_image(priority, consistency, typography, grounding)
    elif goal == "edit":
        primary = route_edit(priority, consistency)
    elif goal == "video":
        primary = route_video(priority)
    elif goal == "voice":
        primary = route_voice()
    elif goal == "music":
        primary = route_music()
    else:
        primary = Route(
            provider="pipeline",
            model_or_endpoint="multi-provider",
            reason="Use staged workflow for polished final output.",
            required_env=["FREEPIK_API_KEY", "FAL_KEY", "INFERENCE_API_KEY or infsh login"],
            command_hint="python3 scripts/creative_brief_to_storyboard.py --brief '...' --duration 45 --out storyboard.json",
        )

    sequence = [
        "Plan storyboard",
        "Generate reusable assets",
        "Generate hero motion scenes",
        "Generate narration and music",
        "Assemble + render in Remotion",
    ]

    return {
        "goal": goal,
        "priority": priority,
        "recommendation": primary.__dict__,
        "pipeline_sequence": sequence,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Choose best provider/model for creative tasks")
    parser.add_argument(
        "--goal",
        default="full-video",
        choices=["image", "edit", "video", "voice", "music", "full-video"],
        help="Primary creative task",
    )
    parser.add_argument(
        "--priority",
        default="balanced",
        choices=["speed", "balanced", "quality"],
        help="Optimization preference",
    )
    parser.add_argument("--needs-consistency", type=parse_bool, default=False)
    parser.add_argument("--needs-typography", type=parse_bool, default=False)
    parser.add_argument("--needs-web-grounding", type=parse_bool, default=False)
    parser.add_argument("--out", help="Optional output file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = route(
        goal=args.goal,
        priority=args.priority,
        consistency=args.needs_consistency,
        typography=args.needs_typography,
        grounding=args.needs_web_grounding,
    )
    payload = json.dumps(result, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(payload + "\n")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
