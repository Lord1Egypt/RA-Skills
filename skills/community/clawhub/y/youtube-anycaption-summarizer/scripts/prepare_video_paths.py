#!/usr/bin/env python3
import argparse
import json
import os
import re
import unicodedata
from pathlib import Path


def sanitize_title(title: str) -> str:
    text = unicodedata.normalize("NFKC", title).strip()
    text = re.sub(r"[^\w\-\s]+", "_", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._ ")
    return text[:120] or "youtube_video"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare safe folder/file paths for YouTube transcript workflow")
    parser.add_argument("--title", required=True)
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--parent", default=str(Path.home() / "Downloads"))
    parser.add_argument("--force-id-suffix", action="store_true")
    args = parser.parse_args()

    parent = Path(os.path.expanduser(args.parent)).resolve()
    safe = sanitize_title(args.title)
    folder_name = f"{safe}__{args.video_id}" if args.force_id_suffix else safe
    folder = parent / folder_name

    data = {
        "title": args.title,
        "safe_title": safe,
        "video_id": args.video_id,
        "parent_folder": str(parent),
        "folder": str(folder),
        "raw_transcript": str(folder / f"{safe}_transcript_raw.md"),
        "summary": str(folder / f"{safe}_Summary.md"),
        "wav": str(folder / f"{safe}.wav"),
        "media_prefix": str(folder / safe),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
