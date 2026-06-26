#!/usr/bin/env python3
"""
Convert a video file to multiple GIF variants with different quality/size tradeoffs.

Generates a matrix of GIFs varying FPS, width, and color count so the user can
visually pick the best one. Optionally trims a time range from the source video.

Prerequisites: FFmpeg, gifsicle (optional, for lossy compression variants)

Usage:
    python video_to_gif.py input.mp4
    python video_to_gif.py input.mp4 --start 5 --end 15
    python video_to_gif.py input.mp4 --width 640 --fps 15
    python video_to_gif.py input.mp4 --presets minimal
"""

import argparse
import itertools
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GifConfig:
    fps: int
    width: int
    colors: int
    lossy: int  # 0 = lossless, >0 = gifsicle lossy level
    dither: str  # FFmpeg dither algorithm

    @property
    def label(self) -> str:
        parts = [f"{self.width}w", f"{self.fps}fps", f"{self.colors}c"]
        if self.lossy > 0:
            parts.append(f"lossy{self.lossy}")
        if self.dither != "sierra2_4a":
            parts.append(self.dither)
        return "_".join(parts)


# Preset configurations targeting different tradeoff points
PRESETS = {
    "full": {
        "fps": [10, 15, 20],
        "width": [480, 640, 800],
        "colors": [128, 256],
        "lossy": [0],
        "dither": ["sierra2_4a"],
    },
    "minimal": {
        "fps": [10, 15],
        "width": [480, 640],
        "colors": [256],
        "lossy": [0],
        "dither": ["sierra2_4a"],
    },
    "lossy": {
        "fps": [12, 15],
        "width": [480, 640],
        "colors": [256],
        "lossy": [0, 30, 80],
        "dither": ["sierra2_4a"],
    },
    "quality": {
        "fps": [15, 20],
        "width": [640, 800, 1024],
        "colors": [256],
        "lossy": [0],
        "dither": ["sierra2_4a", "bayer:bayer_scale=3"],
    },
}


