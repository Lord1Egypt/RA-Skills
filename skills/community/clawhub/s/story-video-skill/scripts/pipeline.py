#!/usr/bin/env python3
"""
pipeline.py — 故事视频完整流水线
一键执行：故事→分镜→图片→视频→合并
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# Import individual step modules
try:
    import story_to_shots
    import generate_shot_images
    import generate_shot_videos
    import merge_videos
    IMPORTS_OK = True
except ImportError as e:
    IMPORTS_OK = False
    IMPORT_ERROR = str(e)


def run_step(name: str, fn, *args, **kwargs):
    """Run a pipeline step with timing and error handling."""
    print(f"\n{'=' * 60}")
    print(f"STEP: {name}")
    print(f"{'=' * 60}")
    start = time.time()
    try:
        result = fn(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[OK] {name} 完成 ({elapsed:.1f}s)")
        return result
    except Exception as e:
        elapsed = time.time() - start
        print(f"[FAIL] {name} 失败 ({elapsed:.1f}s): {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Story → Video 完整流水线")
    parser.add_argument("story", nargs="?", help="故事文本或 .txt 文件路径")
    parser.add_argument("-o", "--output-dir", default="./output", help="输出目录 (默认: ./output)")
    parser.add_argument("--shots", default=None, help="跳过故事→分镜，使用已有分镜JSON")
    parser.add_argument("--images", default=None, help="跳过图片生成，使用已有图片JSON")
    parser.add_argument("--provider", default="minimax", choices=["minimax", "doubao"], help="视频生成 provider (默认: minimax)")
    parser.add_argument("--duration", type=int, default=6, choices=[6, 10], help="视频时长 秒 (默认: 6)")
    parser.add_argument("--shots-count", type=int, default=None, help="强制分镜数量 (默认: 模型自动决定)")
    parser.add_argument("--skip-video", action="store_true", help="只生成到图片，跳过视频")
    args = parser.parse_args()

    # Check imports
    if not IMPORTS_OK:
        print(f"[ERROR] 无法导入子模块: {IMPORT_ERROR}")
        print("请确保所有脚本都在同一目录下")
        sys.exit(1)

    # Validate story input
    if not args.story and not args.shots:
        parser.print_help()
        print("\n[ERROR] 必须提供故事文本或 --shots 参数")
        sys.exit(1)

    # Setup output
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frames_dir = output_dir / "frames"
    videos_dir = output_dir / "videos"
    frames_dir.mkdir(exist_ok=True)
    videos_dir.mkdir(exist_ok=True)

    print(f"Story Video Pipeline")
    print(f"Output directory: {output_dir}")
    print(f"Provider: {args.provider}")
    print(f"Video duration: {args.duration}s")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ===== STEP 1: Story → Shots =====
    if args.shots:
        shots_path = args.shots
        print(f"[INFO] 使用已有分镜: {shots_path}")
    else:
        story_text = args.story
        # If story is a file path, read it
        story_path = Path(story_text)
        if story_path.exists() and story_path.is_file():
            story_text = story_path.read_text(encoding="utf-8")
            print(f"[INFO] 从文件读取故事: {story_path}")

        shots_path = str(output_dir / "shots.json")
        run_step("故事 → 分镜", story_to_shots.story_to_shots, story_text, "-o", shots_path)

    # ===== STEP 2: Shots → Images =====
    if args.images:
        images_path = args.images
        print(f"[INFO] 使用已有图片结果: {images_path}")
    else:
        images_path = str(output_dir / "shot_images.json")
        run_step("分镜 → 图片", generate_shot_images.generate_all_images,
                 shots_path, images_path)

    # ===== STEP 3: Images → Videos =====
    if not args.skip_video:
        videos_path = str(output_dir / "shot_videos.json")
        run_step("图片 → 视频", generate_shot_videos.generate_all_videos,
                 images_path, videos_path,
                 args.provider, args.duration)

    # ===== STEP 4: Merge =====
    if not args.skip_video:
        final_path = str(output_dir / "final_story.mp4")
        run_step("合并视频", merge_videos.merge_all_videos,
                 str(videos_dir), final_path)

        # Generate storyboard
        storyboard_path = output_dir / "storyboard.txt"
        run_step("生成故事板", merge_videos.generate_storyboard,
                 shots_path, images_path, str(storyboard_path))

    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")
    print(f"Output directory: {output_dir}")
    if not args.skip_video:
        print(f"Final video: {output_dir / 'final_story.mp4'}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
