#!/usr/bin/env python3
"""
url2md - Convert web pages to Markdown.

Author:
- rwonly@gmail.com

Supports:
- Single URL to Markdown conversion
- Batch conversion from a file containing URLs
- Custom output path or stdout
"""

from __future__ import annotations

__version__ = "2.1.2"

import sys
import os
import argparse
import html
import json
import hashlib
import mimetypes
from typing import Optional
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
from html.entities import name2codepoint
from datetime import datetime
import re


def _strip_boilerplate_tags(html: str) -> str:
    """Remove script/style/noscript/template blocks before parsing."""
    for tag in ("script", "style", "noscript", "template"):
        html = re.sub(
            rf"<{tag}\b[^>]*>[\s\S]*?</{tag}\s*>",
            "",
            html,
            flags=re.IGNORECASE,
        )
    return html


def _extract_by_tag(html: str, tag: str) -> Optional[str]:
    """Return inner HTML of the first balanced <tag>...</tag> block, or None."""
    open_re = re.compile(rf"<\s*{tag}\b[^>]*>", re.IGNORECASE)
    close_re = re.compile(rf"<\s*/\s*{tag}\s*>", re.IGNORECASE)
    m = open_re.search(html)
    if not m:
        return None
    depth = 1
    pos = m.end()
    outer_start = m.end()
    while depth > 0 and pos < len(html):
        mo = open_re.search(html, pos)
        mc = close_re.search(html, pos)
        if not mc:
            return None
        if mo and mo.start() < mc.start():
            depth += 1
            pos = mo.end()
        else:
            depth -= 1
            if depth == 0:
                return html[outer_start : mc.start()]
            pos = mc.end()
    return None


def _extract_body(html: str) -> Optional[str]:
    m = re.search(r"<body\b[^>]*>", html, re.IGNORECASE)
    if not m:
        return None
    start = m.end()
    m2 = re.search(r"</body\s*>", html[start:], re.IGNORECASE)
    if not m2:
        return html[start:]
    return html[start : start + m2.start()]


def _is_md_pipe_table_row(line: str) -> bool:
    """True if line looks like a GFM pipe table row (not HTML <table>)."""
    s = line.strip()
    if len(s) < 3:
        return False
    if not (s.startswith("|") and s.endswith("|")):
        return False
    # Need at least one interior cell boundary
    return s.count("|") >= 2


def _collapse_blank_lines_between_pipe_tables(md: str) -> str:
    """
    Many CMS pages put each markdown table row inside its own <p>, which produces
    blank lines between | ... | rows and breaks GFM table rendering. Remove those
    gaps while leaving code fences untouched.
    """
    lines = md.splitlines()
    n = len(lines)
    out: list[str] = []
    i = 0
    in_fence = False
    while i < n:
        line = lines[i]
        st = line.strip()
        if st.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue
        if _is_md_pipe_table_row(line):
            # Only collapse blank lines between consecutive table rows,
            # not before the first table row (GFM needs a blank line above)
            if out and _is_md_pipe_table_row(out[-1]):
                while out and out[-1] == "":
                    out.pop()
            out.append(line)
            i += 1
            while i < n:
                ln = lines[i]
                lst = ln.strip()
                if lst.startswith("```"):
                    break
                if _is_md_pipe_table_row(ln):
                    out.append(ln)
                    i += 1
                elif lst == "":
                    j = i + 1
                    while j < n and lines[j].strip() == "":
                        j += 1
                    if j < n and _is_md_pipe_table_row(lines[j]):
                        i = j
                    else:
                        break
                else:
                    break
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def _collapse_excess_blank_lines(md: str, max_consecutive_blank_lines: int = 1) -> str:
    """
    Collapse runs of empty lines (including whitespace-only) outside fenced code
    blocks so the file does not contain large vertical gaps.
    """
    lines = md.splitlines()
    out: list[str] = []
    in_fence = False
    blank_run = 0
    for line in lines:
        st = line.strip()
        if st.startswith("```"):
            in_fence = not in_fence
            blank_run = 0
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if st == "":
            blank_run += 1
            if blank_run <= max_consecutive_blank_lines:
                out.append("")
        else:
            blank_run = 0
            out.append(line)
    return "\n".join(out)


# Lines that are only a Markdown list marker (no item text), e.g. "-" or "12."
_EMPTY_MD_LIST_LINE = re.compile(
    r"^\s*(?:[-*+]|(?:\d{1,9}\.))\s*$",
)


