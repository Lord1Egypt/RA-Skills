from __future__ import annotations

import re
import textwrap
from typing import Any

import markdown
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown

from .utils import decode_escaped_unicode, normalize_whitespace


def parse_frontmatter(md_text: str) -> tuple[dict[str, Any], str]:
    text = decode_escaped_unicode(md_text).lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                return frontmatter, parts[2].strip()
            except Exception:
                pass
    return {}, text


def extract_title_from_markdown(md_text: str) -> str:
    text = decode_escaped_unicode(md_text).lstrip("\ufeff")
    match = re.search(r"^#\s+(.+)$", text, re.M)
    if match:
        return normalize_whitespace(match.group(1))[:64]

    for line in text.splitlines():
        cleaned = re.sub(r"^#+\s*", "", line.strip())
        if cleaned:
            return normalize_whitespace(cleaned)[:64]
    return "未命名文章"


def first_markdown_image(md_text: str) -> str:
    match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", md_text)
    return match.group(1).strip() if match else ""


def markdown_to_html(text: str) -> str:
    return markdown.markdown(
        decode_escaped_unicode(text or ""),
        extensions=["extra", "tables", "nl2br", "codehilite", "sane_lists"],
        output_format="html",
    )


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html or "", "html.parser")
    value = soup.get_text("\n", strip=True)
    return re.sub(r"\n+", "\n", value)


def html_to_markdown_text(html: str) -> str:
    markdown_text = html_to_markdown(
        html or "",
        heading_style="ATX",
        bullets="-",
        wrap=False,
        strip=["script", "style"],
    )
    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)
    return markdown_text.strip()


def trim_digest(text: str, max_chars: int = 120) -> str:
    return normalize_whitespace(text)[:max_chars]


def normalize_code_blocks(soup: BeautifulSoup) -> None:
    for pre in soup.find_all("pre"):
        code = pre.find("code")
        target = code if code else pre
        content = target.get_text() if target else ""
        if not content:
            continue
        content = content.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
        lines = [line.replace("\u00a0", " ").replace("\u3000", " ").rstrip() for line in content.split("\n")]
        cleaned = textwrap.dedent("\n".join(lines).strip("\n"))
        target.clear()
        target.append(cleaned)
