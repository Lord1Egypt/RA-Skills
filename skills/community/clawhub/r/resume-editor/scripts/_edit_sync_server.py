#!/usr/bin/env python3
"""
Tiny local-only HTTP server used by the resume edit mode to write browser
edits back to the source resume.json on disk.

Started as a background subprocess by generate_html.py when an editable HTML
is exported. The page POSTs the edited JSON to /sync; the server validates
the target path matches the one it was started with, then writes atomically.

Safety:
- Binds to 127.0.0.1 only (not exposed to the network).
- Refuses to write any path other than the single resume JSON it was told to
  serve at startup.
- Requires a bearer token that the parent process generates and passes both
  to this server and to the page.

Lifecycle:
- Parent prints `RESUME_SYNC_PORT=<port>` and `RESUME_SYNC_TOKEN=<token>` on
  stdout once the socket is bound; the parent reads these to embed in the
  HTML. The server then runs until it receives POST /shutdown or its parent
  process dies (it ignores SIGINT and exits cleanly on SIGTERM).
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import socket
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def _send_json(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(target_path: Path, token: str):
    target_resolved = target_path.expanduser().resolve()

    class SyncHandler(BaseHTTPRequestHandler):
        # Quiet logging — keep stdout clean so the parent can parse the
        # startup banner. Errors still go to stderr.
        def log_message(self, fmt, *args):
            return

        def _check_token(self):
            auth = self.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return False
            return secrets.compare_digest(auth[len("Bearer "):].strip(), token)

        def do_OPTIONS(self):
            # Allow the page's fetch() preflight.
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
            self.end_headers()

        def do_POST(self):
            if not self._check_token():
                _send_json(self, 403, {"ok": False, "error": "forbidden"})
                return

            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
            try:
                payload = json.loads(raw.decode("utf-8")) if raw else {}
            except Exception as exc:
                _send_json(self, 400, {"ok": False, "error": f"invalid JSON: {exc}"})
                return

            if self.path == "/shutdown":
                _send_json(self, 200, {"ok": True})
                # Defer shutdown so the response flushes first.
                def _stop():
                    try:
                        self.server.shutdown()
                    except Exception:
                        pass
                import threading
                threading.Thread(target=_stop, daemon=True).start()
                return

            if self.path != "/sync":
                _send_json(self, 404, {"ok": False, "error": "not found"})
                return

            requested_path = payload.get("path", "")
            try:
                requested_resolved = Path(requested_path).expanduser().resolve()
            except Exception:
                _send_json(self, 400, {"ok": False, "error": "invalid path"})
                return

            if requested_resolved != target_resolved:
                _send_json(self, 403, {"ok": False, "error": "path not allowed"})
                return

            data = payload.get("data")
            if not isinstance(data, (dict, list)):
                _send_json(self, 400, {"ok": False, "error": "data must be object or array"})
                return

            try:
                target_resolved.parent.mkdir(parents=True, exist_ok=True)
                # Atomic write: temp file in same dir, then rename.
                fd, tmp_path = tempfile.mkstemp(
                    prefix=target_resolved.name + ".",
                    suffix=".tmp",
                    dir=str(target_resolved.parent),
                )
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                        f.write("\n")
                    os.replace(tmp_path, target_resolved)
                except Exception:
                    try:
                        os.unlink(tmp_path)
                    except OSError:
                        pass
                    raise
            except Exception as exc:
                _send_json(self, 500, {"ok": False, "error": f"write failed: {exc}"})
                return

            _send_json(self, 200, {"ok": True, "path": str(target_resolved)})

    return SyncHandler


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main():
    parser = argparse.ArgumentParser(description="Resume edit-mode sync server")
    parser.add_argument("--target", required=True, help="Absolute path to resume.json to serve writes for")
    parser.add_argument("--port", type=int, default=0, help="Port (0 = pick free)")
    parser.add_argument("--token", default="", help="Bearer token; random if omitted")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    token = args.token or secrets.token_urlsafe(24)
    port = args.port or find_free_port()

    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(target, token))

    # Signal the parent. Keep this exact format — generate_html.py parses it.
    print(f"RESUME_SYNC_PORT={port}")
    print(f"RESUME_SYNC_TOKEN={token}")
    print(f"RESUME_SYNC_TARGET={target}")
    sys.stdout.flush()

    def _term(*_):
        # serve_forever() blocks the main thread; calling shutdown() from a
        # signal handler in the same thread would deadlock (shutdown blocks
        # until serve_forever returns). Instead, force-exit. The server has
        # no in-flight state worth preserving between requests.
        try:
            server.server_close()
        except Exception:
            pass
        os._exit(0)
    signal.signal(signal.SIGTERM, _term)
    signal.signal(signal.SIGINT, _term)

    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
