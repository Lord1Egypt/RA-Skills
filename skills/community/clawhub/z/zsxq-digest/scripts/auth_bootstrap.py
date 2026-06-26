#!/usr/bin/env python3
import argparse
import json
import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_COOKIE_NAME = "zsxq_access_token"
DEFAULT_STATE_VERSION = 1
DEFAULT_QR_TTL_SEC = 180


class BootstrapError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def plus_seconds_iso(seconds: int) -> str:
    return (datetime.now().astimezone() + timedelta(seconds=seconds)).isoformat(timespec="seconds")


def load_json(path: Path, default: Any = None):
    if not path.exists():
        if default is not None:
            return default
        raise BootstrapError("AUTH_BOOTSTRAP_REQUIRED", f"state file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise BootstrapError("QUERY_FAILED", f"failed to parse JSON file {path}: {e}")


def atomic_write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def normalize_state(state: dict) -> dict:
    if not isinstance(state, dict):
        raise BootstrapError("QUERY_FAILED", "state file must contain a JSON object")
    return {
        "version": int(state.get("version", DEFAULT_STATE_VERSION)),
        "session_id": state.get("session_id") or str(uuid.uuid4()),
        "status": state.get("status") or "AUTH_BOOTSTRAP_REQUIRED",
        "started_at": state.get("started_at") or now_iso(),
        "updated_at": now_iso(),
        "expires_at": state.get("expires_at"),
        "mode": state.get("mode") or "auth-bootstrap",
        "browser": state.get("browser") if isinstance(state.get("browser"), dict) else {},
        "artifacts": state.get("artifacts") if isinstance(state.get("artifacts"), dict) else {},
        "notes": state.get("notes") if isinstance(state.get("notes"), list) else [],
    }


def load_state(path: Path) -> dict:
    return normalize_state(load_json(path, default={}))


def save_state(path: Path, state: dict) -> dict:
    normalized = normalize_state(state)
    atomic_write_json(path, normalized)
    return normalized


def append_note(state: dict, text: str):
    notes = list(state.get("notes") or [])
    notes.append({"at": now_iso(), "text": text})
    state["notes"] = notes[-20:]


def flatten_cookie_payload(payload: Any) -> List[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("cookies", "items", "result"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        if {"name", "value"}.issubset(set(payload.keys())):
            return [payload]
    raise BootstrapError("AUTH_CAPTURE_UNVERIFIED", "cookie payload must be a list or an object containing a cookies array")


def pick_token_cookie(cookies: List[dict], cookie_name: str) -> dict:
    matches = []
    for cookie in cookies:
        name = str(cookie.get("name") or cookie.get("cookie_name") or "")
        value = cookie.get("value") or cookie.get("cookie_value")
        domain = str(cookie.get("domain") or "")
        if name == cookie_name and value:
            matches.append({
                "name": name,
                "value": str(value),
                "domain": domain or ".zsxq.com",
                "path": cookie.get("path") or "/",
                "source": cookie,
            })
    if not matches:
        raise BootstrapError("AUTH_CAPTURE_UNVERIFIED", f"cookie {cookie_name!r} not found in capture")
    preferred = [c for c in matches if "zsxq.com" in c["domain"]]
    return preferred[0] if preferred else matches[0]


def write_token_file(path: Path, cookie: dict, source: str, user_agent: str = None):
    data = {
        "kind": "cookie",
        "cookie_name": cookie["name"],
        "cookie_value": cookie["value"],
        "domain": cookie.get("domain") or ".zsxq.com",
        "source": source,
        "captured_at": now_iso(),
        "note": "stored locally only; do not commit",
    }
    if user_agent:
        data["user_agent"] = user_agent
    atomic_write_json(path, data)
    return data


def cmd_init(args):
    state = {
        "version": DEFAULT_STATE_VERSION,
        "session_id": args.session_id or str(uuid.uuid4()),
        "status": "AUTH_BOOTSTRAP_REQUIRED",
        "started_at": now_iso(),
        "updated_at": now_iso(),
        "expires_at": plus_seconds_iso(args.qr_ttl_sec),
        "mode": "auth-bootstrap",
        "browser": {
            "profile": args.profile,
            "target_id": args.target_id,
        },
        "artifacts": {},
        "notes": [],
    }
    append_note(state, "bootstrap initialized")
    state = save_state(Path(args.state_file), state)
    return {
        "status": state["status"],
        "session_id": state["session_id"],
        "state_file": args.state_file,
        "expires_at": state["expires_at"],
    }


def cmd_qr_ready(args):
    state = load_state(Path(args.state_file))
    state["status"] = "QR_READY"
    state["expires_at"] = plus_seconds_iso(args.qr_ttl_sec)
    browser = dict(state.get("browser") or {})
    if args.profile:
        browser["profile"] = args.profile
    if args.target_id:
        browser["target_id"] = args.target_id
    if args.page_url:
        browser["page_url"] = args.page_url
    state["browser"] = browser
    artifacts = dict(state.get("artifacts") or {})
    if args.qr_image_path:
        artifacts["qr_image_path"] = args.qr_image_path
    if args.qr_image_url:
        artifacts["qr_image_url"] = args.qr_image_url
    state["artifacts"] = artifacts
    append_note(state, "QR prepared for user scan")
    state = save_state(Path(args.state_file), state)
    return {
        "status": state["status"],
        "session_id": state["session_id"],
        "state_file": args.state_file,
        "expires_at": state["expires_at"],
        "artifacts": state.get("artifacts"),
    }


def cmd_wait(args):
    state = load_state(Path(args.state_file))
    state["status"] = "AUTH_WAITING_CONFIRMATION"
    if args.note:
        append_note(state, args.note)
    else:
        append_note(state, "waiting for user confirmation")
    state = save_state(Path(args.state_file), state)
    return {
        "status": state["status"],
        "session_id": state["session_id"],
        "state_file": args.state_file,
    }


def cmd_capture_unverified(args):
    state = load_state(Path(args.state_file))
    state["status"] = "AUTH_CAPTURE_UNVERIFIED"
    browser = dict(state.get("browser") or {})
    if args.page_url:
        browser["page_url"] = args.page_url
    state["browser"] = browser
    append_note(state, args.note or "QR flow left visible login state; attempt cookie capture")
    state = save_state(Path(args.state_file), state)
    return {
        "status": state["status"],
        "session_id": state["session_id"],
        "state_file": args.state_file,
    }


def cmd_expire(args):
    state = load_state(Path(args.state_file))
    state["status"] = "QR_EXPIRED"
    append_note(state, args.note or "QR expired before confirmation")
    state = save_state(Path(args.state_file), state)
    return {
        "status": state["status"],
        "session_id": state["session_id"],
        "state_file": args.state_file,
    }


def cmd_fallback_manual(args):
    state = load_state(Path(args.state_file))
    state["status"] = "AUTH_BOOTSTRAP_FALLBACK_MANUAL"
    append_note(state, args.note or "fall back to manual token import")
    state = save_state(Path(args.state_file), state)
    return {
        "status": state["status"],
        "session_id": state["session_id"],
        "state_file": args.state_file,
        "next_action": "prepare state/session.token.json manually",
    }


def cmd_finalize_cookies(args):
    state = load_state(Path(args.state_file))
    payload = load_json(Path(args.cookies_file))
    cookies = flatten_cookie_payload(payload)
    token_cookie = pick_token_cookie(cookies, args.cookie_name)
    token = write_token_file(Path(args.token_file), token_cookie, source=args.source, user_agent=args.user_agent)
    state["status"] = "ok"
    artifacts = dict(state.get("artifacts") or {})
    artifacts["token_file"] = args.token_file
    artifacts["cookie_name"] = token["cookie_name"]
    artifacts["cookie_domain"] = token.get("domain")
    state["artifacts"] = artifacts
    append_note(state, f"captured reusable token cookie: {token['cookie_name']}")
    state = save_state(Path(args.state_file), state)
    return {
        "status": "ok",
        "session_id": state["session_id"],
        "state_file": args.state_file,
        "token_file": args.token_file,
        "cookie_name": token["cookie_name"],
        "cookie_domain": token.get("domain"),
        "source": args.source,
    }


def cmd_status(args):
    state = load_state(Path(args.state_file))
    return state


def build_parser():
    parser = argparse.ArgumentParser(description="Manage zsxq-digest auth bootstrap state and token capture")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init")
    init_p.add_argument("--state-file", required=True)
    init_p.add_argument("--session-id")
    init_p.add_argument("--profile", default="chrome")
    init_p.add_argument("--target-id")
    init_p.add_argument("--qr-ttl-sec", type=int, default=DEFAULT_QR_TTL_SEC)
    init_p.set_defaults(func=cmd_init)

    qr_p = sub.add_parser("qr-ready")
    qr_p.add_argument("--state-file", required=True)
    qr_p.add_argument("--profile")
    qr_p.add_argument("--target-id")
    qr_p.add_argument("--page-url")
    qr_p.add_argument("--qr-image-path")
    qr_p.add_argument("--qr-image-url")
    qr_p.add_argument("--qr-ttl-sec", type=int, default=DEFAULT_QR_TTL_SEC)
    qr_p.set_defaults(func=cmd_qr_ready)

    wait_p = sub.add_parser("wait")
    wait_p.add_argument("--state-file", required=True)
    wait_p.add_argument("--note")
    wait_p.set_defaults(func=cmd_wait)

    capture_p = sub.add_parser("capture-unverified")
    capture_p.add_argument("--state-file", required=True)
    capture_p.add_argument("--page-url")
    capture_p.add_argument("--note")
    capture_p.set_defaults(func=cmd_capture_unverified)

    expire_p = sub.add_parser("expire")
    expire_p.add_argument("--state-file", required=True)
    expire_p.add_argument("--note")
    expire_p.set_defaults(func=cmd_expire)

    fallback_p = sub.add_parser("fallback-manual")
    fallback_p.add_argument("--state-file", required=True)
    fallback_p.add_argument("--note")
    fallback_p.set_defaults(func=cmd_fallback_manual)

    fin_p = sub.add_parser("finalize-cookies")
    fin_p.add_argument("--state-file", required=True)
    fin_p.add_argument("--cookies-file", required=True)
    fin_p.add_argument("--token-file", required=True)
    fin_p.add_argument("--cookie-name", default=DEFAULT_COOKIE_NAME)
    fin_p.add_argument("--source", default="browser-bootstrap")
    fin_p.add_argument("--user-agent")
    fin_p.set_defaults(func=cmd_finalize_cookies)

    status_p = sub.add_parser("status")
    status_p.add_argument("--state-file", required=True)
    status_p.set_defaults(func=cmd_status)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except BootstrapError as e:
        print(json.dumps({
            "status": e.status,
            "message": e.message,
            "mode": "auth-bootstrap",
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
