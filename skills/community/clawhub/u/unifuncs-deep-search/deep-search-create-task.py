#!/usr/bin/env python3
"""
UniFuncs Deep Search create_task client.
Usage: ./deep-search-create-task.py "query" [options]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

CREATE_TASK_ENDPOINT = "https://api.unifuncs.com/deepsearch/v1/create_task"
DEFAULT_MODEL = "s3"
DEFAULT_REQUEST_TIMEOUT_SECONDS = 180


class UniFuncsDeepSearchError(Exception):
    """Raised when the UniFuncs Deep Search API call fails."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="UniFuncs Deep Search create_task client")
    parser.add_argument("query", help="User query sent to Deep Search.")
    parser.add_argument(
        "--model",
        choices=["s1", "s2", "s3"],
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument("--language", choices=["zh", "en"], help="Output language.")
    parser.add_argument(
        "--reference-style",
        choices=["link", "character", "hidden"],
        help="Reference marker style.",
    )
    parser.add_argument("--max-depth", type=int, help="Maximum research depth.")
    parser.add_argument("--domain-scope", type=str, help="Comma-separated domain allowlist.")
    parser.add_argument("--domain-blacklist", type=str, help="Comma-separated domain blocklist.")
    parser.add_argument("--output-prompt", type=str, help="Custom output prompt template.")
    parser.add_argument("--important-urls", type=str, help="Comma-separated important URLs.")
    parser.add_argument("--important-keywords", type=str, help="Comma-separated important keywords.")
    parser.add_argument("--important-prompt", type=str, help="Important prompt content.")
    parser.add_argument("--introduction", type=str, help="Researcher role/tone introduction.")
    parser.add_argument("--push-to-share", action="store_true", help="Push result to share space.")
    parser.add_argument("--set-public", action="store_true", help="Set result as public.")
    parser.add_argument(
        "--raw-response",
        action="store_true",
        help="Print full API response JSON instead of task_id.",
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
    if not args.query.strip():
        print("Error: query cannot be empty.", file=sys.stderr)
        sys.exit(1)
    if args.max_depth is not None and args.max_depth <= 0:
        print("Error: max-depth must be greater than 0.", file=sys.stderr)
        sys.exit(1)


def split_csv(value: Optional[str]) -> Optional[list[str]]:
    """Split comma-separated input into a trimmed list."""
    if not value:
        return None
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or None


def build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    """Build request payload for create_task."""
    payload: Dict[str, Any] = {
        "model": args.model,
        "messages": [{"role": "user", "content": args.query}],
    }
    if args.introduction:
        payload["introduction"] = args.introduction
    if args.language:
        payload["language"] = args.language
    if args.reference_style:
        payload["reference_style"] = args.reference_style
    if args.max_depth is not None:
        payload["max_depth"] = args.max_depth
    if args.domain_scope:
        payload["domain_scope"] = split_csv(args.domain_scope)
    if args.domain_blacklist:
        payload["domain_blacklist"] = split_csv(args.domain_blacklist)
    if args.output_prompt:
        payload["output_prompt"] = args.output_prompt
    if args.important_urls:
        payload["important_urls"] = split_csv(args.important_urls)
    if args.important_keywords:
        payload["important_keywords"] = split_csv(args.important_keywords)
    if args.important_prompt:
        payload["important_prompt"] = args.important_prompt
    if args.push_to_share:
        payload["push_to_share"] = True
    if args.set_public:
        payload["set_public"] = True
    return payload


def post_json(url: str, payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    """POST JSON payload and parse JSON response."""
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
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


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    validate_args(args)
    api_key = get_api_key()
    try:
        response = post_json(CREATE_TASK_ENDPOINT, build_payload(args), api_key)
        data = require_ok(response)
        if args.raw_response:
            print(json.dumps(response, ensure_ascii=False, indent=2))
            return
        task_id = data.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise UniFuncsDeepSearchError("create_task succeeded but task_id is missing.")
        print(task_id)
    except UniFuncsDeepSearchError as err:
        print(f"Deep Search create_task failed: {err}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCanceled by user.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
