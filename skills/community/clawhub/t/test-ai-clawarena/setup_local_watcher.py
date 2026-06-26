#!/usr/bin/env python3
"""Prepare and launch the ClawArena local watcher."""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request


CLAW_DIR = Path.home() / ".clawarena"
TOKEN_PATH = CLAW_DIR / "token"
AGENT_ID_PATH = CLAW_DIR / "agent_id"
DELIVERY_CONFIG_PATH = CLAW_DIR / "openclaw_delivery.json"
WATCHER_PID_PATH = CLAW_DIR / "watcher.pid"
WATCHER_LOG_PATH = CLAW_DIR / "watcher.log"
API_BASE = "https://clawarena.halochain.xyz/api/v1"
RECOVERY_REDEEM_URL = f"{API_BASE}/agents/connection-recovery/redeem/"


def stable_subprocess_cwd() -> str:
    for candidate in (Path.home(), Path("/tmp"), Path("/")):
        if candidate.exists() and candidate.is_dir():
            return str(candidate)
    return "/"


def atomic_write(path: Path, content: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(content)
    tmp_path.replace(path)
    if mode is not None:
        path.chmod(mode)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    return {}


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def require_runtime_credentials() -> dict[str, str]:
    missing: list[str] = []
    values: dict[str, str] = {}
    for key, path in {"token": TOKEN_PATH, "agent_id": AGENT_ID_PATH}.items():
        if not path.exists():
            missing.append(str(path))
            continue
        value = path.read_text().strip()
        if not value:
            missing.append(str(path))
            continue
        values[key] = value
    if missing:
        raise SystemExit(
            "ClawArena watcher setup requires a provisioned agent first. "
            "Save ~/.clawarena/token and ~/.clawarena/agent_id before running setup. "
            f"Missing or empty: {', '.join(missing)}"
        )
    return values


def decode_connection_token_agent_id(connection_token: str) -> str:
    import base64

    padded = connection_token + ("=" * ((4 - len(connection_token) % 4) % 4))
    try:
        payload = json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))
        return str(int(payload["a"]))
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Invalid connection token returned by recovery endpoint: {exc}") from exc


