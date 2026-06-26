#!/usr/bin/env python3
"""Video generation script supporting multiple modes: text, singleImage, startEnd, multiImage."""

import argparse
import base64
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

import requests

from utils.api_client import VideoAPIClient
from utils.config_loader import ConfigLoader, ConfigError
from utils.logger import setup_logger


class VideoMode(Enum):
    TEXT = "text"
    SINGLE = "single"
    START_END = "startEnd"
    MULTI = "multi"


@dataclass
class Shot:
    episode: int
    segment: int
    cell_number: int
    prompt: str
    camera: str = ""
    duration: int = 5
    image_path: Optional[Path] = None
    start_image_path: Optional[Path] = None
    end_image_path: Optional[Path] = None


@dataclass
class VideoConfig:
    api_key: str
    endpoint: str
    model: str
    provider: str = "kling"
    default_duration: int = 5
    default_resolution: str = "720p"
    default_aspect_ratio: str = "16:9"
    timeout: int = 600
    max_retries: int = 3


def _resolve_env(value):
    """Resolve ${ENV_VAR} syntax from environment variables."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        env_var = value[2:-1]
        return os.environ.get(env_var, value)
    return value


def load_config(config_path: Path, project_path: Path, logger: logging.Logger) -> VideoConfig:
    """Load video configuration from project.json."""
    project_json = project_path / "project.json"
    if not project_json.exists():
        raise ValueError("project.json not found")

    with open(project_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    video_config = data.get("models", {}).get("video", {})

    base_url = video_config.get("baseUrl", "")
    if base_url:
        endpoint = base_url.rstrip("/")
    else:
        # Default endpoints per provider
        provider = video_config.get("provider", "")
        endpoints = {
            "kling": "https://api.klingai.com",
            "volcengine": "https://ark.cn-beijing.volces.com/api/v3",
        }
        endpoint = endpoints.get(provider, "")

    return VideoConfig(
        api_key=_resolve_env(video_config.get("apiKey", "")),
        endpoint=endpoint,
        model=video_config.get("model", "kling-v1-pro"),
        provider=video_config.get("provider", "kling"),
    )


def parse_storyboard(storyboard_path: Path, logger: logging.Logger) -> list[Shot]:
    """Parse storyboard markdown to extract shots with duration and camera info."""
    shots = []
    content = storyboard_path.read_text(encoding="utf-8")

    segment_pattern = r"## 片段(\d+)：(.*?)(?=\n## |\Z)"
    segments = re.findall(segment_pattern, content, re.DOTALL)

    for segment_num_str, segment_content in segments:
        segment_num = int(segment_num_str)

        shot_pattern = r"### 分镜(\d+)[:：]?\s*(.*?)(?=\n### |\n## |\Z)"
        shot_matches = re.findall(shot_pattern, segment_content, re.DOTALL)

        for shot_num_str, shot_content in shot_matches:
            shot_num = int(shot_num_str)

            # Extract duration if specified
            duration_match = re.search(r'[-*]\s*\*\*时长\*\*:\s*(\d+)s?', shot_content)
            duration = int(duration_match.group(1)) if duration_match else 5

            # Extract camera if specified
            camera_match = re.search(r'[-*]\s*\*\*运镜\*\*:\s*(.+)', shot_content)
            camera = camera_match.group(1).strip() if camera_match else ""

            # Extract cell prompts
            cell_pattern = r'\s*[-*]\s+\*\*镜头(\d+)\*\*:\s*(.+?)(?=\n\s*[-*]\s+\*\*|$)'
            cell_matches = re.findall(cell_pattern, shot_content, re.DOTALL)

            for cell_num_str, cell_prompt in cell_matches:
                cell_num = int(cell_num_str)
                shots.append(Shot(
                    episode=segment_num,
                    segment=shot_num,
                    cell_number=cell_num,
                    prompt=cell_prompt.strip(),
                    camera=camera,
                    duration=duration,
                ))

    logger.info(f"Parsed {len(shots)} shots from {storyboard_path.name}")
    return shots


def find_storyboard_images(project_path: Path, episode: int, shots: list[Shot]) -> None:
    """Find and attach storyboard image paths to shots."""
    images_dir = project_path / "storyboard" / "images"
    if not images_dir.exists():
        return

    for shot in shots:
        # Look for image: 片段{ep}-分镜{shot}-镜头{cell}.jpg
        for ext in ["jpg", "jpeg", "png"]:
            image_name = f"片段{shot.episode}-分镜{shot.segment}-镜头{shot.cell_number}.{ext}"
            image_path = images_dir / image_name
            if image_path.exists():
                shot.image_path = image_path
                break


def generate_video_for_shot(
    api: VideoAPIClient,
    shot: Shot,
    mode: VideoMode,
    config: VideoConfig,
    output_dir: Path,
    logger: logging.Logger,
) -> tuple[bool, Optional[Path]]:
    """Generate video for a single shot.

    Returns:
        Tuple of (success, output_path).
    """
    shot_name = f"ep{shot.episode:02d}-seg{shot.segment:02d}-cell{shot.cell_number:02d}"
    output_path = output_dir / f"{shot_name}.mp4"

    if output_path.exists():
        logger.info(f"  [SKIP] {shot_name} already exists")
        return True, output_path

    logger.info(f"  Processing {shot_name}: {shot.prompt[:50]}...")

    # Prepare image URLs
    image_url = None
    start_url = None
    end_url = None

    if mode == VideoMode.SINGLE and shot.image_path:
        with open(shot.image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{b64}"

    elif mode == VideoMode.START_END:
        if shot.image_path:
            with open(shot.image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            start_url = f"data:image/jpeg;base64,{b64}"
        # For end frame, try to find next shot's image
        # This is simplified; real implementation would need better logic

    try:
        task_id = api.submit(
            prompt=shot.prompt,
            mode=mode.value,
            image_url=image_url,
            start_image_url=start_url,
            end_image_url=end_url,
            duration=shot.duration,
            resolution=config.default_resolution,
            aspect_ratio=config.default_aspect_ratio,
        )

        if not task_id:
            logger.error(f"  No task ID received for {shot_name}")
            return False, None

        logger.info(f"  Task submitted: {task_id}")

        result = api.wait_for_completion(task_id, timeout=config.timeout)

        if result["status"] == "succeeded" and result.get("video_url"):
            video_url = result["video_url"]
            logger.info(f"  Downloading video...")

            # Download video
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(video_url, headers=headers, timeout=300)
            response.raise_for_status()

            output_path.write_bytes(response.content)
            logger.info(f"  [OK] {shot_name}")
            return True, output_path
        else:
            error = result.get("error", "Unknown error")
            logger.error(f"  [FAIL] {shot_name}: {error}")
            return False, None

    except Exception as e:
        logger.error(f"  [FAIL] {shot_name}: {e}")
        return False, None


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate videos from storyboard")
    parser.add_argument("--project", "-p", type=str, required=True, help="Project directory")
    parser.add_argument("--mode", choices=["text", "single", "startEnd", "multi"], default="single")
    parser.add_argument("--episode", type=int, default=1, help="Episode number")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    project_path = Path(args.project)
    logger = setup_logger("video_generator", verbose=args.verbose)

    try:
        loader = ConfigLoader(project_path)
        config = loader.load()
    except ConfigError as e:
        logger.error(str(e))
        return 1

    missing = loader.check_required_models("video")
    if missing:
        print(loader.format_missing_guide(missing))
        return 1

    # Load video config
    try:
        video_config = load_config(project_path / "project.json", project_path, logger)
    except ValueError as e:
        logger.error(str(e))
        return 1

    # Find storyboard file
    storyboard_files = list((project_path / "storyboard").glob(f"storyboard-{args.episode:02d}.md"))
    if not storyboard_files:
        storyboard_files = list((project_path / "storyboard").glob("storyboard-*.md"))

    if not storyboard_files:
        logger.error("No storyboard files found")
        return 1

    api = VideoAPIClient(
        api_key=video_config.api_key,
        base_url=video_config.endpoint,
        model=video_config.model,
        provider=video_config.provider,
        logger=logger,
    )

    mode = VideoMode(args.mode)
    output_dir = project_path / "video"
    output_dir.mkdir(exist_ok=True)

    all_results = []

    for sb_file in sorted(storyboard_files):
        logger.info(f"\nProcessing: {sb_file.name}")
        shots = parse_storyboard(sb_file, logger)

        if mode in (VideoMode.SINGLE, VideoMode.START_END):
            find_storyboard_images(project_path, args.episode, shots)

        if args.dry_run:
            logger.info(f"DRY RUN: Would generate {len(shots)} videos")
            for shot in shots:
                logger.info(f"  {shot.episode}-{shot.segment}-{shot.cell_number}: {shot.prompt[:60]}...")
            continue

        for shot in shots:
            success, path = generate_video_for_shot(api, shot, mode, video_config, output_dir, logger)
            all_results.append((shot, success, path))

    # Summary
    if not args.dry_run:
        success_count = sum(1 for _, s, _ in all_results if s)
        logger.info(f"\nCompleted: {success_count}/{len(all_results)} videos generated")

        if success_count < len(all_results):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
