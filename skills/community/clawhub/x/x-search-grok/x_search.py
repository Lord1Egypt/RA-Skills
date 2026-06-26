#!/usr/bin/env python3
"""
x_search.py — Search X (Twitter) using xAI Grok API

Usage:
  python3 x_search.py account @elonmusk --time 24h
  python3 x_search.py account @user1 @user2 --count 10 --lang en
  python3 x_search.py --output ~/obsidian/X/ account @elonmusk --time 24h
  python3 x_search.py trends "#AI" "#crypto"
  python3 x_search.py topic "Claude MCP" --lang ja
"""

import os
import re
import sys
import time
import argparse
import warnings
from datetime import datetime, timezone, timedelta

try:
    from urllib3.exceptions import NotOpenSSLWarning
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
except ImportError:
    pass

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

API_URL = "https://api.x.ai/v1/responses"
# Default model. Override with XAI_MODEL env var to pin a specific version, e.g.:
#   export XAI_MODEL=grok-4
MODEL = os.environ.get("XAI_MODEL", "grok-4-1-fast-reasoning")

# Languages where the original post is typically already in that language —
# skip the translation field to avoid redundancy.
SKIP_TRANSLATION_LANGS = {"en", "english"}

FIELD_KEYS = {"ACCOUNT", "TIMESTAMP", "TYPE", "ORIGINAL", "TRANSLATION", "SUMMARY", "KEYWORDS"}


def get_api_key() -> str:
    key = os.environ.get("XAI_API_KEY")
    if not key:
        print("Error: XAI_API_KEY environment variable not set.", file=sys.stderr)
        print("Run: export XAI_API_KEY=your_key", file=sys.stderr)
        sys.exit(1)
    return key


def call_grok(prompt: str, tools: list = None) -> str:
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "tools": tools or [{"type": "x_search"}],
        "input": [{"role": "user", "content": prompt}],
    }
    last_exc = None
    resp = None
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            if resp.ok:
                break
            print(f"API error {resp.status_code} (attempt {attempt+1}/3): {resp.text}", file=sys.stderr)
            if resp.status_code < 500:
                resp.raise_for_status()  # 4xx — no retry
            if attempt < 2:
                time.sleep(2 ** attempt * 5)  # 5s, 10s
        except requests.exceptions.RequestException as e:
            last_exc = e
            if attempt < 2:
                time.sleep(2 ** attempt * 5)
    else:
        if last_exc:
            raise last_exc
        resp.raise_for_status()

    data = resp.json()
    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    return content.get("text", "")
    return ""


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _sanitize(text: str, max_len: int = 50) -> str:
    """Sanitize a string for use in a filename."""
    text = text.lstrip("@#")
    text = re.sub(r"[^\w\s-]", "", text)   # remove special chars
    text = re.sub(r"[\s]+", "-", text)      # spaces → hyphens
    text = re.sub(r"-{2,}", "-", text)      # collapse consecutive hyphens
    return text.strip("-")[:max_len]


def _auto_filename(mode: str, args) -> str:
    """Generate a date-stamped filename based on mode and query args."""
    today = _today()
    if mode == "account":
        handles = [a.lstrip("@") for a in args.accounts]
        stem = handles[0] if len(handles) == 1 else "accounts"
    elif mode == "trends":
        parts = "-".join(_sanitize(t) for t in args.trends)
        stem = f"trends-{parts}"
    else:  # topic
        stem = f"topic-{_sanitize(args.topic)}"
    return f"{stem}-{today}.md"


def _resolve_output_path(output: str, filename: str) -> str:
    """Resolve --output to a full file path, creating directories as needed."""
    path = os.path.abspath(os.path.expanduser(output))
    if os.path.isdir(path) or output.endswith("/") or output.endswith(os.sep):
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, filename)
    else:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    return path