def _strip_empty_markdown_list_lines(md: str) -> str:
    """
    Remove lines that are only a list marker (from empty <li> or layout quirks).
    Skips fenced code blocks.
    """
    lines = md.splitlines()
    out: list[str] = []
    in_fence = False
    for line in lines:
        st = line.strip()
        if st.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if _EMPTY_MD_LIST_LINE.match(line):
            continue
        out.append(line)
    return "\n".join(out)


def prepare_html_document(html: str, full_page: bool = False) -> str:
    """
    Strip noisy tags, then prefer article/main/body so output matches
    reader-style tools that focus on primary content.
    """
    html = _strip_boilerplate_tags(html)
    if full_page:
        return _extract_body(html) or html
    frag = _extract_by_tag(html, "article") or _extract_by_tag(html, "main")
    if frag:
        return frag
    return _extract_body(html) or html


def _unescape_meta(val: str) -> str:
    """Clean a meta tag value."""
    t = html.unescape(val.strip())
    t = re.sub(r"\s+", " ", t)
    return t


def _extract_meta(raw_html: str, patterns: list[str]) -> str:
    """Try multiple regex patterns to extract a meta value."""
    for pat in patterns:
        m = re.search(pat, raw_html, re.IGNORECASE | re.DOTALL)
        if m:
            val = _unescape_meta(m.group(1))
            if val:
                return val
    return ""


def extract_metadata(raw_html: str, url: str) -> dict[str, str]:
    """Extract structured metadata from raw HTML."""
    metadata: dict[str, str] = {
        "title": "",
        "author": "",
        "published": "",
        "description": "",
        "source": url,
        "site_name": "",
    }

    # title
    title_patterns = [
        r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']og:title["\']',
        r'<meta[^>]+name=["\']twitter:title["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']twitter:title["\']',
    ]
    metadata["title"] = _extract_meta(raw_html, title_patterns)
    if not metadata["title"]:
        m = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.DOTALL | re.IGNORECASE)
        if m:
            t = _unescape_meta(m.group(1))
            if t:
                metadata["title"] = t

    # description
    desc_patterns = [
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']og:description["\']',
        r'<meta[^>]+name=["\']twitter:description["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']twitter:description["\']',
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']',
    ]
    metadata["description"] = _extract_meta(raw_html, desc_patterns)

    # author
    author_patterns = [
        r'<meta[^>]+name=["\']author["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']author["\']',
    ]
    metadata["author"] = _extract_meta(raw_html, author_patterns)

    # published
    pub_patterns = [
        r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']article:published_time["\']',
        r'<meta[^>]+name=["\']publishedDate["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']publishedDate["\']',
    ]
    metadata["published"] = _extract_meta(raw_html, pub_patterns)

    # site_name
    site_patterns = [
        r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+property=["\']og:site_name["\']',
    ]
    metadata["site_name"] = _extract_meta(raw_html, site_patterns)

    # Schema.org JSON-LD
    _extract_schema_org(raw_html, metadata)

    # tags: heading extraction only if Schema.org did not provide keywords
    if not metadata.get("tags"):
        metadata["tags"] = ", ".join(_extract_tags(raw_html, metadata.get("title", "")))

    return metadata


def _extract_schema_org(raw_html: str, metadata: dict[str, str]) -> None:
    """Extract metadata from Schema.org JSON-LD scripts."""
    try:
        candidates: list[dict] = []
        for m in re.finditer(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            raw_html,
            re.IGNORECASE | re.DOTALL,
        ):
            data = json.loads(m.group(1).strip())
            if not isinstance(data, dict):
                continue
            if "@graph" in data and isinstance(data["@graph"], list):
                for item in data["@graph"]:
                    if isinstance(item, dict):
                        candidates.append(item)
            else:
                candidates.append(data)

        if not candidates:
            return

        # Prefer Article / NewsArticle / BlogPosting over generic WebPage
        def _type_priority(item: dict) -> int:
            t = item.get("@type", "")
            if isinstance(t, list):
                t = " ".join(str(x) for x in t)
            t = str(t).lower()
            if "newsarticle" in t:
                return 0
            if "blogposting" in t:
                return 1
            if "article" in t:
                return 2
            if "techarticle" in t:
                return 3
            if "webpage" in t:
                return 4
            return 5

        candidates.sort(key=_type_priority)

        for item in candidates:
            _apply_schema_org_item(item, metadata)
            if all(metadata.get(k) for k in ("title", "author", "published", "description")):
                break
    except Exception:
        pass


def _schema_text(val) -> str:
    """Extract a plain string from a Schema.org value."""
    if isinstance(val, str) and val:
        return val
    if isinstance(val, dict):
        return val.get("name", "") or val.get("@id", "")
    if isinstance(val, list) and val:
        first = val[0]
        if isinstance(first, dict):
            return first.get("name", "")
        if isinstance(first, str):
            return first
    return ""


def _schema_author(val) -> str:
    """Extract author name(s) from Schema.org Person / Organization."""
    if isinstance(val, str) and val:
        return val
    if isinstance(val, dict):
        return val.get("name", "")
    if isinstance(val, list) and val:
        names = []
        for a in val:
            if isinstance(a, dict):
                n = a.get("name", "")
                if n:
                    names.append(n)
            elif isinstance(a, str) and a:
                names.append(a)
        return ", ".join(names)
    return ""


def _schema_publisher(val) -> str:
    """Extract publisher name from Schema.org Organization."""
    if isinstance(val, str) and val:
        return val
    if isinstance(val, dict):
        return val.get("name", "") or val.get("alternateName", "")
    return ""


def _apply_schema_org_item(item: dict, metadata: dict[str, str]) -> None:
    """Apply a single Schema.org object to the metadata dict."""
    if not metadata.get("title"):
        metadata["title"] = _schema_text(item.get("headline")) or _schema_text(item.get("name"))

    if not metadata.get("description"):
        metadata["description"] = _schema_text(item.get("description"))

    if not metadata.get("author"):
        metadata["author"] = _schema_author(item.get("author"))

    if not metadata.get("published"):
        metadata["published"] = _schema_text(item.get("datePublished"))
    if not metadata.get("published"):
        metadata["published"] = _schema_text(item.get("dateCreated"))

    if not metadata.get("site_name"):
        metadata["site_name"] = _schema_publisher(item.get("publisher"))

    if not metadata.get("tags"):
        kw = item.get("keywords")
        if isinstance(kw, str) and kw:
            metadata["tags"] = kw
        elif isinstance(kw, list):
            metadata["tags"] = ", ".join(str(k) for k in kw if k)

    if not metadata.get("category"):
        section = item.get("articleSection")
        if isinstance(section, str) and section:
            metadata["category"] = section
        elif isinstance(section, list):
            metadata["category"] = ", ".join(str(s) for s in section if s)


# Common English stopwords
_EN_STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "can", "this", "that", "these", "those", "with", "by", "from", "as", "it",
    "its", "into", "out", "up", "down", "over", "under", "again", "further",
    "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "also", "new", "old", "first", "last", "long", "great", "little",
    "series", "detailed", "explanation", "guide", "introduction", "overview",
}

