#!/usr/bin/env python3
"""
WHOOP OAuth 2.0 Authentication Helper
Handles the OAuth flow and saves tokens to ~/.whoop_tokens.json
"""

import argparse
import http.server
import json
import os
import secrets
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

TOKEN_FILE = Path.home() / ".whoop_tokens.json"
AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
REVOKE_URL = "https://api.prod.whoop.com/oauth/oauth2/revoke"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "read:recovery read:cycles read:workout read:sleep read:profile read:body_measurement"


def load_tokens():
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    return None


def save_tokens(tokens):
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    os.chmod(TOKEN_FILE, 0o600)
    print(f"Tokens saved to {TOKEN_FILE}")


def refresh_tokens(client_id, client_secret):
    tokens = load_tokens()
    if not tokens or "refresh_token" not in tokens:
        raise RuntimeError("No refresh token found. Run auth flow first.")

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req) as resp:
        new_tokens = json.loads(resp.read())
        new_tokens["obtained_at"] = int(time.time())
        save_tokens(new_tokens)
        print("Tokens refreshed successfully.")
        return new_tokens


def revoke_tokens(client_id, client_secret):
    tokens = load_tokens()
    if not tokens:
        print("No tokens found.")
        return

    token = tokens.get("access_token", "")
    data = urllib.parse.urlencode({
        "token": token,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(REVOKE_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req):
            pass
        TOKEN_FILE.unlink(missing_ok=True)
        print("Access revoked and tokens deleted.")
    except Exception as e:
        print(f"Revoke failed: {e}")


def run_auth_flow(client_id, client_secret):
    state = secrets.token_urlsafe(16)
    auth_code_holder = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/callback":
                params = urllib.parse.parse_qs(parsed.query)
                auth_code_holder["code"] = params.get("code", [None])[0]
                auth_code_holder["error"] = params.get("error", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h2>Authorization complete. You can close this tab.</h2>")

        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("localhost", 8080), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
    })
    url = f"{AUTH_URL}?{params}"
    print(f"\nOpening browser for WHOOP authorization...\n{url}\n")
    webbrowser.open(url)
    thread.join(timeout=120)

    if auth_code_holder.get("error"):
        raise RuntimeError(f"Authorization error: {auth_code_holder['error']}")
    if not auth_code_holder.get("code"):
        raise RuntimeError("No authorization code received (timeout?)")

    code = auth_code_holder["code"]
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req) as resp:
        tokens = json.loads(resp.read())
        tokens["obtained_at"] = int(time.time())
        save_tokens(tokens)
        print("Authorization successful!")
        return tokens


def main():
    parser = argparse.ArgumentParser(description="WHOOP OAuth Authentication")
    parser.add_argument("--client-id", default=os.environ.get("WHOOP_CLIENT_ID"))
    parser.add_argument("--client-secret", default=os.environ.get("WHOOP_CLIENT_SECRET"))
    parser.add_argument("--revoke", action="store_true", help="Revoke current access token")
    parser.add_argument("--refresh", action="store_true", help="Refresh access token")
    parser.add_argument("--status", action="store_true", help="Show current token status")
    args = parser.parse_args()

    if args.status:
        tokens = load_tokens()
        if not tokens:
            print("No tokens saved.")
        else:
            obtained = tokens.get("obtained_at", 0)
            expires_in = tokens.get("expires_in", 3600)
            expires_at = obtained + expires_in
            remaining = expires_at - int(time.time())
            print(f"Access token: {'valid' if remaining > 0 else 'EXPIRED'} ({max(0, remaining)}s remaining)")
            print(f"Refresh token: {'present' if 'refresh_token' in tokens else 'missing'}")
        return

    if not args.client_id or not args.client_secret:
        parser.error("--client-id and --client-secret are required (or set WHOOP_CLIENT_ID/WHOOP_CLIENT_SECRET)")

    if args.revoke:
        revoke_tokens(args.client_id, args.client_secret)
    elif args.refresh:
        refresh_tokens(args.client_id, args.client_secret)
    else:
        run_auth_flow(args.client_id, args.client_secret)


if __name__ == "__main__":
    main()
