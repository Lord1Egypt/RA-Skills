#!/usr/bin/env python3
"""Wellness Bridge (public HTTPS via Tunnel) — Tier 2 ingest endpoint.

This is a small local HTTP server that accepts signed uploads from a phone-side
exporter (iOS Apple Health / Android Health Connect).

It does NOT scrape phone data itself. The phone exporter reads OS health data
and pushes a daily aggregate JSON into this bridge.

Security model:
- The bridge listens locally (default 127.0.0.1)
- A tunnel (cloudflared/ngrok) exposes it over HTTPS
- Requests must include: Authorization: Bearer <token>

Files:
- Token stored at: ~/.config/openclaw/wellness/bridge/token.json (chmod 600)
- Payloads stored under: ~/.config/openclaw/wellness/bridge/inbox/YYYY-MM-DD/*.json

No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


DEFAULT_STATE_DIR = os.path.expanduser("~/.config/openclaw/wellness/bridge")


def mkdirp(p: str) -> None:
    Path(p).mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def state_dir() -> str:
    return os.environ.get("WELLNESS_BRIDGE_DIR", DEFAULT_STATE_DIR)


def token_file() -> str:
    return os.path.join(state_dir(), "token.json")


def inbox_dir() -> str:
    return os.path.join(state_dir(), "inbox")


def meta_file() -> str:
    return os.path.join(state_dir(), "meta.json")


def load_token() -> Optional[str]:
    p = token_file()
    try:
        doc = json.load(open(p, "r", encoding="utf-8"))
        t = doc.get("token")
        return str(t) if t else None
    except FileNotFoundError:
        return None


def save_token(tok: str) -> str:
    mkdirp(state_dir())
    p = token_file()
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"token": tok, "created_at": now_iso()}, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, p)
    try:
        os.chmod(p, 0o600)
    except PermissionError:
        pass
    return p


def ensure_token(reset: bool = False) -> str:
    if reset:
        tok = secrets.token_urlsafe(32)
        save_token(tok)
        return tok
    existing = load_token()
    if existing:
        return existing
    tok = secrets.token_urlsafe(32)
    save_token(tok)
    return tok


def write_meta(update: Dict[str, Any]) -> None:
    mkdirp(state_dir())
    p = meta_file()
    cur: Dict[str, Any] = {}
    try:
        cur = json.load(open(p, "r", encoding="utf-8"))
    except Exception:
        cur = {}
    cur.update(update)
    cur.setdefault("created_at", now_iso())
    cur["updated_at"] = now_iso()
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, p)


def read_body(handler: BaseHTTPRequestHandler) -> bytes:
    n = int(handler.headers.get("Content-Length", "0") or "0")
    if n <= 0:
        return b""
    return handler.rfile.read(n)


def auth_ok(handler: BaseHTTPRequestHandler, expected_token: str) -> bool:
    auth = handler.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return False
    tok = auth[len("Bearer ") :].strip()
    return secrets.compare_digest(tok, expected_token)


def safe_day(s: str) -> str:
    # YYYY-MM-DD only
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%d")


class Handler(BaseHTTPRequestHandler):
    server_version = "WellnessBridge/0.1"

    def do_GET(self):  # noqa: N802
        if self.path.startswith("/health"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "ts": now_iso()}).encode("utf-8"))
            return

        if self.path.startswith("/status"):
            p = meta_file()
            try:
                doc = json.load(open(p, "r", encoding="utf-8"))
            except Exception:
                doc = {"ok": True, "message": "no meta yet"}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(doc).encode("utf-8"))
            return

        if self.path.startswith("/config"):
            # Non-sensitive config helper for phone exporter setup.
            # Do NOT include token here.
            cfg = {
                "ok": True,
                "endpoints": {
                    "ingest": "/ingest",
                    "health": "/health",
                    "status": "/status",
                    "config": "/config",
                },
                "required_headers": {
                    "Authorization": "Bearer <token>",
                    "Content-Type": "application/json",
                },
                "minimal_payload": {
                    "date": "YYYY-MM-DD",
                    "source": "apple_health|health_connect",
                    "timezone": "IANA/Zone",
                    "generated_at": "ISO-8601",
                    "activity": {"steps": 1234},
                },
                "schema_ref": "references/ingest-protocol.md",
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(cfg).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):  # noqa: N802
        expected = self.server.expected_token  # type: ignore[attr-defined]
        if self.path != "/ingest":
            self.send_response(404)
            self.end_headers()
            return

        if not auth_ok(self, expected):
            self.send_response(401)
            self.end_headers()
            return

        raw = read_body(self)
        try:
            doc = json.loads(raw.decode("utf-8"))
        except Exception:
            self.send_response(400)
            self.end_headers()
            return

        # Expect doc.date, doc.source
        day = safe_day(str(doc.get("date") or ""))
        src = str(doc.get("source") or doc.get("sources_present") or "unknown")

        # Store payload
        target_dir = os.path.join(inbox_dir(), day)
        mkdirp(target_dir)
        fname = f"{int(time.time())}_{secrets.token_hex(4)}.json"
        out_path = os.path.join(target_dir, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, sort_keys=True)
            f.write("\n")

        write_meta({"last_ingest_at": now_iso(), "last_source": src, "last_date": day, "last_file": out_path})

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "stored": out_path}).encode("utf-8"))

    def log_message(self, fmt, *args):
        return


def cmd_init(args: argparse.Namespace) -> None:
    tok = ensure_token(reset=args.reset)
    print("[OK] Wellness Bridge token ready.")
    print(f"Token file: {token_file()}")
    print("\nUse this token in your phone exporter as: Authorization: Bearer <token>")
    print(f"Token: {tok}")


def cmd_run(args: argparse.Namespace) -> None:
    tok = ensure_token(reset=False)
    host = args.host
    port = int(args.port)

    httpd = HTTPServer((host, port), Handler)
    httpd.expected_token = tok  # type: ignore[attr-defined]

    write_meta({"listen": f"http://{host}:{port}", "started_at": now_iso()})

    print("[OK] Wellness Bridge running")
    print(f"Local: http://{host}:{port}")
    print("Endpoints:")
    print("  GET  /health")
    print("  GET  /status")
    print("  POST /ingest  (Authorization: Bearer <token>)")
    print("\nNext: expose it via a tunnel (cloudflared/ngrok). See references/bridge.md")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def cmd_status(args: argparse.Namespace) -> None:
    p = meta_file()
    try:
        doc = json.load(open(p, "r", encoding="utf-8"))
    except Exception:
        doc = {"ok": True, "message": "no status yet"}
    print(json.dumps(doc, indent=2, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_init = sub.add_parser("init", help="Create token (or reset)")
    ap_init.add_argument("--reset", action="store_true")
    ap_init.set_defaults(func=cmd_init)

    ap_run = sub.add_parser("run", help="Run local HTTP ingest server")
    ap_run.add_argument("--host", default="127.0.0.1")
    ap_run.add_argument("--port", default="8787")
    ap_run.set_defaults(func=cmd_run)

    ap_status = sub.add_parser("status", help="Show last ingest meta")
    ap_status.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
