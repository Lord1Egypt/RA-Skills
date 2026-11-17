#!/usr/bin/env python3
"""
智慧课堂教学工作台本地服务（smart-classroom-serve.py）

作用：托管 assets/ 目录（常驻教学工作台）+ 提供 state.json 读写接口，
打通「外部输入（宿主对话/脚本）→ 工作台实时更新」的完整闭环。

用法：
    python smart-classroom-serve.py [端口]     # 默认端口 8765

HTTP 端点：
    GET  /                          -> 工作台页面（smart-classroom-workbench.html）
    GET  /smart-classroom-workbench.html -> 工作台页面
    GET  /state.json                -> 当前教学状态（不存在时返回 404）
    GET  /api/state                 -> 读取当前教学状态（JSON）
    POST /api/state                 -> 写入教学状态（请求体为 JSON），工作台 <=1.2s 内自动渲染

依赖：仅 Python 标准库（http.server），无第三方依赖。
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# 静态根目录 = 本脚本上级目录的 assets/
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS_DIR = os.path.normpath(os.path.join(_SCRIPTS_DIR, "..", "assets"))
_STATE_FILE = os.path.join(_ASSETS_DIR, "state.json")
_INDEX = "smart-classroom-workbench.html"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", ""):
            path = "/" + _INDEX
        if path in ("/state.json", "/api/state"):
            return self._serve_state()
        return self._serve_static(path)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path != "/api/state":
            return self._send_json(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
        except Exception as exc:
            return self._send_json(400, {"error": "invalid JSON: %s" % exc})
        with open(_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return self._send_json(200, {"ok": True, "state": data})

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def _serve_state(self):
        if not os.path.exists(_STATE_FILE):
            return self._send_json(404, {"error": "state.json not found yet"})
        with open(_STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self._send_json(200, data)

    def _serve_static(self, path):
        rel = path.lstrip("/") or _INDEX
        filepath = os.path.normpath(os.path.join(_ASSETS_DIR, rel))
        if not filepath.startswith(_ASSETS_DIR + os.sep):
            return self._send_json(403, {"error": "forbidden"})
        if not os.path.isfile(filepath):
            return self._send_json(404, {"error": "not found: %s" % rel})
        ctype = "text/html" if filepath.endswith(".html") else "application/octet-stream"
        with open(filepath, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, status, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, fmt, *args):
        sys.stderr.write("[serve] " + fmt % args + "\n")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = HTTPServer(("127.0.0.1", port), Handler)
    print("Teaching workbench running at http://127.0.0.1:%d/" % port)
    print("State file: %s" % _STATE_FILE)
    print("Write state: POST http://127.0.0.1:%d/api/state (JSON body)" % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
