#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import re


def sanitize_path_segment(value: str) -> str:
    normalized = re.sub(r"\s+", "-", value.strip())
    normalized = re.sub(r'[\\/:*?"<>|#\[\]{}]+', "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-._ ")
    return normalized or "untitled"


def derive_title_from_content(content: str) -> str:
    for line in content.splitlines():
        candidate = line.strip()
        if candidate and not candidate.startswith("#"):
            return candidate[:80]
    return "未命名记录"


def render_frontmatter(data: dict[str, object]) -> str:
    lines: list[str] = ["---"]
    for key, value in data.items():
        if value in ("", None, [], {}):
            continue
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                escaped_item = str(item).replace("\"", "\\\"")
                lines.append(f'  - "{escaped_item}"')
            continue
        if isinstance(value, str):
            escaped = value.replace("\"", "\\\"")
            lines.append(f'{key}: "{escaped}"')
            continue
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 10_000):
        candidate = path.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Unable to allocate a unique path")


def append_journal_block(content: str, title: str, source_url: str, now: datetime) -> tuple[Path, str]:
    vault_root = Path(__file__).resolve().parents[4]
    year = now.strftime("%Y")
    month = now.strftime("%Y-%m")
    date_stamp = now.strftime("%Y-%m-%d")
    journal_path = vault_root / "Journal" / year / month / f"{date_stamp}.md"
    journal_path.parent.mkdir(parents=True, exist_ok=True)

    if not journal_path.exists():
        initial = render_frontmatter(
            {
                "entryType": "daily",
                "title": date_stamp,
                "date": date_stamp,
                "status": "active",
                "updatedAt": now.isoformat(),
            }
        )
        journal_path.write_text(initial, encoding="utf-8")

    block_title = title.strip() or now.strftime("%H:%M:%S")
    source_section = f"\n> 来源：{source_url}\n" if source_url.strip() else "\n"
    block = "\n".join(
        [
            "---",
            "",
            f"### {block_title}",
            "",
            content.strip(),
            source_section.rstrip(),
            "",
        ]
    )
    existing = journal_path.read_text(encoding="utf-8").rstrip()
    journal_path.write_text(f"{existing}\n\n{block.strip()}\n", encoding="utf-8")
    return journal_path, "journal"


def create_inbox_note(content: str, title: str, source_url: str, tags: list[str], now: datetime) -> tuple[Path, str]:
    vault_root = Path(__file__).resolve().parents[4]
    year = now.strftime("%Y")
    month = now.strftime("%Y-%m")
    date_stamp = now.strftime("%Y-%m-%d")
    clock_stamp = now.strftime("%H%M%S")
    note_title = title.strip() or derive_title_from_content(content)
    file_name = f"{date_stamp}--{clock_stamp}--{sanitize_path_segment(note_title)}.md"
    note_path = vault_root / "Inbox" / year / month / file_name
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path = ensure_unique_path(note_path)

    rendered = (
        render_frontmatter(
            {
                "title": note_title,
                "kind": "inbox",
                "status": "open",
                "tags": tags,
                "createdAt": now.isoformat(),
                "updatedAt": now.isoformat(),
                "sourceUrl": source_url.strip(),
            }
        )
        + content.strip()
        + "\n"
    )
    note_path.write_text(rendered, encoding="utf-8")
    return note_path, "inbox"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture notes into Elysia Inbox or Journal")
    parser.add_argument("destination", choices=["inbox", "journal"])
    parser.add_argument("--title", default="", help="Note title or Journal block title")
    parser.add_argument("--content", required=True, help="Note content")
    parser.add_argument("--source-url", default="", help="Optional source URL")
    parser.add_argument("--tags", default="", help="Comma-separated tags for Inbox notes")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    now = datetime.now().astimezone()
    tags = [item.strip() for item in re.split(r"[,，\n]+", args.tags) if item.strip()]

    if args.destination == "journal":
        path, destination = append_journal_block(args.content, args.title, args.source_url, now)
    else:
        path, destination = create_inbox_note(args.content, args.title, args.source_url, tags, now)

    print(
        json.dumps(
            {
                "ok": True,
                "destination": destination,
                "path": str(path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
