#!/usr/bin/env python3
"""
WHOOP OAuth 2.0 Setup

Guides you through connecting your WHOOP account:
  1. Prompts for your WHOOP Developer App client ID and secret
  2. Opens a browser to authorize access (local server or manual code paste)
  3. Saves tokens to ~/.config/whoop-skill/credentials.json

Run this once to get set up. Tokens are refreshed automatically by other scripts.

Usage:
  python3 scripts/auth.py
"""

import json
import secrets
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as _cfg

AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
SCOPES = "offline read:recovery read:cycles read:workout read:sleep read:profile read:body_measurement"
REDIRECT_PORT = 8888
REDIRECT_URI_LOCAL = f"http://localhost:{REDIRECT_PORT}/callback"

auth_code = None
state_value = None


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urlparse(self.path)
        if parsed.path == "/callback":
            params = parse_qs(parsed.query)
            returned_state = params.get("state", [None])[0]
            if returned_state != state_value:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"State mismatch -- possible CSRF. Try again.")
                return
            auth_code = params.get("code", [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><body><h2>WHOOP connected!</h2><p>You can close this tab and return to your terminal.</p></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress server logs


def prompt(label, secret=False):
    import getpass
    if secret:
        return getpass.getpass(f"{label}: ").strip()
    return input(f"{label}: ").strip()


def main():
    global state_value

    creds_path = _cfg.creds_path()

    print("=" * 60)
    print("  WHOOP Skill — First-Time Setup")
    print("=" * 60)
    print()

    # Step 1: Choose callback method
    print("Step 1 of 3 — Choose your callback method")
    print()
    print("  [A] Local server (default)")
    print(f"      Redirect URI: {REDIRECT_URI_LOCAL}")
    print("      Spins up a temporary server on localhost:8888 to catch the redirect.")
    print("      Requires a browser on the same machine as OpenClaw.")
    print()
    print("  [B] Manual code paste (remote/cloud installs)")
    print(f"      Redirect URI: {REDIRECT_URI_LOCAL}")
    print("      Open the auth URL in any browser, authorize, then copy the")
    print("      ?code= value from the redirect URL and paste it here.")
    print("      No local browser or open ports needed on the server.")
    print()
    choice = input("Choice [A]: ").strip().upper()

    if choice == "B":
        mode = "manual"
    else:
        mode = "local"

    redirect_uri = REDIRECT_URI_LOCAL

    # Step 2: Create the WHOOP app with the correct redirect URI
    print()
    print("Step 2 of 3 — Create your WHOOP Developer App")
    print()
    print("  1. Go to https://developer-dashboard.whoop.com")
    print("  2. Sign in with your WHOOP account")
    print("  3. Create a Team if prompted (any name works)")
    print("  4. Click 'Create App' and fill in:")
    print("       - App name: anything (e.g. 'My WHOOP Skill')")
    print(f"       - Redirect URI: {redirect_uri}")
    print("       - Scopes: select all read:* scopes + offline")
    print("  5. Copy your Client ID and Client Secret")
    print()
    input("Press Enter when your app is created and you have your Client ID and Secret...")

    # Step 3: Collect credentials
    print()
    print("Step 3 of 3 — Connect your WHOOP account")
    print()

    # Load existing creds if present (allow re-auth without re-entering ID/secret)
    existing = {}
    if creds_path.exists():
        try:
            with open(creds_path) as f:
                existing = json.load(f)
        except Exception:
            pass

    if existing.get("client_id"):
        print(f"Existing credentials found at {creds_path}")
        reuse = input("Re-use existing client ID and secret? [Y/n]: ").strip().lower()
        if reuse in ("", "y", "yes"):
            client_id = existing["client_id"]
            client_secret = existing["client_secret"]
        else:
            client_id = prompt("Client ID")
            client_secret = prompt("Client Secret", secret=True)
    else:
        client_id = prompt("Client ID")
        client_secret = prompt("Client Secret", secret=True)

    if not client_id or not client_secret:
        print("ERROR: Client ID and Client Secret are required.")
        sys.exit(1)

    state_value = secrets.token_urlsafe(16)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "state": state_value,
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"

    if mode == "manual":
        print()
        print("Open this URL in your browser to authorize:")
        print(f"\n  {auth_url}\n")
        print("After authorizing, WHOOP will redirect to localhost:8888 — the page")
        print("won't load, but the URL will contain your authorization code.")
        print("Copy the value of the '?code=' parameter from that URL and paste it below.")
        print()
        manual_code = input("Paste the code here: ").strip()
        if not manual_code:
            print("ERROR: No code entered.")
            sys.exit(1)
        print("Exchanging code for tokens...")
        resp = requests.post(TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": manual_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        })
        if not resp.ok:
            print(f"ERROR: Token exchange failed: {resp.text}")
            sys.exit(1)
        data = resp.json()

    else:  # local server
        print()
        print("Opening your browser to authorize WHOOP access...")
        print("If it doesn't open automatically, visit this URL:")
        print(f"\n  {auth_url}\n")
        webbrowser.open(auth_url)
        print(f"Waiting for authorization (listening on http://localhost:{REDIRECT_PORT}) ...")
        server = HTTPServer(("localhost", REDIRECT_PORT), CallbackHandler)
        server.handle_request()

        if not auth_code:
            print("ERROR: No authorization code received.")
            sys.exit(1)

        print("Exchanging code for tokens...")
        resp = requests.post(TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        })
        if not resp.ok:
            print(f"ERROR: Token exchange failed: {resp.text}")
            sys.exit(1)
        data = resp.json()

    creds = {
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", ""),
        "expires_at": int(time.time()) + data.get("expires_in", 3600),
    }

    creds_path.parent.mkdir(parents=True, exist_ok=True)
    with open(creds_path, "w") as f:
        json.dump(creds, f, indent=2)
    creds_path.chmod(0o600)

    print()
    print(f"✓ Setup complete! Credentials saved to {creds_path}")
    print(f"  Access token expires: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creds['expires_at']))}")
    print()
    print("You're all set. Ask your agent about your WHOOP data!")


if __name__ == "__main__":
    main()
