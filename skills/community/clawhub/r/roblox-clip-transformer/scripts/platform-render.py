#!/usr/bin/env python3
"""
Render platform-optimized video from analyzed footage.

Supports:
- Aspect ratio conversion (16:9 → 9:16)
- Smart trimming based on analysis
- Music sync
- Brand overlays

Usage:
    python platform-render.py input.mp4 --analysis analysis.json --platform tiktok --output output.mp4
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


# Platform specifications
PLATFORM_SPECS = {
    "tiktok": {
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 60,
        "fps": 30,
        "format": "mp4",
        "codec": "libx264",
        "audio_codec": "aac",
    },
    "shorts": {
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 60,
        "fps": 30,
        "format": "mp4",
        "codec": "libx264",
        "audio_codec": "aac",
    },
    "reels": {
        "aspect_ratio": "9:16",
        "width": 1080,
        "height": 1920,
        "max_duration": 90,
        "fps": 30,
        "format": "mp4",
        "codec": "libx264",
        "audio_codec": "aac",
    },
    "youtube": {
        "aspect_ratio": "16:9",
        "width": 1920,
        "height": 1080,
        "max_duration": None,  # No limit
        "fps": 30,
        "format": "mp4",
        "codec": "libx264",
        "audio_codec": "aac",
    },
}


def get_best_segments(analysis: dict, max_duration: float) -> list:
    """Extract best segments based on analysis."""
    if "action_moments" not in analysis:
        return [(0, min(max_duration, analysis.get("duration", 60)))]
    
    # Sort action moments by score
    moments = sorted(analysis["action_moments"], key=lambda x: x["score"], reverse=True)
    
    # Select segments until we reach max duration
    selected = []
    total = 0
    
    for moment in moments:
        start = moment["start"]
        end = moment["end"]
        duration = end - start
        
        if total + duration <= max_duration:
            selected.append((start, end))
            total += duration
        elif max_duration - total > 3:  # At least 3s
            # Trim to fit
            selected.append((start, start + (max_duration - total)))
            break
        else:
            break
    
    # Sort by time
    selected.sort(key=lambda x: x[0])
    
    return selected if selected else [(0, min(max_duration, analysis.get("duration", 60)))]


def detect_input_aspect(video_path: str) -> tuple:
    """Detect input video aspect ratio."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return (1920, 1080)  # Default
    
    try:
        width, height = map(int, result.stdout.strip().split(','))
        return (width, height)
    except ValueError:
        return (1920, 1080)


def build_filter_chain(input_width: int, input_height: int, 
                        output_width: int, output_height: int,
                        add_captions: bool = False,
                        logo_path: str = None) -> str:
    """Build FFmpeg filter chain for aspect ratio conversion."""
    filters = []
    
    input_aspect = input_width / input_height
    output_aspect = output_width / output_height
    
    if input_aspect > output_aspect:
        # Horizontal to vertical: crop and blur background
        # Scale input to fit height, then crop center
        scale_height = output_height
        scale_width = int(output_height * input_aspect)
        
        # Create blurred background
        filters.append(f"split[main][bg]")
        filters.append(f"[bg]scale={output_width}:{output_height}:force_original_aspect_ratio=decrease,boxblur=20:5[blurred]")
        filters.append(f"[main]scale={output_width}:{output_height}:force_original_aspect_ratio=decrease[cropped]")
        filters.append(f"[blurred][cropped]overlay=(W-w)/2:(H-h)/2")
        
    else:
        # Vertical to horizontal or same aspect: scale and pad
        filters.append(f"scale={output_width}:{output_height}:force_original_aspect_ratio=decrease")
        filters.append(f"pad={output_width}:{output_height}:(ow-iw)/2:(oh-ih)/2")
    
    # Add logo if provided
    if logo_path and Path(logo_path).exists():
        filters.append(f"overlay={output_width-150}:{output_height-150}")
    
    return ",".join(filters)


