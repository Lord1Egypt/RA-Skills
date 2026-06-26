#!/usr/bin/env python3
from __future__ import annotations
"""
Save any web page as an Obsidian Markdown clipping.

Usage:
  python3 save_web_page.py --url "https://www.v2ex.com/t/1197958"
  python3 save_web_page.py --url "https://..." --folder "clippings/tech"
  python3 save_web_page.py --url "https://..." --tags "ai,news"
  python3 save_web_page.py --url "https://..." --vault "/path/to/vault"
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests


# Only these keys are loaded from .env — no other secrets are touched
_ALLOWED_ENV_KEYS = {"JINA_API_KEY", "OPENCLAW_VAULT"}


def _load_env() -> None:
    """Load selected keys from ~/.openclaw/.env into os.environ.

    Only keys listed in _ALLOWED_ENV_KEYS are imported.
    All other secrets in .env are ignored.
    """
    env_path = Path.home() / ".openclaw" / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key in _ALLOWED_ENV_KEYS and key not in os.environ:
                os.environ[key] = value


_load_env()

# DEFAULT_VAULT can be overridden via OPENCLAW_VAULT env var
DEFAULT_VAULT = os.environ.get(
    "OPENCLAW_VAULT",
    os.path.expanduser("~/.openclaw/obsidian-cache")
)
DEFAULT_FOLDER = "clippings"



# --- Jina Reader API integration ---
def fetch_page(url: str) -> tuple[str, str]:
    """
    Fetch a remote web page using Jina Reader API and return (title, markdown_content).
    Works without an API key (free tier, lower rate limit).
    Set JINA_API_KEY in ~/.openclaw/.env for higher rate limits.
    Only accepts http:// and https:// URLs — local file paths are not supported.
    """
    # Security: only allow remote HTTP/HTTPS URLs
    if not url.startswith(("http://", "https://")):
        raise ValueError(
            f"Only http:// and https:// URLs are supported. "
            f"Local file paths are not allowed: {url!r}"
        )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # Add API key if available — gives higher rate limits but not required
    api_key = os.environ.get("JINA_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = requests.post("https://r.jina.ai/", headers=headers, json={"url": url}, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    content = data.get("data", {}).get("content")
    title = data.get("data", {}).get("title") or url
    if not content:
        raise RuntimeError(f"Jina Reader API returned no content for {url}")
    return title, content




def sanitize_filename(text: str, max_length: int = 80) -> str:
    text = re.sub(r"[^\w\s\-\(\)\[\]（）【】《》]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_length] if text else "untitled"


def save_clipping(url: str, vault: str, folder: str, tags: list[str]) -> str:
    title, content = fetch_page(url)

    folder_path = Path(vault) / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    safe_title = sanitize_filename(title)
    filename = f"{date_str} {safe_title}.md"
    filepath = folder_path / filename

    counter = 1
    while filepath.exists():
        filename = f"{date_str} {safe_title} ({counter}).md"
        filepath = folder_path / filename
        counter += 1

    tag_line = " ".join(f"#{t}" for t in tags) if tags else ""
    frontmatter = f"""---
title: "{title}"
source: "{url}"
saved: "{date_str} {time_str}"
tags: [{", ".join(tags)}]
---

"""

    note = frontmatter
    if tag_line:
        note += f"{tag_line}\n\n"
    note += f"# {title}\n\n"
    note += f"> Source: {url}\n> Saved: {date_str} {time_str}\n\n"
    note += "---\n\n"
    note += content

    filepath.write_text(note, encoding="utf-8")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Save web page as Obsidian clipping")
    parser.add_argument("--url", required=True, help="URL to save")
    parser.add_argument("--vault", default=DEFAULT_VAULT, help="Obsidian vault path")
    parser.add_argument("--folder", default=DEFAULT_FOLDER, help="Subfolder within vault")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    try:
        saved_path = save_clipping(args.url, args.vault, args.folder, tags)
        print(f"Saved: {saved_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