def _extract_headings(raw_html: str) -> list[str]:
    """Extract inner text from h2/h3 tags."""
    headings: list[str] = []
    for level in (2, 3):
        pattern = rf"<h{level}\b[^>]*>(.*?)</h{level}\s*>"
        for m in re.finditer(pattern, raw_html, re.IGNORECASE | re.DOTALL):
            text = re.sub(r"<[^>]+>", "", m.group(1))
            text = html.unescape(text).strip()
            if text:
                headings.append(text)
    return headings


def _extract_tokens(text: str) -> list[str]:
    """Extract English candidate tag tokens from a piece of text."""
    if not text:
        return []

    # Clean: remove parenthetical/bracket content and separators
    clean = re.sub(r"[（(][^）)]+[）)]", "", text)
    clean = re.sub(r"[【\[][^】\]]+[】\]]", "", clean)
    clean = re.sub(r"[:：|·\-\-\—]+", " ", clean)

    tokens: list[str] = []
    for word in re.findall(r"[a-zA-Z][a-zA-Z0-9]+", clean):
        if len(word) >= 2 and word.lower() not in _EN_STOPWORDS:
            tokens.append(word)
    return tokens


def _singular_form(word: str) -> str:
    """Simple heuristic to map a plural English word to its singular form."""
    w = word.lower()
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("es") and len(w) > 3:
        return w[:-2]
    if w.endswith("s") and len(w) > 2:
        return w[:-1]
    return w


def _merge_plural_forms(token_sources: dict[str, int], token_display: dict[str, str]) -> dict[str, tuple[str, int]]:
    """Merge plural/singular variants, keeping the form with the highest source count."""
    merged: dict[str, tuple[str, int]] = {}  # canonical -> (display, count)

    for key, count in token_sources.items():
        display = token_display[key]
        singular = _singular_form(key)

        # Determine canonical form (prefer the one that already exists with higher count)
        if singular in merged:
            existing_display, existing_count = merged[singular]
            if count > existing_count:
                merged[singular] = (display, count)
            elif count == existing_count and display[0].isupper() and not existing_display[0].isupper():
                merged[singular] = (display, count)
            else:
                merged[singular] = (existing_display, existing_count + count)
        elif key in merged:
            existing_display, existing_count = merged[key]
            if count > existing_count:
                merged[key] = (display, count)
            else:
                merged[key] = (existing_display, existing_count + count)
        else:
            # Check if this key is the singular of an already-stored plural
            found = False
            for canonical in list(merged.keys()):
                if _singular_form(canonical) == key or _singular_form(key) == canonical:
                    existing_display, existing_count = merged[canonical]
                    if count > existing_count:
                        merged[canonical] = (display, count)
                    else:
                        merged[canonical] = (existing_display, existing_count + count)
                    found = True
                    break
            if not found:
                merged[key] = (display, count)

    return merged


