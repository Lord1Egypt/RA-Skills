"""
X Helper — OAuth 2.0 PKCE authorization and token management.
Used as a subprocess by x_client.py. Pure stdlib, no dependencies.
"""

import base64
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.parse
import urllib.request
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.error import URLError


AUTH_DIR = os.path.expanduser("~/.x-helper")
AUTH_FILE = os.path.join(AUTH_DIR, "auth.json")
CALLBACK_PORT = 8080
CALLBACK_PATH = "/callback"
REDIRECT_URI = f"http://localhost:{CALLBACK_PORT}{CALLBACK_PATH}"
AUTHORIZE_URL = "https://x.com/i/oauth2/authorize"
TOKEN_URL = "https://api.x.com/2/oauth2/token"
SCOPES = "tweet.read tweet.write users.read follows.read follows.write like.read like.write bookmark.read bookmark.write offline.access list.read list.write"


def _ensure_dir():
    os.makedirs(AUTH_DIR, mode=0o700, exist_ok=True)


def _load_auth():
    if not os.path.isfile(AUTH_FILE):
        return None
    try:
        with open(AUTH_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _save_auth(data):
    _ensure_dir()
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f)
    os.chmod(AUTH_FILE, 0o600)


def _delete_auth():
    if os.path.isfile(AUTH_FILE):
        os.remove(AUTH_FILE)


def _pkce_challenge(verifier):
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def _token_post(data, client_id=None, client_secret=None):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if client_secret:
        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers["Authorization"] = f"Basic {creds}"
        data = {k: v for k, v in data.items() if k not in ("client_id", "client_secret")}
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        TOKEN_URL, data=body, headers=headers
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except URLError as e:
        error_body = e.read().decode() if hasattr(e, 'read') else str(e)
        return {"error": True, "detail": error_body}
    except Exception as e:
        return {"error": True, "detail": str(e)}


def authorize(client_id, client_secret=None, headless=False):
    """Run the OAuth 2.0 PKCE authorization flow."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = _pkce_challenge(code_verifier)
    state = secrets.token_urlsafe(32)
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"
    auth_code = [None]
    received_state = [None]

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            if "code" in qs:
                auth_code[0] = qs["code"][0]
                received_state[0] = qs.get("state", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>Authorization successful!</h1><p>You can close this window.</p>")
            else:
                err = qs.get("error", ["unknown"])[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h1>Authorization failed</h1><p>Error: {err}</p>".encode())
            # Signal the server to shut down
            self.server.shutdown_signal = True

        def log_message(self, format, *args):
            pass  # suppress logs

    if headless:
        print(f"Open this URL in your browser:\n{auth_url}\n", file=sys.stderr)
        print("After authorizing, paste the full redirect URL here:", file=sys.stderr, end=" ")
        redirect_input = sys.stdin.readline().strip()
        parsed = urllib.parse.urlparse(redirect_input)
        qs = urllib.parse.parse_qs(parsed.query)
        if "code" in qs:
            auth_code[0] = qs["code"][0]
            received_state[0] = qs.get("state", [None])[0]
        else:
            print(json.dumps({"error": True, "detail": "No authorization code received"}))
            sys.exit(1)
    else:
        print("Opening browser for X authorization...", file=sys.stderr)
        webbrowser.open(auth_url)
        server = HTTPServer(("", CALLBACK_PORT), CallbackHandler)
        server.shutdown_signal = False
        timeout = 300
        while not server.shutdown_signal and timeout > 0:
            server.handle_request()
            timeout -= 1
        if timeout <= 0:
            print(json.dumps({"error": True, "detail": "Authorization timed out"}))
            sys.exit(1)

    if received_state[0] != state:
        print(json.dumps({"error": True, "detail": "State mismatch — possible CSRF attack"}))
        sys.exit(1)

    token_data = {
        "code": auth_code[0],
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    result = _token_post(token_data, client_id, client_secret)
    if result.get("error"):
        print(json.dumps(result))
        sys.exit(1)

    result["client_id"] = client_id
    if client_secret:
        result["client_secret"] = client_secret
    result["expires_at"] = int(time.time()) + result.get("expires_in", 7200)
    result["code_verifier"] = code_verifier

    # Fetch current user info
    user_info = _fetch_user_info(result["access_token"])
    if user_info:
        result.update(user_info)

    _save_auth(result)
    print(json.dumps({"ok": True, "user_id": result.get("user_id"), "username": result.get("username")}))


def _fetch_user_info(access_token):
    """Fetch the authenticated user's info."""
    req = urllib.request.Request(
        "https://api.x.com/2/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            user = data.get("data", {})
            return {
                "user_id": user.get("id"),
                "username": user.get("username"),
                "user_name": user.get("name"),
            }
    except Exception:
        return None


def status():
    """Print current auth status as JSON."""
    auth = _load_auth()
    if not auth:
        print(json.dumps({"authenticated": False}))
        return

    token = auth.get("access_token", "")
    masked = token[:10] + "..." + token[-4:] if len(token) > 20 else "***"
    expires_at = auth.get("expires_at", 0)
    now = int(time.time())
    expires_in = max(0, expires_at - now)

    print(json.dumps({
        "authenticated": True,
        "user_id": auth.get("user_id"),
        "username": auth.get("username"),
        "user_name": auth.get("user_name"),
        "token_preview": masked,
        "expires_in_seconds": expires_in,
        "scope": auth.get("scope", ""),
    }))


def logout():
    """Delete stored credentials."""
    _delete_auth()
    print(json.dumps({"ok": True}))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": True, "detail": "Usage: x_auth.py <authorize|status|logout>"}))
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "authorize":
        client_id = os.environ.get("X_CLIENT_ID") or ""
        client_secret = os.environ.get("X_CLIENT_SECRET")
        headless = "--headless" in sys.argv
        # Allow override via args
        for i, arg in enumerate(sys.argv):
            if arg == "--client-id" and i + 1 < len(sys.argv):
                client_id = sys.argv[i + 1]
            if arg == "--client-secret" and i + 1 < len(sys.argv):
                client_secret = sys.argv[i + 1]
        if not client_id:
            print(json.dumps({"error": True, "detail": "CLIENT_ID required. Set X_CLIENT_ID env var or pass --client-id"}))
            sys.exit(1)
        authorize(client_id, client_secret, headless=headless)
    elif cmd == "status":
        status()
    elif cmd == "logout":
        logout()
    else:
        print(json.dumps({"error": True, "detail": f"Unknown command: {cmd}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
