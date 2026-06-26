#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parent
STATE_DIR = SKILL_ROOT / "state"
DEFAULT_STATE_FILE = STATE_DIR / "auth-bootstrap.json"
DEFAULT_TOKEN_FILE = STATE_DIR / "session.token.json"
DEFAULT_COOKIES_FILE = STATE_DIR / "captured-cookies.json"
DEFAULT_VERIFY_OUTPUT = STATE_DIR / "groups.probe.json"
DEFAULT_CAPTURE_URLS = ["https://wx.zsxq.com/", "https://wx.zsxq.com/login"]
AUTH = ROOT / "auth_bootstrap.py"
SYNC = ROOT / "sync_auth_bootstrap.py"
CAPTURE = ROOT / "capture_browser_cookies.js"
COLLECT = ROOT / "collect_from_session.py"


class WorkflowError(Exception):
    def __init__(self, status: str, message: str, payload: Optional[dict] = None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.payload = payload or {}


def parse_json_output(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {}
    return json.loads(text)


def run_json(cmd: List[str]) -> dict:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    payload = None
    for candidate in (proc.stdout, proc.stderr):
        try:
            if candidate and candidate.strip():
                payload = parse_json_output(candidate)
                break
        except Exception:
            continue
    if proc.returncode != 0:
        if isinstance(payload, dict):
            raise WorkflowError(payload.get("status", "QUERY_FAILED"), payload.get("message", "command failed"), payload)
        raise WorkflowError("QUERY_FAILED", proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(cmd)}")
    if isinstance(payload, dict):
        return payload
    raise WorkflowError("QUERY_FAILED", f"failed to parse JSON output from: {' '.join(cmd)}")


def sync_phase(args) -> dict:
    cmd = [
        sys.executable,
        str(SYNC),
        "--state-file",
        str(args.state_file),
        "--profile",
        args.profile,
        "--qr-ttl-sec",
        str(args.qr_ttl_sec),
    ]
    if args.zsxq_ws_url:
        cmd += ["--zsxq-ws-url", args.zsxq_ws_url]
    if args.wechat_ws_url:
        cmd += ["--wechat-ws-url", args.wechat_ws_url]
    return run_json(cmd)


def finalize_phase(args) -> dict:
    capture_ws_url = args.capture_ws_url or args.zsxq_ws_url
    if not capture_ws_url:
        raise WorkflowError("QUERY_FAILED", "capture ws url is required for finalize phase")

    capture_cmd = [
        "node",
        str(CAPTURE),
        "--ws-url",
        capture_ws_url,
        "--cookie-name",
        args.cookie_name,
        "--output",
        str(args.cookies_file),
    ]
    capture_urls = args.capture_url or list(DEFAULT_CAPTURE_URLS)
    for url in capture_urls:
        capture_cmd += ["--url", url]
    capture_payload = run_json(capture_cmd)

    finalize_cmd = [
        sys.executable,
        str(AUTH),
        "finalize-cookies",
        "--state-file",
        str(args.state_file),
        "--cookies-file",
        str(args.cookies_file),
        "--token-file",
        str(args.token_file),
        "--cookie-name",
        args.cookie_name,
        "--source",
        args.source,
    ]
    if args.user_agent:
        finalize_cmd += ["--user-agent", args.user_agent]
    finalize_payload = run_json(finalize_cmd)

    verify_payload = None
    verification_warning = None
    if args.verify_mode != "none":
        verify_cmd = [
            sys.executable,
            str(COLLECT),
            "--token-file",
            str(args.token_file),
            "--mode",
            args.verify_mode,
        ]
        if args.verify_mode == "probe":
            if not args.verify_url:
                raise WorkflowError("QUERY_FAILED", "--verify-url is required when --verify-mode=probe")
            verify_cmd += ["--url", args.verify_url]
        if args.verify_output:
            verify_cmd += ["--output", str(args.verify_output)]
        try:
            verify_payload = run_json(verify_cmd)
        except WorkflowError as e:
            verify_payload = {
                "status": e.status,
                "message": e.message,
                "details": e.payload,
            }
            verification_warning = f"token file was written but verification failed: {e.message}"

    return {
        "status": "ok",
        "capture": capture_payload,
        "finalize": finalize_payload,
        "verify": verify_payload,
        "verification_warning": verification_warning,
        "capture_ws_url": capture_ws_url,
        "cookies_file": str(args.cookies_file),
        "token_file": str(args.token_file),
    }


def build_result(sync_payload: Optional[dict], finalize_payload: Optional[dict]) -> dict:
    current_status = None
    session_id = None
    next_hint = None
    result_status = "ok"
    verification_warning = None
    if sync_payload:
        current_status = sync_payload.get("current_status")
        session_id = sync_payload.get("session_id")
        next_hint = sync_payload.get("next_hint")
    if finalize_payload:
        result_status = finalize_payload.get("status", result_status)
        current_status = finalize_payload.get("finalize", {}).get("status", current_status)
        verification_warning = finalize_payload.get("verification_warning")
        if verification_warning:
            next_hint = verification_warning
    return {
        "status": result_status,
        "session_id": session_id,
        "current_status": current_status,
        "sync": sync_payload,
        "finalize": finalize_payload,
        "verification_warning": verification_warning,
        "next_hint": next_hint,
    }


def common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)
    parser.add_argument("--token-file", type=Path, default=DEFAULT_TOKEN_FILE)
    parser.add_argument("--cookies-file", type=Path, default=DEFAULT_COOKIES_FILE)
    parser.add_argument("--verify-output", type=Path, default=DEFAULT_VERIFY_OUTPUT)
    parser.add_argument("--profile", default="chrome")
    parser.add_argument("--qr-ttl-sec", type=int, default=180)
    parser.add_argument("--zsxq-ws-url")
    parser.add_argument("--wechat-ws-url")
    parser.add_argument("--capture-ws-url")
    parser.add_argument("--capture-url", action="append", default=[])
    parser.add_argument("--cookie-name", default="zsxq_access_token")
    parser.add_argument("--source", default="browser-bootstrap")
    parser.add_argument("--user-agent")
    parser.add_argument("--verify-mode", choices=["none", "groups", "probe"], default="groups")
    parser.add_argument("--verify-url")


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified browser-assisted bootstrap workflow for zsxq-digest")
    sub = parser.add_subparsers(dest="command", required=True)

    sync_p = sub.add_parser("sync", help="prepare / probe QR state and update auth-bootstrap.json")
    common_args(sync_p)

    finalize_p = sub.add_parser("finalize", help="capture cookies, finalize token, and verify token mode")
    common_args(finalize_p)

    run_p = sub.add_parser("run", help="run sync first, then optionally finalize if capture is requested")
    common_args(run_p)
    run_p.add_argument("--auto-finalize", action="store_true")

    args = parser.parse_args()

    try:
        sync_payload = None
        finalize_payload = None

        if args.command in ("sync", "run"):
            sync_payload = sync_phase(args)

        if args.command == "finalize":
            finalize_payload = finalize_phase(args)
        elif args.command == "run":
            should_finalize = args.auto_finalize or bool(args.capture_ws_url)
            if should_finalize:
                finalize_payload = finalize_phase(args)

        print(json.dumps(build_result(sync_payload, finalize_payload), ensure_ascii=False, indent=2))
    except WorkflowError as e:
        print(json.dumps({
            "status": e.status,
            "message": e.message,
            "mode": "browser-bootstrap-workflow",
            "details": e.payload,
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
