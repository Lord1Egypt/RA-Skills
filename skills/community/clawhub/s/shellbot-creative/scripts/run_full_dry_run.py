#!/usr/bin/env python3
"""Run a local end-to-end dry run for the creative pipeline without API calls."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from creative_brief_to_storyboard import build_storyboard, clamp
from creative_provider_router import route
from remotion_manifest_from_storyboard import build_manifest


def ensure_dirs(base_dir: Path) -> Dict[str, Path]:
    paths = {
        "assets": base_dir / "assets",
        "scenes": base_dir / "scenes",
        "audio": base_dir / "audio",
        "final": base_dir / "final",
        "manifests": base_dir / "manifests",
        "commands": base_dir / "commands",
        "logs": base_dir / "logs",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def pick_recommendation(task: str, provider_order: List[str]) -> Dict[str, str]:
    candidates: Dict[str, List[Dict[str, str]]] = {
        "image": [
            {
                "provider": "freepik",
                "model": "/v1/ai/mystic",
                "reason": "High-fidelity product marketing stills.",
            },
            {
                "provider": "fal",
                "model": "fal-ai/flux-2-pro",
                "reason": "Fast high-quality ideation fallback.",
            },
            {
                "provider": "nano-banana-2",
                "model": "google/gemini-3-1-flash-image-preview",
                "reason": "Consistency-focused multi-image edits.",
            },
        ],
        "edit": [
            {
                "provider": "freepik",
                "model": "/v1/ai/text-to-image/seedream-v4-5-edit",
                "reason": "Deterministic instruction-based revision flow.",
            },
            {
                "provider": "nano-banana-2",
                "model": "google/gemini-3-1-flash-image-preview",
                "reason": "Iterative edits with multi-reference support.",
            },
            {
                "provider": "fal",
                "model": "fal-ai/flux-2-pro",
                "reason": "General fallback when others are unavailable.",
            },
        ],
        "video": [
            {
                "provider": "freepik",
                "model": "/v1/ai/video/kling-v3-omni-pro",
                "reason": "Best quality default for cinematic hero scenes.",
            },
            {
                "provider": "fal",
                "model": "fal-ai/kling-video/v2/image-to-video",
                "reason": "Strong fallback for image-to-video animation.",
            },
        ],
        "voice": [
            {
                "provider": "freepik",
                "model": "/v1/ai/voiceover/elevenlabs-turbo-v2-5",
                "reason": "Direct ElevenLabs voiceover workflow.",
            },
            {
                "provider": "fal",
                "model": "text-to-speech (search endpoint)",
                "reason": "Fallback when Freepik is unavailable.",
            },
        ],
        "music": [
            {
                "provider": "freepik",
                "model": "/v1/ai/music-generation",
                "reason": "Simple text-to-music for ad and explainer videos.",
            },
            {
                "provider": "fal",
                "model": "audio generation model (search endpoint)",
                "reason": "Fallback music option.",
            },
        ],
    }

    ordered = sorted(
        candidates[task],
        key=lambda item: provider_order.index(item["provider"]) if item["provider"] in provider_order else 999,
    )
    return ordered[0]


def freepik_command_templates(storyboard: Dict[str, object]) -> List[Dict[str, str]]:
    scenes = storyboard["scenes"]
    commands: List[Dict[str, str]] = []

    for scene in scenes:
        sid = scene["id"]
        commands.append(
            {
                "step": f"asset_scene_{sid}",
                "provider": "freepik",
                "command": (
                    "curl -s -X POST https://api.freepik.com/v1/ai/mystic "
                    "-H 'x-freepik-api-key: $FREEPIK_API_KEY' "
                    "-H 'Content-Type: application/json' "
                    f"-d '{{\"prompt\":\"{scene['visual_prompt']}\",\"resolution\":\"2k\",\"styling\":{{\"style\":\"photo\"}}}}'"
                ),
            }
        )

    hero_ids = [scene["id"] for scene in scenes if scene["id"] % 2 == 1]
    for sid in hero_ids:
        commands.append(
            {
                "step": f"video_scene_{sid}",
                "provider": "freepik",
                "command": (
                    "curl -s -X POST https://api.freepik.com/v1/ai/video/kling-v3-omni-pro "
                    "-H 'x-freepik-api-key: $FREEPIK_API_KEY' "
                    "-H 'Content-Type: application/json' "
                    f"-d '{{\"prompt\":\"Animate scene {sid} with cinematic product motion\",\"duration\":5}}'"
                ),
            }
        )

    commands.extend(
        [
            {
                "step": "voiceover",
                "provider": "freepik",
                "command": (
                    "curl -s -X POST https://api.freepik.com/v1/ai/voiceover/elevenlabs-turbo-v2-5 "
                    "-H 'x-freepik-api-key: $FREEPIK_API_KEY' "
                    "-H 'Content-Type: application/json' "
                    "-d '{\"text\":\"Replace with stitched scene narration\",\"voice_id\":\"21m00Tcm4TlvDq8ikWAM\"}'"
                ),
            },
            {
                "step": "music",
                "provider": "freepik",
                "command": (
                    "curl -s -X POST https://api.freepik.com/v1/ai/music-generation "
                    "-H 'x-freepik-api-key: $FREEPIK_API_KEY' "
                    "-H 'Content-Type: application/json' "
                    "-d '{\"prompt\":\"upbeat modern product marketing background music\",\"music_length_seconds\":45}'"
                ),
            },
        ]
    )
    return commands


def write_shell_plan(path: Path, commands: List[Dict[str, str]]) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "if [[ -z \"${FREEPIK_API_KEY:-}\" ]]; then",
        "  echo \"FREEPIK_API_KEY is required for this Freepik-first run.\" >&2",
        "  exit 1",
        "fi",
        "",
        "mkdir -p ./creative-output/{assets,scenes,audio,final,manifests}",
        "",
    ]

    for item in commands:
        lines.append(f"echo \"=== {item['step']} ({item['provider']}) ===\"")
        lines.append(item["command"])
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(path, 0o755)


def write_report(
    path: Path,
    storyboard_path: Path,
    remotion_manifest_path: Path,
    route_path: Path,
    shell_plan_path: Path,
    provider_order: List[str],
) -> None:
    report = f"""# Dry Run Report (Freepik-first)

