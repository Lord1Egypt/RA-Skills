#!/usr/bin/env python3
"""Extract transcript from YouMind getMaterial API response (stdin) and write to markdown file."""
import sys
import json
import re

d = json.loads(sys.stdin.read(), strict=False)
title = d.get("title", "Untitled")
t = d.get("transcript", {}) or {}
c = t.get("contents", [])
plain = c[0].get("plain", "") if c else ""
lang = c[0].get("language", "unknown") if c else "unknown"
words = len(plain.split())
board_id = (d.get("boardIds") or [""])[0]
material_id = d.get("id", "")
slug = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "-")[:60].rstrip("-").lower()
filename = f"transcript-{slug}.md" if slug else "transcript.md"
endpoint = "youmind.com"
link = f"https://{endpoint}/boards/{board_id}?material-id={material_id}&utm_source=youmind-youtube-transcript"
youtube_url = sys.argv[1] if len(sys.argv) > 1 else "<YOUTUBE_URL>"
md = f"# {title}\n\n- **Source**: {youtube_url}\n- **Language**: {lang}\n- **YouMind**: {link}\n\n---\n\n## Transcript\n\n{plain}\n"
with open(filename, "w") as f:
    f.write(md)
print(f"Title: {title}")
print(f"Language: {lang}")
print(f"Words: {words}")
print(f"File: {filename}")
print(f"YouMind: {link}")
