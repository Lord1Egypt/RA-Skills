#!/usr/bin/env python3
"""Download SVG icons from SVG Repo based on icons_index.json.

Usage:
    python3 download_icons.py [--icons-dir PATH]

Icons are saved to the same directory as icons_index.json by default.
Skips icons that already exist locally.
"""

import json
import os
import sys
import urllib.request
import urllib.error
import time
from pathlib import Path

SVGREPO_SEARCH = "https://www.svgrepo.com/vectors/{name}/"
ICONS_DIR = Path(__file__).parent.parent / "templates" / "icons"


def download_icon_from_svgrepo(name: str, dest: Path, retries: int = 2) -> bool:
    """Try to download an icon SVG from SVG Repo by searching for it."""
    url = f"https://www.svgrepo.com/download/{name}.svg"
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                dest.write_bytes(data)
                return True
        except (urllib.error.HTTPError, urllib.error.URLError, OSError):
            if attempt < retries:
                time.sleep(1)
    return False


def main():
    icons_dir = ICONS_DIR
    if "--icons-dir" in sys.argv:
        idx = sys.argv.index("--icons-dir")
        icons_dir = Path(sys.argv[idx + 1])

    index_file = icons_dir / "icons_index.json"
    if not index_file.exists():
        print(f"Error: {index_file} not found")
        sys.exit(1)

    with open(index_file) as f:
        index = json.load(f)

    icon_names = list(index.keys()) if isinstance(index, dict) else index
    total = len(icon_names)
    skipped = 0
    downloaded = 0
    failed = []

    print(f"Found {total} icons in index. Checking local files...")

    for i, name in enumerate(icon_names, 1):
        dest = icons_dir / f"{name}.svg"
        if dest.exists():
            skipped += 1
            continue

        print(f"  [{i}/{total}] Downloading {name}.svg ...", end=" ", flush=True)
        if download_icon_from_svgrepo(name, dest):
            downloaded += 1
            print("OK")
        else:
            failed.append(name)
            print("FAILED")

        # Rate limiting
        if downloaded % 10 == 0 and downloaded > 0:
            time.sleep(1)

    print(f"\nDone: {downloaded} downloaded, {skipped} already existed, {len(failed)} failed")
    if failed:
        print(f"Failed icons: {', '.join(failed[:20])}")
        if len(failed) > 20:
            print(f"  ... and {len(failed) - 20} more")


if __name__ == "__main__":
    main()