def redeem_recovery_key(recovery_key: str) -> dict[str, str]:
    payload = json.dumps({"recovery_key": recovery_key}).encode("utf-8")
    req = request.Request(
        RECOVERY_REDEEM_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Recovery key redemption failed ({exc.code}): {detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Recovery key redemption failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Recovery endpoint returned invalid JSON: {exc}") from exc

    connection_token = str(data.get("connection_token") or "").strip()
    agent_id = str(data.get("agent_id") or "").strip()
    if not connection_token:
        raise SystemExit("Recovery endpoint did not return a connection_token.")
    decoded_agent_id = decode_connection_token_agent_id(connection_token)
    if agent_id and agent_id != decoded_agent_id:
        raise SystemExit("Recovery endpoint returned mismatched agent IDs.")
    return {
        "token": connection_token,
        "agent_id": agent_id or decoded_agent_id,
        "agent_name": str(data.get("agent_name") or ""),
    }


def write_runtime_credentials(credentials: dict[str, str]) -> None:
    atomic_write(TOKEN_PATH, credentials["token"].strip() + "\n", 0o600)
    atomic_write(AGENT_ID_PATH, credentials["agent_id"].strip() + "\n", 0o600)


def stop_existing_watcher() -> None:
    if not WATCHER_PID_PATH.exists():
        return
    try:
        pid = int(WATCHER_PID_PATH.read_text().strip())
    except ValueError:
        WATCHER_PID_PATH.unlink(missing_ok=True)
        return
    if process_alive(pid):
        os.kill(pid, signal.SIGTERM)
        for _ in range(20):
            if not process_alive(pid):
                break
            time.sleep(0.2)
    WATCHER_PID_PATH.unlink(missing_ok=True)


def write_delivery_config(args: argparse.Namespace) -> dict[str, Any]:
    existing = read_json(DELIVERY_CONFIG_PATH)
    channel = args.channel or existing.get("channel")
    target = args.to or existing.get("to")
    reply_account = args.reply_account or existing.get("reply_account")
    if not channel or not target:
        raise SystemExit(
            "channel and to are required on first setup; reruns can reuse the saved config."
        )
    config = {
        "channel": channel,
        "to": target,
    }
    if reply_account:
        config["reply_account"] = reply_account
    atomic_write(
        DELIVERY_CONFIG_PATH,
        json.dumps(config, indent=2, sort_keys=True) + "\n",
        0o600,
    )
    return config


def verify_delivery(config: dict[str, Any]) -> dict[str, Any]:
    cmd = [
        "openclaw",
        "agent",
        "--message",
        "ClawArena delivery test. Reply with exactly: ClawArena delivery OK.",
        "--deliver",
        "--channel",
        str(config["channel"]),
        "--to",
        str(config["to"]),
        "--json",
    ]
    reply_account = config.get("reply_account")
    if reply_account:
        cmd.extend(["--reply-account", str(reply_account)])

    try:
        proc = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
            cwd=stable_subprocess_cwd(),
        )
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Delivery verification failed: {exc}") from exc

    output = (proc.stdout or proc.stderr or "").strip()
    result = {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output": output[:1000],
    }
    if proc.returncode != 0:
        raise SystemExit(
            "Delivery verification failed. OpenClaw could not deliver back "
            f"to this chat. Output: {output[:1000]}"
        )
    return result


def start_watcher(skill_root: Path) -> int:
    WATCHER_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    watcher_path = skill_root / "watcher.py"
    with WATCHER_LOG_PATH.open("ab") as log_file:
        proc = subprocess.Popen(  # noqa: S603
            [sys.executable, str(watcher_path)],
            stdout=log_file,
            stderr=log_file,
            cwd=str(skill_root),
            start_new_session=True,
        )
    WATCHER_PID_PATH.write_text(f"{proc.pid}\n")
    return proc.pid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set up the ClawArena local watcher")
    parser.add_argument("--channel", help="Active OpenClaw channel for delivery, e.g. telegram")
    parser.add_argument("--to", help="Active chat target, e.g. a Telegram numeric chat id")
    parser.add_argument(
        "--recovery-key",
        help="One-use recovery key from Command Center. Redeems it, saves fresh credentials, and restarts the watcher.",
    )
    parser.add_argument(
        "--connection-token",
        help="Fresh connection token to save before starting the watcher. Prefer --recovery-key for user recovery.",
    )
    parser.add_argument("--agent-id", help="Agent id for --connection-token. If omitted, it is decoded from the token.")
    parser.add_argument(
        "--reply-account",
        help="Optional OpenClaw account id for outbound delivery",
    )
    parser.add_argument(
        "--verify-delivery",
        action="store_true",
        help="Send a short OpenClaw delivery test to the configured chat before starting the watcher.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Managed-runtime mode. Save credentials and start the watcher without delivery config.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent
    recovery_applied = False
    if args.recovery_key:
        credentials = redeem_recovery_key(args.recovery_key)
        write_runtime_credentials(credentials)
        recovery_applied = True
    elif args.connection_token:
        credentials = {
            "token": args.connection_token,
            "agent_id": args.agent_id or decode_connection_token_agent_id(args.connection_token),
        }
        write_runtime_credentials(credentials)
        recovery_applied = True
    else:
        credentials = require_runtime_credentials()
    if args.headless:
        config = {}
        delivery_verification = None
    else:
        config = write_delivery_config(args)
        delivery_verification = verify_delivery(config) if args.verify_delivery else None
    stop_existing_watcher()
    pid = start_watcher(skill_root)
    print(
        json.dumps(
            {
                "watcher_started": True,
                "recovery_applied": recovery_applied,
                "pid": pid,
                "agent_id": credentials["agent_id"],
                "headless": args.headless,
                "channel": config.get("channel"),
                "to": config.get("to"),
                "reply_account": config.get("reply_account"),
                "delivery_verification": delivery_verification,
                "watcher_script": str(skill_root / "watcher.py"),
                "log_file": str(WATCHER_LOG_PATH),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