def get_video_info(input_file: str) -> dict:
    """Get video duration, width, height via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", "-select_streams", "v:0",
        input_file,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "duration": float(data["format"].get("duration", 0)),
    }


def generate_gif(
    input_file: str,
    output_file: str,
    config: GifConfig,
    start: float | None = None,
    end: float | None = None,
) -> dict:
    """Generate a single GIF with the given config. Returns metadata dict."""
    # Build time trim args
    time_args = []
    if start is not None:
        time_args += ["-ss", str(start)]
    if end is not None:
        if start is not None:
            time_args += ["-t", str(end - start)]
        else:
            time_args += ["-t", str(end)]

    # Two-pass palette-based GIF generation for best quality
    palette_file = output_file + ".palette.png"

    # Pass 1: generate palette
    palette_filter = (
        f"fps={config.fps},scale={config.width}:-1:flags=lanczos,"
        f"palettegen=max_colors={config.colors}:stats_mode=diff"
    )
    cmd_palette = (
        ["ffmpeg", "-y"] + time_args +
        ["-i", input_file, "-vf", palette_filter, palette_file]
    )
    subprocess.run(cmd_palette, capture_output=True, check=True)

    # Pass 2: apply palette
    gif_filter = (
        f"fps={config.fps},scale={config.width}:-1:flags=lanczos"
        f"[x];[x][1:v]paletteuse=dither={config.dither}"
    )
    cmd_gif = (
        ["ffmpeg", "-y"] + time_args +
        ["-i", input_file, "-i", palette_file,
         "-filter_complex", gif_filter, output_file]
    )
    subprocess.run(cmd_gif, capture_output=True, check=True)

    # Clean up palette
    os.remove(palette_file)

    # Optional lossy compression with gifsicle
    if config.lossy > 0 and shutil.which("gifsicle"):
        lossy_file = output_file + ".tmp.gif"
        cmd_lossy = [
            "gifsicle", "--optimize=3",
            f"--lossy={config.lossy}",
            output_file, "-o", lossy_file,
        ]
        subprocess.run(cmd_lossy, capture_output=True, check=True)
        os.replace(lossy_file, output_file)

    size_bytes = os.path.getsize(output_file)
    return {
        "file": output_file,
        "config": config.label,
        "fps": config.fps,
        "width": config.width,
        "colors": config.colors,
        "lossy": config.lossy,
        "size_kb": round(size_bytes / 1024, 1),
        "size_mb": round(size_bytes / (1024 * 1024), 2),
    }


def build_configs(preset_name: str) -> list[GifConfig]:
    """Build all GifConfig combinations from a preset."""
    preset = PRESETS[preset_name]
    configs = []
    for fps, width, colors, lossy, dither in itertools.product(
        preset["fps"], preset["width"], preset["colors"],
        preset["lossy"], preset["dither"],
    ):
        configs.append(GifConfig(fps=fps, width=width, colors=colors,
                                 lossy=lossy, dither=dither))
    return configs


def main():
    parser = argparse.ArgumentParser(
        description="Convert video to multiple GIF variants for visual comparison."
    )
    parser.add_argument("input", help="Input video file path")
    parser.add_argument("-o", "--output-dir",
                        help="Output directory (default: <input>_gifs/)")
    parser.add_argument("--start", type=float, default=None,
                        help="Start time in seconds")
    parser.add_argument("--end", type=float, default=None,
                        help="End time in seconds")
    parser.add_argument("--presets", default="full",
                        choices=list(PRESETS.keys()),
                        help="Preset config set (default: full)")
    # Allow overriding individual axes
    parser.add_argument("--fps", type=int, nargs="+",
                        help="Override FPS values (e.g., --fps 10 15 20)")
    parser.add_argument("--width", type=int, nargs="+",
                        help="Override width values (e.g., --width 480 640)")
    parser.add_argument("--colors", type=int, nargs="+",
                        help="Override color counts (e.g., --colors 128 256)")
    parser.add_argument("--lossy", type=int, nargs="+",
                        help="Gifsicle lossy levels (e.g., --lossy 0 30 80)")

    args = parser.parse_args()

    input_file = args.input
    if not os.path.isfile(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    # Get video info
    info = get_video_info(input_file)
    print(f"Source: {input_file}")
    print(f"  Resolution: {info['width']}x{info['height']}")
    print(f"  Duration: {info['duration']:.1f}s")
    if args.start is not None or args.end is not None:
        s = args.start or 0
        e = args.end or info["duration"]
        print(f"  Trimming: {s:.1f}s - {e:.1f}s ({e - s:.1f}s)")
    print()

    # Setup output dir
    if args.output_dir:
        out_dir = args.output_dir
    else:
        out_dir = str(Path(input_file).with_suffix("")) + "_gifs"
    os.makedirs(out_dir, exist_ok=True)

    # Build configs
    configs = build_configs(args.presets)

    # Apply overrides
    if args.fps or args.width or args.colors or args.lossy:
        preset = PRESETS[args.presets].copy()
        if args.fps:
            preset["fps"] = args.fps
        if args.width:
            preset["width"] = args.width
        if args.colors:
            preset["colors"] = args.colors
        if args.lossy:
            preset["lossy"] = args.lossy
        configs = []
        for fps, width, colors, lossy, dither in itertools.product(
            preset["fps"], preset["width"], preset["colors"],
            preset["lossy"], preset["dither"],
        ):
            # Skip widths larger than source
            if width > info["width"]:
                continue
            configs.append(GifConfig(fps=fps, width=width, colors=colors,
                                     lossy=lossy, dither=dither))
    else:
        # Filter out widths larger than source
        configs = [c for c in configs if c.width <= info["width"]]

    if not configs:
        print("Error: no valid configurations (all widths exceed source resolution)")
        sys.exit(1)

    print(f"Generating {len(configs)} GIF variants (preset: {args.presets})...")
    print(f"Output directory: {out_dir}")
    print()

    # Check for gifsicle if lossy configs exist
    has_gifsicle = shutil.which("gifsicle") is not None
    lossy_configs = [c for c in configs if c.lossy > 0]
    if lossy_configs and not has_gifsicle:
        print("Warning: gifsicle not found, skipping lossy compression variants")
        configs = [c for c in configs if c.lossy == 0]

    results = []
    for i, config in enumerate(configs, 1):
        output_file = os.path.join(out_dir, f"{config.label}.gif")
        print(f"  [{i}/{len(configs)}] {config.label}...", end=" ", flush=True)
        try:
            meta = generate_gif(input_file, output_file, config,
                                start=args.start, end=args.end)
            results.append(meta)
            print(f"{meta['size_kb']:.0f} KB ({meta['size_mb']:.2f} MB)")
        except subprocess.CalledProcessError as e:
            print(f"FAILED: {e}")

    # Summary table sorted by file size
    print()
    print("=" * 72)
    print("RESULTS (sorted by file size, smallest first)")
    print("=" * 72)
    results.sort(key=lambda r: r["size_kb"])

    print(f"{'File':<40} {'Size':>10} {'FPS':>5} {'Width':>6} {'Colors':>7}")
    print("-" * 72)
    for r in results:
        fname = os.path.basename(r["file"])
        if r["size_kb"] >= 1024:
            size_str = f"{r['size_mb']:.1f} MB"
        else:
            size_str = f"{r['size_kb']:.0f} KB"
        lossy_str = f" L{r['lossy']}" if r["lossy"] > 0 else ""
        print(f"{fname:<40} {size_str:>10} {r['fps']:>5} {r['width']:>6} "
              f"{r['colors']:>5}{lossy_str}")

    print()
    print(f"Total: {len(results)} GIFs in {out_dir}/")
    smallest = results[0]
    largest = results[-1]
    print(f"Smallest: {os.path.basename(smallest['file'])} "
          f"({smallest['size_kb']:.0f} KB)")
    print(f"Largest:  {os.path.basename(largest['file'])} "
          f"({largest['size_kb']:.0f} KB)")
    print()
    print("Pick the one that balances size and visual quality for your use case.")


if __name__ == "__main__":
    main()
