#!/usr/bin/env python3
"""
Shared client module for TencentCloud Oceanus CLI.

Provides:
- TC3-HMAC-SHA256 signature implementation (zero external dependencies)
- Generic API call function supporting all Oceanus cloud APIs
- Output formatting (json / table / text)
- Safety confirmation logic (TTY interactive prompt / non-TTY error)
- Standardized response envelope
- Input validation utilities
"""

import hashlib
import hmac
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

API_VERSION = "2019-04-22"
SERVICE = "oceanus"
_DEFAULT_HOST = "oceanus.tencentcloudapi.com"
HOST = os.environ.get("OCEANUS_ENDPOINT", _DEFAULT_HOST)
ENDPOINT = f"https://{HOST}"
DEFAULT_USER_AGENT = "TencentCloud-Agent-Skills/tencentcloud-oceanus-ops"


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


def get_credentials():
    """Return (secret_id, secret_key) from environment variables.

    Raises SystemExit with structured error if not configured.
    """
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not secret_id or not secret_key:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": {
                        "code": "MissingCredentials",
                        "message": (
                            "TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY "
                            "environment variables are required."
                        ),
                    },
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    return secret_id, secret_key


# ---------------------------------------------------------------------------
# TC3-HMAC-SHA256 Signature
# ---------------------------------------------------------------------------


def _hmac_sha256(key, msg):
    """HMAC-SHA256 sign. key is bytes, msg is str or bytes."""
    if isinstance(msg, str):
        msg = msg.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).digest()


def _build_authorization(
    secret_id,
    secret_key,
    service,
    date,
    timestamp,
    payload,
):
    """Build the TC3-HMAC-SHA256 Authorization header value."""
    # Step 1: Canonical Request
    http_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    content_type = "application/json; charset=utf-8"
    signed_headers = "content-type;host"
    hashed_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    canonical_request = (
        f"{http_method}\n"
        f"{canonical_uri}\n"
        f"{canonical_querystring}\n"
        f"content-type:{content_type}\n"
        f"host:{HOST}\n\n"
        f"{signed_headers}\n"
        f"{hashed_payload}"
    )

    # Step 2: String to Sign
    credential_scope = f"{date}/{service}/tc3_request"
    hashed_canonical = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()

    string_to_sign = (
        f"TC3-HMAC-SHA256\n"
        f"{timestamp}\n"
        f"{credential_scope}\n"
        f"{hashed_canonical}"
    )

    # Step 3: Signing Key
    secret_date = _hmac_sha256(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = _hmac_sha256(secret_date, service)
    secret_signing = _hmac_sha256(secret_service, "tc3_request")

    # Step 4: Signature
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # Step 5: Authorization
    authorization = (
        f"TC3-HMAC-SHA256 "
        f"Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    return authorization


# ---------------------------------------------------------------------------
# Generic API call
# ---------------------------------------------------------------------------


def call_api(action, params, region, version=API_VERSION, service=SERVICE):
    """Call a TencentCloud API action with TC3-HMAC-SHA256 signature.

    Args:
        action: API action name (e.g. "CreateJob", "DescribeJobs")
        params: Request parameters as dict
        region: Region string (e.g. "ap-guangzhou")
        version: API version (default "2019-04-22")
        service: Service name (default "oceanus")

    Returns:
        Standardized response envelope dict.
    """
    secret_id, secret_key = get_credentials()

    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    payload = json.dumps(params)

    # Build authorization
    authorization = _build_authorization(
        secret_id, secret_key, service, date, str(timestamp), payload
    )

    # Build request headers
    connect_timeout = int(os.environ.get("OCEANUS_API_CONNECT_TIMEOUT", "10"))
    read_timeout = int(os.environ.get("OCEANUS_API_READ_TIMEOUT", "60"))

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": HOST,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version,
        "X-TC-Region": region,
        "User-Agent": DEFAULT_USER_AGENT,
    }

    # Optional: Token for temporary credentials
    token = os.environ.get("TENCENTCLOUD_SECURITY_TOKEN", "")
    if token:
        headers["X-TC-Token"] = token

    try:
        req = Request(
            ENDPOINT,
            data=payload.encode("utf-8"),
            headers=headers,
            method="POST",
        )
        resp = urlopen(req, timeout=max(connect_timeout, read_timeout))
        resp_body = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        try:
            resp_body = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return error_response(
                action,
                "HttpError",
                f"HTTP {e.code}: {body[:500]}",
            )
    except URLError as e:
        return error_response(action, "NetworkError", str(e.reason))
    except Exception as e:
        if os.environ.get("OCEANUS_CLI_DEBUG"):
            traceback.print_exc(file=sys.stderr)
        return error_response(action, "RequestError", str(e))

    # Parse TencentCloud API response format
    response = resp_body.get("Response", {})
    error = response.get("Error")
    request_id = response.get("RequestId", "")

    if error:
        return error_response(
            action,
            error.get("Code", "UnknownError"),
            error.get("Message", "Unknown error"),
            request_id,
        )

    # Remove RequestId from data to avoid duplication
    data = {k: v for k, v in response.items() if k != "RequestId"}
    return success_response(action, data, request_id)


# ---------------------------------------------------------------------------
# Standardised response helpers
# ---------------------------------------------------------------------------


def success_response(operation, data, request_id=""):
    """Build a success envelope dict."""
    return {
        "success": True,
        "operation": operation,
        "data": data,
        "request_id": request_id,
    }


def error_response(operation, code, message, request_id=""):
    """Build an error envelope dict."""
    return {
        "success": False,
        "operation": operation,
        "error": {"code": code, "message": message},
        "request_id": request_id,
    }


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def output(result, fmt="json"):
    """Print *result* envelope to stdout in the requested format."""
    if fmt == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif fmt == "table":
        _print_table(result)
    elif fmt == "text":
        _print_text(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result.get("success") else 1)


def _print_table(result):
    """Pretty-print *result* as an aligned table."""
    if not result.get("success"):
        err = result.get("error", {})
        print(
            f"ERROR [{err.get('code', '?')}]: {err.get('message', '?')}",
            file=sys.stderr,
        )
        return

    data = result.get("data")
    if data is None:
        print("(no data)")
        return

    rows = _extract_rows(data)
    if rows is None:
        for k, v in (data if isinstance(data, dict) else {}).items():
            print(f"{k}: {v}")
        return

    if not rows:
        print("(empty)")
        return

    if isinstance(rows[0], dict):
        cols = list(rows[0].keys())
        widths = {c: len(c) for c in cols}
        str_rows = []
        for r in rows:
            sr = {}
            for c in cols:
                val = str(r.get(c, ""))
                sr[c] = val
                widths[c] = max(widths[c], len(val))
            str_rows.append(sr)

        header = "  ".join(c.upper().ljust(widths[c]) for c in cols)
        print(header)
        for sr in str_rows:
            print("  ".join(sr[c].ljust(widths[c]) for c in cols))
    else:
        for r in rows:
            print(r)


def _print_text(result):
    """Print tab-separated values suitable for piping."""
    if not result.get("success"):
        err = result.get("error", {})
        print(f"{err.get('code', '?')}\t{err.get('message', '?')}", file=sys.stderr)
        return

    data = result.get("data")
    if data is None:
        return

    rows = _extract_rows(data)
    if rows is None:
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"{k}\t{v}")
        return

    for r in rows:
        if isinstance(r, dict):
            print("\t".join(str(v) for v in r.values()))
        else:
            print(r)