def _extract_tags(raw_html: str, title: str) -> list[str]:
    """Extract English tags from meta keywords, title, and h2/h3 headings.

    Tags are merged from two sources:
    - Meta keywords (if present on the page)
    - Tokens that appear in >= 2 sources (title + h2/h3 headings)

    Single-source words are kept only if they look like all-caps acronyms
    from the title (e.g. AI, API, URL).
    """
    # 1. Collect tokens per source (title = 1 source, each h2/h3 = 1 source)
    sources: list[list[str]] = []
    if title:
        sources.append(_extract_tokens(title))
    for heading in _extract_headings(raw_html):
        sources.append(_extract_tokens(heading))

    # Count how many distinct sources contain each token
    token_sources: dict[str, int] = {}
    token_display: dict[str, str] = {}

    for tokens in sources:
        seen_in_source: set[str] = set()
        for token in tokens:
            key = token.lower()
            if key not in seen_in_source:
                seen_in_source.add(key)
                token_sources[key] = token_sources.get(key, 0) + 1
            # Prefer capitalized display form for English
            if key not in token_display:
                token_display[key] = token
            elif token[0].isupper() and not token_display[key][0].isupper():
                token_display[key] = token

    # Merge singular/plural forms
    merged = _merge_plural_forms(token_sources, token_display)

    # Keep tokens that appear in >= 2 sources ("repeatedly occurring")
    # OR are all-caps acronyms from the title
    title_keys = {t.lower() for t in sources[0]} if sources else set()
    heading_tags: list[tuple[str, int]] = []

    for key, (display, count) in merged.items():
        if count >= 2:
            heading_tags.append((display, count))
        elif count == 1 and key in title_keys:
            if display.isupper() and len(display) >= 2:
                heading_tags.append((display, count))

    heading_tags.sort(key=lambda x: -x[1])

    # 2. Meta keywords (merge with heading tags, deduplicated)
    kw_patterns = [
        r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^"\']*)["\']',
        r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']keywords["\']',
    ]
    keywords = _extract_meta(raw_html, kw_patterns)
    meta_tags: list[str] = []
    if keywords:
        meta_tags = [t.strip() for t in re.split(r"[,;，；]", keywords) if t.strip()]

    seen: set[str] = set()
    results: list[str] = []
    for tag in meta_tags + [t for t, _ in heading_tags]:
        key = tag.lower()
        if key not in seen:
            seen.add(key)
            results.append(tag)

    return results[:10]


def _format_date(val: str) -> str:
    """Extract YYYY-MM-DD from various date string formats."""
    if not val:
        return ""
    # ISO 8601: 2024-03-12T08:00:00Z
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", val)
    if m:
        return m.group(0)
    # Slash format: 2024/03/12
    m = re.match(r"(\d{4})/(\d{2})/(\d{2})", val)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    # Chinese format: 2024年03月12日
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", val)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return val[:10] if len(val) >= 10 else val


def format_frontmatter(metadata: dict[str, str]) -> str:
    """Format metadata as YAML frontmatter."""
    lines = ["---"]

    # Author fallback: use site_name if author is empty
    author = metadata.get("author", "")
    if not author:
        author = metadata.get("site_name", "")

    # Format published date to YYYY-MM-DD
    published = _format_date(metadata.get("published", ""))

    # Current date as created
    created = datetime.now().strftime("%Y-%m-%d")

    # Tags as YAML list
    tags_str = metadata.get("tags", "")
    tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

    fields = [
        ("title", metadata.get("title", "")),
        ("author", author),
        ("published", published),
        ("created", created),
        ("description", metadata.get("description", "")),
        ("category", metadata.get("category", "")),
        ("source", metadata.get("source", "")),
    ]

    for key, val in fields:
        if val:
            if ":" in val or val.startswith((" ", '"', "'")) or "\n" in val:
                val = json.dumps(val, ensure_ascii=False)
            lines.append(f"{key}: {val}")

    if tags:
        lines.append("tags:")
        for tag in tags:
            lines.append(f"  - {tag}")

    lines.append("---")
    return "\n".join(lines)


