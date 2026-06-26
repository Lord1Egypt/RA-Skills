#!/usr/bin/env python3
"""
UniFuncs Deep Search query_task client.
Usage: ./deep-search-query-task.py "task_id" [options]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict

QUERY_TASK_ENDPOINT = "https://api.unifuncs.com/deepsearch/v1/query_task"
DEFAULT_REQUEST_TIMEOUT_SECONDS = 180


class UniFuncsDeepSearchError(Exception):
    """Raised when the UniFuncs Deep Search API call fails."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="UniFuncs Deep Search query_task client")
    parser.add_argument("task_id", help="Task ID returned by create_task.")
    parser.add_argument(
        "--raw-response",
        action="store_true",
        help="Print full API response JSON instead of concise output.",
    )
    return parser.parse_args()


def get_api_key() -> str:
    """Read API key from UNIFUNCS_API_KEY."""
    api_key = os.environ.get("UNIFUNCS_API_KEY")
    if not api_key:
        print("Error: UNIFUNCS_API_KEY is not set.", file=sys.stderr)
        print("Visit https://unifuncs.com/account to get your API key.", file=sys.stderr)
        sys.exit(1)
    return api_key


def validate_args(args: argparse.Namespace) -> None:
    """Validate argument values."""
    if not args.task_id.strip():
        print("Error: task_id cannot be empty.", file=sys.stderr)
        sys.exit(1)


def get_json(url: str, params: Dict[str, str], api_key: str) -> Dict[str, Any]:
    """GET JSON response with query params."""
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{url}?{query}",
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        raise UniFuncsDeepSearchError(f"HTTP {err.code}: {error_body}") from err
    except urllib.error.URLError as err:
        raise UniFuncsDeepSearchError(f"Network error: {err.reason}") from err
    except json.JSONDecodeError as err:
        raise UniFuncsDeepSearchError(f"Invalid JSON response: {err}") from err


def require_ok(response: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure API response code is successful and return data object."""
    code = response.get("code", -1)
    if code != 0:
        message = response.get("message", "Unknown API error")
        raise UniFuncsDeepSearchError(f"API error [{code}]: {message}")
    data = response.get("data")
    if not isinstance(data, dict):
        raise UniFuncsDeepSearchError("API response missing object field: data")
    return data


def render_data(data: Dict[str, Any], raw_response: bool) -> str:
    """Format query_task data for CLI output."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    validate_args(args)
    api_key = get_api_key()
    try:
        response = get_json(QUERY_TASK_ENDPOINT, {"task_id": args.task_id}, api_key)
        data = require_ok(response)
        print(render_data(data, args.raw_response))
    except UniFuncsDeepSearchError as err:
        print(f"Deep Search query_task failed: {err}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCanceled by user.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
