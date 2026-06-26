#!/usr/bin/env python3
"""
UniFuncs Web Search API client script.
Usage: ./search.py "search query" [options]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

API_URL = "https://api.unifuncs.com/api/web-search/search"
REQUEST_TIMEOUT_SECONDS = 180
TEXT_FORMATS = {"markdown", "md", "text", "txt"}
ERROR_MESSAGES = {
    -20001: "Server error. Please contact support or try again later.",
    -20011: "Access denied. Your account may not have permission for this API.",
    -20014: "Account disabled. Please contact support for details.",
    -20021: "Invalid or expired API key. Please verify your API key.",
    -20025: "Insufficient balance. Please top up your account.",
    -20033: "Rate limit exceeded. Reduce request frequency or upgrade your UniFuncs user tier.",
    -30000: "Search failed. Please contact support for details.",
    -30001: "Invalid search query. Please check your keywords.",
}


class UniFuncsSearchError(Exception):
    """Raised when the UniFuncs Search API call fails."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="UniFuncs real-time Web Search API client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "today's gold price" --page 1 --count 10
        """,
    )

    parser.add_argument(
        "query",
        help=(
            "Search query. Full search engine syntax is supported "
            "(for example site filters and exact-match with quotes)."
        ),
    )
    parser.add_argument(
        "--freshness",
        choices=["Day", "Week", "Month", "Year"],
        help="Result freshness filter. Use only when strong recency is required.",
    )
    parser.add_argument(
        "--include-images",
        default=False,
        action="store_true",
        help="Include image results (default: false).",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="Result page number (default: 1).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Results per page, range 1-50 (default: 10).",
    )
    parser.add_argument(
        "--format",
        dest="format_type",
        choices=["json", "markdown", "md", "text", "txt"],
        default="json",
        help="Output format (default: json).",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Validate command-line argument values."""
    if not args.query or not args.query.strip():
        print("Error: query cannot be empty.", file=sys.stderr)
        sys.exit(1)
    if not 1 <= args.count <= 50:
        print("Error: count must be between 1 and 50.", file=sys.stderr)
        sys.exit(1)


def get_api_key() -> str:
    """Read API key from UNIFUNCS_API_KEY environment variable."""
    api_key = os.environ.get("UNIFUNCS_API_KEY")
    if not api_key:
        print("Error: UNIFUNCS_API_KEY is not set.", file=sys.stderr)
        print("Visit https://unifuncs.com/account to get your API key.", file=sys.stderr)
        sys.exit(1)
    return api_key


def build_payload(
    query: str,
    page: int,
    count: int,
    format_type: str,
    include_images: bool,
    freshness: Optional[str],
) -> Dict[str, Any]:
    """Build request payload for the API."""
    payload: Dict[str, Any] = {
        "query": query,
        "page": page,
        "count": count,
        "format": format_type,
        "includeImages": include_images,
    }
    if freshness:
        payload["freshness"] = freshness
    return payload


def execute_search(payload: Dict[str, Any], api_key: str) -> Dict[str, Any] | str:
    """Call UniFuncs Search API and return parsed response."""
    json_data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(API_URL, data=json_data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            response_data = response.read().decode("utf-8")
            try:
                return json.loads(response_data)
            except json.JSONDecodeError:
                # API can return plain text for markdown/text output modes.
                return response_data
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            message = error_data.get("message", "Unknown error")
            raise UniFuncsSearchError(f"HTTP {err.code}: {message}") from err
        except json.JSONDecodeError:
            raise UniFuncsSearchError(f"HTTP {err.code}: {error_body}") from err
    except urllib.error.URLError as err:
        raise UniFuncsSearchError(f"Network error: {err.reason}") from err


def get_api_error_message(code: int, fallback_message: str) -> str:
    """Map API error code to a readable message."""
    return ERROR_MESSAGES.get(code, fallback_message)


def format_output(response: Dict[str, Any] | str, output_format: str) -> str:
    """Format API response for CLI output."""
    if isinstance(response, str):
        return response

    code = response.get("code", -1)
    if code != 0:
        message = get_api_error_message(code, response.get("message", "Unknown error"))
        raise UniFuncsSearchError(f"API error [{code}]: {message}")

    if output_format in TEXT_FORMATS:
        data = response.get("data", "")
        if isinstance(data, str):
            return data

    if output_format == "json":
        return json.dumps(response, ensure_ascii=False, indent=2)

    data = response.get("data", {})
    web_pages = data.get("webPages", [])
    images = data.get("images", [])

    output = [f"# Search Results\n", f"Found {len(web_pages)} web page results\n"]
    for idx, page in enumerate(web_pages, 1):
        output.append(f"\n## {idx}. {page.get('name', 'Untitled')}")
        output.append(f"**URL**: {page.get('url', '')}")
        if page.get("siteName"):
            output.append(f"**Source**: {page.get('siteName')}")
        output.append(f"\n{page.get('snippet', page.get('summary', ''))}\n")

    if images:
        output.append(f"\n---\n\n# Image Results ({len(images)} images)\n")
        for idx, img in enumerate(images, 1):
            output.append(f"{idx}. ![Image]({img.get('thumbnailUrl', '')})")
            output.append(f"   Full image: {img.get('contentUrl', '')}\n")

    return "\n".join(output)


def run(args: argparse.Namespace) -> str:
    """Execute request flow and return formatted output."""
    payload = build_payload(
        query=args.query,
        page=args.page,
        count=args.count,
        format_type=args.format_type,
        include_images=args.include_images,
        freshness=args.freshness,
    )
    api_key = get_api_key()
    response = execute_search(payload, api_key)
    return format_output(response, args.format_type)


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    validate_args(args)

    try:
        print(run(args))
    except UniFuncsSearchError as err:
        print(f"Search failed: {err}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nSearch canceled.", file=sys.stderr)
        sys.exit(130)
    except Exception as err:  # pragma: no cover - fallback safety
        print(f"Unexpected error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
