"""
Security utility functions for sanitizing untrusted input.
"""

import re
import html
from urllib.parse import urlparse


def sanitize_http_url(url) -> str:
    """
    Return a trusted http(s) URL string.
    Invalid scheme or too long returns empty string.

    Security: Only allows http/https schemes to prevent javascript:/data: injection.
    """
    if url is None:
        return ""
    if not isinstance(url, str):
        url = str(url)
    url = url.strip()
    if not url or len(url) > 4096:
        return ""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return ""
    return url


def safe_href_url(url) -> str:
    """
    HTML href attribute value: sanitize then escape.
    Prevents javascript:/data: scheme and attribute injection.

    Returns "#" for invalid/empty URLs.
    """
    u = sanitize_http_url(url)
    if not u:
        return "#"
    return html.escape(u, quote=True)


def safe_wechat_account_id(account_id) -> str:
    """
    WeChat official account ID/username for QR code link query parameters.
    Invalid characters are stripped.

    Only allows: A-Za-z0-9._-
    Max length: 64 characters.
    """
    if account_id is None:
        return ""
    s = str(account_id).strip()
    if not s or len(s) > 64:
        return ""
    if not re.fullmatch(r"[A-Za-z0-9._-]+", s):
        return ""
    return s


def safe_filename_from_keyword(keyword: str, max_len: int = 120) -> str:
    """
    Derive output filename from keyword, removing path separators and traversal sequences.
    Reduces path traversal risk.

    - Strips whitespace, replaces \\ / with underscore
    - Removes null bytes
    - Collapses 2+ consecutive dots to single underscore
    - Blocks "." and ".." (becomes "keyword")
    - Blocks ".." path traversal (becomes "keyword")
    - Truncates to max_len
    """
    original = keyword.strip() if keyword else ""
    if not original:
        return ""
    # Block exact "." and ".."; also reject ".." near path separators (path traversal)
    if original in (".", "..") or re.search(r"(^|[/\\])\.\.(/|$)", original):
        return "keyword"
    base = original.replace("\\", "_").replace("/", "_").replace("\x00", "")
    # Collapse 2+ consecutive dots to single underscore FIRST
    base = re.sub(r"\.{2,}", "_", base)
    # After collapsing, check for remaining path traversal
    if base in (".", "..") or ".." in base:
        base = "keyword"
    return base[:max_len] if len(base) > max_len else base