from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        payload = json.loads(raw.decode("utf-8")) if raw else {}
        text = str(payload.get("text", "")).strip()
        source_lang = str(payload.get("source_lang", "")).strip()
        target_lang = str(payload.get("target_lang", "")).strip()

        result = {
            "translation": f"[{source_lang}->{target_lang}] {text}"
        }
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock translation service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18080)
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), Handler)
    print(f"Mock translation service listening on http://{args.host}:{args.port}")
    server.serve_forever()
