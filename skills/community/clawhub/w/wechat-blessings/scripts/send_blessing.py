#!/usr/bin/env python3
"""Preview and send an already-approved blessing through the private operations gateway."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from typing import Any


class UsageError(ValueError):
    pass


def emit(value: Any, *, stream=sys.stdout) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True), file=stream)


def targets_from(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        for item in value.replace("\n", ",").split(","):
            item = item.strip()
            if item and item not in seen:
                seen.add(item)
                result.append(item)
    if not result:
        raise UsageError("at least one --target is required")
    if len(result) > 500:
        raise UsageError("at most 500 distinct targets are allowed")
    return result


def validate_schedule(value: str) -> str:
    value = value.strip()
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise UsageError("--send-at must use YYYY-MM-DD HH:MM:SS") from exc
    return value


def confirmation_code(operation_type: str, payload: dict[str, Any]) -> str:
    raw = json.dumps(
        {"operationType": operation_type, "payload": payload},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12].upper()


def post_operation(operation_type: str, payload: dict[str, Any], code: str, timeout: float) -> Any:
    url = os.getenv("WX_OPENCLAW_OPS_URL", "").strip()
    token = os.getenv("WX_OPENCLAW_OPS_TOKEN", "").strip()
    if not url or not token:
        raise UsageError("WX_OPENCLAW_OPS_URL and WX_OPENCLAW_OPS_TOKEN are required for execution")
    request_id = f"skill-{uuid.uuid4().hex}"
    request = urllib.request.Request(
        url,
        data=json.dumps(
            {
                "version": "1.0",
                "requestId": request_id,
                "operationType": operation_type,
                "channel": "OPENCLAW",
                "payload": payload,
            },
            ensure_ascii=False,
        ).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "X-Confirmation-Code": code,
            "User-Agent": "wechat-blessings/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:2000]
        raise RuntimeError(f"operations gateway returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"operations gateway is unreachable: {exc.reason}") from exc
    try:
        return {"requestId": request_id, "gatewayResponse": json.loads(raw)}
    except json.JSONDecodeError as exc:
        raise RuntimeError("operations gateway returned non-JSON data") from exc


def build_operation(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    targets = targets_from(args.target)
    text = args.text.strip()
    if not text:
        raise UsageError("--text is required")
    if args.send_at:
        return "MASS_SEND_SCHEDULE", {
            "targets": targets,
            "text": text,
            "publishAt": validate_schedule(args.send_at),
            "intervalSeconds": max(0.0, args.interval_seconds),
            "pauseBot": True,
        }
    if len(targets) == 1:
        return "SEND_TEXT", {
            "targetType": args.target_type,
            "targetId": targets[0],
            "text": text,
        }
    return "MASS_SEND_TEXT", {
        "targets": targets,
        "text": text,
        "intervalSeconds": max(0.0, args.interval_seconds),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", action="append", required=True)
    parser.add_argument("--target-type", choices=("CONTACT", "GROUP"), default="CONTACT")
    parser.add_argument("--text", required=True)
    parser.add_argument("--send-at", default="")
    parser.add_argument("--interval-seconds", type=float, default=1.2)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm", default="")
    parser.add_argument("--timeout", type=float, default=35.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        operation_type, payload = build_operation(args)
        code = confirmation_code(operation_type, payload)
        output: dict[str, Any] = {
            "mode": "execute" if args.execute else "preview",
            "confirmationRequired": True,
            "confirmationCode": code,
            "operationType": operation_type,
            "payload": payload,
        }
        if not args.execute:
            emit(output)
            return 0
        if args.confirm.strip().upper() != code:
            raise UsageError("confirmation code does not match this exact blessing and recipient list")
        output["result"] = post_operation(operation_type, payload, code, args.timeout)
        emit(output)
        return 0
    except UsageError as exc:
        emit({"ok": False, "error": "INVALID_REQUEST", "message": str(exc)}, stream=sys.stderr)
        return 2
    except Exception as exc:
        emit({"ok": False, "error": "EXECUTION_FAILED", "message": str(exc)}, stream=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