def _extract_rows(data):
    """Try to find a list of records inside *data*."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                return v
    return None


# ---------------------------------------------------------------------------
# Safety confirmation
# ---------------------------------------------------------------------------


def require_confirmation(operation, message, flag_present):
    """
    Check the safety confirmation gate.

    If *flag_present* is True the caller already passed --confirm
    and we proceed silently.

    Otherwise:
      - In an interactive TTY -> prompt the user.
      - In a non-interactive pipe / agent context -> return an error dict.

    Returns None on success (proceed) or an error-dict to output and abort.
    """
    if flag_present:
        return None

    if sys.stdin.isatty() and sys.stdout.isatty():
        print(f"\n\u26a0\ufe0f  {message}", file=sys.stderr)
        answer = input("    Proceed? [y/N]: ")
        if answer.strip().lower() in ("y", "yes"):
            return None
        return error_response(operation, "Cancelled", "User cancelled the operation.")

    return error_response(
        operation,
        "SafetyCheckRequired",
        f"{message} Add --confirm to proceed.",
    )


# ---------------------------------------------------------------------------
# Input validation helpers
# ---------------------------------------------------------------------------


def require_args(args, *names):
    """
    Validate that every *name* is present (not None / empty) on *args*.
    Returns None if OK, or an error-dict describing the first missing param.
    """
    for name in names:
        val = getattr(args, name, None)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            return error_response(
                getattr(args, "subcommand", "unknown"),
                "ValidationError",
                f"Parameter '--{name}' is required.",
            )
    return None


# ---------------------------------------------------------------------------
# Common argparse helpers
# ---------------------------------------------------------------------------


def add_common_args(parser):
    """Add common global flags to *parser*."""
    parser.add_argument(
        "--region",
        help="Region (e.g. ap-guangzhou, ap-beijing)",
    )
    parser.add_argument(
        "--workspace_id",
        help="Workspace SerialId (e.g. space-xxxx)",
    )
    parser.add_argument(
        "-o", "--output",
        choices=["json", "table", "text"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show request details",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress status messages",
    )
