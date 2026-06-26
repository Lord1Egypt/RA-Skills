"""Shared HTTP helper for stocki-financial-reader scripts.

Reads STOCKI_GATEWAY_URL and STOCKI_API_KEY from env. Provides
gateway_request() and handle_error(). stdlib-only (urllib + json).
Exit code mapping (uniform with doctor/diagnose):
  0 = ok
  1 = auth invalid (auth_missing / auth_invalid)
  2 = unreachable (TCP/DNS, URLError)
  3 = stocki unavailable (5xx, timeout)
  4 = rate limited / quota exceeded
"""

import json
import os
import socket
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _env():
    base = os.environ.get("STOCKI_GATEWAY_URL", "").rstrip("/")
    key = os.environ.get("STOCKI_API_KEY", "")
    if not base or not key:
        missing = [n for n, v in (("STOCKI_GATEWAY_URL", base), ("STOCKI_API_KEY", key)) if not v]
        print(f"Missing env: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    return base, key


def handle_error(code, message, details=None):
    if code in ("auth_missing", "auth_invalid"):
        print(f"Auth error: {message}", file=sys.stderr)
        sys.exit(1)
    if code == "stocki_unavailable":
        print(f"Stocki unavailable: {message}", file=sys.stderr)
        sys.exit(3)
    if code in ("rate_limited", "quota_exceeded"):
        retry = (details or {}).get("retry_after", "")
        suffix = f" (retry after {retry}s)" if retry else ""
        print(f"Rate limited: {message}{suffix}", file=sys.stderr)
        sys.exit(4)
    if code == "unreachable":
        print(f"Unreachable: {message}", file=sys.stderr)
        sys.exit(2)
    print(f"Error [{code}]: {message}", file=sys.stderr)
    sys.exit(1)


def gateway_request(method, path, body=None, timeout=30):
    base, key = _env()
    url = f"{base}{path}"
    headers = {"Authorization": f"Bearer {key}"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8"))
            handle_error(err.get("error", "unknown"), err.get("message", str(e)), err.get("details"))
        except (ValueError, UnicodeDecodeError):
            if e.code == 401:
                handle_error("auth_invalid", e.reason)
            elif e.code == 429:
                handle_error("rate_limited", e.reason)
            elif e.code >= 500:
                handle_error("stocki_unavailable", f"{e.code} {e.reason}")
            else:
                handle_error("unknown", f"HTTP {e.code} {e.reason}")
    except (TimeoutError, socket.timeout) as e:
        handle_error("stocki_unavailable", f"timeout: {e}")
    except URLError as e:
        # URLError may wrap a timeout via .reason — check before classifying.
        # Explicit if/else (not fall-through) so behavior doesn't silently break
        # if handle_error is ever refactored to not exit.
        if isinstance(getattr(e, "reason", None), (TimeoutError, socket.timeout)):
            handle_error("stocki_unavailable", f"timeout: {e.reason}")
        else:
            handle_error("unreachable", str(e))
    except OSError as e:
        handle_error("unreachable", str(e))
