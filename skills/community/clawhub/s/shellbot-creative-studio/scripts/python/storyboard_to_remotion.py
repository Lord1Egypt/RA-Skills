#!/usr/bin/env python3
"""Convert storyboard JSON into a Remotion-friendly manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def aspect_to_dimensions(aspect_ratio: str) -> Tuple[int, int]:
    mapping = {
        "16:9": (1920, 1080),
        "9:16": (1080, 1920),
        "1:1": (1080, 1080),
        "4:5": (1080, 1350),
        "4:3": (1440, 1080),
    }
    return mapping.get(aspect_ratio, (1920, 1080))


def load_storyboard(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def to_frames(seconds: float, fps: int) -> int:
    return max(1, int(round(seconds * fps)))


def build_manifest(storyboard: Dict[str, object], fps: int, voiceover_url: str, music_url: str) -> Dict[str, object]:
    aspect_ratio = str(storyboard.get("aspect_ratio", "16:9"))
    width, height = aspect_to_dimensions(aspect_ratio)
    scenes = storyboard.get("scenes", [])

    sequence_entries: List[Dict[str, object]] = []
    current_frame = 0

    for scene in scenes:
        duration_seconds = float(scene.get("duration_seconds", 4))
        duration_frames = to_frames(duration_seconds, fps)
        entry = {
            "id": scene.get("id"),
            "name": scene.get("name"),
            "from": current_frame,
            "durationInFrames": duration_frames,
            "goal": scene.get("goal"),
            "visualPrompt": scene.get("visual_prompt"),
            "animationHint": scene.get("animation_hint"),
            "narration": scene.get("narration"),
            "onScreenText": scene.get("on_screen_text"),
            "asset": {
                "type": "image_or_video",
                "src": f"./assets/scene-{scene.get('id')}.mp4",
                "fallbackImage": f"./assets/scene-{scene.get('id')}.png",
            },
        }
        sequence_entries.append(entry)
        current_frame += duration_frames

    composition_id = f"Creative_{storyboard.get('project_name', 'Project')}"

    return {
        "composition": {
            "id": composition_id,
            "fps": fps,
            "width": width,
            "height": height,
            "durationInFrames": current_frame,
            "defaultProps": {
                "title": storyboard.get("creative_brief"),
                "aspectRatio": aspect_ratio,
                "sequences": sequence_entries,
                "audio": {
                    "voiceover": voiceover_url,
                    "music": music_url,
                    "musicVolume": 0.2,
                    "voiceVolume": 1.0,
                },
                "style": {
                    "captionSafeMargin": 80,
                    "textColor": "#FFFFFF",
                    "brandAccent": "#6C5CE7",
                },
            },
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Remotion manifest from storyboard JSON")
    parser.add_argument("--storyboard", required=True, help="Path to storyboard JSON")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--voiceover-url", default="", help="Narration audio URL or local path")
    parser.add_argument("--music-url", default="", help="Background music URL or local path")
    parser.add_argument("--out", required=True, help="Output JSON path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    storyboard = load_storyboard(Path(args.storyboard))
    manifest = build_manifest(
        storyboard=storyboard,
        fps=max(1, args.fps),
        voiceover_url=args.voiceover_url,
        music_url=args.music_url,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
