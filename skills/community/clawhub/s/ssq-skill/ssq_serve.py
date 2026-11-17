# -*- coding: utf-8 -*-
"""双色球 · 本地共享状态服务（跨报告持久化招财猫 / 心愿单 / 彩友圈）

纯标准库 http.server。启动后：
  - 服务 scripts/lib 目录（含生成的报告 HTML）
  - GET  /                  -> 重定向到 latest_report.html（若存在），否则列报告
  - GET  /api/state         -> 返回 ssq_cat_state.json（无则 {}）
  - POST /api/state         -> 合并写入 ssq_cat_state.json，返回 {"ok":true}
  - GET  /api/state?reset=1 -> 清空状态

用法：
  python3 ssq_serve.py [--port 8765] [--dir 目录] [--open]
  （--open 会尝试用系统默认浏览器打开 http://127.0.0.1:PORT/）

仅绑定 127.0.0.1，不联网、不接收外部请求，仅本机使用。
关掉终端 / Ctrl+C 即停止。
"""
import sys
import os
import json
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = "ssq_cat_state.json"


class Handler(BaseHTTPRequestHandler):
    def _state_path(self):
        return os.path.join(self.server.serve_dir, STATE_FILE)

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/state":
            sp = self._state_path()
            data = {}
            if os.path.exists(sp):
                try:
                    data = json.load(open(sp, encoding="utf-8"))
                except Exception:
                    data = {}
            self._send(200, data)
            return
        if path in ("/", "/index.html"):
            lp = os.path.join(self.server.serve_dir, "latest_report.html")
            if os.path.exists(lp):
                self.send_response(302)
                self.send_header("Location", "/latest_report.html")
                self.end_headers()
                return
            self._list()
            return
        self._static(path)

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/api/state":
            try:
                length = int(self.headers.get("Content-Length", 0) or 0)
                raw = self.rfile.read(length) if length else b"{}"
                incoming = json.loads((raw or b"{}").decode("utf-8") or "{}")
            except Exception as e:
                self._send(400, {"ok": False, "error": str(e)})
                return
            sp = self._state_path()
            cur = {}
            if os.path.exists(sp):
                try:
                    cur = json.load(open(sp, encoding="utf-8"))
                except Exception:
                    cur = {}
            if isinstance(incoming, dict):
                cur.update(incoming)
            try:
                json.dump(cur, open(sp, "w", encoding="utf-8"),
                          ensure_ascii=False, indent=2)
                self._send(200, {"ok": True})
            except Exception as e:
                self._send(500, {"ok": False, "error": str(e)})
            return
        self._send(404, {"ok": False})

    def _static(self, path):
        rel = path.lstrip("/")
        fp = os.path.normpath(os.path.join(self.server.serve_dir, rel))
        base = os.path.abspath(self.server.serve_dir)
        if not fp.startswith(base) or not os.path.isfile(fp):
            self._send(404, "not found", "text/plain; charset=utf-8")
            return
        ctype = "text/html; charset=utf-8"
        if fp.endswith(".js"):
            ctype = "application/javascript; charset=utf-8"
        elif fp.endswith(".json"):
            ctype = "application/json; charset=utf-8"
        elif fp.endswith(".css"):
            ctype = "text/css; charset=utf-8"
        elif fp.endswith((".png", ".jpg", ".jpeg", ".gif")):
            ctype = "image/" + fp.rsplit(".", 1)[1]
        try:
            data = open(fp, "rb").read()
        except Exception:
            self._send(404, "not found", "text/plain; charset=utf-8")
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _list(self):
        d = self.server.serve_dir
        items = []
        try:
            for f in sorted(os.listdir(d)):
                if f.endswith(".html"):
                    items.append('<li><a href="/%s">%s</a></li>' % (f, f))
        except Exception:
            pass
        html = ("<!doctype html><meta charset=utf-8><title>双色球报告</title>"
                "<h2>双色球报告列表</h2><ul>%s</ul>"
                "<p>提示：用 <code>python3 ssq_serve.py</code> 启动后访问本页，"
                "招财猫状态跨报告保存。直接双击 html 也行（仅本文件内保存）。</p>"
                % "".join(items))
        self._send(200, html, "text/html; charset=utf-8")

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser(description="双色球本地共享状态服务")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--dir", default=HERE,
                    help="要服务的目录（默认本模块所在 lib/）")
    ap.add_argument("--open", action="store_true",
                    help="启动后用默认浏览器打开")
    args = ap.parse_args()
    serve_dir = os.path.abspath(args.dir)
    srv = HTTPServer(("127.0.0.1", args.port), Handler)
    srv.serve_dir = serve_dir
    url = "http://127.0.0.1:%d/" % args.port
    print("双色球本地服务已启动：%s" % url)
    print("  服务目录: %s" % serve_dir)
    print("  状态文件: %s" % os.path.join(serve_dir, STATE_FILE))
    print("  仅本机 127.0.0.1 可访问，不联网。Ctrl+C 停止。")
    if args.open:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")


if __name__ == "__main__":
    main()
