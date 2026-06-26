"""
Shared HTTP helper for Stocki OpenClaw scripts.

Reads STOCKI_GATEWAY_URL and STOCKI_API_KEY from environment.
Provides gateway_request(), gateway_request_raw(), handle_error(), and format_for_wechat().
Uses only Python stdlib (urllib, json).
"""

import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _env():
    """Return (base_url, api_key) or exit 1 if missing."""
    base_url = os.environ.get("STOCKI_GATEWAY_URL", "").rstrip("/")
    api_key = os.environ.get("STOCKI_API_KEY", "")
    missing = []
    if not base_url:
        missing.append("STOCKI_GATEWAY_URL")
    if not api_key:
        missing.append("STOCKI_API_KEY")
    if missing:
        print(
            f"Missing environment variable(s): {', '.join(missing)}\n"
            "Set them with:\n"
            '  export STOCKI_GATEWAY_URL="https://api.stocki.com.cn"\n'
            '  export STOCKI_API_KEY="sk_your_key_here"',
            file=sys.stderr,
        )
        sys.exit(1)
    return base_url, api_key


def handle_error(code, message, details=None):
    """Map Gateway error codes to exit codes and print message."""
    if code in ("auth_missing", "auth_invalid"):
        print(f"Auth error: {message}", file=sys.stderr)
        if code == "auth_missing":
            print(
                'Set your API key: export STOCKI_API_KEY="sk_your_key_here"',
                file=sys.stderr,
            )
        sys.exit(1)
    elif code == "quota_exceeded":
        print(f"Quota exceeded: {message}", file=sys.stderr)
        invite = (details or {}).get("invite_url", "")
        if invite:
            print(f"Invite friends to get more quota: {invite}", file=sys.stderr)
        sys.exit(3)
    elif code == "stocki_unavailable":
        print(f"Stocki unavailable: {message}", file=sys.stderr)
        sys.exit(2)
    elif code == "rate_limited":
        retry = (details or {}).get("retry_after", "")
        msg = f"Rate limited: {message}"
        if retry:
            msg += f" (retry after {retry}s)"
        print(msg, file=sys.stderr)
        sys.exit(3)
    else:
        print(f"Error [{code}]: {message}", file=sys.stderr)
        sys.exit(1)


def _handle_http_error(e):
    """Parse HTTP error response and call handle_error."""
    try:
        err_body = json.loads(e.read().decode())
        handle_error(
            err_body.get("error", "unknown"),
            err_body.get("message", str(e)),
            err_body.get("details"),
        )
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(2 if e.code >= 500 else 1)


def gateway_request(method, path, body=None, timeout=120):
    """Make an HTTP request to the Gateway. Returns parsed JSON dict."""
    base_url, api_key = _env()
    url = f"{base_url}{path}"
    headers = {"Authorization": f"Bearer {api_key}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    data = json.dumps(body).encode() if body is not None else None
    req = Request(url, data=data, headers=headers, method=method)

    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        _handle_http_error(e)
    except (URLError, TimeoutError, OSError) as e:
        print(f"Stocki unavailable: {e}", file=sys.stderr)
        sys.exit(2)


def gateway_request_raw(method, path, timeout=120):
    """Make an HTTP request to the Gateway. Returns raw bytes and content-type."""
    base_url, api_key = _env()
    url = f"{base_url}{path}"
    headers = {"Authorization": f"Bearer {api_key}"}
    req = Request(url, headers=headers, method=method)

    try:
        with urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()
            return raw, content_type
    except HTTPError as e:
        _handle_http_error(e)
    except (URLError, TimeoutError, OSError) as e:
        print(f"Stocki unavailable: {e}", file=sys.stderr)
        sys.exit(2)


def format_for_wechat(text):
    """Convert Stocki markdown output to WeChat-friendly plain text."""
    # 1. <stockidata> -> bracket highlights
    text = re.sub(r"<stockidata>(.*?)</stockidata>", r"[\1]", text)

    # 2. Collect inline markdown links as footnotes
    links = []

    def _replace_link(m):
        _label, url = m.group(1), m.group(2)
        links.append(url)
        return f"[{len(links)}]"

    text = re.sub(r"\[+([^\]]*)\]+\((https?://[^\)]+)\)", _replace_link, text)

    # 3. Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # 4. Simplify markdown formatting
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"^[\-\*]\s+", "· ", text, flags=re.MULTILINE)

    # 5. Append footnote references
    if links:
        text = text.rstrip() + "\n\n---\n"
        for i, url in enumerate(links, 1):
            text += f"[{i}] {url}\n"

    return text
