#!/usr/bin/env python3
"""Tiny web form for fast OTP code entry during Telegram login."""

import argparse
import http.server
import os

HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width">
<title>Telegram Login</title>
<style>body{font-family:sans-serif;text-align:center;padding:40px;background:#1a1a2e;color:white}
input{font-size:32px;padding:15px;width:200px;text-align:center;border-radius:10px;border:none}
button{font-size:24px;padding:15px 40px;margin:20px;border-radius:10px;border:none;background:#10B981;color:white;cursor:pointer}
</style></head><body>
<h1>🔐 Telegram Login</h1>
<p>Enter the code you received:</p>
<form method="GET" action="/submit">
<input type="text" name="code" autofocus inputmode="numeric" pattern="[0-9]*"><br>
<button type="submit">Submit ✅</button>
</form></body></html>"""


def make_handler(code_file):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/submit?code="):
                code = self.path.split("code=")[1].split("&")[0].strip()
                with open(code_file, "w") as f:
                    f.write(code)
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    f"<html><body style='background:#1a1a2e;color:#10B981;text-align:center;"
                    f"padding:40px;font-size:24px'><h1>✅ Code {code} sent!</h1>"
                    f"<p>You can close this page.</p></body></html>".encode()
                )
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(HTML.encode())

        def log_message(self, *a):
            pass

    return Handler


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=19997)
    p.add_argument("--code-file", default="enter_code.txt")
    args = p.parse_args()
    server = http.server.HTTPServer(("127.0.0.1", args.port), make_handler(args.code_file))
    print(f"Code server on :{args.port}", flush=True)
    server.serve_forever()
