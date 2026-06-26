#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent
AUTH = ROOT / "auth_bootstrap.py"
PREPARE = ROOT / "prepare_zsxq_qr_bootstrap.js"
PROBE = ROOT / "probe_wechat_qr_state.js"


class SyncError(Exception):
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
            raise SyncError(payload.get("status", "QUERY_FAILED"), payload.get("message", "command failed"), payload)
        raise SyncError("QUERY_FAILED", proc.stderr.strip() or proc.stdout.strip() or "command failed")
    if isinstance(payload, dict):
        return payload
    raise SyncError("QUERY_FAILED", f"failed to parse JSON output from: {' '.join(cmd)}")


def ensure_state(args) -> dict:
    state_path = Path(args.state_file)
    if state_path.exists():
        return run_json([sys.executable, str(AUTH), "status", "--state-file", args.state_file])
    return run_json([
        sys.executable,
        str(AUTH),
        "init",
        "--state-file",
        args.state_file,
        "--profile",
        args.profile,
        "--qr-ttl-sec",
        str(args.qr_ttl_sec),
    ])


def call_qr_ready(args, page_url: Optional[str] = None, qr_image_url: Optional[str] = None) -> dict:
    cmd = [
        sys.executable,
        str(AUTH),
        "qr-ready",
        "--state-file",
        args.state_file,
        "--profile",
        args.profile,
        "--qr-ttl-sec",
        str(args.qr_ttl_sec),
    ]
    if page_url:
        cmd += ["--page-url", page_url]
    if qr_image_url:
        cmd += ["--qr-image-url", qr_image_url]
    return run_json(cmd)


def main():
    parser = argparse.ArgumentParser(description="Synchronize zsxq auth bootstrap state using browser CDP helper scripts")
    parser.add_argument("--state-file", required=True)
    parser.add_argument("--profile", default="chrome")
    parser.add_argument("--qr-ttl-sec", type=int, default=180)
    parser.add_argument("--zsxq-ws-url")
    parser.add_argument("--wechat-ws-url")
    args = parser.parse_args()

    try:
        actions: List[dict] = []
        ensure_state(args)

        prepare_payload = None
        if args.zsxq_ws_url:
            prepare_payload = run_json(["node", str(PREPARE), "--ws-url", args.zsxq_ws_url])
            actions.append({"step": "prepare_zsxq", "result": prepare_payload})
            if prepare_payload.get("status") == "QR_READY":
                qr_state = call_qr_ready(args, page_url=prepare_payload.get("url"))
                actions.append({"step": "mark_qr_ready_from_zsxq", "result": qr_state})

        probe_payload = None
        if args.wechat_ws_url:
            probe_payload = run_json(["node", str(PROBE), "--ws-url", args.wechat_ws_url])
            actions.append({"step": "probe_wechat_qr", "result": probe_payload})
            status = probe_payload.get("status")
            if status == "QR_READY":
                qr_state = call_qr_ready(args, page_url=probe_payload.get("url"), qr_image_url=probe_payload.get("qr_image_url"))
                actions.append({"step": "mark_qr_ready_from_wechat", "result": qr_state})
            elif status == "AUTH_WAITING_CONFIRMATION":
                wait_state = run_json([
                    sys.executable,
                    str(AUTH),
                    "wait",
                    "--state-file",
                    args.state_file,
                    "--note",
                    "wechat qr scanned; waiting for confirmation",
                ])
                actions.append({"step": "mark_waiting_confirmation", "result": wait_state})
            elif status == "QR_EXPIRED":
                expire_state = run_json([
                    sys.executable,
                    str(AUTH),
                    "expire",
                    "--state-file",
                    args.state_file,
                    "--note",
                    "wechat qr expired; refresh bootstrap",
                ])
                actions.append({"step": "mark_qr_expired", "result": expire_state})
            elif status == "AUTH_CAPTURE_UNVERIFIED":
                capture_state = run_json([
                    sys.executable,
                    str(AUTH),
                    "capture-unverified",
                    "--state-file",
                    args.state_file,
                    "--page-url",
                    probe_payload.get("url") or "",
                    "--note",
                    "wechat flow left QR state; attempt cookie capture on the logged-in zsxq page",
                ])
                actions.append({"step": "mark_capture_unverified", "result": capture_state})

        final_state = run_json([sys.executable, str(AUTH), "status", "--state-file", args.state_file])

        next_hint = None
        if probe_payload and probe_payload.get("status") == "QR_READY":
            next_hint = "send the QR image to the user and wait for scan"
        elif probe_payload and probe_payload.get("status") == "AUTH_WAITING_CONFIRMATION":
            next_hint = "user has likely scanned the code; wait for WeChat confirmation and then capture cookies"
        elif probe_payload and probe_payload.get("status") == "AUTH_CAPTURE_UNVERIFIED":
            next_hint = "QR flow is no longer visible; attempt cookie capture on the logged-in zsxq page"
        elif prepare_payload and prepare_payload.get("iframe_url") and not args.wechat_ws_url:
            next_hint = "open the returned iframe_url as its own browser tab, then rerun with --wechat-ws-url"
        elif final_state.get("status") == "QR_EXPIRED":
            next_hint = "refresh QR bootstrap and resend a fresh QR"

        result = {
            "status": "ok",
            "state_file": args.state_file,
            "current_status": final_state.get("status"),
            "session_id": final_state.get("session_id"),
            "actions": actions,
            "next_hint": next_hint,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SyncError as e:
        print(json.dumps({
            "status": e.status,
            "message": e.message,
            "mode": "auth-bootstrap-sync",
            "details": e.payload,
        }, ensure_ascii=False, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
