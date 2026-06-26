"""Shared utility functions for web-fetcher."""
import re


def slugify(title, fallback="article"):
    """Generate filesystem-safe slug from article title."""
    slug = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug[:100] if slug else fallback


def extract_title(md_text):
    """Extract title from first heading or first non-empty line."""
    for line in md_text.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            return re.sub(r'^#+\s*', '', line).strip()
        if line and len(line) > 2:
            return line[:80]
    return None
