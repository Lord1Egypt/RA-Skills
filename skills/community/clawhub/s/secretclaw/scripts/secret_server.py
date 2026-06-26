#!/usr/bin/env python3
"""
secret_server.py — Secure secret input server

Usage:
    python3 secret_server.py --config-key "env.FAL_KEY" --label "FAL_KEY"
    python3 secret_server.py --config-key "channels.discord.token" --label "Discord Token"

How it works:
    1. Start a local HTTP server on a random port
    2. Create an external HTTPS tunnel via cloudflared
    3. Record tunnel info in TUNNELS.md
    4. Output URL + token (agent forwards to user)
    5. On form submission, save via `openclaw config set`
    6. Shut down server + remove TUNNELS.md entry
"""

import argparse
import http.server
import json
import os
import re
import secrets
import signal
import subprocess
import sys
import threading
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))
TUNNELS_MD = WORKSPACE / "TUNNELS.md"
PORT_RANGE = (18400, 18499)


def find_free_port() -> int:
    import socket
    for port in range(*PORT_RANGE):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port available in range")


def update_tunnels_md(action: str, service: str, port: int, url: str, token: str, label: str):
    """Add or remove tunnel info from TUNNELS.md."""
    if not TUNNELS_MD.exists():
        TUNNELS_MD.write_text("# TUNNELS.md — Active Tunnels\n\nActive Cloudflare tunnels managed by the agent.\nAutomatically removed on server shutdown.\n\n| Service | Port | URL | Description |\n|---------|------|-----|-------------|\n")

    content = TUNNELS_MD.read_text()

    if action == "add":
        now = datetime.now().strftime("%H:%M")
        row = f"| {service} | {port} | {url} | {label} ({now}) |\n"
        TUNNELS_MD.write_text(content + row)

    elif action == "remove":
        lines = content.splitlines(keepends=True)
        filtered = [l for l in lines if f"| {service} |" not in l]
        TUNNELS_MD.write_text("".join(filtered))


def start_cloudflare_tunnel(port: int) -> tuple[subprocess.Popen, str]:
    """Start a cloudflared tunnel and return the public URL."""
    proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    url = None
    deadline = time.time() + 30
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        m = re.search(r"https://[\w\-]+\.trycloudflare\.com", line)
        if m:
            url = m.group(0)
            # Keep reading stdout in background to prevent blocking
            threading.Thread(target=lambda: [proc.stdout.readline() for _ in iter(int, 1)], daemon=True).start()
            break

    if not url:
        proc.terminate()
        raise RuntimeError("cloudflared URL not found within timeout")

    return proc, url


def make_handler(token: str, config_key: str, label: str, shutdown_event: threading.Event, cleanup_fn=None):
    HTML_FORM = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Enter {label}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 480px; margin: 80px auto; padding: 20px; background: #f5f5f5; }}
  .card {{ background: white; padding: 32px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,.1); }}
  h2 {{ margin-top: 0; color: #333; }}
  input {{ width: 100%; padding: 12px; font-size: 15px; margin: 12px 0; box-sizing: border-box; border: 1px solid #ddd; border-radius: 8px; font-family: monospace; }}
  button {{ background: #5865F2; color: white; border: none; padding: 14px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; margin-top: 8px; }}
  button:hover {{ background: #4752c4; }}
  .note {{ color: #888; font-size: 13px; margin-top: 12px; }}
</style></head>
<body><div class="card">
<h2>🔑 Enter {label}</h2>
<p>Your value will be saved immediately and this server will shut down automatically.<br>Nothing is stored in chat history.</p>
<form method="POST" action="/submit?token={token}">
  <input type="password" name="value" placeholder="Enter your value" autocomplete="off" autofocus required>
  <button type="submit">Save</button>
</form>
<p class="note">Config path: <code>{config_key}</code></p>
</div></body></html>"""

    HTML_DONE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Saved</title>
<style>body{{font-family:-apple-system,sans-serif;text-align:center;margin-top:100px;color:#333}}</style></head>
<body><h2>✅ Saved successfully!</h2><p>You can close this tab now.</p></body></html>"""

    HTML_ERROR = """<!DOCTYPE html>
<html><body><h2>❌ Error</h2><p>Invalid request.</p></body></html>"""

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if parsed.path == "/" and params.get("token", [""])[0] == token:
                self._respond(200, HTML_FORM)
            else:
                self._respond(403, HTML_ERROR)

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if parsed.path == "/submit" and params.get("token", [""])[0] == token:
                length = int(self.headers.get("Content-Length", 0))
                body = urllib.parse.parse_qs(self.rfile.read(length).decode())
                value = body.get("value", [""])[0].strip()
                if value:
                    result = subprocess.run(
                        ["openclaw", "config", "set", config_key, value],
                        capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        self._respond(200, HTML_DONE)
                        if cleanup_fn:
                            cleanup_fn()
                        print(f"SECRET_SAVED:{config_key}", flush=True)
                        shutdown_event.set()
                    else:
                        print(f"ERROR: {result.stderr}", file=sys.stderr, flush=True)
                        self._respond(500, f"<h2>Save failed</h2><pre>{result.stderr}</pre>")
                else:
                    self._respond(400, HTML_ERROR)
            else:
                self._respond(403, HTML_ERROR)

        def _respond(self, code, html):
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

    return Handler


def main():
    parser = argparse.ArgumentParser(description="Secure secret input server")
    parser.add_argument("--config-key", required=True, help="openclaw config key path (e.g. env.FAL_KEY)")
    parser.add_argument("--label", required=True, help="Human-readable label (e.g. FAL_KEY)")
    parser.add_argument("--service", default="secret-input", help="Service name for TUNNELS.md")
    args = parser.parse_args()

    token = secrets.token_urlsafe(16)
    port = find_free_port()
    shutdown_event = threading.Event()

    # Start HTTP server
    handler = make_handler(token, args.config_key, args.label, shutdown_event)
    httpd = http.server.HTTPServer(("0.0.0.0", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    # Start cloudflare tunnel
    try:
        cf_proc, public_url = start_cloudflare_tunnel(port)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        httpd.shutdown()
        sys.exit(1)

    # Cleanup function — called on success or interrupt
    def cleanup():
        update_tunnels_md("remove", args.service, port, public_url, token, args.label)

    # Update TUNNELS.md
    update_tunnels_md("add", args.service, port, public_url, token, args.label)

    # Rebuild handler with cleanup_fn
    handler = make_handler(token, args.config_key, args.label, shutdown_event, cleanup_fn=cleanup)
    httpd.RequestHandlerClass = handler

    # Output URL for agent
    form_url = f"{public_url}/?token={token}"
    print(f"SECRET_URL:{form_url}", flush=True)
    print(f"Waiting for {args.label} input at: {form_url}", flush=True)

    # Wait for submission or interrupt
    try:
        while not shutdown_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        cleanup()
    finally:
        cf_proc.terminate()
        httpd.shutdown()
        print("SERVER_CLOSED", flush=True)


if __name__ == "__main__":
    main()