## Summary

- This was a local dry run (no network calls were made).
- Provider order used: {', '.join(provider_order)}
- Routing and manifests were generated and saved.

## Artifacts

- Storyboard: `{storyboard_path}`
- Remotion manifest: `{remotion_manifest_path}`
- Routing summary: `{route_path}`
- Executable API plan: `{shell_plan_path}`

## Next action for real generation

1. Export keys: `FREEPIK_API_KEY` (and optional `FAL_KEY`, `INFERENCE_API_KEY`).
2. Review prompts in the API plan shell script.
3. Run the shell plan, then map returned URLs into the Remotion manifest.
4. Render with Remotion.
"""
    path.write_text(report, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a local full creative dry run")
    parser.add_argument("--brief", required=True, help="Creative brief")
    parser.add_argument("--format", default="product-marketing", choices=["product-marketing", "explainer", "social-ad", "feature-launch"])
    parser.add_argument("--duration", type=int, default=45)
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--provider-order", default="freepik,fal,nano-banana-2")
    parser.add_argument("--out-dir", default="creative-output/dry-run-freepik-first")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_dir = Path(args.out_dir).resolve()
    dirs = ensure_dirs(base_dir)

    provider_order = [part.strip() for part in args.provider_order.split(",") if part.strip()]
    total_seconds = clamp(args.duration, 6, 300)

    storyboard = build_storyboard(
        brief=args.brief,
        format_name=args.format,
        total_seconds=total_seconds,
        aspect_ratio=args.aspect_ratio,
        scenes_override=None,
        cta="Try it today",
    )
    storyboard_path = dirs["manifests"] / "storyboard.json"
    storyboard_path.write_text(json.dumps(storyboard, indent=2) + "\n", encoding="utf-8")

    routing = {
        "provider_order": provider_order,
        "recommended": {
            "image": pick_recommendation("image", provider_order),
            "edit": pick_recommendation("edit", provider_order),
            "video": pick_recommendation("video", provider_order),
            "voice": pick_recommendation("voice", provider_order),
            "music": pick_recommendation("music", provider_order),
        },
        "base_router_output": {
            "image": route("image", "quality", False, False, False),
            "edit": route("edit", "quality", False, False, False),
            "video": route("video", "quality", False, False, False),
            "voice": route("voice", "quality", False, False, False),
            "music": route("music", "quality", False, False, False),
            "full_video": route("full-video", "quality", True, True, False),
        },
    }
    route_path = dirs["manifests"] / "routing.json"
    route_path.write_text(json.dumps(routing, indent=2) + "\n", encoding="utf-8")

    remotion_manifest = build_manifest(
        storyboard=storyboard,
        fps=max(1, args.fps),
        voiceover_url="./audio/voiceover.mp3",
        music_url="./audio/music.mp3",
    )
    remotion_manifest_path = dirs["manifests"] / "remotion-manifest.json"
    remotion_manifest_path.write_text(json.dumps(remotion_manifest, indent=2) + "\n", encoding="utf-8")

    commands = freepik_command_templates(storyboard)
    command_manifest_path = dirs["commands"] / "freepik-task-plan.json"
    command_manifest_path.write_text(json.dumps(commands, indent=2) + "\n", encoding="utf-8")

    shell_plan_path = dirs["commands"] / "run-freepik-first.sh"
    write_shell_plan(shell_plan_path, commands)

    report_path = base_dir / "dry-run-report.md"
    write_report(
        report_path,
        storyboard_path,
        remotion_manifest_path,
        route_path,
        shell_plan_path,
        provider_order,
    )

    summary = {
        "out_dir": str(base_dir),
        "storyboard": str(storyboard_path),
        "routing": str(route_path),
        "remotion_manifest": str(remotion_manifest_path),
        "commands_json": str(command_manifest_path),
        "commands_sh": str(shell_plan_path),
        "report": str(report_path),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
