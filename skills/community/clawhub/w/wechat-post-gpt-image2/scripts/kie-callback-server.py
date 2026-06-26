#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from datetime import datetime
import json
import os

HOST = os.environ.get("KIE_CALLBACK_HOST", "0.0.0.0")
PORT = int(os.environ.get("KIE_CALLBACK_PORT", "8787"))
OUT_DIR = Path(os.environ.get("KIE_CALLBACK_DIR", "/root/.openclaw/workspace/temp/kie-callback"))
OUT_DIR.mkdir(parents=True, exist_ok=True)

class Handler(BaseHTTPRequestHandler):
    def _reply(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/healthz", "/kie-callback", "/kie-callback/"):
            return self._reply(200, {"ok": True, "service": "kie-callback", "path": self.path})
        return self._reply(404, {"ok": False, "error": "not_found", "path": self.path})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        text = raw.decode("utf-8", errors="replace")

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        stem = f"callback-{ts}"
        (OUT_DIR / f"{stem}.json").write_text(text, encoding="utf-8")

        try:
            parsed = json.loads(text)
        except Exception:
            parsed = {"raw": text}

        summary = {
            "receivedAt": datetime.now().isoformat(),
            "path": self.path,
            "headers": {k: v for k, v in self.headers.items()},
            "body": parsed,
        }
        (OUT_DIR / f"{stem}.summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[kie-callback] received", self.path, flush=True)
        self._reply(200, {"ok": True, "saved": stem})

if __name__ == "__main__":
    print(f"KIE callback server listening on http://{HOST}:{PORT}", flush=True)
    print(f"Saving payloads to {OUT_DIR}", flush=True)
    HTTPServer((HOST, PORT), Handler).serve_forever()
