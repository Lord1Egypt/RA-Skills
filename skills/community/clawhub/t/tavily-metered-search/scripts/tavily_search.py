#!/usr/bin/env python3
"""
Tavily Search with Monthly Usage Tracking

Usage:
  python3 tavily_search.py --query "..." [--max-results N] [--format raw|brave|md]
                          [--include-answer] [--no-count]

Features:
  - Web search via Tavily API
  - Monthly usage tracking with configurable limit
  - Auto-reset on the 1st of each month
  - Warning when approaching limit

Configuration:
  - Config file: {skill_dir}/config/config.json
  - Usage tracking: {skill_dir}/data/tavily-usage.json
  - API key: ~/.openclaw/.env (TAVILY_API_KEY)
"""

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request
from datetime import datetime

TAVILY_URL = "https://api.tavily.com/search"

# Default values (used when config file doesn't exist)
DEFAULT_CONFIG = {
    "limit": 900,
    "warningThreshold": 800,
    "searchDepth": "basic",
    "defaultMaxResults": 5
}


def get_skill_dir() -> pathlib.Path:
    """Get the skill directory path."""
    return pathlib.Path(__file__).parent.parent


def get_config_file_path() -> pathlib.Path:
    """Get the path to the config file.

    Location: {skill_dir}/config/config.json
    """
    return get_skill_dir() / "config" / "config.json"


def get_usage_file_path() -> pathlib.Path:
    """Get the path to the usage tracking file.

    Location: {skill_dir}/data/tavily-usage.json
    """
    data_dir = get_skill_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "tavily-usage.json"


def load_config() -> dict:
    """Load configuration from file.

    Returns config dict with defaults for missing keys.
    """
    config_file = get_config_file_path()
    config = DEFAULT_CONFIG.copy()

    if config_file.exists():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for key in config:
                    if key in data and data[key] is not None:
                        config[key] = data[key]
        except (json.JSONDecodeError, Exception):
            pass

    return config


def load_key() -> str | None:
    """Load Tavily API key from environment or .env file."""
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key.strip()

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*TAVILY_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass

    return None


def read_usage(usage_file: pathlib.Path, limit: int) -> dict:
    """Read usage data from file, initializing if needed."""
    current_month = datetime.now().strftime("%Y-%m")

    if not usage_file.exists():
        return {
            "currentMonth": current_month,
            "count": 0,
            "limit": limit,
            "lastReset": f"{current_month}-01"
        }

    try:
        data = json.loads(usage_file.read_text(encoding="utf-8"))
        # Reset counter if month changed
        if data.get("currentMonth") != current_month:
            data = {
                "currentMonth": current_month,
                "count": 0,
                "limit": limit,
                "lastReset": f"{current_month}-01"
            }
        # Update limit from config
        data["limit"] = limit
        return data
    except (json.JSONDecodeError, Exception):
        return {
            "currentMonth": current_month,
            "count": 0,
            "limit": limit,
            "lastReset": f"{current_month}-01"
        }


def write_usage(usage_file: pathlib.Path, data: dict):
    """Write usage data to file."""
    usage_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def check_usage_limit(usage_data: dict) -> tuple[bool, str]:
    """Check if usage limit is reached.

    Returns: (is_limited, message)
    """
    count = usage_data.get("count", 0)
    limit = usage_data.get("limit", DEFAULT_CONFIG["limit"])
    current_month = usage_data.get("currentMonth", "")

    if count >= limit:
        # Calculate next reset date
        year, month = map(int, current_month.split("-"))
        if month == 12:
            next_month = f"{year + 1}-01"
        else:
            next_month = f"{year}-{month + 1:02d}"

        msg = (
            f"⚠️  Warning: Monthly Tavily search limit reached ({limit} searches)\n"
            f"📅 Resets on: {next_month}-01\n\n"
            f"Please provide a specific URL and use web_fetch to retrieve content."
        )
        return True, msg

    return False, ""


