#!/usr/bin/env python3
"""
Chart Skill — project-based static server + save APIs

Usage:
  python3 chart_server.py [serve_dir] [port]

Defaults:
  serve_dir = /data/workspace/output/chart-html
  port = 7860

Endpoints:
- POST /save-chart : Save PNG to current project directory as screenshot.png (or filename)
- GET  /           : Static files from serve_dir

Notes:
- Gallery and library APIs are intentionally removed.
- Each chart should live in: output/chart-html/<project>/index.html
"""

import sys
import os
import json
import base64
import re
from pathlib import Path
from urllib.parse import urlsplit
from http.server import HTTPServer, SimpleHTTPRequestHandler

WORKSPACE = Path("/data/workspace")
DEFAULT_SERVE_DIR = WORKSPACE / "output" / "chart-html"
DEFAULT_SERVE_DIR.mkdir(parents=True, exist_ok=True)


def _safe_filename(name: str, ext: str) -> str:
    name = re.sub(r"[^\w\u4e00-\u9fff.\-]", "_", name or "")
    if not name:
        name = f"screenshot{ext}"
    if not name.endswith(ext):
        name += ext
    return name


class ChartHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, serve_dir=None, **kwargs):
        self._serve_dir = Path(serve_dir or DEFAULT_SERVE_DIR)
        super().__init__(*args, directory=str(self._serve_dir), **kwargs)

    def log_message(self, format, *args):
        pass

    def _normalized_path(self):
        # Preview proxy may forward as /preview/{id}/<endpoint>
        p = self.path.split('?', 1)[0]
        m = re.match(r"^/preview/[^/]+/(.*)$", p)
        if m:
            p = '/' + m.group(1)
        return p

    def _translate_preview_path(self, raw_path: str) -> str:
        """Map /preview/<id>/<project>/... to /<project>/... before static lookup."""
        # keep query string when present
        split = urlsplit(raw_path)
        p = split.path
        m = re.match(r"^/preview/[^/]+/(.*)$", p)
        if m:
            mapped = '/' + m.group(1)
        else:
            mapped = p
        if split.query:
            mapped = f"{mapped}?{split.query}"
        return mapped

    def translate_path(self, path):
        # SimpleHTTPRequestHandler resolves filesystem paths via this method.
        # We normalize preview-prefixed URLs first so static files map correctly.
        return super().translate_path(self._translate_preview_path(path))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        return super().do_GET()

    def do_POST(self):
        p = self._normalized_path()
        if p in ("/save-chart", "/save-chart/"):
            return self._handle_save_chart()
        self.send_error(404, "Not found")

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        return json.loads(raw)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _resolve_project_dir(self, project: str):
        # project like "btc-90d-20260401" or "btc-90d-20260401/subdir"
        project = (project or "").strip().strip('/')
        if not project:
            return None
        target = (self._serve_dir / project).resolve()

        # Prevent path traversal
        try:
            target.relative_to(self._serve_dir.resolve())
        except ValueError:
            return None

        if not target.exists() or not target.is_dir():
            return None
        return target

    def _handle_save_chart(self):
        try:
            data = self._read_json_body()
            data_url = data.get("dataUrl", "")
            filename = _safe_filename(data.get("filename", "screenshot"), ".png")
            project = data.get("project", "")

            project_dir = self._resolve_project_dir(project)
            if project_dir is None:
                return self._send_json({"ok": False, "error": "Invalid or missing project"}, status=400)

            if "," in data_url:
                _, b64 = data_url.split(",", 1)
            else:
                b64 = data_url
            png_bytes = base64.b64decode(b64)

            out_path = project_dir / filename
            out_path.write_bytes(png_bytes)

            rel_path = out_path.relative_to(self._serve_dir).as_posix()
            self._send_json({"ok": True, "filename": filename, "path": str(out_path), "url": f"/{rel_path}"})
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, status=500)


def run(serve_dir, port):
    os.chdir(serve_dir)
    server = HTTPServer(("127.0.0.1", port), lambda *a, **k: ChartHandler(*a, serve_dir=serve_dir, **k))
    print(f"[chart-server] serving {serve_dir} on port {port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    serve_dir = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_SERVE_DIR)
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7860
    Path(serve_dir).mkdir(parents=True, exist_ok=True)
    run(serve_dir, port)