def _save(content: str, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved → {path}", file=sys.stderr)


def _parse_time_range(time_range: str) -> str:
    """Convert time range string (24h, 48h, 7d) to from_date ISO string."""
    tr = time_range.lower().strip()
    if tr.endswith("h"):
        delta = timedelta(hours=int(tr[:-1]))
    elif tr.endswith("d"):
        delta = timedelta(days=int(tr[:-1]))
    else:
        raise ValueError(f"Unrecognised time range '{time_range}'. Use formats like 24h, 48h, 7d.")
    return (datetime.now(timezone.utc) - delta).strftime("%Y-%m-%d")


def _translation_field(lang: str, include_translation: bool) -> str:
    return f"TRANSLATION: [translate the post to {lang}]\n" if include_translation else ""


def _structured_prompt_body(lang: str, include_translation: bool) -> str:
    """Return the common structured output format block used in all prompts."""
    tf = _translation_field(lang, include_translation)
    return f"""ACCOUNT: @username
TIMESTAMP: YYYY-MM-DD HH:MM UTC
TYPE: Post (if it's an original post) or Reply (if it's a reply to someone else)
ORIGINAL: [verbatim post text]
{tf}SUMMARY: [one-sentence summary in {lang}]
KEYWORDS: term1::explanation in {lang} | term2::explanation in {lang}

Separate each post with:
---POST_SEPARATOR---

Output nothing else outside this structure."""


def _parse_fields(post_text: str) -> dict[str, str]:
    """Parse structured post fields, correctly handling multiline values."""
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for line in post_text.splitlines():
        if ": " in line:
            key, _, value = line.partition(": ")
            key = key.strip()
            if key in FIELD_KEYS:
                if current_key:
                    fields[current_key] = "\n".join(current_lines).strip()
                current_key = key
                current_lines = [value]
                continue
        if current_key:
            current_lines.append(line)

    if current_key:
        fields[current_key] = "\n".join(current_lines).strip()

    return fields


def _render_post(i: int, fields: dict[str, str], lang: str, include_translation: bool) -> str:
    account     = fields.get("ACCOUNT", "")
    timestamp   = fields.get("TIMESTAMP", "")
    post_type   = fields.get("TYPE", "").strip()
    original    = fields.get("ORIGINAL", "")
    translation = fields.get("TRANSLATION", "")
    summary     = fields.get("SUMMARY", "")
    kw_raw      = fields.get("KEYWORDS", "")

    type_label = f" {post_type}" if post_type else ""
    out = [f"## {i}.{type_label}{' · ' + account if account else ''}\n\n"]

    if timestamp:
        out.append(f"**Time:** {timestamp}\n\n")
    if original:
        quoted = "\n> ".join(original.splitlines())
        out.append(f"**Original:**\n> {quoted}\n\n")
    if include_translation and translation:
        out.append(f"**Translation ({lang}):** {translation}\n\n")
    if summary:
        out.append(f"**Summary:** {summary}\n\n")
    if kw_raw:
        kw_items = []
        for kw in kw_raw.split("|"):
            kw = kw.strip()
            if "::" in kw:
                term, _, explanation = kw.partition("::")
                kw_items.append(f"- `{term.strip()}` — {explanation.strip()}")
        if kw_items:
            out.append("**Keywords:**\n" + "\n".join(kw_items) + "\n\n")

    out.append("---\n\n")
    return "".join(out)


def _render_raw_posts(raw: str, lang: str, include_translation: bool) -> str:
    """Parse and render all posts from a raw API response string."""
    parts = [p.strip() for p in raw.split("---POST_SEPARATOR---") if p.strip()]
    rendered = []
    for i, part in enumerate(parts, 1):
        fields = _parse_fields(part)
        rendered.append(_render_post(i, fields, lang, include_translation))
    return "".join(rendered)


# ---------------------------------------------------------------------------
# Mode: account
# ---------------------------------------------------------------------------

_TYPE_FILTER = {
    "post":  "Return ONLY original posts (not replies). Skip any reply.",
    "reply": "Return ONLY replies to other people's posts. Skip any original post.",
    "all":   "Return all posts and replies.",
}

_TYPE_LABEL = {
    "post":  "Posts only",
    "reply": "Replies only",
}


def search_accounts(accounts: list[str], time_range: str = None,
                    count: int = None, lang: str = "zh",
                    post_type: str = "all") -> str:
    handles = [a.lstrip("@") for a in accounts]
    accounts_str = ", ".join("@" + h for h in handles)

    if time_range:
        scope = f"last {time_range}"
    elif count:
        scope = f"latest {count} posts"
    else:
        scope = "latest 10 posts"

    tool: dict = {
        "type": "x_search",
        "allowed_x_handles": handles,
        "max_search_results": 50,
    }
    if time_range:
        tool["from_date"] = _parse_time_range(time_range)
        tool["to_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    include_translation = lang.lower() not in SKIP_TRANSLATION_LANGS

    prompt = f"""Search X for posts from these accounts: {accounts_str}

{_TYPE_FILTER[post_type]}

Return the {scope} from each account. For EVERY post found, use exactly this format:

{_structured_prompt_body(lang, include_translation)}"""

    raw = call_grok(prompt, tools=[tool])
    if not raw.strip():
        print("Warning: Grok returned no content. Check XAI_API_KEY or try again.", file=sys.stderr)
    return _format_account_output(raw, accounts, scope, lang, include_translation, post_type)


def _format_account_output(raw: str, accounts: list[str], scope: str,
                            lang: str, include_translation: bool,
                            post_type: str = "all") -> str:
    today = _today()
    accounts_display = " · ".join(accounts)
    type_suffix = f" · {_TYPE_LABEL[post_type]}" if post_type in _TYPE_LABEL else ""

    header = (
        f"# X Feed · {accounts_display} · {today}\n"
        f"**Scope:** {scope} · **Lang:** {lang}{type_suffix}\n\n---\n\n"
    )

    raw_posts = [p.strip() for p in raw.split("---POST_SEPARATOR---") if p.strip()]

    # Parse, filter by type, and skip empty entries in a single pass
    valid: list[dict] = []
    for post in raw_posts:
        fields = _parse_fields(post)
        if not (fields.get("ORIGINAL") or fields.get("TIMESTAMP")):
            continue
        t = fields.get("TYPE", "").lower()
        if post_type == "post" and "reply" in t:
            continue
        if post_type == "reply" and "reply" not in t:
            continue
        valid.append(fields)

    rendered = [header]
    for i, fields in enumerate(valid, 1):
        rendered.append(_render_post(i, fields, lang, include_translation))

    if not valid:
        rendered.append(f"_No {_TYPE_LABEL.get(post_type, 'results')} found in the given scope._\n")

    return "".join(rendered)


# ---------------------------------------------------------------------------
# Mode: trends
# ---------------------------------------------------------------------------

def search_trends(trends: list[str], lang: str = "en") -> str:
    trends_str = ", ".join(trends)
    include_translation = lang.lower() not in SKIP_TRANSLATION_LANGS

    prompt = f"""Use the x_search tool to search X (Twitter) RIGHT NOW for the top most engaging posts about: {trends_str}

You MUST call x_search to retrieve real posts. Do NOT generate or simulate any data.

For EVERY post found, use exactly this format:

{_structured_prompt_body(lang, include_translation)}"""

    raw = call_grok(prompt, tools=[{"type": "x_search"}])
    if not raw.strip():
        print("Warning: Grok returned no content. Check XAI_API_KEY or try again.", file=sys.stderr)

    today = _today()
    header = f"# X Trends Top 10 · {' · '.join(trends)} · {today}\n\n**Lang:** {lang}\n\n---\n\n"
    body = _render_raw_posts(raw, lang, include_translation) if raw.strip() else "_No results returned. Check XAI_API_KEY or try again._\n"
    return header + body


# ---------------------------------------------------------------------------
# Mode: topic
# ---------------------------------------------------------------------------

def search_topic(topic: str, lang: str = "en") -> str:
    include_translation = lang.lower() not in SKIP_TRANSLATION_LANGS

    prompt = f"""Use the x_search tool to search X (Twitter) RIGHT NOW for hot discussions about: {topic}

You MUST call x_search to retrieve real posts. Do NOT generate or simulate any data.

For EVERY post found, use exactly this format:

{_structured_prompt_body(lang, include_translation)}"""

    raw = call_grok(prompt, tools=[{"type": "x_search"}])
    if not raw.strip():
        print("Warning: Grok returned no content. Check XAI_API_KEY or try again.", file=sys.stderr)

    today = _today()
    header = f"# X Topic · {topic} · {today}\n\n**Lang:** {lang}\n\n---\n\n"
    body = _render_raw_posts(raw, lang, include_translation) if raw.strip() else "_No results returned. Check XAI_API_KEY or try again._\n"
    return header + body


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Search X (Twitter) using Grok API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--lang", "-l", default="zh", metavar="LANG",
        help="Output language for translation/summary/keywords (default: zh). "
             "Use 'en' to skip translation field.",
    )
    parser.add_argument(
        "--output", "-o", default=None, metavar="PATH",
        help="Save output to file. Pass a directory for auto-naming, or a full path. "
             "Same-day runs overwrite the existing file.",
    )
    parser.add_argument(
        "--progress-only", action="store_true",
        help="Print only a one-line summary to stdout (for automated pipelines). "
             "Full Markdown is still written to --output.",
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    # account
    p_account = sub.add_parser("account", help="Search posts from specific accounts")
    p_account.add_argument("accounts", nargs="+", help="Account handles (e.g. @elonmusk)")
    p_account.add_argument("--time", "-t", metavar="RANGE",
                           help="Time range: 24h, 48h, 7d, etc.")
    p_account.add_argument("--count", "-n", type=int, metavar="N",
                           help="Number of posts to retrieve")
    p_account.add_argument("--type", dest="post_type", default="all",
                           choices=["post", "reply", "all"],
                           help="Filter by type: post, reply, or all (default: all)")

    # trends
    sub.add_parser("trends", help="Top 10 posts per trend").add_argument(
        "trends", nargs="+", help="Trend hashtags or keywords"
    )

    # topic
    sub.add_parser("topic", help="Hot discussions about a topic").add_argument(
        "topic", help="Topic to search"
    )

    args = parser.parse_args()

    if args.mode == "account":
        result = search_accounts(args.accounts, time_range=args.time,
                                 count=args.count, lang=args.lang,
                                 post_type=args.post_type)
    elif args.mode == "trends":
        result = search_trends(args.trends, lang=args.lang)
    elif args.mode == "topic":
        result = search_topic(args.topic, lang=args.lang)

    if args.output:
        filename = _auto_filename(args.mode, args)
        path = _resolve_output_path(args.output, filename)
        _save(result, path)
        if args.progress_only:
            post_count = result.count("\n## ")
            print(f"[x_search] {args.mode} → {os.path.basename(path)} ({post_count} posts)")
            return

    if not args.progress_only:
        print(result)


if __name__ == "__main__":
    main()
