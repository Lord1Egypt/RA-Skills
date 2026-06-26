#!/usr/bin/env python3
"""
UniFuncs Web Reader API client script.
Usage: ./read.py "URL" [options]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict

API_URL = "https://api.unifuncs.com/api/web-reader/read"
REQUEST_TIMEOUT_SECONDS = 300
DEFAULT_READ_TIMEOUT_MS = 180000
DEFAULT_EXTRACT_TIMEOUT_MS = 180000
DEFAULT_MAX_WORDS = 1_000_000
TEXT_FORMATS = {"markdown", "md", "text", "txt"}

ERROR_MESSAGES = {
    -20001: "Server error. Please contact support or try again later.",
    -20011: "Access denied. Your account may not have permission for this API.",
    -20014: "Account disabled. Please contact support for details.",
    -20021: "Invalid or expired API key. Please verify your API key.",
    -20025: "Insufficient balance. Please top up your account.",
    -20033: "Rate limit exceeded. Reduce request frequency or upgrade your UniFuncs user tier.",
    -30000: "Invalid target URL. Please check the URL.",
    -30001: "Failed to access target URL. Please check the URL.",
    -30002: "Request timed out. Please retry.",
    -30003: "Target URL content is empty. Retry or use another URL.",
    -30004: "Target URL may deny access or require verification. Retry or use another URL.",
}


class UniFuncsReaderError(Exception):
    """Raised when the UniFuncs Reader API call fails."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="UniFuncs Web Reader API client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://mp.weixin.qq.com/s/wmoNh44A4ofkawPNVx_g6A" --format md
        """,
    )

    parser.add_argument("url", help="Target URL to read.")
    parser.add_argument(
        "--format",
        dest="format_type",
        choices=["markdown", "md", "text", "txt"],
        default="md",
        help="Output format (default: md).",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Exclude images from output.",
    )
    parser.add_argument(
        "--only-css-selectors",
        nargs="+",
        help='Only include elements matching CSS selectors (e.g. ".article_content").',
    )
    parser.add_argument(
        "--wait-for-css-selectors",
        nargs="+",
        help='Wait until these CSS selectors appear before parsing (e.g. "#main" ".content").',
    )
    parser.add_argument(
        "--exclude-css-selectors",
        nargs="+",
        help='Exclude elements matching CSS selectors (e.g. "#footer" ".copyright").',
    )
    parser.add_argument(
        "--link-summary",
        action="store_true",
        help="Append all page links to the end of content.",
    )
    parser.add_argument(
        "--ignore-cache",
        action="store_true",
        help="Ignore cache and fetch fresh content.",
    )
    parser.add_argument(
        "--set-cookie",
        type=str,
        help="Set Cookie header value for pages requiring authentication.",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=DEFAULT_MAX_WORDS,
        help="Maximum character count to read, range 0-1000000 (default: 1000000).",
    )
    parser.add_argument(
        "--read-timeout",
        type=int,
        default=DEFAULT_READ_TIMEOUT_MS,
        help=f"Read timeout in milliseconds (default: {DEFAULT_READ_TIMEOUT_MS}).",
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Extract topic-focused content using an LLM.",
    )
    parser.add_argument(
        "--preserve-source",
        action="store_true",
        help="Attach source references to each extracted paragraph.",
    )
    parser.add_argument(
        "--extract-timeout",
        type=int,
        default=DEFAULT_EXTRACT_TIMEOUT_MS,
        help=f"Topic extraction timeout in milliseconds (default: {DEFAULT_EXTRACT_TIMEOUT_MS}).",
    )
    return parser.parse_args()


def validate_url(url: str) -> bool:
    """Perform a permissive URL format check."""
    try:
        parsed = urllib.parse.urlparse(url)
        return bool(parsed.netloc or parsed.path)
    except Exception:
        return False


def validate_args(args: argparse.Namespace) -> None:
    """Validate command-line argument values."""
    if not args.url or not args.url.strip():
        print("Error: URL cannot be empty.", file=sys.stderr)
        sys.exit(1)
    if not validate_url(args.url):
        print("Error: URL format appears invalid.", file=sys.stderr)
        sys.exit(1)
    if not 0 <= args.max_words <= 1_000_000:
        print("Error: max-words must be between 0 and 1000000.", file=sys.stderr)
        sys.exit(1)
    if args.read_timeout <= 0:
        print("Error: read-timeout must be greater than 0.", file=sys.stderr)
        sys.exit(1)
    if args.extract_timeout <= 0:
        print("Error: extract-timeout must be greater than 0.", file=sys.stderr)
        sys.exit(1)


def get_api_key() -> str:
    """Read API key from UNIFUNCS_API_KEY environment variable."""
    api_key = os.environ.get("UNIFUNCS_API_KEY")
    if not api_key:
        print("Error: UNIFUNCS_API_KEY is not set.", file=sys.stderr)
        print("Visit https://unifuncs.com/account to get your API key.", file=sys.stderr)
        sys.exit(1)
    return api_key


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    """Build request payload for latest Web Reader API."""
    payload: Dict[str, Any] = {
        "url": args.url,
        "format": args.format_type,
        "includeImages": not args.no_images,
        "linkSummary": args.link_summary,
        "ignoreCache": args.ignore_cache,
        "maxWords": args.max_words,
        "readTimeout": args.read_timeout,
    }

    if args.only_css_selectors:
        payload["onlyCSSSelectors"] = args.only_css_selectors
    if args.wait_for_css_selectors:
        payload["waitForCSSSelectors"] = args.wait_for_css_selectors
    if args.exclude_css_selectors:
        payload["excludeCSSSelectors"] = args.exclude_css_selectors
    if args.set_cookie:
        payload["setCookie"] = args.set_cookie
    if args.topic:
        payload["topic"] = args.topic
        payload["preserveSource"] = args.preserve_source
        payload["extractTimeout"] = args.extract_timeout

    return payload


def execute_read(payload: Dict[str, Any], api_key: str) -> Dict[str, Any] | str:
    """Call UniFuncs Web Reader API and return parsed response."""
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
            raise UniFuncsReaderError(f"HTTP {err.code}: {message}") from err
        except json.JSONDecodeError:
            raise UniFuncsReaderError(f"HTTP {err.code}: {error_body}") from err
    except urllib.error.URLError as err:
        raise UniFuncsReaderError(f"Network error: {err.reason}") from err


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
        raise UniFuncsReaderError(f"API error [{code}]: {message}")

    if output_format in TEXT_FORMATS:
        data = response.get("data", "")
        if isinstance(data, str):
            return data

    return json.dumps(response, ensure_ascii=False, indent=2)


def run(args: argparse.Namespace) -> str:
    """Execute request flow and return formatted output."""
    payload = build_payload(args)
    api_key = get_api_key()
    response = execute_read(payload, api_key)
    return format_output(response, args.format_type)


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    validate_args(args)

    try:
        print(run(args))
    except UniFuncsReaderError as err:
        print(f"Read failed: {err}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nRead canceled.", file=sys.stderr)
        sys.exit(130)
    except Exception as err:  # pragma: no cover - fallback safety
        print(f"Unexpected error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
