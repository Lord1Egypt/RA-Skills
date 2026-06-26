#!/usr/bin/env python3
"""
Compress screenshot images (PNG/JPEG) in place using pngquant and jpegoptim.

Requires system tools: pngquant (for PNG), jpegoptim (for JPEG).
These must be installed separately — the script will check and exit with
clear instructions if they are missing.

Usage:
    python compress_screenshots.py image1.png image2.jpg
    python compress_screenshots.py /path/to/screenshots/
    python compress_screenshots.py /path/to/screenshots/ --recursive
    python compress_screenshots.py *.png --png-quality 90-100
    python compress_screenshots.py *.jpg --jpeg-quality 90
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def check_dependencies() -> list[str]:
    """Check if required system tools are installed. Return list of missing ones."""
    missing = []
    if not shutil.which("pngquant"):
        missing.append("pngquant")
    if not shutil.which("jpegoptim"):
        missing.append("jpegoptim")
    return missing


def compress_image(
    path: Path, png_quality: str = "80-95", jpeg_quality: int = 85
) -> dict | None:
    """Compress a single image file in place. Returns metadata dict or None if skipped."""
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return None

    old_size = path.stat().st_size

    if ext == ".png":
        subprocess.run(
            [
                "pngquant",
                f"--quality={png_quality}",
                "--force",
                "--ext",
                ".png",
                str(path),
            ],
            capture_output=True,
        )
    elif ext in (".jpg", ".jpeg"):
        subprocess.run(
            ["jpegoptim", f"--max={jpeg_quality}", "--strip-all", str(path)],
            capture_output=True,
        )

    new_size = path.stat().st_size
    return {
        "file": str(path),
        "name": path.name,
        "old_kb": old_size / 1024,
        "new_kb": new_size / 1024,
        "reduction_pct": 100 - new_size * 100 // old_size if old_size > 0 else 0,
    }


def collect_files(paths: list[str], recursive: bool = False) -> list[Path]:
    """Collect all supported image files from the given paths."""
    files = []
    for p_str in paths:
        p = Path(p_str)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(p)
        elif p.is_dir():
            pattern = "**/*" if recursive else "*"
            for f in p.glob(pattern):
                if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(f)
    return sorted(set(files))


def main():
    parser = argparse.ArgumentParser(
        description="Compress PNG/JPEG screenshots in place using pngquant and jpegoptim."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Image files or directories to compress",
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Recursively process directories",
    )
    parser.add_argument(
        "--png-quality",
        default="80-95",
        help="pngquant quality range (default: 80-95)",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=85,
        help="jpegoptim max quality (default: 85)",
    )

    args = parser.parse_args()

    # Check dependencies before doing anything
    missing = check_dependencies()
    if missing:
        print("Error: the following required tools are not installed:")
        for tool in missing:
            print(f"  - {tool}")
        print()
        print("Please install them before running this script:")
        print()
        print("  # macOS")
        print(f"  brew install {' '.join(missing)}")
        print()
        print("  # Ubuntu / Debian")
        print(f"  sudo apt install {' '.join(missing)}")
        print()
        print("  # CentOS / RHEL")
        print(f"  sudo yum install {' '.join(missing)}")
        sys.exit(1)

    files = collect_files(args.paths, recursive=args.recursive)
    if not files:
        print("No supported image files found (PNG/JPEG).")
        sys.exit(0)

    print(f"Compressing {len(files)} image(s)...")
    print(f"  PNG quality: {args.png_quality}  |  JPEG quality: {args.jpeg_quality}")
    print()

    results = []
    for f in files:
        result = compress_image(f, args.png_quality, args.jpeg_quality)
        if result:
            results.append(result)
            print(
                f"  {result['name']}: {result['old_kb']:.0f} KB -> "
                f"{result['new_kb']:.0f} KB ({result['reduction_pct']}% reduction)"
            )

    # Summary
    if results:
        total_old = sum(r["old_kb"] for r in results)
        total_new = sum(r["new_kb"] for r in results)
        total_saved = total_old - total_new
        total_pct = 100 - int(total_new * 100 / total_old) if total_old > 0 else 0
        print()
        print(f"Done! {len(results)} files compressed.")
        print(f"Total: {total_old:.0f} KB -> {total_new:.0f} KB "
              f"(saved {total_saved:.0f} KB, {total_pct}% reduction)")


if __name__ == "__main__":
    main()
