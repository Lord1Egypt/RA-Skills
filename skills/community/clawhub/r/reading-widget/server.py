#!/usr/bin/env python3
"""Local helper for the reading widget.

Serves widget.html over http://127.0.0.1:PORT so that:
  - the goal you edit on the card is POSTed to /set-goal and saved into config.json
    (survives restarts — config.json is the source of truth, not browser localStorage)
  - the reading data is automatically re-fetched on a timer (no manual update.py runs)

Stdlib only. Runs quietly in the background under launchd.
"""
import json
import os
import pathlib
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).parent
PORT = 47900
REFRESH_INTERVAL = 1800  # seconds between automatic data re-fetches (30 min)


def regenerate():
    """Re-run update.py in a fresh process so it picks up the latest config.json."""
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "update.py")],
            cwd=str(ROOT),
            env=os.environ.copy(),
            timeout=60,
            check=False,
        )
    except Exception as e:
        print(f"[helper] regenerate failed: {e}", flush=True)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path != "/set-goal":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            goal = int(data.get("goal", 0))
            if not (1 <= goal <= 999):
                raise ValueError("goal out of range")
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"ok":false}')
            return

        cfg_path = ROOT / "config.json"
        cfg = json.loads(cfg_path.read_text())
        cfg["goal_hours"] = goal
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
        regenerate()

        body = json.dumps({"ok": True, "goal": goal}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # stay quiet in the log


def auto_refresh():
    while True:
        time.sleep(REFRESH_INTERVAL)
        regenerate()


if __name__ == "__main__":
    # Bind the port first, then refresh data in the background. A blocked WeRead
    # fetch (e.g. launchd has no proxy env) must not delay the port coming up.
    threading.Thread(target=regenerate, daemon=True).start()
    threading.Thread(target=auto_refresh, daemon=True).start()
    print(f"[helper] reading-widget on http://127.0.0.1:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