def increment_usage(usage_file: pathlib.Path, usage_data: dict, warning_threshold: int) -> str | None:
    """Increment usage counter after successful search.

    Returns warning message if approaching limit, None otherwise.
    """
    limit = usage_data.get("limit", DEFAULT_CONFIG["limit"])

    usage_data["count"] = usage_data.get("count", 0) + 1
    new_count = usage_data["count"]

    write_usage(usage_file, usage_data)

    if new_count >= warning_threshold:
        remaining = limit - new_count
        return (
            f"\n\n⚠️  Warning: {new_count} searches used this month, "
            f"approaching limit ({limit})\n"
            f"📊 Remaining: {remaining} searches"
        )

    return None


def tavily_search(
    query: str,
    max_results: int,
    include_answer: bool,
    search_depth: str
) -> dict:
    """Execute Tavily search API call."""
    key = load_key()
    if not key:
        raise SystemExit(
            "Missing TAVILY_API_KEY. Set env var TAVILY_API_KEY or add it to ~/.openclaw/.env"
        )

    payload = {
        "api_key": key,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": bool(include_answer),
        "include_images": False,
        "include_raw_content": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TAVILY_URL,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Tavily returned non-JSON: {body[:300]}")

    out = {
        "query": query,
        "answer": obj.get("answer"),
        "results": [],
    }

    for r in (obj.get("results") or [])[:max_results]:
        out["results"].append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),
            }
        )

    if not include_answer:
        out.pop("answer", None)

    return out


def to_brave_like(obj: dict) -> dict:
    """Convert to Brave-like format (title/url/snippet)."""
    results = []
    for r in obj.get("results", []) or []:
        results.append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content"),
            }
        )
    out = {"query": obj.get("query"), "results": results}
    if "answer" in obj:
        out["answer"] = obj.get("answer")
    return out


def to_markdown(obj: dict) -> str:
    """Convert results to human-readable Markdown."""
    lines = []
    if obj.get("answer"):
        lines.append(obj["answer"].strip())
        lines.append("")
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   - {snippet}")
    return "\n".join(lines).strip() + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="Tavily Search with Monthly Usage Tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --query "AI news today" --max-results 5 --format md
  %(prog)s --query "python tutorial" --include-answer
  %(prog)s --query "test" --no-count  # Skip usage tracking

Configuration:
  Edit config/config.json in the skill directory to change default settings:
  {
    "limit": 900,
    "warningThreshold": 800,
    "searchDepth": "basic",
    "defaultMaxResults": 5
  }
        """
    )
    ap.add_argument("--query", required=True, help="Search query string")
    ap.add_argument("--max-results", type=int, help="Max results (1-10), default from config")
    ap.add_argument("--include-answer", action="store_true", help="Include short answer in response")
    ap.add_argument(
        "--search-depth",
        choices=["basic", "advanced"],
        help="Tavily search depth, default from config"
    )
    ap.add_argument(
        "--format",
        default="md",
        choices=["raw", "brave", "md"],
        help="Output format: raw (JSON) | brave (JSON) | md (Markdown, default)"
    )
    ap.add_argument(
        "--no-count",
        action="store_true",
        help="Skip usage tracking (still consumes API quota)"
    )

    args = ap.parse_args()

    # Load configuration
    config = load_config()

    # Apply command-line overrides or use config defaults
    max_results = args.max_results or config.get("defaultMaxResults", 5)
    search_depth = args.search_depth or config.get("searchDepth", "basic")
    limit = config.get("limit", 900)
    warning_threshold = config.get("warningThreshold", 800)

    # Usage tracking
    if not args.no_count:
        usage_file = get_usage_file_path()
        usage_data = read_usage(usage_file, limit)

        # Check limit before search
        is_limited, limit_msg = check_usage_limit(usage_data)
        if is_limited:
            print(limit_msg, file=sys.stderr)
            sys.exit(2)

    # Execute search
    try:
        res = tavily_search(
            query=args.query,
            max_results=max(1, min(max_results, 10)),
            include_answer=args.include_answer,
            search_depth=search_depth,
        )
    except Exception as e:
        print(f"Search failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Increment usage after successful search
    warning = None
    if not args.no_count:
        warning = increment_usage(usage_file, usage_data, warning_threshold)

    # Output results
    if args.format == "md":
        output = to_markdown(res)
        sys.stdout.write(output)
        if warning:
            sys.stdout.write(warning + "\n")
    elif args.format == "brave":
        res = to_brave_like(res)
        json.dump(res, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:  # raw
        json.dump(res, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()