def apply_template(template: str, metadata: dict[str, str], content: str) -> str:
    """Replace variables in a template string."""
    now = datetime.now()
    author = metadata.get("author", "") or metadata.get("site_name", "")
    published = _format_date(metadata.get("published", ""))
    tags_str = metadata.get("tags", "")
    variables = {
        "{{title}}": metadata.get("title", ""),
        "{{url}}": metadata.get("source", ""),
        "{{source}}": metadata.get("source", ""),
        "{{date}}": now.strftime("%Y-%m-%d"),
        "{{datetime}}": now.strftime("%Y-%m-%d %H:%M:%S"),
        "{{created}}": now.strftime("%Y-%m-%d"),
        "{{content}}": content,
        "{{author}}": author,
        "{{description}}": metadata.get("description", ""),
        "{{published}}": published,
        "{{site_name}}": metadata.get("site_name", ""),
        "{{tags}}": tags_str,
    }
    result = template
    for var, value in variables.items():
        result = result.replace(var, value)
    return result


def extract_page_title(raw_html: str) -> str:
    """Prefer Open Graph title, then Twitter card, then <title>."""
    return extract_metadata(raw_html, "").get("title", "")


class HTMLToMarkdown(HTMLParser):
    """HTML to Markdown using only the standard library."""

    def __init__(self, base_url: str = ""):
        super().__init__()
        self.base_url = base_url
        self.md: list[str] = []
        self.in_ignore = 0
        self.list_stack: list[str] = []  # 'ul' | 'ol'
        self.ol_index_stack: list[int] = []
        self.link_url: Optional[str] = None
        self.link_text: list[str] = []
        self.in_link = False
        self.header_level = 0
        self.skip_tags = {
            "script",
            "style",
            "nav",
            "aside",
            "footer",
            "noscript",
            "iframe",
            "canvas",
            "svg",
            "form",
            "button",
            "select",
            "textarea",
            "label",
            "title",
            "head",
            "template",
        }
        self.block_tags = {
            "p",
            "div",
            "section",
            "figure",
            "figcaption",
            "blockquote",
            "address",
        }
        self.pre_depth = 0
        self.pre_parts: list[str] = []
        self.pre_lang = ""
        self.inline_code_depth = 0
        self.bold_depth = 0
        self.em_depth = 0
        # Tables
        self.table_depth = 0
        self.table_rows: list[list[str]] = []
        self.current_row: list[str] = []
        self.in_cell = False
        self.cell_parts: list[str] = []

    def _append_li_prefix(self) -> None:
        if not self.list_stack:
            return
        depth = max(0, len(self.list_stack) - 1)
        indent = "  " * depth
        if self.list_stack[-1] == "ul":
            marker = "- "
        else:
            if not self.ol_index_stack:
                return
            self.ol_index_stack[-1] += 1
            marker = f"{self.ol_index_stack[-1]}. "
        self.md.append(f"\n{indent}{marker}")

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag in self.skip_tags:
            self.in_ignore += 1
            return
        if self.in_ignore > 0:
            return

        if self.pre_depth > 0:
            if tag == "code":
                cls = attrs_dict.get("class") or ""
                for part in cls.split():
                    if part.startswith("language-"):
                        self.pre_lang = part.split("-", 1)[1]
                        break
            return

        if tag == "a":
            href = attrs_dict.get("href", "")
            if href:
                self.link_url = urljoin(self.base_url, href)
                self.in_link = True
                self.link_text = []
        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            if src:
                full_src = urljoin(self.base_url, src)
                self.md.append(f"![{alt}]({full_src})")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.header_level = int(tag[1])
        elif tag == "br":
            self.md.append("\n")
        elif tag == "hr":
            self.md.append("\n---\n")
        elif tag == "ul":
            self.list_stack.append("ul")
            self.ol_index_stack.append(0)
        elif tag == "ol":
            self.list_stack.append("ol")
            self.ol_index_stack.append(0)
        elif tag == "li":
            self._append_li_prefix()
        elif tag == "code":
            self.inline_code_depth += 1
            self.md.append("`")
        elif tag == "pre":
            self.pre_depth += 1
            if self.pre_depth == 1:
                self.pre_parts = []
                self.pre_lang = ""
        elif tag == "blockquote":
            self.md.append("\n> ")
        elif tag in ("strong", "b"):
            self.bold_depth += 1
            self.md.append("**")
        elif tag in ("em", "i"):
            self.em_depth += 1
            self.md.append("*")
        elif tag == "table":
            self.table_depth += 1
            if self.table_depth == 1:
                self.table_rows = []
        elif tag == "tr":
            if self.table_depth == 1:
                self.current_row = []
        elif tag in ("th", "td"):
            if self.table_depth == 1:
                self.in_cell = True
                self.cell_parts = []
        elif tag in ("main", "article", "header"):
            self.md.append("\n")

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.in_ignore -= 1
            return
        if self.in_ignore > 0:
            return

        if self.pre_depth > 0:
            if tag == "pre":
                self.pre_depth -= 1
                if self.pre_depth == 0:
                    body = "".join(self.pre_parts).rstrip("\n")
                    lang = self.pre_lang or ""
                    fence = "```"
                    self.md.append(f"\n{fence}{lang}\n{body}\n{fence}\n")
                    self.pre_parts = []
                    self.pre_lang = ""
            return

        if tag == "a":
            if self.in_link and self.link_url:
                text = "".join(self.link_text).strip()
                if not text:
                    text = self.link_url
                if text == self.link_url:
                    self.md.append(text)
                else:
                    esc = text.replace("]", "\\]")
                    self.md.append(f"[{esc}]({self.link_url})")
            self.in_link = False
            self.link_url = None
            self.link_text = []
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.md.append("\n")
            self.header_level = 0
        elif tag in self.block_tags:
            self.md.append("\n\n")
        elif tag == "ul" or tag == "ol":
            if self.list_stack:
                self.list_stack.pop()
            if self.ol_index_stack:
                self.ol_index_stack.pop()
            self.md.append("\n")
        elif tag == "li":
            self.md.append("\n")
        elif tag == "code":
            if self.inline_code_depth > 0:
                self.inline_code_depth -= 1
                self.md.append("`")
        elif tag == "blockquote":
            self.md.append("\n")
        elif tag in ("strong", "b"):
            if self.bold_depth > 0:
                self.bold_depth -= 1
                self.md.append("**")
        elif tag in ("em", "i"):
            if self.em_depth > 0:
                self.em_depth -= 1
                self.md.append("*")
        elif tag == "table":
            if self.table_depth == 1:
                self._flush_table()
            self.table_depth = max(0, self.table_depth - 1)
        elif tag in ("th", "td"):
            if self.table_depth == 1:
                raw = "".join(self.cell_parts)
                cell = re.sub(r"\s+", " ", raw.strip())
                self.current_row.append(cell)
                self.in_cell = False
                self.cell_parts = []
        elif tag == "tr":
            if self.table_depth == 1 and self.current_row:
                self.table_rows.append(self.current_row)
                self.current_row = []
        elif tag in ("main", "article", "header"):
            self.md.append("\n")

    def _flush_table(self) -> None:
        rows = [r for r in self.table_rows if r]
        self.table_rows = []
        if not rows:
            self.md.append("\n")
            return
        ncol = max(len(r) for r in rows)

        def pad(row: list[str]) -> list[str]:
            out = row[:ncol]
            while len(out) < ncol:
                out.append("")
            return out

        def esc_cell(s: str) -> str:
            return s.replace("|", "\\|").replace("\n", " ").strip()

        rows = [pad(r) for r in rows]
        lines = ["", "| " + " | ".join(esc_cell(c) for c in rows[0]) + " |"]
        lines.append("| " + " | ".join(["---"] * ncol) + " |")
        for r in rows[1:]:
            lines.append("| " + " | ".join(esc_cell(c) for c in r) + " |")
        lines.append("")
        self.md.append("\n".join(lines))

    def handle_data(self, data):
        if self.in_ignore > 0:
            return

        if self.pre_depth > 0:
            self.pre_parts.append(data)
            return

        if self.in_cell and self.table_depth == 1:
            self.cell_parts.append(data)
            return

        if self.in_link:
            self.link_text.append(data)
            return

        text = data.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = text.replace("\n", " ")
        if not text.strip():
            return

        if self.header_level > 0:
            hashes = "#" * self.header_level
            self.md.append(f"\n{hashes} {text.strip()}\n")
            return

        self.md.append(text)

    def handle_entityref(self, name):
        try:
            char = chr(name2codepoint[name])
        except KeyError:
            char = f"&{name};"
        self.handle_data(char)

    def handle_charref(self, name):
        try:
            if name.startswith("x"):
                char = chr(int(name[1:], 16))
            else:
                char = chr(int(name))
        except (ValueError, OverflowError):
            char = f"&#{name};"
        self.handle_data(char)

    def get_markdown(self) -> str:
        md = "".join(self.md)
        md = re.sub(r"\n{3,}", "\n\n", md)
        md = _collapse_blank_lines_between_pipe_tables(md)
        md = _strip_empty_markdown_list_lines(md)
        md = _collapse_excess_blank_lines(md)
        return md.strip()


