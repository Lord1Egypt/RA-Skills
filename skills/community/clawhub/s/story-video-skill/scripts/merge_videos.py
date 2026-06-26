#!/usr/bin/env python3
"""
merge_videos.py
Merges all videos in ./output/videos/ into a single video using ffmpeg concat demuxer.
Also creates a text-based storyboard summary.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

# Output directories
OUTPUT_DIR = Path("./output")
VIDEOS_DIR = OUTPUT_DIR / "videos"
FRAMES_DIR = OUTPUT_DIR / "frames"

# Final output
FINAL_VIDEO = OUTPUT_DIR / "final_story.mp4"
STORYBOARD_FILE = OUTPUT_DIR / "storyboard.txt"
SRT_FILE = OUTPUT_DIR / "subtitles.srt"


def find_videos() -> List[Path]:
    """Find all video files in the videos directory."""
    if not VIDEOS_DIR.exists():
        return []
    
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'}
    videos = []
    
    for ext in video_extensions:
        videos.extend(VIDEOS_DIR.glob(f"*{ext}"))
    
    # Sort by name for consistent ordering
    videos.sort()
    return videos


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available."""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def install_ffmpeg() -> bool:
    """
    Attempt to install ffmpeg based on the detected OS.
    Returns True if installation appears successful.
    """
    import platform
    system = platform.system().lower()

    print("[INFO] FFmpeg not found. Attempting auto-install...")

    if system == "linux":
        # Try apt (Debian/Ubuntu/WSL)
        print("[INFO] Detected Linux — running: sudo apt-get update && sudo apt-get install -y ffmpeg")
        try:
            result = subprocess.run(
                ['sudo', 'apt-get', 'update'],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                print(f"[WARN] apt-get update failed: {result.stderr.strip()}")
            result = subprocess.run(
                ['sudo', 'apt-get', 'install', '-y', 'ffmpeg'],
                capture_output=True, text=True, timeout=180
            )
            if result.returncode == 0:
                print("[OK] FFmpeg installed via apt-get")
                return True
            print(f"[WARN] apt-get install ffmpeg failed: {result.stderr.strip()}")
        except subprocess.SubprocessError as e:
            print(f"[WARN] apt-get install failed: {e}")

    elif system == "darwin":
        # macOS — try brew
        print("[INFO] Detected macOS — running: brew install ffmpeg")
        try:
            result = subprocess.run(
                ['brew', 'install', 'ffmpeg'],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0:
                print("[OK] FFmpeg installed via Homebrew")
                return True
            print(f"[WARN] brew install ffmpeg failed: {result.stderr.strip()}")
        except subprocess.SubprocessError as e:
            print(f"[WARN] brew install failed: {e}")

    elif system == "windows":
        print("[WARN] Windows detected — please install FFmpeg manually:")
        print("  Option 1: winget install ffmpeg")
        print("  Option 2: Download from https://ffmpeg.org/download.html#build-windows")
        print("  Option 3: choco install ffmpeg (if Chocolatey is installed)")

    else:
        print(f"[WARN] Unknown OS ({system}) — cannot auto-install ffmpeg")
        print("  Please install ffmpeg manually: https://ffmpeg.org/download.html")

    return False


def get_video_duration(video_path: Path) -> Optional[float]:
    """Get video duration in seconds using ffprobe."""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except (subprocess.SubprocessError, ValueError):
        pass
    return None


def merge_videos_concat_demuxer(videos: List[Path], output_path: Path) -> bool:
    """
    Merge videos using ffmpeg concat demuxer.
    Creates a temporary file list and feeds it to ffmpeg.
    """
    if not videos:
        print("[ERROR] No videos to merge")
        return False
    
    # Create file list for concat demuxer
    list_file = OUTPUT_DIR / "concat_list.txt"
    
    with open(list_file, 'w', encoding='utf-8') as f:
        for video in videos:
            f.write(f"file '{video.absolute()}'\n")
    
    try:
        print(f"[...] Merging {len(videos)} videos...")
        
        # Use concat demuxer
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-f', 'concat',
            '-safe', '0',  # Allow unsafe file names
            '-i', str(list_file),
            '-c', 'copy',  # Copy streams without re-encoding
            '-bsf:a', 'aac_adtstoasc',  # Fix AAC audio
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        
        if result.returncode != 0:
            # Try with re-encoding if copy fails
            print(f"  Copy failed, trying with re-encoding...")
            cmd = [
                'ffmpeg',
                '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(list_file),
                '-c:v', 'libx264',
                '-crf', '23',
                '-preset', 'fast',
                '-c:a', 'aac',
                '-b:a', '128k',
                str(output_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
        
        if result.returncode == 0:
            print(f"[OK] Merged video saved to {output_path}")
            return True
        else:
            print(f"[ERROR] FFmpeg error:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[ERROR] FFmpeg timed out after 600s")
        return False
    except subprocess.SubprocessError as e:
        print(f"[ERROR] FFmpeg error: {e}")
        return False
    finally:
        # Clean up list file
        if list_file.exists():
            list_file.unlink()


def load_shots_and_images() -> tuple:
    """Load shots and image data if available."""
    shots_path = OUTPUT_DIR / "shots.json"
    images_path = OUTPUT_DIR / "shot_images.json"
    
    shots = []
    images = []
    
    if shots_path.exists():
        try:
            with open(shots_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                shots = data if isinstance(data, list) else data.get("shots", [])
        except Exception:
            pass
    
    if images_path.exists():
        try:
            with open(images_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                images = data if isinstance(data, list) else data.get("shots", [])
        except Exception:
            pass
    
    return shots, images


def build_shot_timeline(videos: List[Path], shots: List[Dict]) -> List[tuple]:
    """
    Build a timeline of (start_time, end_time, description) for each video.
    Uses ffprobe to get actual durations, accumulates time offsets.
    Returns list of (start_sec, end_sec, text) tuples.
    """
    timeline = []
    current_time = 0.0

    for i, video in enumerate(videos):
        shot_num = i + 1
        duration = get_video_duration(video) or 6.0  # fallback to 6s

        # Find matching shot description
        text = f"Shot {shot_num}"
        if shots:
            # Match by shot_number or by index
            matched = next(
                (s for s in shots if s.get("shot_number") == shot_num),
                shots[i] if i < len(shots) else None
            )
            if matched:
                text = matched.get("description", text)

        timeline.append((current_time, current_time + duration, text))
        current_time += duration

    return timeline


def format_timestamp(seconds: float) -> str:
    """Format seconds as SRT timestamp: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(timeline: List[tuple], output_path: Path) -> bool:
    """Generate SRT subtitle file from timeline data."""
    if not timeline:
        return False

    lines = []
    for i, (start, end, text) in enumerate(timeline, 1):
        lines.append(str(i))
        lines.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        lines.append(text)
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] SRT saved to {output_path}")
    return True


def burn_subtitles(input_video: Path, srt_path: Path, output_video: Path) -> bool:
    """
    Burn SRT subtitles into video using ffmpeg subtitles filter.
    """
    if not srt_path.exists():
        print("[WARN] SRT file not found, skipping subtitles")
        return False

    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_video),
        '-vf', f"subtitles={srt_path}",
        '-c:a', 'copy',
        str(output_video)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode == 0:
        print(f"[OK] Subtitles burned → {output_video}")
        return True
    else:
        print(f"[WARN] subtitles filter failed: {result.stderr.strip()[:200]}")
        return False


def create_storyboard_summary(
    videos: List[Path],
    shots: List[Dict],
    images: List[Dict]
) -> str:
    """Create text-based storyboard summary."""
    lines = []
    lines.append("=" * 70)
    lines.append("STORYBOARD SUMMARY")
    lines.append("=" * 70)
    lines.append("")
    
    # Build lookup maps
    shots_by_num = {shot.get("shot_number", i+1): shot for i, shot in enumerate(shots)}
    images_by_num = {img.get("shot_number", i+1): img for i, img in enumerate(images)}
    
    total_duration = 0
    
    for i, video in enumerate(videos):
        shot_num = i + 1
        
        lines.append(f"SHOT {shot_num}")
        lines.append("-" * 40)
        
        # Shot info
        shot = shots_by_num.get(shot_num, {})
        if shot:
            lines.append(f"Description: {shot.get('description', 'N/A')}")
            lines.append(f"Visual: {shot.get('visual_description', 'N/A')[:100]}...")
            lines.append(f"Duration: {shot.get('duration_suggestion', 'N/A')}s")
            lines.append(f"Camera: {shot.get('camera_movement', 'N/A')}")
        else:
            lines.append(f"Description: (no data)")
        
        # Video file info
        lines.append(f"Video: {video.name}")
        
        duration = get_video_duration(video)
        if duration:
            total_duration += duration
            lines.append(f"Actual Duration: {duration:.2f}s")
        
        # Image file
        image = images_by_num.get(shot_num, {})
        if image:
            local_path = image.get("local_path")
            if local_path:
                lines.append(f"Image: {Path(local_path).name}")
        
        lines.append("")
    
    lines.append("=" * 70)
    lines.append(f"TOTAL SHOTS: {len(videos)}")
    if total_duration > 0:
        lines.append(f"TOTAL DURATION: {total_duration:.2f}s ({total_duration/60:.1f} min)")
    lines.append(f"OUTPUT VIDEO: {FINAL_VIDEO.name}")
    lines.append("=" * 70)
    
    return "\n".join(lines)


def merge_videos(
    videos_dir: str = "./output/videos",
    output_path: str = "./output/final_story.mp4",
    create_summary: bool = True,
    subtitles: bool = False
) -> bool:
    """
    Merge all videos in directory into a single video.

    Args:
        videos_dir: Directory containing video files
        output_path: Path for merged output video
        create_summary: Whether to create storyboard summary
        subtitles: Whether to generate and burn SRT subtitles from shots.json descriptions

    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print("MERGE VIDEOS")
    print("=" * 60)

    # Check ffmpeg; auto-install if missing
    if not check_ffmpeg():
        print("[WARN] FFmpeg not found.")
        if not install_ffmpeg():
            print("[ERROR] FFmpeg installation failed or not supported on this OS.")
            print("  Please install ffmpeg manually and try again.")
            return False
        if not check_ffmpeg():
            print("[ERROR] FFmpeg still not found after installation attempt.")
            return False
    print("[OK] FFmpeg available")

    # Find videos
    global VIDEOS_DIR
    VIDEOS_DIR = Path(videos_dir)

    videos = find_videos()
    if not videos:
        print(f"[ERROR] No videos found in {VIDEOS_DIR}")
        print("  Expected files like: video_001.mp4, video_002.mp4, ...")
        return False

    print(f"[OK] Found {len(videos)} videos:")
    for v in videos:
        print(f"  - {v.name}")

    # Load metadata if available
    shots, images = load_shots_and_images()
    if shots:
        print(f"[OK] Loaded {len(shots)} shot descriptions")
    if images:
        print(f"[OK] Loaded {len(images)} image records")

    # Merge videos
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    success = merge_videos_concat_demuxer(videos, output_file)

    if not success:
        return False

    # Get final video info
    if output_file.exists():
        size = output_file.stat().st_size
        duration = get_video_duration(output_file)

        print(f"\n[OK] Final video created:")
        print(f"  Path: {output_file}")
        print(f"  Size: {size / (1024*1024):.2f} MB")
        if duration:
            print(f"  Duration: {duration:.2f}s ({duration/60:.1f} min)")

    # Generate and optionally burn subtitles
    if subtitles and shots:
        print("\n[...] Generating subtitles...")
        timeline = build_shot_timeline(videos, shots)
        if timeline:
            generate_srt(timeline, SRT_FILE)
            # Try to burn subtitles
            temp_output = output_file.parent / "final_with_subs.mp4"
            if burn_subtitles(output_file, SRT_FILE, temp_output):
                # Replace original with subtitled version
                temp_output.replace(output_file)
                print(f"[OK] Subtitles burned into final video")
            else:
                print(f"[WARN] Could not burn subtitles — ffmpeg may lack ASS support")

    # Create storyboard summary
    if create_summary:
        print("\n[...] Creating storyboard summary...")
        summary = create_storyboard_summary(videos, shots, images)

        summary_file = Path("./output/storyboard.txt")
        summary_file.write_text(summary, encoding='utf-8')
        print(f"[OK] Storyboard saved to: {summary_file}")

        print("\n" + summary)

    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Merge videos into single file")
    parser.add_argument("-i", "--input", default="./output/videos", help="Input videos directory")
    parser.add_argument("-o", "--output", default="./output/final_story.mp4", help="Output video path")
    parser.add_argument("--no-summary", action="store_true", help="Skip storyboard summary")
    parser.add_argument("--subtitles", action="store_true", help="Generate and burn SRT subtitles from shots.json")
    
    args = parser.parse_args()
    
    try:
        success = merge_videos(
            videos_dir=args.input,
            output_path=args.output,
            create_summary=not args.no_summary,
            subtitles=args.subtitles
        )
        if success:
            print("\nVideos merged successfully!")
        else:
            print("\nFailed to merge videos.")
            exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        exit(1)
