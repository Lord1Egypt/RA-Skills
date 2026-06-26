#!/usr/bin/env python3
"""Serve Stock Invest Master reports with Markdown rendering and directory browsing.

Usage:
    python3 serve_reports.py [port]

Features:
    - Pretty directory listing (styled HTML table)
    - Automatic Markdown rendering via marked.js (CDN)
    - Direct browser viewing of HTML/JSON/TXT/CSV/XML files
    - File-type filtering: only shows browsable formats in directory listing
    - Chinese/Unicode filename support (URL-decoded paths)
    - Directory traversal protection
    - Health check endpoint (/health)
    - PID file management for daemon operation
"""

import os
import sys
import html
import json
import signal
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
REPORTS_DIR = os.path.expanduser("~/.stock-invest-master")
DEFAULT_PORT = 8888

# File extensions that can be viewed directly in the browser
BROWSABLE_EXTENSIONS = {
    # Documents
    ".md", ".markdown",
    ".html", ".htm",
    ".txt", ".text",
    ".csv",
    ".xml",
    ".json",
    ".yaml", ".yml",
    # Images (served directly by browser)
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
}

# Extensions to highlight in directory listing
MARKDOWN_EXTENSIONS = {".md", ".markdown"}
HTML_EXTENSIONS = {".html", ".htm"}
DATA_EXTENSIONS = {".json", ".csv", ".xml", ".yaml", ".yml"}
TEXT_EXTENSIONS = {".txt", ".text", ".log"}

PID_FILE = os.path.join(REPORTS_DIR, ".server.pid")


def get_file_icon(name):
    """Return an emoji icon based on file extension."""
    if os.path.isdir(os.path.join(REPORTS_DIR, name)):
        return "📂"
    ext = os.path.splitext(name)[1].lower()
    if ext in MARKDOWN_EXTENSIONS:
        return "📝"
    if ext in HTML_EXTENSIONS:
        return "🌐"
    if ext in DATA_EXTENSIONS:
        return "📊"
    if ext in TEXT_EXTENSIONS:
        return "📄"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
        return "🖼️"
    if ext in {".py", ".js", ".sh"}:
        return "⚙️"
    return "📄"


def is_browsable(name):
    """Check if a file should be shown in the directory listing."""
    if name.startswith("."):
        return False
    if os.path.isdir(os.path.join(REPORTS_DIR, name)):
        return True
    ext = os.path.splitext(name)[1].lower()
    return ext in BROWSABLE_EXTENSIONS