def fetch_url(url, timeout=30, user_agent=None):
    """Fetch HTML content from a URL."""
    if not user_agent:
        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            charset = "utf-8"
            if "charset=" in content_type.lower():
                part = content_type.lower().split("charset=")[-1]
                charset = part.split(";")[0].strip().strip('"').strip("'")

            html_bytes = response.read()
            try:
                html_str = html_bytes.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                html_str = html_bytes.decode("utf-8", errors="replace")
            return html_str
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP error {e.code}: {e.reason} for URL: {url}") from e
    except urllib.error.URLError as e:
        raise Exception(f"URL error: {e.reason} for URL: {url}") from e
    except Exception as e:
        raise Exception(f"Failed to fetch {url}: {str(e)}") from e


def _download_image(img_url: str, dest_dir: str, base_url: str = "") -> Optional[str]:
    """Download an image and return its local filename, or None on failure."""
    try:
        full_url = urljoin(base_url, img_url)
        parsed = urlparse(full_url)
        basename = os.path.basename(parsed.path)
        if not basename or "." not in basename:
            basename = ""

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": base_url,
        }
        req = urllib.request.Request(full_url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")

            if not basename:
                ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ".bin"
                basename = hashlib.md5(full_url.encode()).hexdigest() + ext

            # Sanitize basename
            basename = re.sub(r'[^a-zA-Z0-9._-]', '-', basename)
            if basename.startswith("-"):
                basename = basename[1:]

            dest_path = os.path.join(dest_dir, basename)
            counter = 1
            stem, ext = os.path.splitext(basename)
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_dir, f"{stem}-{counter}{ext}")
                counter += 1

            with open(dest_path, "wb") as f:
                f.write(response.read())

        return os.path.basename(dest_path)
    except Exception:
        return None


