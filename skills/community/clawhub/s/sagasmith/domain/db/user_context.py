"""Managed USER.md fragments that follow campaign snapshots."""

from __future__ import annotations

import os
import re
from pathlib import Path


def _markers(campaign_id: str) -> tuple[str, str]:
    return (
        f"<!-- dnd-campaign:{campaign_id}:players:start -->",
        f"<!-- dnd-campaign:{campaign_id}:players:end -->",
    )


def read_player_roles(workspace: str | Path, campaign_id: str) -> str:
    path = Path(workspace).expanduser().resolve() / "USER.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    start, end = _markers(campaign_id)
    match = re.search(
        re.escape(start) + r"\s*\n?(.*?)\n?\s*" + re.escape(end),
        text,
        flags=re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def write_player_roles(workspace: str | Path, campaign_id: str, content: str) -> Path:
    root = Path(workspace).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    path = root / "USER.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# USER.md\n"
    start, end = _markers(campaign_id)
    block = f"{start}\n{content.strip()}\n{end}"
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end), flags=re.DOTALL
    )
    if pattern.search(text):
        updated = pattern.sub(block, text, count=1)
    else:
        updated = text.rstrip() + "\n\n" + block + "\n"
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(updated, encoding="utf-8")
    os.replace(tmp, path)
    return path
