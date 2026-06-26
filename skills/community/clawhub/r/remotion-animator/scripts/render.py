#!/usr/bin/env python3
"""
render.py — Wrapper around `npx remotion render` with sensible defaults.

Usage:
    python render.py [composition-id] [--output out/video.mp4] [--codec h264] [--quality high]

Runs from the current working directory (your Remotion project).
"""

import argparse
import subprocess
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Render a Remotion video")
    parser.add_argument("composition", nargs="?", default="MyVideo", help="Composition ID")
    parser.add_argument("-o", "--output", default="out/video.mp4", help="Output path")
    parser.add_argument("--codec", default="h264", choices=["h264", "h265", "vp8", "vp9", "prores"])
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high", "ultra"])
    parser.add_argument("--concurrency", type=int, default=None, help="Parallel renders")
    parser.add_argument("--no-open", action="store_true", help="Don't open browser after render")
    args = parser.parse_args()

    crf_map = {"low": 30, "medium": 23, "high": 18, "ultra": 14}
    crf = crf_map[args.quality]

    # Ensure output dir exists
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts",
        args.composition,
        args.output,
        "--codec", args.codec,
        "--crf", str(crf),
    ]

    if args.concurrency:
        cmd += ["--concurrency", str(args.concurrency)]

    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
