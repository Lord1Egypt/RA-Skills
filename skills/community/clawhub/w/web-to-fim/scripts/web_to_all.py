#!/usr/bin/env python3
"""
Web Content → Markdown → Obsidian/Feishu/IMA

Convert any web URL or local file to Markdown, then:
1. Save to Obsidian Vault (configurable via OBSIDIAN_VAULT_PATH)
2. Save to Feishu Cloud Document (optional)
3. Save to Tencent IMA Note (optional)

Usage:
  python3 web_to_all.py --url <url_or_path>
  python3 web_to_all.py --url <url_or_path> --title "Custom Title"
  python3 web_to_all.py --url <url_or_path> --no-feishu --no-ima
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from web_to_md import convert as convert_to_md
from feishu_client import FeishuClient
from ima_client import IMAClient


def get_obsidian_vault_path() -> Path:
    """
    Get Obsidian Vault path from environment variable or use default.
    
    Environment variable: OBSIDIAN_VAULT_PATH
    
    Defaults:
    - Windows: E:\Obsidian\md\inbox
    - macOS/Linux: ~/Obsidian/inbox
    """
    env_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_path:
        return Path(env_path).expanduser()
    
    # Default paths by OS
    if sys.platform.startswith("win"):
        return Path(r"E:\Obsidian\md\inbox")
    else:
        return Path.home() / "Obsidian" / "inbox"


OBSIDIAN_VAULT = get_obsidian_vault_path()


def save_to_obsidian(content: str, title: str, url: str = None) -> str:
    """Save Markdown to Obsidian Vault"""
    vault_path = Path(OBSIDIAN_VAULT)
    vault_path.mkdir(parents=True, exist_ok=True)

    safe_title = "".join(c if c.isalnum() or c in " -_()[]" else "_" for c in title)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_title[:50]}_{timestamp}.md"
    filepath = vault_path / filename

    frontmatter = []
    frontmatter.append("---")
    frontmatter.append(f"title: {title}")
    frontmatter.append(f"date: {datetime.now().isoformat()}")
    if url:
        frontmatter.append(f"source: {url}")
    frontmatter.append("---")
    frontmatter_str = "\n".join(frontmatter)

    full_content = f"{frontmatter_str}\n\n{content}"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"✅ Obsidian: {filepath}")
    return str(filepath)


def save_to_feishu(content: str, title: str) -> dict:
    """Save to Feishu Cloud Document"""
    try:
        client = FeishuClient()
        result = client.create_document(title=title, content_md=content)
        print(f"✅ Feishu: {result.get('url', 'N/A')}")
        return result
    except Exception as e:
        print(f"⚠️ Feishu failed: {e}", file=sys.stderr)
        return None


def save_to_ima(content: str, title: str) -> dict:
    """Save to Tencent IMA Note"""
    try:
        client = IMAClient()
        result = client.create_note(title=title, content=content)
        print(f"✅ IMA: {result.get('url', 'N/A')}")
        return result
    except Exception as e:
        print(f"⚠️ IMA failed: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Web Content → Markdown → Obsidian/Feishu/IMA"
    )
    parser.add_argument("--url", required=True, help="URL or local file path to convert")
    parser.add_argument("--title", help="Custom title for the document")
    parser.add_argument("--no-feishu", action="store_true", help="Skip Feishu")
    parser.add_argument("--no-ima", action="store_true", help="Skip IMA")
    parser.add_argument("--no-obsidian", action="store_true", help="Skip Obsidian")
    args = parser.parse_args()

    url = args.url

    print(f"🔍 Converting: {url}")
    try:
        markdown = convert_to_md(url)
    except Exception as e:
        print(f"❌ Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)

    title = args.title
    if not title:
        first_line = markdown.strip().split("\n", 1)[0]
        if first_line.startswith("# "):
            title = first_line[2:].strip()
        else:
            title = f"Untitled - {datetime.now().strftime('%Y-%m-%d')}"

    print(f"\n📄 Title: {title}")
    print(f"📝 Markdown length: {len(markdown)} chars\n")

    results = {}

    if not args.no_obsidian:
        results["obsidian"] = save_to_obsidian(markdown, title, url)

    if not args.no_feishu:
        results["feishu"] = save_to_feishu(markdown, title)

    if not args.no_ima:
        results["ima"] = save_to_ima(markdown, title)

    print(f"\n✅ Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