def _localize_images(md: str, base_url: str, image_dir: str, output_path: Optional[str] = None) -> str:
    """Replace remote image URLs in Markdown with local relative paths.

    image_dir is the relative path written into Markdown (e.g. "assets").
    The actual download directory is resolved against output_path if given.
    """
    if output_path:
        base_dir = os.path.dirname(os.path.abspath(output_path))
        dest_dir = os.path.join(base_dir, image_dir)
    else:
        dest_dir = os.path.abspath(image_dir)

    os.makedirs(dest_dir, exist_ok=True)
    seen: dict[str, str] = {}

    def _replace(match):
        alt = match.group(1)
        url = match.group(2)

        if not (url.startswith("http://") or url.startswith("https://")):
            return match.group(0)

        if url in seen:
            local_name = seen[url]
        else:
            local_name = _download_image(url, dest_dir, base_url)
            seen[url] = local_name or url

        if local_name is None:
            return match.group(0)

        rel_path = image_dir.replace("\\", "/") + "/" + local_name
        return f"![{alt}]({rel_path})"

    return re.sub(r"!\[(.*?)\]\((.*?)\)", _replace, md)


def url_to_markdown(url, title=True, timeout=30, full_page=False, frontmatter=False, template=None, raw_html=None, image_dir=None, output_path=None):
    """Convert a URL to Markdown."""
    if raw_html is None:
        raw_html = fetch_url(url, timeout=timeout)
    metadata = extract_metadata(raw_html, url)
    page_title = metadata.get("title", "") if title else ""

    fragment = prepare_html_document(raw_html, full_page=full_page)
    converter = HTMLToMarkdown(base_url=url)
    converter.feed(fragment)
    md = converter.get_markdown()

    if template:
        md = apply_template(template, metadata, md)
    elif frontmatter:
        fm = format_frontmatter(metadata)
        if page_title:
            md_stripped = md.lstrip()
            if not md_stripped.startswith(f"# {page_title}"):
                md = f"# {page_title}\n\n{md}"
        md = f"{fm}\n\n{md}"
    else:
        if page_title:
            md_stripped = md.lstrip()
            if not md_stripped.startswith(f"# {page_title}"):
                md = f"# {page_title}\n\n{md}"

    if image_dir:
        md = _localize_images(md, url, image_dir, output_path)

    return md


def _render_filename(template: str, metadata: dict[str, str], index: int) -> str:
    """Generate a filename from a template string and metadata."""
    now = datetime.now()
    author = metadata.get("author", "") or metadata.get("site_name", "")
    published = _format_date(metadata.get("published", ""))
    safe_title = re.sub(r'[\\/*?:"<>|]', "-", metadata.get("title", "")).strip("-")
    variables = {
        "{{title}}": safe_title,
        "{{date}}": now.strftime("%Y-%m-%d"),
        "{{datetime}}": now.strftime("%Y-%m-%d-%H%M%S"),
        "{{author}}": author,
        "{{published}}": published,
        "{{site_name}}": metadata.get("site_name", ""),
        "{{url}}": metadata.get("source", ""),
        "{{source}}": metadata.get("source", ""),
        "{{index}}": str(index),
    }
    result = template
    for var, value in variables.items():
        result = result.replace(var, value)
    # Final sanitize
    result = re.sub(r'[\\/*?:"<>|]', "-", result)
    result = re.sub(r"-+", "-", result).strip("-.")
    if not result:
        result = f"url-{index}"
    return result


