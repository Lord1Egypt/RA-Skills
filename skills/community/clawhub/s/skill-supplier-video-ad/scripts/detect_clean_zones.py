#!/usr/bin/env python3
"""
detect_clean_zones.py — Step 1: Supplier Video Ad Builder
Extracts 1fps frames from source video so you can visually identify text-free zones.

Usage:
    python3 detect_clean_zones.py <video_path> [--output-dir ./frames]

Output:
    frames/<video_stem>/f_01.jpg, f_02.jpg, ...   (one frame per second)
    frames/<video_stem>/summary.txt               (frame list with timestamps)

After running: analyze frames with an image model or manually.
Text-free frames define clean_zones in your product config JSON.
"""

import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video', help='Path to source video')
    parser.add_argument('--output-dir', default='./frames', help='Output directory for frames')
    args = parser.parse_args()

    video = Path(args.video)
    out_dir = Path(args.output_dir) / video.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    # Get video duration
    r = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', str(video)],
        capture_output=True, text=True
    )
    duration = float(r.stdout.strip())
    n_frames = int(duration)

    print(f'📹 {video.name} — {duration:.1f}s → extracting {n_frames} frames at 1fps...')

    subprocess.run([
        'ffmpeg', '-y', '-i', str(video),
        '-vf', 'fps=1,scale=480:-1',
        str(out_dir / 'f_%02d.jpg'),
        '-loglevel', 'error'
    ], check=True)

    # Write summary
    summary_lines = [f'# Frame Summary — {video.name}', f'Duration: {duration:.1f}s', '']
    for i in range(1, n_frames + 1):
        summary_lines.append(f'f_{i:02d}.jpg  →  t={i}s  (ss={i-1} to {i})')

    summary = out_dir / 'summary.txt'
    summary.write_text('\n'.join(summary_lines))

    print(f'✅ {n_frames} frames → {out_dir}/')
    print(f'   Review: inspect each frame for baked-in supplier text/watermarks.')
    print(f'   Prompt for image model: "For each frame (f_01=t1s, ...), is there baked-in text? YES/NO"')
    print(f'   Text-free frames → use ss/dur values as clean_zones in your config.')


if __name__ == '__main__':
    main()
