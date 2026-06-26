#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path


LIKELY_NAME_RE = re.compile(
    r"(tokenrouter|channel|provider|model|route|config)", re.IGNORECASE
)
LIKELY_CONTENT_RE = re.compile(
    r"(tokenrouter|channels|providers|models|routes|baseURL|baseurl|base_url|upstream|model_map|apiKey|api_key|api\.tokenrouter\.com|open\.palebluedot\.ai|kling|hailuo|MiniMax|kling-v2-6|kling-v3|seedance|dreamina-seedance)",
    re.IGNORECASE,
)
ALLOWED_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".js", ".ts", ".cjs", ".mjs"}
SKIP_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "coverage",
    ".turbo",
    ".cache",
    "vendor",
}


def candidate_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            path = base / filename
            if path.suffix.lower() not in ALLOWED_SUFFIXES:
                continue
            if LIKELY_NAME_RE.search(filename):
                yield path
                continue
            try:
                sample = path.read_text(encoding="utf-8", errors="ignore")[:4000]
            except OSError:
                continue
            if LIKELY_CONTENT_RE.search(sample):
                yield path


def score(path: Path) -> tuple[int, int, str]:
    name_score = 0
    text_score = 0
    try:
        sample = path.read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        sample = ""
    if "tokenrouter" in path.name.lower():
        name_score += 4
    if any(
        key in path.name.lower()
        for key in ["channel", "provider", "model", "route", "config"]
    ):
        name_score += 2
    for key in [
        "channels",
        "providers",
        "models",
        "routes",
        "upstream",
        "baseurl",
        "base_url",
        "baseURL",
        "api.tokenrouter.com",
        "open.palebluedot.ai",
    ]:
        if key in sample:
            text_score += 1
    return (-name_score, -text_score, str(path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Find likely tokenrouter config files")
    parser.add_argument("path", nargs="?", default=".", help="Workspace path to scan")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    matches = sorted(set(candidate_files(root)), key=score)

    if not matches:
        print("No likely tokenrouter config files found.")
        return

    print("Likely tokenrouter config files:")
    for match in matches:
        print(match)


if __name__ == "__main__":
    main()
