"""videoarm-download: Download video from URL via yt-dlp."""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from videoarm_lib.config import VIDEO_DATABASE_FOLDER


def main():
    parser = argparse.ArgumentParser(description="Download video from URL")
    parser.add_argument("url", help="Video URL")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    dl_dir = Path(args.output_dir) if args.output_dir else VIDEO_DATABASE_FOLDER / "temp" / "downloads"
    dl_dir.mkdir(parents=True, exist_ok=True)

    url_hash = hashlib.md5(args.url.encode()).hexdigest()[:12]
    out = dl_dir / f"{url_hash}.mp4"

    if out.exists():
        json.dump({"path": str(out), "cached": True}, sys.stdout)
        print()
        return

    result = subprocess.run(
        ["yt-dlp", "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
         "--merge-output-format", "mp4", "-o", str(out), args.url],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr[:500]}", file=sys.stderr)
        sys.exit(1)

    json.dump({"path": str(out), "cached": False}, sys.stdout)
    print()


if __name__ == "__main__":
    main()
