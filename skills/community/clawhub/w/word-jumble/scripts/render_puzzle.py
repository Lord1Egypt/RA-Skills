#!/usr/bin/env python3
"""
Render a Word Jumble puzzle to a PNG screenshot using a local HTTP server + Chrome DevTools.

Usage:
  render_puzzle.py <puzzle.json> <cartoon_image_path> <output_png>

Requires:
  - Python 3.9+
  - Google Chrome / Chromium accessible via CDP (port 18800, OpenClaw managed)
  - The puzzle-template.html asset in the same directory as this script's parent assets/

Note: This script is intended to be driven by an OpenClaw agent via the browser tool.
      The agent handles CDP interaction; this script prepares the HTML and serves it.
"""

import argparse
import http.server
import json
import os
import shutil
import signal
import socket
import sys
import tempfile
import threading
import time


def find_free_port(start=7891, end=7990):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found in range")


def build_html(template_path: str, puzzle: dict, cartoon_filename: str) -> str:
    with open(template_path) as f:
        html = f.read()
    html = html.replace("__PUZZLE_JSON__", json.dumps(puzzle))
    html = html.replace("__CARTOON_IMAGE__", cartoon_filename)
    return html


def serve_dir(directory: str, port: int) -> http.server.HTTPServer:
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None  # silence logs
    os.chdir(directory)
    server = http.server.HTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_json", help="Path to puzzle JSON file")
    parser.add_argument("cartoon_image", help="Path to cartoon image file")
    parser.add_argument("output_png", help="Output PNG path")
    args = parser.parse_args()

    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    template_path = os.path.join(assets_dir, "puzzle-template.html")

    with open(args.puzzle_json) as f:
        puzzle = json.load(f)

    # Build into a temp dir so the server can serve both HTML and the image
    tmpdir = tempfile.mkdtemp(prefix="word-jumble-")
    try:
        cartoon_filename = os.path.basename(args.cartoon_image)
        shutil.copy(args.cartoon_image, os.path.join(tmpdir, cartoon_filename))

        html = build_html(template_path, puzzle, cartoon_filename)
        html_path = os.path.join(tmpdir, "puzzle.html")
        with open(html_path, "w") as f:
            f.write(html)

        port = find_free_port()
        server = serve_dir(tmpdir, port)

        print(f"Serving at http://localhost:{port}/puzzle.html")
        print(f"Viewport: 1200x900")
        print(f"Output: {args.output_png}")
        print("READY")  # Signal to the agent that it can screenshot now

        # Wait for agent to signal done (or timeout after 60s)
        deadline = time.time() + 60
        while time.time() < deadline:
            time.sleep(1)

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
