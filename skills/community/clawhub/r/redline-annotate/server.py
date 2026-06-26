#!/usr/bin/env python3
"""
redline local server.

接收浏览器 POST 过来的标注 JSON，写入指定的 inbox 文件。
仅绑定 127.0.0.1，单机使用。

启动:
  python3 server.py [port]

POST /feedback
  body: {"inbox": "/abs/path/.redline-inbox.json", "payload": {...}}
  resp: {"ok": true} | {"ok": false, "error": "..."}

GET /ping
  resp: {"ok": true, "port": <port>}
"""

import http.server
import json
import os
import socketserver
import sys
from pathlib import Path


def is_path_allowed(p: Path) -> bool:
    """只允许写到用户家目录或 /tmp 下，避免任意路径写入。"""
    try:
        p = p.resolve()
    except Exception:
        return False
    home = Path.home().resolve()
    tmp = Path("/tmp").resolve()
    return any(str(p).startswith(str(root) + os.sep) for root in (home, tmp))


class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, body: dict):
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/ping":
            self._json(200, {"ok": True, "port": self.server.server_address[1]})
        else:
            self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        if self.path != "/feedback":
            return self._json(404, {"ok": False, "error": "not found"})

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            body = json.loads(raw)
        except Exception as e:
            return self._json(400, {"ok": False, "error": f"invalid json: {e}"})

        inbox = body.get("inbox")
        payload = body.get("payload")
        if not inbox or not isinstance(payload, dict):
            return self._json(
                400, {"ok": False, "error": "missing inbox or payload"}
            )

        inbox_path = Path(inbox)
        if not is_path_allowed(inbox_path):
            return self._json(
                403, {"ok": False, "error": f"path not allowed: {inbox_path}"}
            )

        try:
            inbox_path.parent.mkdir(parents=True, exist_ok=True)
            inbox_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            return self._json(500, {"ok": False, "error": f"write failed: {e}"})

        self._json(200, {"ok": True, "inbox": str(inbox_path)})

    def log_message(self, *args, **kwargs):
        pass  # silence default access log


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7893
    with ReusableTCPServer(("127.0.0.1", port), Handler) as httpd:
        actual_port = httpd.server_address[1]
        print(f"redline server listening on 127.0.0.1:{actual_port}", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nshutting down")


if __name__ == "__main__":
    main()
