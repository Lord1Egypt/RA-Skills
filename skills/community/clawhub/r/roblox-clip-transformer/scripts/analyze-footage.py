#!/usr/bin/env python3
"""
Analyze Roblox gameplay footage for smart editing.

Detects:
- Action moments (movement, changes)
- Dead time (menus, loading screens, AFK)
- Audio peaks for caption timing

Usage:
    python analyze-footage.py input.mp4 --output analysis.json
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def get_video_info(video_path: str) -> dict:
    """Extract video metadata using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return json.loads(result.stdout)


def analyze_scene_changes(video_path: str, threshold: float = 0.3) -> list:
    """Detect scene changes using FFmpeg."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse showinfo output for timestamps
    changes = []
    for line in result.stderr.split('\n'):
        if 'pts_time:' in line:
            try:
                ts = float(line.split('pts_time:')[1].split()[0])
                changes.append(ts)
            except (IndexError, ValueError):
                continue
    return changes


def analyze_audio_levels(video_path: str) -> list:
    """Analyze audio levels for peak detection."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse audio level metadata
    levels = []
    for line in result.stderr.split('\n'):
        if 'lavfi.astats.Overall.RMS_level' in line:
            try:
                db = float(line.split('=')[1])
                levels.append(db)
            except (IndexError, ValueError):
                continue
    return levels


def detect_silence(video_path: str, noise_threshold: float = -50, duration: float = 1.0) -> list:
    """Detect silent/quiet segments (menus, loading screens)."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-af", f"silencedetect=noise={noise_threshold}dB:d={duration}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Parse silence detection output
    silent_regions = []
    current_start = None
    for line in result.stderr.split('\n'):
        if 'silence_start:' in line:
            try:
                current_start = float(line.split('silence_start:')[1].strip())
            except (IndexError, ValueError):
                pass
        elif 'silence_end:' in line and current_start is not None:
            try:
                end = float(line.split('silence_end:')[1].split('|')[0].strip())
                silent_regions.append((current_start, end))
                current_start = None
            except (IndexError, ValueError):
                pass
    
    return silent_regions


def analyze_footage(video_path: str, output_path: str, verbose: bool = False) -> dict:
    """Full analysis of footage."""
    print(f"Analyzing: {video_path}")
    
    # Get video info
    info = get_video_info(video_path)
    duration = float(info['format']['duration'])
    
    if verbose:
        print(f"  Duration: {duration:.2f}s")
        print(f"  Format: {info['format']['format_name']}")
    
    # Detect scene changes
    if verbose:
        print("  Detecting scene changes...")
    scene_changes = analyze_scene_changes(video_path)
    
    # Detect silent regions (potential dead time)
    if verbose:
        print("  Detecting silent regions...")
    silent_regions = detect_silence(video_path)
    
    # Analyze audio levels
    if verbose:
        print("  Analyzing audio levels...")
    audio_levels = analyze_audio_levels(video_path)
    
    # Calculate action moments (inverse of silence)
    action_moments = []
    prev_end = 0
    for start, end in silent_regions:
        if start > prev_end + 1:  # At least 1s of action
            action_moments.append({
                "start": prev_end,
                "end": start,
                "type": "action",
                "score": 1.0 - (end - start) / duration  # Higher score for longer action
            })
        prev_end = end
    
    # Add final action segment if any
    if prev_end < duration - 1:
        action_moments.append({
            "start": prev_end,
            "end": duration,
            "type": "action",
            "score": 0.5
        })
    
    # Build analysis result
    analysis = {
        "video_path": video_path,
        "duration": duration,
        "format": info['format']['format_name'],
        "scene_changes": scene_changes[:50],  # Limit to first 50
        "silent_regions": silent_regions,
        "action_moments": action_moments,
        "audio_peaks": len([l for l in audio_levels if l > -20]) if audio_levels else 0,
        "recommendations": generate_recommendations(duration, silent_regions, action_moments)
    }
    
    # Save to file
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    if verbose:
        print(f"  Found {len(scene_changes)} scene changes")
        print(f"  Found {len(silent_regions)} silent regions ({sum(e-s for s,e in silent_regions):.1f}s total)")
        print(f"  Found {len(action_moments)} action moments")
        print(f"  Analysis saved to: {output_path}")
    
    return analysis


def generate_recommendations(duration: float, silent_regions: list, action_moments: list) -> list:
    """Generate editing recommendations."""
    recommendations = []
    
    total_silence = sum(end - start for start, end in silent_regions)
    silence_ratio = total_silence / duration if duration > 0 else 0
    
    if silence_ratio > 0.4:
        recommendations.append({
            "type": "trim",
            "priority": "high",
            "message": f"Video has {silence_ratio*100:.0f}% silent/dead time. Consider aggressive trimming."
        })
    
    if len(action_moments) >= 3:
        recommendations.append({
            "type": "montage",
            "priority": "medium",
            "message": "Multiple action segments detected. Consider montage style."
        })
    
    if duration > 120:
        recommendations.append({
            "type": "duration",
            "priority": "high",
            "message": "Video exceeds 2 minutes. For TikTok/Shorts, focus on best 15-60 seconds."
        })
    
    # Find best action moment
    if action_moments:
        best = max(action_moments, key=lambda x: x['score'])
        recommendations.append({
            "type": "highlight",
            "priority": "high",
            "message": f"Best action segment: {best['start']:.0f}s - {best['end']:.0f}s"
        })
    
    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Analyze Roblox gameplay footage")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--output", "-o", default="analysis.json", help="Output analysis file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    try:
        analyze_footage(args.input, args.output, args.verbose)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()