"""Verify that the rendered HTML preserves every visible character that was in the
original Markdown. Catches accidental drops introduced by an over-eager renderer.
"""

from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from typing import Iterable, List, Optional, Tuple

from .markdown_engine import is_table_separator


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_depth = 0
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag in {"script", "style"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.parts.append(data)

    def text(self) -> str:
        return normalize_text(" ".join(self.parts))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", html.unescape(text or ""))


def markdown_fragments(markdown_text: str) -> Iterable[str]:
    in_code = False
    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not line or is_table_separator(line):
            continue
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            for cell in cells:
                cleaned = clean_markdown_text(cell)
                if cleaned:
                    yield cleaned
            continue
        cleaned = clean_markdown_text(line)
        if cleaned:
            yield cleaned


def clean_markdown_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^#{1,6}\s+", "", cleaned)
    cleaned = re.sub(r"^>\s*", "", cleaned)
    cleaned = re.sub(r"^[-*]\s+", "", cleaned)
    cleaned = cleaned.strip("= ")
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = cleaned.replace("**", "").replace("*", "").replace("`", "")
    return normalize_text(cleaned)


def validate_text_preserved(markdown_text: str, html_text: str) -> None:
    parser = VisibleTextParser()
    parser.feed(html_text)
    visible = parser.text()
    missing: List[str] = []
    for fragment in markdown_fragments(markdown_text):
        if len(fragment) < 2:
            continue
        if fragment not in visible:
            missing.append(fragment)
        if len(missing) >= 10:
            break
    if missing:
        preview = "\n".join(f"- {item[:120]}" for item in missing)
        raise RuntimeError(f"HTML text preservation check failed; missing fragments:\n{preview}")
