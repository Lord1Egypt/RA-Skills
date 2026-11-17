#!/usr/bin/env python3
"""Three failure modes that really occur in the field, for offline tests.

    /dead      an endpoint that exists but answers "OParl is not active."
    /botcheck  an HTML bot check page instead of JSON, as CC e-gov serves
    /blocked   a path that this server's own robots.txt disallows

    python3 tests/mock_broken.py &
    python3 scripts/ratsinfo.py check http://127.0.0.1:8798/dead
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

BOT_CHECK_PAGE = (
    b"<html><body><h1>Zugriff pruefen</h1>"
    b"<p>Zum Schutz vor automatisierten Zugriffen ist die folgende "
    b"Pruefung einmalig notwendig.</p></body></html>"
)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        path = self.path.split("?")[0]

        if path == "/robots.txt":
            body = b"User-agent: *\nDisallow: /blocked\n"
        elif path == "/dead":
            body = json.dumps(
                {
                    "type": "https://schema.oparl.org/1.0/Error",
                    "message": "OParl is not active.",
                    "debug": "Error-Code 1",
                }
            ).encode()
        elif path == "/botcheck":
            body = BOT_CHECK_PAGE
        else:
            body = b"{}"

        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8798), Handler).serve_forever()
