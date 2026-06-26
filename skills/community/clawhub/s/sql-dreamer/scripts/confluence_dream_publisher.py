"""
scripts/confluence_dream_publisher.py — Post-dream Confluence wiki publisher

Runs AFTER post_dream_archiver.py (e.g., 4:30 AM).

What it does:
1. Reads wiki/main/syntheses/*.md from the OpenClaw wiki vault
2. Pushes each synthesis as a Confluence child page under Memory Palace parent
3. Creates page if it doesn't exist; updates if it does (keyed by title)

Requires confluence.enabled = true in config.yml.
Credentials via env: CONFLUENCE_API_TOKEN

Usage:
    python scripts/confluence_dream_publisher.py
    python scripts/confluence_dream_publisher.py --config /path/to/config.yml
    python scripts/confluence_dream_publisher.py --dry-run
"""

import sys
import os
import argparse
import re
import requests
from pathlib import Path
from base64 import b64encode

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def md_to_confluence_storage(md_content: str) -> str:
    """
    Minimal markdown → Confluence storage format conversion.
    Handles headings, paragraphs, code blocks, bullets.
    For production, use a proper converter library.
    """
    lines = []
    in_code = False
    lang = "none"

    for line in md_content.splitlines():
        if line.startswith("```"):
            if not in_code:
                lang = line[3:].strip() or "none"
                lines.append(f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{lang}</ac:parameter><ac:plain-text-body><![CDATA[')
                in_code = True
            else:
                lines.append("]]></ac:plain-text-body></ac:structured-macro>")
                in_code = False
        elif in_code:
            lines.append(line)
        elif re.match(r"^#{1,6} ", line):
            level = len(re.match(r"^(#+)", line).group(1))
            text = line.lstrip("#").strip()
            lines.append(f"<h{level}>{text}</h{level}>")
        elif line.startswith("- ") or line.startswith("* "):
            lines.append(f"<li>{line[2:].strip()}</li>")
        elif line.startswith("|"):
            # Skip markdown tables — complex to convert; just use pre
            lines.append(f"<p><code>{line}</code></p>")
        elif line.strip():
            lines.append(f"<p>{line}</p>")
        else:
            lines.append("")

    return "\n".join(lines)


class ConfluencePublisher:
    """Minimal Confluence REST API client for dream wiki publishing."""

    def __init__(self, domain: str, email: str, api_token: str):
        self.base_url = f"https://{domain}/wiki/rest/api"
        creds = b64encode(f"{email}:{api_token}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_page_by_title(self, space_key: str, title: str) -> dict | None:
        """Search for a page by title in a space. Returns page dict or None."""
        r = requests.get(
            f"{self.base_url}/content",
            headers=self.headers,
            params={"spaceKey": space_key, "title": title, "expand": "version"},
        )
        r.raise_for_status()
        results = r.json().get("results", [])
        return results[0] if results else None

    def create_page(self, space_key: str, parent_id: str, title: str, body: str) -> dict:
        """Create a new child page under parent_id."""
        payload = {
            "type": "page",
            "title": title,
            "ancestors": [{"id": parent_id}],
            "space": {"key": space_key},
            "body": {"storage": {"value": body, "representation": "storage"}},
        }
        r = requests.post(f"{self.base_url}/content", headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()

    def update_page(self, page_id: str, title: str, body: str, version: int) -> dict:
        """Update an existing page."""
        payload = {
            "type": "page",
            "title": title,
            "version": {"number": version + 1},
            "body": {"storage": {"value": body, "representation": "storage"}},
        }
        r = requests.put(f"{self.base_url}/content/{page_id}", headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()


def run(config_path: str, dry_run: bool = False) -> None:
    cfg = load_config(config_path)
    cf_cfg = cfg.get("confluence", {})

    if not cf_cfg.get("enabled", False):
        print("confluence_dream_publisher: Confluence disabled in config. Set confluence.enabled = true to activate.")
        return

    domain = cf_cfg.get("domain", "")
    email = cf_cfg.get("email", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", cf_cfg.get("api_token", ""))
    space_key = cf_cfg.get("space_key", "")
    parent_page_id = cf_cfg.get("parent_page_id", "")

    if not all([domain, email, api_token, space_key, parent_page_id]):
        print("❌ Missing Confluence config: domain, email, CONFLUENCE_API_TOKEN, space_key, parent_page_id all required")
        return

    workspace_dir = Path(cfg["dreaming"]["workspace_dir"])
    syntheses_dir = workspace_dir / ".." / ".." / ".openclaw" / "wiki" / "main" / "syntheses"
    syntheses_dir = syntheses_dir.resolve()

    if not syntheses_dir.exists():
        print(f"⚠️  Syntheses directory not found: {syntheses_dir}")
        return

    synthesis_files = [f for f in syntheses_dir.glob("*.md") if f.name != "index.md"]
    print(f"confluence_dream_publisher: Found {len(synthesis_files)} synthesis files")

    if not synthesis_files:
        print("  No synthesis files to publish")
        return

    if dry_run:
        for f in synthesis_files:
            print(f"  [dry-run] would publish: {f.name}")
        return

    publisher = ConfluencePublisher(domain, email, api_token)
    published = 0
    updated = 0

    for f in synthesis_files:
        content = f.read_text(encoding="utf-8")
        # Extract title from frontmatter or first heading
        title_match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", content, re.MULTILINE)
        h1_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        title = (title_match.group(1) if title_match else None) or (h1_match.group(1) if h1_match else f.stem)

        # Strip frontmatter before converting
        body_md = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL).strip()
        body_cf = md_to_confluence_storage(body_md)

        existing = publisher.get_page_by_title(space_key, title)
        if existing:
            version = existing["version"]["number"]
            publisher.update_page(existing["id"], title, body_cf, version)
            print(f"  ✏️  Updated: {title}")
            updated += 1
        else:
            publisher.create_page(space_key, parent_page_id, title, body_cf)
            print(f"  ✅ Created: {title}")
            published += 1

    print(f"\n✅ Confluence publish complete: {published} created, {updated} updated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post-dream Confluence wiki publisher")
    parser.add_argument("--config", default="config/config.yml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run(args.config, dry_run=args.dry_run)