def batch_convert(urls_file, output_dir=None, full_page=False, title=True, frontmatter=False, template=None, filename_template=None, image_dir=None):
    """Convert multiple URLs from a file."""
    results = []
    errors = []

    with open(urls_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Converting: {url}", file=sys.stderr)
        try:
            raw_html = fetch_url(url)
            metadata = extract_metadata(raw_html, url)
            if output_dir:
                if filename_template:
                    filename = _render_filename(filename_template, metadata, i)
                    if not filename.lower().endswith(".md"):
                        filename += ".md"
                else:
                    parsed = urlparse(url)
                    filename = re.sub(r"[^a-zA-Z0-9]+", "-", parsed.netloc + parsed.path).strip("-")
                    if not filename:
                        filename = f"url-{i}"
                    filename += ".md"
                filepath = os.path.join(output_dir, filename)
                md = url_to_markdown(url, title=title, full_page=full_page, frontmatter=frontmatter, template=template, raw_html=raw_html, image_dir=image_dir, output_path=filepath)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(md)
                results.append((url, filepath))
            else:
                md = url_to_markdown(url, title=title, full_page=full_page, frontmatter=frontmatter, template=template, raw_html=raw_html, image_dir=image_dir)
                results.append((url, md))
        except Exception as e:
            errors.append((url, str(e)))
            print(f"  ERROR: {e}", file=sys.stderr)

    return results, errors


def main():
    parser = argparse.ArgumentParser(
        description="Convert web pages to Markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com/article
  %(prog)s https://example.com/page -o output.md
  %(prog)s -f urls.txt -d ./markdown_files/
        """,
    )
    parser.add_argument("url", nargs="?", help="URL to convert")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument("-f", "--file", help="File containing URLs to convert (one per line)")
    parser.add_argument("-d", "--dir", help="Output directory for batch conversion")
    parser.add_argument("--no-title", action="store_true", help="Skip adding page title as H1")
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="Use full <body> instead of article/main extraction (more noise, wider coverage)",
    )
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--frontmatter",
        action="store_true",
        help="Add YAML frontmatter with extracted metadata (title, author, published, etc.)",
    )
    parser.add_argument(
        "-t",
        "--template",
        help="Path to a template file for customizing output (variables: {{title}}, {{content}}, {{url}}, {{author}}, {{published}}, {{description}}, {{site_name}}, {{date}}, {{datetime}})",
    )
    parser.add_argument(
        "--filename-template",
        help="Batch mode filename pattern using variables: {{title}}, {{date}}, {{datetime}}, {{author}}, {{published}}, {{site_name}}, {{url}}, {{index}}. Default: URL-based slug",
    )
    parser.add_argument(
        "--download-images",
        help="Download remote images to a local folder and rewrite Markdown references (e.g. 'assets')",
    )

    args = parser.parse_args()

    template_content = None
    if args.template:
        if not os.path.exists(args.template):
            print(f"Error: Template file not found: {args.template}", file=sys.stderr)
            sys.exit(1)
        with open(args.template, "r", encoding="utf-8") as f:
            template_content = f.read()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        if args.dir:
            os.makedirs(args.dir, exist_ok=True)
        results, errors = batch_convert(
            args.file,
            args.dir,
            full_page=args.full_page,
            title=not args.no_title,
            frontmatter=args.frontmatter,
            template=template_content,
            filename_template=args.filename_template,
            image_dir=args.download_images,
        )
        if errors:
            print(
                f"\nCompleted with {len(errors)} errors out of {len(results) + len(errors)} URLs",
                file=sys.stderr,
            )
        else:
            print(f"\nSuccessfully converted all {len(results)} URLs", file=sys.stderr)
        sys.exit(0 if not errors else 1)

    if not args.url:
        parser.print_help()
        sys.exit(1)

    try:
        output_path = args.output if args.output else None
        md = url_to_markdown(
            args.url,
            title=not args.no_title,
            timeout=args.timeout,
            full_page=args.full_page,
            frontmatter=args.frontmatter,
            template=template_content,
            image_dir=args.download_images,
            output_path=output_path,
        )
        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"Saved to: {args.output}")
        else:
            print(md)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
