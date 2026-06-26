#!/usr/bin/env python3
"""
visual_ref.py — Search and download reference images from Pexels.

Usage:
    python3 visual_ref.py "luxury real estate nordic" --count 5 --output /tmp/refs/
    python3 visual_ref.py "product photo minimalist" --count 3
"""

import argparse
import os
import sys
import json
import random
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")


def search_photos(query: str, count: int = 5, orientation: str = None) -> list[dict]:
    """Search photos on Pexels and return a list of results."""
    params = {
        "query": query,
        "per_page": count,
        "page": random.randint(1, 5),
    }
    if orientation:
        params["orientation"] = orientation  # landscape | portrait | square

    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "visual-ref-skill/2.0",
    })

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("photos", [])
    except urllib.error.HTTPError as e:
        print(f"Error: Pexels API returned {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)


def download_photo(photo: dict, output_dir: Path, index: int) -> tuple:
    """Download a photo at large resolution."""
    # Pexels provides multiple sizes: original, large2x, large, medium, small
    img_url = photo["src"]["large2x"]
    photo_id = photo["id"]
    photographer = photo["photographer"]
    ext = "jpg"
    filename = output_dir / f"ref_{index:02d}_{photo_id}.{ext}"

    req = urllib.request.Request(img_url, headers={"User-Agent": "visual-ref-skill/2.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        filename.write_bytes(resp.read())

    return filename, photographer


def main():
    parser = argparse.ArgumentParser(description="Download visual references from Pexels")
    parser.add_argument("query", help='Search query, e.g. "luxury real estate minimalist"')
    parser.add_argument("--count", type=int, default=5, help="Number of images (default: 5)")
    parser.add_argument("--output", default="/tmp/visual-refs", help="Output folder")
    parser.add_argument("--orientation", choices=["landscape", "portrait", "square"], help="Orientation (optional)")
    parser.add_argument("--list-only", action="store_true", help="List URLs only, no download")
    args = parser.parse_args()

    if not PEXELS_API_KEY:
        print("Error: PEXELS_API_KEY not found in environment.", file=sys.stderr)
        print("  Set it with: export PEXELS_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    # Clean previous references to avoid accumulation across searches
    if output_dir.exists():
        for old_file in output_dir.glob("ref_*"):
            old_file.unlink()
        meta = output_dir / "refs_meta.json"
        if meta.exists():
            meta.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f'Searching "{args.query}" on Pexels ({args.count} images)...')
    photos = search_photos(args.query, args.count, args.orientation)
    random.shuffle(photos)

    if not photos:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    results = []
    for i, photo in enumerate(photos, 1):
        desc = photo.get("alt", "") or "No description"
        photographer = photo["photographer"]

        if args.list_only:
            print(f"  [{i}] {desc[:60]} — {photographer}")
            print(f"       {photo['src']['large2x']}")
            results.append({"index": i, "description": desc, "photographer": photographer, "url": photo["src"]["large2x"]})
        else:
            print(f"  [{i}/{len(photos)}] Downloading: {desc[:50]}...")
            try:
                path, name = download_photo(photo, output_dir, i)
                print(f"       OK: {path.name}  (Photo by {photographer})")
                results.append({"index": i, "file": str(path), "description": desc, "photographer": photographer})
            except Exception as e:
                print(f"       Error: {e}")

    if not args.list_only:
        print(f"\n{len(results)} references saved to: {output_dir}")
        print("\nAttribution (Pexels license):")
        for r in results:
            print(f"   Photo by {r.get('photographer', '?')} on Pexels")

    # JSON output for programmatic use
    json_path = output_dir / "refs_meta.json"
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nMetadata: {json_path}")


if __name__ == "__main__":
    main()
