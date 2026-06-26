#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Download a YouTube video's thumbnail into 01-source.")
    parser.add_argument("url")
    parser.add_argument("--out-dir", type=Path, default=Path("01-source"))
    parser.add_argument("--format", default="jpg", choices=("jpg", "png", "webp"), help="Converted thumbnail format")
    args = parser.parse_args()

    if shutil.which("yt-dlp") is None:
        print("FAIL: yt-dlp is required")
        return 1
    args.out_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(args.out_dir / "%(id)s.thumbnail.%(ext)s")
    command = [
        "yt-dlp",
        "--skip-download",
        "--write-thumbnail",
        "--convert-thumbnails",
        args.format,
        "-o",
        output_template,
        args.url,
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        print("FAIL: thumbnail download failed")
        return result.returncode
    print(result.stdout, end="")
    thumbnails = sorted(args.out_dir.glob(f"*.thumbnail.{args.format}"))
    if not thumbnails:
        print(f"FAIL: no .thumbnail.{args.format} file found in {args.out_dir}")
        return 1
    print(f"PASS: downloaded thumbnail {thumbnails[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
