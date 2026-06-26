#!/usr/bin/env python3
"""
WHOOP OAuth 2.0 Authorization Flow.

Two modes:
  1. Local  — browser can reach localhost:9527, fully automatic
  2. Remote — server can't receive browser callback, manually provide the code

Usage:
    # Local (browser on same machine):
    python3 auth.py

    # Remote (OpenClaw on server, browser on another machine):
    python3 auth.py --print-url          # Step 1: get the auth URL
    python3 auth.py --code <auth_code>   # Step 2: exchange code for tokens

    # Or provide the full callback URL:
    python3 auth.py --callback-url "http://localhost:9527/callback?code=xxx&state=yyy"
"""

import argparse
import http.server
import json
import os
import secrets
import sys
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TOKEN_FILE = DATA_DIR / "tokens.json"
STATE_FILE = DATA_DIR / ".auth_state"  # persists state for remote flow

AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
REDIRECT_URI = "http://localhost:9527/callback"
SCOPES = "read:recovery read:cycles read:workout read:sleep read:profile read:body_measurement offline"


def get_credentials():
    """Get client_id and client_secret from environment or 1Password."""
    client_id = os.environ.get("WHOOP_CLIENT_ID")
    client_secret = os.environ.get("WHOOP_CLIENT_SECRET")

    if client_id and client_secret:
        return client_id, client_secret

    # Try 1Password
    try:
        op_token_path = Path.home() / ".openclaw" / ".op-token"
        if op_token_path.exists():
            os.environ["OP_SERVICE_ACCOUNT_TOKEN"] = op_token_path.read_text().strip()

        import subprocess
        result = subprocess.run(
            ["op", "item", "get", "whoop", "--vault", "Agent", "--format", "json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            item = json.loads(result.stdout)
            for f in item.get("fields", []):
                if f.get("purpose") == "USERNAME":
                    client_id = f.get("value", "")
                elif f.get("purpose") == "PASSWORD":
                    client_secret = f.get("value", "")
            if client_id and client_secret:
                return client_id, client_secret
    except Exception as e:
        print(f"1Password read failed: {e}", file=sys.stderr)

    print("Error: WHOOP_CLIENT_ID and WHOOP_CLIENT_SECRET required.", file=sys.stderr)
    print("Set env vars or store in 1Password (vault: Agent, item: whoop).", file=sys.stderr)
    sys.exit(1)


def exchange_code(code: str, client_id: str, client_secret: str) -> dict:
    """Exchange authorization code for tokens via curl (bypasses Cloudflare 1010)."""
    import subprocess
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    })

    r = subprocess.run([
        "curl", "-s", "-w", "\n%{http_code}",
        "-X", "POST", TOKEN_URL,
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "-d", data,
    ], capture_output=True, text=True, timeout=15)
    lines = r.stdout.strip().rsplit("\n", 1)
    body = lines[0] if len(lines) > 1 else r.stdout
    status = lines[-1] if len(lines) > 1 else "?"
    if status != "200":
        print(f"Token exchange failed: {status} {body[:300]}", file=sys.stderr)
        sys.exit(1)
    return json.loads(body)


def save_tokens(tokens: dict):
    """Save tokens to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    os.chmod(TOKEN_FILE, 0o600)
    print(f"✅ Tokens saved to {TOKEN_FILE}")
    print(f"   Access token expires in {tokens.get('expires_in', '?')} seconds")
    if "refresh_token" in tokens:
        print("   Refresh token: ✅ (auto-renewal enabled)")
    else:
        print("   ⚠️ No refresh token — did you include 'offline' scope?")


def build_auth_url(client_id: str, state: str) -> str:
    """Build the OAuth authorization URL."""
    params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
    })
    return f"{AUTH_URL}?{params}"


def mode_local(client_id: str, client_secret: str):
    """Full local flow: start callback server, wait for browser redirect."""
    state = secrets.token_urlsafe(8)[:8]
    auth_url = build_auth_url(client_id, state)

    print(f"\n🔗 Open this URL in your browser to authorize:\n\n{auth_url}\n")
    print(f"Waiting for callback on http://localhost:9527 ... (timeout: 3 min)\n")

    authorization_code = None

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal authorization_code
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)

            if "code" in qs:
                returned_state = qs.get("state", [""])[0]
                if returned_state != state:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"<h1>State mismatch!</h1><p>Try again from the beginning.</p>")
                    return

                authorization_code = qs["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Authorization successful!</h1><p>You can close this tab.</p>")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No code received.")

        def log_message(self, format, *args):
            pass  # Suppress log output

    server = http.server.HTTPServer(("localhost", 9527), CallbackHandler)
    server.timeout = 180  # 3 minutes
    server.handle_request()

    if not authorization_code:
        print("Error: No authorization code received.", file=sys.stderr)
        sys.exit(1)

    print("✅ Got authorization code, exchanging for tokens...")
    tokens = exchange_code(authorization_code, client_id, client_secret)
    save_tokens(tokens)


def mode_print_url(client_id: str):
    """Remote step 1: print auth URL and save state for later."""
    state = secrets.token_urlsafe(8)[:8]
    auth_url = build_auth_url(client_id, state)

    # Save state so --code can verify it later
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"state": state}))

    print(f"\n🔗 Open this URL in your browser to authorize:\n")
    print(auth_url)
    print(f"\nAfter authorizing, the browser will redirect to localhost:9527 (which won't load).")
    print(f"Copy the FULL URL from the browser address bar and run:\n")
    print(f"  python3 auth.py --callback-url \"<paste the full URL here>\"\n")
    print(f"Or extract the 'code' parameter and run:\n")
    print(f"  python3 auth.py --code \"<the code value>\"\n")


def mode_exchange_code(code: str, client_id: str, client_secret: str):
    """Remote step 2: exchange a manually-provided code for tokens."""
    print("Exchanging authorization code for tokens...")
    tokens = exchange_code(code, client_id, client_secret)
    save_tokens(tokens)
    # Clean up state file
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def mode_callback_url(url: str, client_id: str, client_secret: str):
    """Remote step 2 (alt): extract code from a pasted callback URL."""
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)

    code = qs.get("code", [None])[0]
    if not code:
        print("Error: No 'code' parameter found in the URL.", file=sys.stderr)
        print(f"URL received: {url}", file=sys.stderr)
        sys.exit(1)

    # Optionally verify state
    returned_state = qs.get("state", [None])[0]
    if returned_state and STATE_FILE.exists():
        saved = json.loads(STATE_FILE.read_text())
        if saved.get("state") != returned_state:
            print(f"⚠️  State mismatch (expected {saved.get('state')}, got {returned_state}).")
            print("   Proceeding anyway — the code may still be valid.\n")

    mode_exchange_code(code, client_id, client_secret)


def main():
    parser = argparse.ArgumentParser(description="WHOOP OAuth 2.0 Authorization")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--print-url", action="store_true",
                       help="Print auth URL only (for remote/server use)")
    group.add_argument("--code",
                       help="Exchange an authorization code directly (remote step 2)")
    group.add_argument("--callback-url",
                       help="Extract code from the full callback URL (remote step 2)")
    args = parser.parse_args()

    client_id, client_secret = get_credentials()

    if args.print_url:
        mode_print_url(client_id)
    elif args.code:
        mode_exchange_code(args.code, client_id, client_secret)
    elif args.callback_url:
        mode_callback_url(args.callback_url, client_id, client_secret)
    else:
        mode_local(client_id, client_secret)


if __name__ == "__main__":
    main()
