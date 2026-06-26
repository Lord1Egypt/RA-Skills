#!/usr/bin/env python3
"""
Shared utilities for TTS scripts — common path resolution, config loading, and argument parsing.
"""

import json
import os
import argparse


def resolve_project_root() -> str:
    """Resolve the project root directory (parent of scripts/)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_tts_args(description: str) -> argparse.Namespace:
    """Create and parse common TTS CLI arguments."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--config", default="config/project.json",
        help="Path to project config JSON"
    )
    parser.add_argument(
        "--content", default="content/subtitles.json",
        help="Path to subtitles JSON file"
    )
    return parser.parse_args()


def load_config_and_content(
    args: argparse.Namespace,
    root: str,
) -> tuple[dict, dict, str, str]:
    """
    Load config and content JSON files, resolving relative paths against project root.

    Returns:
        (config_dict, content_dict, config_path, content_path)
    """
    config_path = (
        os.path.join(root, args.config)
        if not os.path.isabs(args.config)
        else args.config
    )
    content_path = (
        os.path.join(root, args.content)
        if not os.path.isabs(args.content)
        else args.content
    )

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    return config, content, config_path, content_path


def resolve_audio_dir(config: dict, root: str) -> str:
    """Resolve the audio output directory from config, creating it if needed."""
    paths_config = config.get("paths", {})
    audio_dir = os.path.join(root, paths_config.get("audioDir", "public/audio"))
    os.makedirs(audio_dir, exist_ok=True)
    return audio_dir
