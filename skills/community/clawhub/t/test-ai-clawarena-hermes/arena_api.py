#!/usr/bin/env python3
"""Thin ClawArena API helper for OpenClaw skill commands.

This script centralizes:
- connection token loading from ~/.clawarena/token
- UTF-8 JSON request encoding
- minimal GET/POST calls for the active gameplay loop

It intentionally does not contain any game-specific logic.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request


DEFAULT_API_BASE = "https://clawarena.halochain.xyz/api/v1"
DEFAULT_TOKEN_PATH = Path.home() / ".clawarena" / "token"


def emit_json(payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    sys.stdout.write("\n")


def load_token(token_path: Path) -> str:
    try:
        token = token_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing connection token: {token_path}") from exc
    if not token:
        raise SystemExit(f"Empty connection token: {token_path}")
    return token


def parse_json_or_text(raw: bytes) -> Any:
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def api_request(
    method: str,
    url: str,
    *,
    token: str | None = None,
    payload: Any | None = None,
    timeout: float = 30.0,
) -> tuple[bool, str | dict[str, Any]]:
    headers = {"Accept": "application/json"}
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        text = raw.decode("utf-8")
        if not text.endswith("\n"):
            text += "\n"
        return True, text
    except error.HTTPError as exc:
        body = exc.read()
        return False, {
            "error": "http_error",
            "http_status": exc.code,
            "body": parse_json_or_text(body),
        }
    except (error.URLError, TimeoutError, socket.timeout) as exc:
        return False, {
            "error": "network_error",
            "detail": str(exc),
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ClawArena API helper with stable token loading and UTF-8 JSON transport."
    )
    parser.add_argument(
        "--api-base",
        default=DEFAULT_API_BASE,
        help=f"API base URL (default: {DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--token-path",
        default=str(DEFAULT_TOKEN_PATH),
        help=f"Connection token path (default: {DEFAULT_TOKEN_PATH})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    poll = subparsers.add_parser("poll", help="GET /agents/game/")
    poll.add_argument("--wait", type=int, default=0, help="wait query parameter")
    poll.add_argument(
        "--consume-history",
        type=int,
        choices=(0, 1),
        default=1,
        help="consume_history query parameter",
    )

    action = subparsers.add_parser(
        "action",
        help="POST /agents/action/ with payload from stdin or --payload",
    )
    action.add_argument(
        "--payload",
        help="JSON action payload string. Prefer stdin/heredoc for non-ASCII content.",
    )

    reflection = subparsers.add_parser(
        "reflection-context",
        help="GET /agents/strategy-reflection/ for a finished match",
    )
    reflection.add_argument("--match-id", required=True, type=int, help="Finished match id")

    save_prompt = subparsers.add_parser(
        "save-strategy-prompt",
        help="POST /agents/strategy-prompt/ with payload from stdin or --payload",
    )
    save_prompt.add_argument(
        "--payload",
        help="JSON payload string. Prefer stdin/heredoc for non-ASCII content.",
    )

    return parser


def load_json_payload(payload_arg: str | None, *, label: str = "payload") -> Any:
    if payload_arg is not None:
        return json.loads(payload_arg)
    raw = sys.stdin.read()
    if not raw.strip():
        raise SystemExit(f"Missing {label}. Provide JSON on stdin or with --payload.")
    return json.loads(raw)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    token_path = Path(args.token_path).expanduser()

    if args.command == "poll":
        token = load_token(token_path)
        query = parse.urlencode(
            {
                "wait": args.wait,
                "consume_history": args.consume_history,
            }
        )
        ok, result = api_request(
            "GET",
            f"{args.api_base}/agents/game/?{query}",
            token=token,
            timeout=args.timeout,
        )
    elif args.command == "action":
        token = load_token(token_path)
        try:
            payload = load_json_payload(args.payload, label="action payload")
        except json.JSONDecodeError as exc:
            emit_json(
                {
                    "error": "invalid_json",
                    "detail": exc.msg,
                    "line": exc.lineno,
                    "column": exc.colno,
                    "position": exc.pos,
                }
            )
            return 0
        ok, result = api_request(
            "POST",
            f"{args.api_base}/agents/action/",
            token=token,
            payload=payload,
            timeout=args.timeout,
        )
    elif args.command == "reflection-context":
        token = load_token(token_path)
        query = parse.urlencode({"match_id": args.match_id})
        ok, result = api_request(
            "GET",
            f"{args.api_base}/agents/strategy-reflection/?{query}",
            token=token,
            timeout=args.timeout,
        )
    elif args.command == "save-strategy-prompt":
        token = load_token(token_path)
        try:
            payload = load_json_payload(args.payload, label="strategy prompt payload")
        except json.JSONDecodeError as exc:
            emit_json(
                {
                    "error": "invalid_json",
                    "detail": exc.msg,
                    "line": exc.lineno,
                    "column": exc.colno,
                    "position": exc.pos,
                }
            )
            return 0
        ok, result = api_request(
            "POST",
            f"{args.api_base}/agents/strategy-prompt/",
            token=token,
            payload=payload,
            timeout=args.timeout,
        )
    else:
        parser.error(f"Unsupported command: {args.command}")
        return 2

    if ok:
        sys.stdout.write(result)
    else:
        emit_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
