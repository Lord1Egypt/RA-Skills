#!/usr/bin/env python3
"""
Confluence Export Parser

Parses Confluence HTML/XML exports to extract documentation content.

Usage:
    python3 confluence_parser.py --file confluence_export.zip --target "Alex Chen" --output /tmp/conf_out.txt
    python3 confluence_parser.py --dir confluence_html/ --output /tmp/conf_out.txt
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
import tempfile
from pathlib import Path
from typing import Optional


def strip_html(html: str) -> str:
    """Convert HTML to plain text."""
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'</tr>', '\n', text)
    text = re.sub(r'</td>', ' | ', text)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'<li[^>]*>', '- ', text)
    text = re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>', lambda m: '#' * int(m.group(1)) + ' ' + m.group(2) + '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_html_file(file_path: Path) -> dict:
    """Parse a single Confluence HTML file."""
    content = file_path.read_text(encoding="utf-8", errors="replace")

    # Extract title from <title> tag or filename
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else file_path.stem

    # Extract author if present
    author = ""
    author_match = re.search(r'class="author"[^>]*>(.*?)<', content)
    if author_match:
        author = strip_html(author_match.group(1))

    text = strip_html(content)

    return {
        "title": title,
        "author": author,
        "content": text[:10000],
        "path": str(file_path),
    }


def parse_export(export_path: str, target: Optional[str], output: str):
    """Parse a Confluence export."""
    path = Path(export_path)

    # Handle zip
    if path.suffix == ".zip":
        tmp_dir = tempfile.mkdtemp(prefix="confluence_export_")
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(tmp_dir)
        search_dir = Path(tmp_dir)
    elif path.is_dir():
        search_dir = path
    else:
        print(f"❌ Expected directory or zip file: {path}")
        sys.exit(1)

    # Find all HTML files
    docs = []
    for f in sorted(search_dir.rglob("*.html")):
        if f.name.startswith("."):
            continue
        doc = parse_html_file(f)
        if doc["content"] and len(doc["content"]) > 50:
            if target:
                # Include if target is author or mentioned in content
                if (target.lower() in doc.get("author", "").lower() or
                    target.lower() in doc["content"][:500].lower() or
                    not doc["author"]):  # Include docs without author info
                    docs.append(doc)
            else:
                docs.append(doc)

    # Write output
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Confluence Documents\n")
        f.write(f"# Total: {len(docs)} pages\n\n")

        for doc in docs:
            f.write(f"## {doc['title']}\n")
            if doc["author"]:
                f.write(f"Author: {doc['author']}\n")
            f.write(f"\n{doc['content']}\n")
            f.write("\n---\n\n")

    print(f"✅ Parsed {len(docs)} Confluence pages → {output}")


def main():
    parser = argparse.ArgumentParser(description="Parse Confluence export")
    parser.add_argument("--file", "--dir", dest="export_path", required=True)
    parser.add_argument("--target", help="Target author name")
    parser.add_argument("--output", required=True)

    args = parser.parse_args()
    parse_export(args.export_path, args.target, args.output)


if __name__ == "__main__":
    main()
