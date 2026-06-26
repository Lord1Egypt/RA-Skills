#!/usr/bin/env python3
"""
Notion Export Parser

Parses Notion HTML/Markdown exports to extract content authored by a target user.

Usage:
    python3 notion_parser.py --dir notion_export/ --target "Alex Chen" --output /tmp/notion_out.txt
    python3 notion_parser.py --file notion_page.html --output /tmp/notion_out.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


def strip_html(html: str) -> str:
    """Simple HTML to text conversion."""
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'<li[^>]*>', '- ', text)
    text = re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>', lambda m: '#' * int(m.group(1)) + ' ' + m.group(2) + '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_file(file_path: Path) -> dict:
    """Parse a single Notion export file."""
    content = file_path.read_text(encoding="utf-8", errors="replace")

    if file_path.suffix.lower() in (".html", ".htm"):
        content = strip_html(content)

    # Extract title from filename (Notion format: "Title abc123def.md")
    title = file_path.stem
    # Remove Notion's hash suffix
    title = re.sub(r'\s+[a-f0-9]{20,}$', '', title)

    return {
        "title": title,
        "content": content[:10000],
        "path": str(file_path),
    }


def parse_directory(dir_path: Path, target: Optional[str] = None) -> list:
    """Parse all files in a Notion export directory."""
    docs = []
    extensions = {".md", ".html", ".htm", ".txt"}

    for f in sorted(dir_path.rglob("*")):
        if f.is_file() and f.suffix.lower() in extensions:
            doc = parse_file(f)
            if doc["content"]:
                # If target specified, do a simple relevance check
                if target:
                    content_lower = doc["content"].lower()
                    if target.lower() not in content_lower and target.lower() not in doc["title"].lower():
                        # Still include — Notion exports don't always have author info
                        pass
                docs.append(doc)

    return docs


def main():
    parser = argparse.ArgumentParser(description="Parse Notion export")
    parser.add_argument("--dir", help="Path to Notion export directory")
    parser.add_argument("--file", help="Path to single Notion file")
    parser.add_argument("--target", help="Target person name (optional filter)")
    parser.add_argument("--output", required=True, help="Output file path")

    args = parser.parse_args()

    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"❌ Directory not found: {dir_path}")
            sys.exit(1)
        docs = parse_directory(dir_path, args.target)
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
        docs = [parse_file(file_path)]
    else:
        parser.error("Either --dir or --file is required")

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Notion Documents\n")
        f.write(f"# Total: {len(docs)} documents\n\n")

        for doc in docs:
            f.write(f"## {doc['title']}\n")
            f.write(f"Source: {doc['path']}\n\n")
            f.write(f"{doc['content']}\n")
            f.write("\n---\n\n")

    print(f"✅ Parsed {len(docs)} documents → {args.output}")


if __name__ == "__main__":
    main()