class ReportServer(SimpleHTTPRequestHandler):
    """HTTP server that renders Markdown and provides styled directory browsing."""

    def do_GET(self):
        path = unquote(self.path.split("?")[0])

        # Health check endpoint
        if path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = json.dumps({
                "status": "ok",
                "directory": REPORTS_DIR,
                "port": self.server.server_address[1],
                "files": len([f for f in os.listdir(REPORTS_DIR) if is_browsable(f)]),
            })
            self.wfile.write(response.encode("utf-8"))
            return

        # Security: prevent directory traversal
        if ".." in path:
            self.send_error(400, "Bad Request")
            return

        full_path = os.path.abspath(os.path.join(REPORTS_DIR, path.lstrip("/")))

        if not full_path.startswith(os.path.abspath(REPORTS_DIR)):
            self.send_error(403, "Forbidden")
            return

        if os.path.isdir(full_path):
            if not path.endswith("/"):
                self.send_response(301)
                self.send_header("Location", path + "/")
                self.end_headers()
                return
            self.serve_dir(full_path, path)
        elif full_path.endswith((".md", ".markdown")):
            self.serve_md(full_path)
        elif full_path.endswith((".html", ".htm")):
            self.serve_static(full_path, "text/html")
        elif full_path.endswith(".json"):
            self.serve_static(full_path, "application/json")
        elif full_path.endswith(".csv"):
            self.serve_static(full_path, "text/csv")
        elif full_path.endswith(".xml"):
            self.serve_static(full_path, "application/xml")
        elif full_path.endswith((".yaml", ".yml")):
            self.serve_static(full_path, "text/yaml")
        elif full_path.endswith((".txt", ".text", ".log", ".py", ".js", ".css", ".sh", ".bash", ".sql", ".conf", ".cfg", ".ini")):
            self.serve_text(full_path)
        elif full_path.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            self.serve_image(full_path)
        else:
            super().do_GET()

    def serve_dir(self, full_path, url_path):
        """Serve a custom, styled directory listing with file-type filtering."""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        try:
            entries = sorted(os.listdir(full_path))
        except PermissionError:
            self.send_error(403, "Forbidden")
            return

        # Filter: only show browsable file types
        visible = [e for e in entries if is_browsable(e)]
        # Sort: directories first, then files; within each group, alphabetical
        dirs = sorted([e for e in visible if os.path.isdir(os.path.join(full_path, e))])
        files = sorted([e for e in visible if not os.path.isdir(os.path.join(full_path, e))])
        sorted_entries = dirs + files

        rows = ""
        for name in sorted_entries:
            is_dir = os.path.isdir(os.path.join(full_path, name))
            link = html.escape(url_path + name + ("/" if is_dir else ""))
            icon = get_file_icon(name)
            display = html.escape(name)

            # File size for files
            size_info = ""
            if not is_dir:
                try:
                    size = os.path.getsize(os.path.join(full_path, name))
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size / 1024:.1f} KB"
                    else:
                        size_str = f"{size / (1024 * 1024):.1f} MB"
                    size_info = f'<td style="color:#888;font-size:0.85em;text-align:right;">{size_str}</td>'
                except OSError:
                    size_info = '<td style="color:#888;font-size:0.85em;">-</td>'

            rows += f'<tr><td style="width:30px;">{icon}</td><td><a href="{link}">{display}</a></td>{size_info}</tr>'

        # Breadcrumb navigation
        parts = url_path.strip("/").split("/")
        breadcrumbs = '<a href="/">🏠 根目录</a>'
        current = ""
        for part in parts:
            if part:
                current += "/" + part
                breadcrumbs += f' / <a href="{current}/">{html.escape(part)}</a>'

        body = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Stock Invest Master - Reports</title>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
                .container {{ max-width: 900px; margin: 0 auto; }}
                .header {{ background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px 32px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
                .header h1 {{ font-size: 1.5em; color: #1a1a2e; margin-bottom: 8px; }}
                .breadcrumbs {{ font-size: 0.85em; color: #666; }}
                .breadcrumbs a {{ color: #667eea; text-decoration: none; }}
                .breadcrumbs a:hover {{ text-decoration: underline; }}
                .card {{ background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background: #f8f9fa; padding: 12px 16px; text-align: left; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.5px; color: #666; border-bottom: 2px solid #eee; }}
                td {{ padding: 12px 16px; border-bottom: 1px solid #f0f0f0; }}
                tr:last-child td {{ border-bottom: none; }}
                tr:hover {{ background: #f8f9ff; }}
                a {{ text-decoration: none; color: #1a1a2e; font-weight: 500; }}
                a:hover {{ color: #667eea; }}
                .empty {{ text-align: center; padding: 60px 20px; color: #888; }}
                .empty-icon {{ font-size: 3em; margin-bottom: 16px; }}
                .footer {{ text-align: center; padding: 16px; color: rgba(255,255,255,0.7); font-size: 0.8em; margin-top: 20px; }}
                .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.7em; font-weight: 600; margin-left: 8px; }}
                .badge-md {{ background: #e3f2fd; color: #1565c0; }}
                .badge-json {{ background: #f3e5f5; color: #7b1fa2; }}
                .badge-html {{ background: #e8f5e9; color: #2e7d32; }}
                .badge-csv {{ background: #fff3e0; color: #ef6c00; }}
                .badge-txt {{ background: #f5f5f5; color: #616161; }}
                .count {{ font-size: 0.85em; color: #888; margin-top: 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Stock Invest Master Reports</h1>
                    <div class="breadcrumbs">{breadcrumbs}</div>
                    <div class="count">共 {len(sorted_entries)} 个文件/目录（已过滤系统文件）</div>
                </div>
                <div class="card">
                    {f'''<table>
                        <tr><th style="width:50px;"></th><th>名称</th><th style="width:80px;text-align:right;">大小</th></tr>
                        {rows}
                    </table>''' if rows else '<div class="empty"><div class="empty-icon">📭</div><p>暂无报告文件</p><p style="font-size:0.85em;margin-top:8px;">完成投资分析后，报告将自动保存到此目录</p></div>'}
                </div>
                <div class="footer">Stock Invest Master v3.1 &bull; Powered by Hermes Agent</div>
            </div>
        </body>
        </html>"""
        self.wfile.write(body.encode("utf-8"))

    def serve_md(self, full_path):
        """Read a Markdown file and render it in the browser using marked.js."""
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        title = os.path.basename(full_path)
        safe_content = html.escape(content)

        body = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{html.escape(title)} - Stock Invest Master</title>
            <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown-light.min.css">
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #f6f8fa; }}
                .nav-bar {{ position: sticky; top: 0; z-index: 100; background: white; border-bottom: 1px solid #e1e4e8; padding: 12px 24px; display: flex; align-items: center; gap: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
                .nav-bar a {{ color: #586069; text-decoration: none; font-size: 0.9em; display: flex; align-items: center; gap: 6px; }}
                .nav-bar a:hover {{ color: #0366d6; }}
                .nav-title {{ font-weight: 600; color: #24292e; font-size: 0.9em; margin-left: auto; }}
                .markdown-body {{ max-width: 900px; margin: 24px auto; padding: 40px; background: white; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
                @media (max-width: 768px) {{ .markdown-body {{ padding: 20px; margin: 12px; }} }}
            </style>
        </head>
        <body>
            <div class="nav-bar">
                <a href="/">⬅ 返回目录</a>
                <span class="nav-title">{html.escape(title)}</span>
            </div>
            <div class="markdown-body" id="content"></div>
            <pre id="source" style="display:none">{safe_content}</pre>
            <script>
                try {{
                    document.getElementById('content').innerHTML = marked.parse(document.getElementById('source').textContent);
                }} catch(e) {{
                    document.getElementById('content').innerHTML = '<p>Markdown 渲染失败，显示原始内容</p><pre>' + document.getElementById('source').textContent + '</pre>';
                }}
            </script>
        </body>
        </html>"""
        self.wfile.write(body.encode("utf-8"))

    def serve_static(self, full_path, content_type):
        """Serve static files (HTML, JSON, CSV, XML, YAML) directly."""
        try:
            with open(full_path, "rb") as f:
                content = f.read()
        except Exception:
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def serve_text(self, full_path):
        """Serve plain text files with basic HTML wrapping."""
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            self.send_error(404, "Not Found")
            return

        title = os.path.basename(full_path)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{html.escape(title)}</title>
            <style>
                body {{ font-family: monospace; background: #1e1e1e; color: #d4d4d4; padding: 24px; font-size: 14px; line-height: 1.5; }}
                .nav {{ margin-bottom: 16px; }}
                .nav a {{ color: #569cd6; text-decoration: none; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            </style>
        </head>
        <body>
            <div class="nav"><a href="/">⬅ Back to List</a> | {html.escape(title)}</div>
            <pre>{html.escape(content)}</pre>
        </body>
        </html>"""
        self.wfile.write(body.encode("utf-8"))

    def serve_image(self, full_path):
        """Serve image files with correct MIME type."""
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".webp": "image/webp",
        }
        ext = os.path.splitext(full_path)[1].lower()
        mime = mime_map.get(ext, "application/octet-stream")

        try:
            with open(full_path, "rb") as f:
                content = f.read()
        except Exception:
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Minimal logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def write_pid():
    """Write current process PID to file."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def cleanup_pid(signum, frame):
    """Remove PID file on exit."""
    try:
        os.remove(PID_FILE)
    except OSError:
        pass
    sys.exit(0)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

    if not os.path.isdir(REPORTS_DIR):
        os.makedirs(REPORTS_DIR, exist_ok=True)

    # Register signal handlers
    signal.signal(signal.SIGTERM, cleanup_pid)
    signal.signal(signal.SIGINT, cleanup_pid)

    # Write PID file
    write_pid()

    print(f"Serving Stock Invest Master Reports")
    print(f"  URL:       http://0.0.0.0:{port}")
    print(f"  Directory: {REPORTS_DIR}")
    print(f"  PID:       {os.getpid()}")
    print(f"  Press Ctrl+C to stop.")
    print(f"  Health:    http://localhost:{port}/health")

    server = HTTPServer(("", port), ReportServer)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_pid(None, None)


if __name__ == "__main__":
    main()
