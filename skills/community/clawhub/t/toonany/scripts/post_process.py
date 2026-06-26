#!/usr/bin/env python3
"""Post-processing: concatenate videos, mix audio, burn subtitles.

Produces final episode video from generated segments.
"""

import argparse
import json
import logging
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.logger import setup_logger


@dataclass
class PostProcessConfig:
    project_path: Path
    episode: int
    video_dir: Path
    audio_dir: Path
    subtitle_dir: Path
    output_dir: Path
    add_audio: bool = True
    add_subtitles: bool = True
    bgm_path: Optional[Path] = None

    def __post_init__(self):
        self.video_dir = self.project_path / "video"
        self.audio_dir = self.project_path / "audio" / f"ep{self.episode:02d}"
        self.subtitle_dir = self.project_path / "subtitle"
        self.output_dir = self.project_path / "final"


def check_ffmpeg() -> bool:
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def concatenate_videos(video_files: list[Path], output_path: Path, logger: logging.Logger) -> bool:
    """Concatenate multiple video files using ffmpeg."""
    if not video_files:
        logger.error("No video files to concatenate")
        return False

    if len(video_files) == 1:
        shutil.copy(video_files[0], output_path)
        return True

    # Create concat list
    concat_list = output_path.parent / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for vf in video_files:
            f.write(f"file '{vf.absolute()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(output_path)
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True)
        concat_list.unlink()
        logger.info(f"Concatenated {len(video_files)} videos")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg concat failed: {e}")
        concat_list.unlink()
        return False


def add_audio_to_video(video_path: Path, audio_path: Path, output_path: Path, logger: logging.Logger) -> bool:
    """Mix audio into video."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path)
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True)
        logger.info(f"Added audio: {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Audio mix failed: {e}")
        return False


def burn_subtitles(video_path: Path, subtitle_path: Path, output_path: Path, logger: logging.Logger) -> bool:
    """Burn subtitles into video using ASS filter."""
    # Convert SRT to ASS for better styling
    ass_path = subtitle_path.with_suffix(".ass")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(subtitle_path), str(ass_path)],
            capture_output=True, check=True
        )
    except subprocess.CalledProcessError:
        ass_path = subtitle_path  # Fallback to SRT

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"ass={ass_path}",
        "-c:a", "copy",
        str(output_path)
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True)
        if ass_path != subtitle_path:
            ass_path.unlink()
        logger.info(f"Burned subtitles: {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Subtitle burn failed: {e}")
        return False


def process_episode(config: PostProcessConfig, logger: logging.Logger) -> bool:
    """Process a full episode."""
    config.output_dir.mkdir(exist_ok=True)

    # Find video files
    video_files = sorted(config.video_dir.glob(f"ep{config.episode:02d}-*.mp4"))
    if not video_files:
        logger.error(f"No video files found for episode {config.episode}")
        return False

    logger.info(f"Found {len(video_files)} video segments")

    # Step 1: Concatenate videos
    logger.info("\n[1/3] Concatenating video segments...")
    concat_path = config.output_dir / f"episode{config.episode:02d}_video_only.mp4"
    if not concatenate_videos(video_files, concat_path, logger):
        return False

    current_video = concat_path

    # Step 2: Add audio
    if config.add_audio:
        logger.info("\n[2/3] Adding audio...")
        audio_files = list(config.audio_dir.glob("*.mp3"))
        if audio_files:
            # Concatenate audio files first
            audio_concat = config.output_dir / f"episode{config.episode:02d}_audio.mp3"
            if len(audio_files) == 1:
                shutil.copy(audio_files[0], audio_concat)
            else:
                concat_list = config.output_dir / "audio_concat.txt"
                with open(concat_list, "w", encoding="utf-8") as f:
                    for af in sorted(audio_files):
                        f.write(f"file '{af.absolute()}'\n")
                try:
                    subprocess.run([
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(concat_list), "-c", "copy", str(audio_concat)
                    ], capture_output=True, check=True)
                    concat_list.unlink()
                except subprocess.CalledProcessError:
                    logger.warning("Audio concatenation failed, skipping audio")
                    audio_concat = None

            if audio_concat and audio_concat.exists():
                audio_output = config.output_dir / f"episode{config.episode:02d}_with_audio.mp4"
                if add_audio_to_video(current_video, audio_concat, audio_output, logger):
                    current_video = audio_output
        else:
            logger.warning("No audio files found, skipping audio")

    # Step 3: Burn subtitles
    if config.add_subtitles:
        logger.info("\n[3/3] Burning subtitles...")
        subtitle_path = config.subtitle_dir / f"episode{config.episode:02d}.srt"
        if subtitle_path.exists():
            final_output = config.output_dir / f"episode{config.episode:02d}.mp4"
            if burn_subtitles(current_video, subtitle_path, final_output, logger):
                current_video = final_output
        else:
            logger.warning("No subtitle file found, skipping subtitles")
            # Rename to final
            final_output = config.output_dir / f"episode{config.episode:02d}.mp4"
            shutil.move(current_video, final_output)
            current_video = final_output

    logger.info(f"\n{'=' * 50}")
    logger.info(f"Final output: {current_video}")
    logger.info(f"{'=' * 50}")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-process episode video")
    parser.add_argument("--project", "-p", type=str, required=True, help="Project directory")
    parser.add_argument("--episode", type=int, default=1, help="Episode number")
    parser.add_argument("--no-audio", action="store_true", help="Skip audio mixing")
    parser.add_argument("--no-subtitles", action="store_true", help="Skip subtitle burn")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logger = setup_logger("post_process", verbose=args.verbose)

    if not check_ffmpeg():
        logger.error("ffmpeg not found. Please install ffmpeg first.")
        logger.error("  macOS: brew install ffmpeg")
        logger.error("  Ubuntu: sudo apt install ffmpeg")
        logger.error("  Windows: choco install ffmpeg")
        return 1

    config = PostProcessConfig(
        project_path=Path(args.project),
        episode=args.episode,
        add_audio=not args.no_audio,
        add_subtitles=not args.no_subtitles,
    )

    success = process_episode(config, logger)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
