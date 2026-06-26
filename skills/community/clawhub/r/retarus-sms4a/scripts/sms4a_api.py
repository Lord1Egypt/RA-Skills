#!/usr/bin/env python3
"""
Helper for the Retarus SMS for Applications REST API.

Supports:
- Sending a simple SMS job or a full payload file
- Fetching per-recipient status for a job ID
- Optional version checks for safe connectivity testing
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request

BASE_URLS = {
    "de1": "https://sms4a.de1.retarus.com/rest/v1",
    "de2": "https://sms4a.de2.retarus.com/rest/v1",
    "eu": "https://sms4a.eu.retarus.com/rest/v1",
}
STATUS_AUTO_ORDER = ("de2", "de1")
DEFAULT_TIMEOUT = 30
DEFAULT_SECRET_PATHS = (
    Path("~/.openclaw/secrets/retarus-sms4a.env").expanduser(),
    Path("~/.openclaw/secrets/retarus-sms4a.json").expanduser(),
)


class Sms4aError(Exception):
    """Base error for this helper."""


class CredentialError(Sms4aError):
    """Raised when credentials cannot be resolved."""


class ApiResponseError(Sms4aError):
    """Raised when the API returns an unsuccessful response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        datacenter: str | None = None,
        base_url: str | None = None,
        body: Any = None,
        attempts: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.datacenter = datacenter
        self.base_url = base_url
        self.body = body
        self.attempts = attempts or []


def add_shared_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--username", help="SMS4A username")
    parser.add_argument("--password", help="SMS4A password")
    parser.add_argument(
        "--secret-file",
        help="Path to a JSON or .env-style secret file containing username/password",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retarus SMS4A helper for send and status operations."
    )
    add_shared_options(parser)

    subparsers = parser.add_subparsers(dest="command", required=True)

    send_parser = subparsers.add_parser("send", help="Send an SMS job")
    add_shared_options(send_parser)
    send_parser.add_argument(
        "--datacenter",
        choices=("de1", "de2", "eu"),
        default="eu",
        help="Target datacenter for send requests (default: eu)",
    )
    send_parser.add_argument(
        "--payload-file",
        help="Path to a JSON file containing a full JobRequest payload",
    )
    send_parser.add_argument("--text", help="SMS body for a simple one-message job")
    send_parser.add_argument(
        "--recipient",
        action="append",
        default=[],
        help="Recipient mobile number; repeat for multiple recipients",
    )
    send_parser.add_argument("--src", help="Sender ID")
    send_parser.add_argument(
        "--encoding",
        choices=("STANDARD", "UTF-16"),
        help="Encoding for the SMS job",
    )
    send_parser.add_argument("--billcode", help="Billing code")
    send_parser.add_argument(
        "--status-requested",
        action="store_true",
        help="Request delivery notifications",
    )
    send_parser.add_argument(
        "--flash",
        action="store_true",
        help="Send as flash SMS",
    )
    send_parser.add_argument("--customer-ref", help="Customer reference")
    send_parser.add_argument(
        "--validity-min",
        type=int,
        help="SMS validity in minutes",
    )
    send_parser.add_argument(
        "--max-parts",
        type=int,
        help="Maximum number of message parts",
    )
    send_parser.add_argument(
        "--invalid-characters",
        choices=("REFUSE", "REPLACE", "TO_UTF16", "TRANSLITERATE"),
        help="Invalid character handling mode",
    )
    send_parser.add_argument(
        "--qos",
        choices=("EXPRESS", "NORMAL"),
        help="Quality of service",
    )
    send_parser.add_argument(
        "--job-period",
        help="Schedule timestamp in ISO-8601 format",
    )
    send_parser.add_argument(
        "--duplicate-detection",
        action="store_true",
        help="Enable duplicate detection",
    )
    send_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prepared request without sending it",
    )

    status_parser = subparsers.add_parser(
        "status", help="Fetch recipient delivery status for a job ID"
    )
    add_shared_options(status_parser)
    status_parser.add_argument(
        "--datacenter",
        choices=("auto", "de1", "de2", "eu"),
        default="auto",
        help="Datacenter selection for status lookups (default: auto)",
    )
    status_parser.add_argument("--job-id", required=True, help="Retarus job ID")
    status_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the lookup plan without making HTTP requests",
    )

    version_parser = subparsers.add_parser(
        "version", help="Fetch /version for a connectivity check"
    )
    add_shared_options(version_parser)
    version_parser.add_argument(
        "--datacenter",
        choices=("de1", "de2", "eu"),
        default="eu",
        help="Datacenter for the version request (default: eu)",
    )
    version_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned request without making the HTTP call",
    )

    return parser.parse_args()


