#!/usr/bin/env python3
"""
SolScribe HTTP Server — Background daemon for SolScribe.
Listens on localhost:3847. Accepts JSON POST requests.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from solscribe import (
    create_chapter, get_chapter, get_chapters, update_chapter, revise_chapter,
    delete_chapter, append_to_chapter, parse_incoming, set_book_meta,
    export_docx, total_words, load_state, count_words, log_session
)
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

PORT = 3847

class SolScribeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            state = load_state()
            chapters = get_chapters()
            self.wfile.write(json.dumps({
                "status": "ok",
                "book": state["book_title"],
                "author": state["author"],
                "chapters": len(chapters),
                "total_words": total_words()
            }).encode())
            return

        if self.path == "/chapters":
            chapters = get_chapters()
            data = []
            for ch in chapters:
                icon = {"planned": "○", "drafted": "◐", "complete": "●"}.get(ch["status"], "○")
                data.append({
                    "id": ch["id"],
                    "order": ch["order"],
                    "title": ch["title"],
                    "status": ch["status"],
                    "word_count": ch["word_count"],
                    "icon": icon
                })
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            return

        if self.path.startswith("/chapter/"):
            chapter_id = self.path.split("/")[-1]
            ch = get_chapter(chapter_id)
            if ch:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(ch).encode())
            else:
                self.send_response(404)
                self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path == "/write":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}

            text = data.get("text", "")
            chapter_hint = data.get("chapter_hint")

            # Route through skill.py handler
            from skill import handle
            response, _ = handle(text, chapter_hint)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": response}).encode())
            return

        if self.path == "/export":
            state = load_state()
            if not state["chapters"]:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No chapters to export"}).encode())
                return

            safe_title = re.sub(r"[^\w\s-]", "", state["book_title"]).strip()
            output_path = Path.home() / "Documents" / f"{safe_title}.docx"
            try:
                export_docx(str(output_path))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"path": str(output_path)}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Quiet logs

if __name__ == "__main__":
    import re
    server = HTTPServer(("localhost", PORT), SolScribeHandler)
    print(f"SolScribe server running on http://localhost:{PORT}")
    server.serve_forever()