def render_video(input_path: str, output_path: str, platform: str,
                  analysis_path: str = None, 
                  start: float = None, end: float = None,
                  logo: str = None, music: str = None,
                  title: str = None, cta: str = None,
                  max_duration: float = None,
                  verbose: bool = False) -> bool:
    """Render platform-optimized video."""
    
    # Get platform spec
    if platform not in PLATFORM_SPECS:
        print(f"Error: Unknown platform '{platform}'. Supported: {list(PLATFORM_SPECS.keys())}")
        return False
    
    spec = PLATFORM_SPECS[platform]
    
    # Load analysis if provided
    analysis = None
    if analysis_path and Path(analysis_path).exists():
        with open(analysis_path) as f:
            analysis = json.load(f)
    
    # Detect input dimensions
    input_width, input_height = detect_input_aspect(input_path)
    
    if verbose:
        print(f"Input: {input_width}x{input_height}")
        print(f"Output: {spec['width']}x{spec['height']} ({spec['aspect_ratio']})")
    
    # Determine segments
    if start is not None and end is not None:
        segments = [(start, end)]
    elif analysis and spec["max_duration"]:
        segments = get_best_segments(analysis, spec["max_duration"])
    else:
        segments = None
    
    # Build FFmpeg command
    cmd = ["ffmpeg", "-y", "-i", input_path]
    
    # Add music if provided
    if music and Path(music).exists():
        cmd.extend(["-i", music])
        audio_filter = "amix=inputs=2:duration=first:dropout_transition=2"
    else:
        audio_filter = None
    
    # Build video filter
    vfilter = build_filter_chain(
        input_width, input_height,
        spec["width"], spec["height"],
        logo_path=logo
    )
    
    # Add title/CTA text if provided
    if title or cta:
        drawtext = []
        if title:
            drawtext.append(f"drawtext=text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h*0.1")
        if cta:
            drawtext.append(f"drawtext=text='{cta}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h*0.85")
        
        if drawtext:
            vfilter = f"{vfilter},{''.join(drawtext)}"
    
    # Apply video filter
    cmd.extend(["-vf", vfilter])
    
    # Apply audio filter
    if audio_filter:
        cmd.extend(["-af", audio_filter])
    
    # Output settings
    cmd.extend([
        "-c:v", spec["codec"],
        "-c:a", spec["audio_codec"],
        "-r", str(spec["fps"]),
        "-t", str(max_duration or spec["max_duration"] or 9999),
        output_path
    ])
    
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"FFmpeg error: {result.stderr}")
        return False
    
    if verbose:
        print(f"Output saved to: {output_path}")
    
    return True


def render_all_platforms(input_path: str, output_dir: str, 
                         analysis_path: str = None,
                         **kwargs) -> dict:
    """Render for all platforms."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = {}
    for platform in PLATFORM_SPECS:
        output_path = str(Path(output_dir) / f"{platform}.{PLATFORM_SPECS[platform]['format']}")
        success = render_video(
            input_path, output_path, platform,
            analysis_path=analysis_path,
            **kwargs
        )
        results[platform] = {
            "success": success,
            "path": output_path if success else None
        }
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Render platform-optimized Roblox video")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--output", "-o", default="output.mp4", help="Output video file")
    parser.add_argument("--platform", "-p", choices=list(PLATFORM_SPECS.keys()), 
                        default="tiktok", help="Target platform")
    parser.add_argument("--analysis", "-a", help="Analysis JSON from analyze-footage.py")
    parser.add_argument("--start", type=float, help="Start time (seconds)")
    parser.add_argument("--end", type=float, help="End time (seconds)")
    parser.add_argument("--logo", help="Logo overlay image (PNG)")
    parser.add_argument("--music", help="Background music file")
    parser.add_argument("--title", help="Title text overlay")
    parser.add_argument("--cta", help="Call-to-action text overlay")
    parser.add_argument("--max-duration", type=float, help="Maximum duration")
    parser.add_argument("--all", action="store_true", help="Render for all platforms")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if args.all:
        results = render_all_platforms(
            args.input, 
            Path(args.output).parent,
            analysis_path=args.analysis,
            logo=args.logo,
            music=args.music,
            title=args.title,
            cta=args.cta,
            max_duration=args.max_duration,
            verbose=args.verbose
        )
        
        print("\nRendered videos:")
        for platform, info in results.items():
            status = "✓" if info["success"] else "✗"
            print(f"  {status} {platform}: {info['path'] or 'failed'}")
        
        sys.exit(0 if all(r["success"] for r in results.values()) else 1)
    
    # Single platform render
    success = render_video(
        args.input, args.output, args.platform,
        analysis_path=args.analysis,
        start=args.start, end=args.end,
        logo=args.logo, music=args.music,
        title=args.title, cta=args.cta,
        max_duration=args.max_duration,
        verbose=args.verbose
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()