"""
Yuque API client - shared module for all scripts.
Handles authentication (config.json / env var) and HTTP requests.
Zero external dependencies - uses only Python standard library.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# Resolve config relative to the scripts/ directory
_SKILL_DIR = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _SKILL_DIR / "config.json"
_DEFAULT_BASE_URL = "https://www.yuque.com"


def load_config():
    """Load API token and base URL from config.json (priority) or env var (fallback)."""
    api_token = None
    base_url = _DEFAULT_BASE_URL

    # Priority 1: config.json in skill directory
    if _CONFIG_PATH.exists():
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            api_token = config.get("api_token", "").strip() or None
            base_url = config.get("base_url", _DEFAULT_BASE_URL).strip().rstrip("/")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to read {_CONFIG_PATH}: {e}", file=sys.stderr)

    # Priority 2: environment variable
    if not api_token:
        api_token = os.environ.get("YUQUE_TOKEN", "").strip() or None

    if not api_token:
        print(
            "Error: No API token found.\n"
            f"Please either:\n"
            f"  1. Create {_CONFIG_PATH} with your api_token (see config.json.example)\n"
            f"  2. Set the YUQUE_TOKEN environment variable",
            file=sys.stderr,
        )
        sys.exit(1)

    return api_token, base_url


def api_request(method, path, data=None, params=None):
    """
    Make an HTTP request to the Yuque API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: API path, e.g. "/api/v2/user"
        data: Request body dict (for POST/PUT), will be JSON-encoded
        params: Query parameters dict (for GET)

    Returns:
        Parsed JSON response dict

    Raises:
        SystemExit on error
    """
    api_token, base_url = load_config()

    url = f"{base_url}{path}"
    if params:
        query_string = urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None}
        )
        if query_string:
            url = f"{url}?{query_string}"

    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("X-Auth-Token", api_token)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "yuque-skill/1.0")

    try:
        with urllib.request.urlopen(req) as resp:
            resp_body = resp.read().decode("utf-8")
            if resp_body:
                return json.loads(resp_body)
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        error_msg = _format_http_error(e.code, error_body)
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Network error - {e.reason}", file=sys.stderr)
        sys.exit(1)


def _format_http_error(code, body):
    """Format HTTP error into a readable message."""
    messages = {
        400: "Bad request - check your parameters",
        401: "Unauthorized - API token is invalid or expired",
        403: "Forbidden - no permission for this operation",
        404: "Not found - check repo/doc ID",
        422: "Validation failed - check required fields",
        429: "Rate limited - please wait and retry",
        500: "Server error - Yuque internal issue",
    }
    base_msg = messages.get(code, f"HTTP {code}")
    try:
        detail = json.loads(body).get("message", "")
        if detail:
            return f"{base_msg}: {detail}"
    except (json.JSONDecodeError, AttributeError):
        pass
    return base_msg


def output_json(data):
    """Print JSON to stdout for agent consumption."""
    print(json.dumps(data, ensure_ascii=False, indent=2))