def load_secret_file(secret_path: str) -> tuple[str | None, str | None]:
    path = Path(secret_path).expanduser()
    if not path.is_file():
        raise CredentialError(f"Secret file not found: {path}")

    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise CredentialError(f"Secret file is empty: {path}")

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = parse_env_secret(raw)

    if not isinstance(parsed, dict):
        raise CredentialError(f"Unsupported secret file format: {path}")

    username = first_non_empty(
        parsed.get("username"),
        parsed.get("user"),
        parsed.get("RETARUS_SMS4A_USERNAME"),
    )
    password = first_non_empty(
        parsed.get("password"),
        parsed.get("pass"),
        parsed.get("RETARUS_SMS4A_PASSWORD"),
    )
    return username, password


def parse_env_secret(raw: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def first_non_empty(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def resolve_credentials(args: argparse.Namespace) -> tuple[str, str, str]:
    env_user = os.getenv("RETARUS_SMS4A_USERNAME")
    env_password = os.getenv("RETARUS_SMS4A_PASSWORD")

    secret_user = None
    secret_password = None
    secret_path = first_non_empty(args.secret_file, os.getenv("RETARUS_SMS4A_SECRET_FILE"))
    if not secret_path:
        for candidate in DEFAULT_SECRET_PATHS:
            if candidate.is_file():
                secret_path = str(candidate)
                break
    if secret_path:
        secret_user, secret_password = load_secret_file(secret_path)

    username = first_non_empty(args.username, env_user, secret_user)
    password = first_non_empty(args.password, env_password, secret_password)

    if username and password:
        source = "cli"
        if not args.username and not args.password and env_user and env_password:
            source = "environment"
        elif not args.username and not args.password and secret_user and secret_password:
            source = f"secret-file:{Path(secret_path).expanduser()}"
        return username, password, source

    raise CredentialError(
        "Missing credentials. Use --username/--password, "
        "RETARUS_SMS4A_USERNAME/RETARUS_SMS4A_PASSWORD, or a secret file."
    )


def request_json(
    *,
    method: str,
    base_url: str,
    path: str,
    username: str,
    password: str,
    timeout: int,
    payload: dict[str, Any] | None = None,
) -> tuple[int, Any]:
    url = f"{base_url.rstrip('/')}{path}"
    headers = {
        "Accept": "application/json",
        "Authorization": build_auth_header(username, password),
    }
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")

    req = request.Request(url=url, method=method, headers=headers, data=body)

    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
            return response.status, decode_body(raw_body)
    except error.HTTPError as exc:
        raw_body = exc.read().decode("utf-8", errors="replace")
        raise ApiResponseError(
            f"API request failed with status {exc.code}",
            status_code=exc.code,
            base_url=base_url,
            body=decode_body(raw_body),
        ) from exc
    except error.URLError as exc:
        raise ApiResponseError(
            f"Transport error while calling {url}: {exc.reason}",
            base_url=base_url,
        ) from exc


def build_auth_header(username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def decode_body(raw_body: str) -> Any:
    if not raw_body:
        return None
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body


def build_send_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.payload_file:
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise Sms4aError("Payload file must contain a JSON object")
        return payload

    if not args.text:
        raise Sms4aError("Provide --text for a simple send or use --payload-file")
    if not args.recipient:
        raise Sms4aError(
            "Provide at least one --recipient for a simple send or use --payload-file"
        )

    payload: dict[str, Any] = {
        "messages": [
            {
                "text": args.text,
                "recipients": [{"dst": recipient} for recipient in args.recipient],
            }
        ]
    }

    options: dict[str, Any] = {}
    if args.src:
        options["src"] = args.src
    if args.encoding:
        options["encoding"] = args.encoding
    if args.billcode:
        options["billcode"] = args.billcode
    if args.status_requested:
        options["statusRequested"] = True
    if args.flash:
        options["flash"] = True
    if args.customer_ref:
        options["customerRef"] = args.customer_ref
    if args.validity_min is not None:
        options["validityMin"] = args.validity_min
    if args.max_parts is not None:
        options["maxParts"] = args.max_parts
    if args.invalid_characters:
        options["invalidCharacters"] = args.invalid_characters
    if args.qos:
        options["qos"] = args.qos
    if args.job_period:
        options["jobPeriod"] = args.job_period
    if args.duplicate_detection:
        options["duplicateDetection"] = True
    if options:
        payload["options"] = options

    return payload


def status_targets(datacenter: str) -> list[tuple[str, str]]:
    if datacenter in ("auto", "eu"):
        return [(name, BASE_URLS[name]) for name in STATUS_AUTO_ORDER]
    secondary = "de1" if datacenter == "de2" else "de2"
    return [
        (datacenter, BASE_URLS[datacenter]),
        (secondary, BASE_URLS[secondary]),
    ]


def handle_send(args: argparse.Namespace) -> dict[str, Any]:
    payload = build_send_payload(args)
    base_url = BASE_URLS[args.datacenter]

    if args.dry_run:
        return {
            "operation": "send",
            "dryRun": True,
            "datacenter": args.datacenter,
            "baseUrl": base_url,
            "payload": payload,
        }

    username, password, credential_source = resolve_credentials(args)
    status_code, body = request_json(
        method="POST",
        base_url=base_url,
        path="/jobs",
        username=username,
        password=password,
        timeout=args.timeout,
        payload=payload,
    )
    return {
        "operation": "send",
        "datacenter": args.datacenter,
        "baseUrl": base_url,
        "credentialSource": credential_source,
        "statusCode": status_code,
        "jobId": body.get("jobId") if isinstance(body, dict) else None,
        "response": body,
    }


def handle_status(args: argparse.Namespace) -> dict[str, Any]:
    targets = status_targets(args.datacenter)

    if args.dry_run:
        return {
            "operation": "status",
            "dryRun": True,
            "jobId": args.job_id,
            "targets": [
                {"datacenter": datacenter, "baseUrl": base_url}
                for datacenter, base_url in targets
            ],
        }

    username, password, credential_source = resolve_credentials(args)
    attempts: list[dict[str, Any]] = []

    for datacenter, base_url in targets:
        try:
            status_code, body = request_json(
                method="GET",
                base_url=base_url,
                path=f"/sms?jobId={parse.quote(args.job_id, safe='')}",
                username=username,
                password=password,
                timeout=args.timeout,
            )
            return {
                "operation": "status",
                "jobId": args.job_id,
                "credentialSource": credential_source,
                "successfulDatacenter": datacenter,
                "baseUrl": base_url,
                "statusCode": status_code,
                "attempts": attempts + [{"datacenter": datacenter, "statusCode": status_code}],
                "response": body,
            }
        except ApiResponseError as exc:
            attempt = {
                "datacenter": datacenter,
                "baseUrl": base_url,
                "statusCode": exc.status_code,
                "body": exc.body,
            }
            attempts.append(attempt)
            if exc.status_code in (400, 401):
                raise ApiResponseError(
                    "Status lookup failed with a non-retriable response",
                    status_code=exc.status_code,
                    datacenter=datacenter,
                    base_url=base_url,
                    body=exc.body,
                    attempts=attempts,
                ) from exc

    raise ApiResponseError(
        "Status lookup failed in all candidate datacenters",
        attempts=attempts,
        body={"jobId": args.job_id},
    )


def handle_version(args: argparse.Namespace) -> dict[str, Any]:
    base_url = BASE_URLS[args.datacenter]

    if args.dry_run:
        return {
            "operation": "version",
            "dryRun": True,
            "datacenter": args.datacenter,
            "baseUrl": base_url,
        }

    username, password, credential_source = resolve_credentials(args)
    status_code, body = request_json(
        method="GET",
        base_url=base_url,
        path="/version",
        username=username,
        password=password,
        timeout=args.timeout,
    )
    return {
        "operation": "version",
        "datacenter": args.datacenter,
        "baseUrl": base_url,
        "credentialSource": credential_source,
        "statusCode": status_code,
        "response": body,
    }


def emit_json(payload: dict[str, Any], pretty: bool) -> None:
    indent = 2 if pretty else None
    print(json.dumps(payload, indent=indent, sort_keys=pretty))


def emit_error(exc: Exception, pretty: bool) -> None:
    payload: dict[str, Any] = {"error": str(exc)}
    if isinstance(exc, ApiResponseError):
        if exc.status_code is not None:
            payload["statusCode"] = exc.status_code
        if exc.datacenter:
            payload["datacenter"] = exc.datacenter
        if exc.base_url:
            payload["baseUrl"] = exc.base_url
        if exc.body is not None:
            payload["response"] = exc.body
        if exc.attempts:
            payload["attempts"] = exc.attempts
    indent = 2 if pretty else None
    print(json.dumps(payload, indent=indent, sort_keys=pretty), file=sys.stderr)


def main() -> int:
    args = parse_args()
    pretty = args.pretty or getattr(args, "dry_run", False)

    try:
        if args.command == "send":
            emit_json(handle_send(args), pretty)
        elif args.command == "status":
            emit_json(handle_status(args), pretty)
        elif args.command == "version":
            emit_json(handle_version(args), pretty)
        else:
            raise Sms4aError(f"Unsupported command: {args.command}")
        return 0
    except Exception as exc:
        emit_error(exc, pretty)
        return 1


if __name__ == "__main__":
    sys.exit(main())
