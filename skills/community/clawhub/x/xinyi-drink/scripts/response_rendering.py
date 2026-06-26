#!/usr/bin/env python3
from __future__ import annotations

from typing import Any


def render_primary_response(title: str, lines: list[str]) -> str:
    parts = [title.strip()]
    parts.extend(line.strip() for line in lines if line and line.strip())
    return "\n".join(parts)


def escape_table_cell(value: Any) -> str:
    if value is None:
        return "-"

    if isinstance(value, bool):
        text = "是" if value else "否"
    elif isinstance(value, (list, tuple, set)):
        items = [escape_table_cell(item) for item in value]
        text = "、".join(item for item in items if item != "-")
    else:
        text = str(value).strip()

    if not text:
        return "-"

    return text.replace("|", "\\|").replace("\n", "<br>")


def render_markdown_table(
    title: str,
    headers: list[str],
    rows: list[list[Any]],
    empty_text: str,
) -> str:
    parts = [f"## {title}"]

    if not rows:
        parts.append(empty_text)
        return "\n".join(parts)

    parts.append(f"| {' | '.join(headers)} |")
    parts.append(f"| {' | '.join('---' for _ in headers)} |")

    for row in rows:
        parts.append(f"| {' | '.join(escape_table_cell(cell) for cell in row)} |")

    return "\n".join(parts)


def render_text_section(title: str, lines: list[str]) -> str:
    return render_primary_response(
        f"## {title}",
        lines,
    )
