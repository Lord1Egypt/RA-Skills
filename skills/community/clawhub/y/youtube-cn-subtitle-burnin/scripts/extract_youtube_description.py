#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def load_info(path_or_url: str) -> dict:
    path = Path(path_or_url)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    if shutil.which("yt-dlp") is None:
        raise SystemExit("yt-dlp is required when input is a URL")
    result = subprocess.run(
        ["yt-dlp", "--skip-download", "--dump-json", path_or_url],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract a YouTube video's metadata and description.")
    parser.add_argument("info_json_or_url", help="yt-dlp info JSON path or YouTube URL")
    parser.add_argument("--out", type=Path, required=True, help="Output Markdown file")
    args = parser.parse_args()

    info = load_info(args.info_json_or_url)
    title = info.get("title") or ""
    channel = info.get("channel") or info.get("uploader") or ""
    url = info.get("webpage_url") or info.get("original_url") or ""
    description = (info.get("description") or "").strip()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "\n".join(
            [
                f"# {title}",
                "",
                f"- URL: {url}",
                f"- Channel: {channel}",
                f"- Description language: {'Chinese or mixed Chinese' if contains_chinese(description) else 'non-Chinese or empty'}",
                "",
                "## Original Description",
                "",
                description,
                "",
            ]
        ),
        encoding="utf-8",
    )
    if description:
        print(f"PASS: wrote description to {args.out}")
        print("needs_translation:", "no" if contains_chinese(description) else "yes")
        return 0
    print(f"WARN: description is empty; wrote metadata to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
