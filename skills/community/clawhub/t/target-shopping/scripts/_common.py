"""Shared HTTP client and helpers for Target's public-facing API.

Uses stdlib urllib only (zero deps) so the skill stays small and portable.
All scripts emit JSON to stdout; errors emit JSON with an "error" key and
exit non-zero.
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://redsky.target.com/redsky_aggregations/v1/web"

# Public static key baked into target.com's JS bundle. Not a secret.
# Override with TARGET_API_KEY if Target rotates it.
DEFAULT_KEY = "9f36aeafbe60771e321a7cc95a78140772ab3e96"

# San Jose Central — same fallback target.com uses when no store is set.
DEFAULT_STORE_ID = "2281"

DEFAULT_USER_AGENT = "target-com-shopper-skill/0.1 (+https://github.com/openclaw)"

# Stable visitor_id — required by plp_search_v2 (NonNull). Random 32+ chars.
DEFAULT_VISITOR_ID = "0000000000000000000000000000000000"


def get_key() -> str:
    return os.environ.get("TARGET_API_KEY", DEFAULT_KEY).strip()


def get_user_agent() -> str:
    return os.environ.get("TARGET_USER_AGENT", DEFAULT_USER_AGENT).strip()


def get_default_store() -> str:
    return os.environ.get("TARGET_DEFAULT_STORE_ID", DEFAULT_STORE_ID).strip()


def get_timeout() -> float:
    try:
        return float(os.environ.get("TARGET_HTTP_TIMEOUT", "10"))
    except ValueError:
        return 10.0


def get_min_interval() -> float:
    try:
        return float(os.environ.get("TARGET_MIN_INTERVAL", "1.0"))
    except ValueError:
        return 1.0


_last_call_ts: float = 0.0


def _throttle() -> None:
    """Enforce TARGET_MIN_INTERVAL seconds between successive requests."""
    global _last_call_ts
    interval = get_min_interval()
    elapsed = time.monotonic() - _last_call_ts
    if elapsed < interval:
        time.sleep(interval - elapsed)
    _last_call_ts = time.monotonic()


def api_get(
    operation: str,
    params: dict[str, Any],
    *,
    base: str = BASE_URL,
    retries: int = 2,
    backoff: float = 2.0,
) -> dict[str, Any]:
    """GET a public-API operation and return the parsed JSON body.

    Treats HTTP 200 and 206 (Partial Content, normal for plp_search_v2) as success.
    Retries on 5xx and network errors with exponential backoff. Does not retry on 4xx.
    """
    # Always inject the public key.
    full_params = {"key": get_key(), **{k: v for k, v in params.items() if v is not None}}
    qs = urllib.parse.urlencode(full_params, doseq=True)
    url = f"{base}/{operation}?{qs}"

    headers = {
        "User-Agent": get_user_agent(),
        "Accept": "application/json",
        "Origin": "https://www.target.com",
        "Referer": "https://www.target.com/",
    }

    last_err: Exception | None = None
    for attempt in range(retries + 1):
        _throttle()
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=get_timeout(), context=ctx) as resp:
                status = resp.status
                body = resp.read()
                if status in (200, 206):
                    return json.loads(body.decode("utf-8"))
                # Non-2xx but not raised — treat as error.
                raise _http_error(status, body, url)
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            if 500 <= e.code < 600 and attempt < retries:
                last_err = e
                time.sleep(backoff ** attempt)
                continue
            raise _http_error(e.code, body, url) from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt < retries:
                last_err = e
                time.sleep(backoff ** attempt)
                continue
            raise RuntimeError(f"network error: {e}") from e
    raise RuntimeError(f"unreachable; last_err={last_err}")


def _http_error(status: int, body: bytes, url: str) -> RuntimeError:
    snippet = body[:300].decode("utf-8", errors="replace")
    hint = {
        400: "bad request — check required params (visitor_id, key) or operation name",
        404: "not found — invalid TCIN or operation path",
        410: "endpoint removed — check references/endpoints.md for current name",
        429: "rate limited — slow down (TARGET_MIN_INTERVAL)",
        403: "blocked — IP may be throttled or behind WAF",
    }.get(status, "unexpected status")
    return RuntimeError(f"HTTP {status} from {url}: {hint}; body={snippet}")


def emit(payload: dict[str, Any]) -> None:
    """Print JSON to stdout, sorted keys, 2-space indent."""
    json.dump(payload, sys.stdout, indent=2, sort_keys=False, ensure_ascii=False)
    sys.stdout.write("\n")


def fail(message: str, *, status: int | None = None, hint: str | None = None) -> None:
    """Emit error JSON to stdout and exit non-zero."""
    payload: dict[str, Any] = {"error": message}
    if status is not None:
        payload["status"] = status
    if hint:
        payload["hint"] = hint
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    sys.exit(1)


def safe_get(d: Any, *path: str | int, default: Any = None) -> Any:
    """Walk a nested dict/list path, returning default on any miss."""
    cur: Any = d
    for key in path:
        if cur is None:
            return default
        try:
            cur = cur[key]
        except (KeyError, IndexError, TypeError):
            return default
    return cur if cur is not None else default
