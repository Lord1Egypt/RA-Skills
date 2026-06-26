#!/usr/bin/env python3
"""Spotify OAuth2 Authorization Code flow for OpenClaw skill."""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
import base64

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "..", "config.json")

SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-library-read",
    "user-library-modify",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private",
    "playlist-read-collaborative",
    "user-top-read",
    "user-read-recently-played",
    "user-follow-read",
    "user-follow-modify",
    "user-read-email",
    "user-read-private",
]


def load_config():
    """Load config from config.json, with env var overrides."""
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    # Env vars override config.json values
    if os.environ.get("SPOTIFY_CLIENT_ID"):
        cfg["client_id"] = os.environ["SPOTIFY_CLIENT_ID"]
    if os.environ.get("SPOTIFY_CLIENT_SECRET"):
        cfg["client_secret"] = os.environ["SPOTIFY_CLIENT_SECRET"]
    if os.environ.get("SPOTIFY_REDIRECT_URI"):
        cfg["redirect_uri"] = os.environ["SPOTIFY_REDIRECT_URI"]
    return cfg


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def refresh_token(cfg=None):
    if cfg is None:
        cfg = load_config()
    tokens = cfg.get("tokens")
    if not tokens or not tokens.get("refresh_token"):
        return False

    auth = base64.b64encode(f"{cfg['client_id']}:{cfg['client_secret']}".encode()).decode()
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
    }).encode()
    req = urllib.request.Request("https://accounts.spotify.com/api/token", data=data, headers={
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        tokens["access_token"] = result["access_token"]
        tokens["expires_at"] = int(time.time()) + result.get("expires_in", 3600)
        if "refresh_token" in result:
            tokens["refresh_token"] = result["refresh_token"]
        cfg["tokens"] = tokens
        save_config(cfg)
        return True
    except Exception as e:
        print(f"Token refresh failed: {e}", file=sys.stderr)
        return False


def get_valid_token():
    cfg = load_config()
    tokens = cfg.get("tokens")
    if not tokens or not tokens.get("access_token"):
        return None
    if tokens.get("expires_at", 0) - time.time() < 60:
        if not refresh_token(cfg):
            return None
        cfg = load_config()
    return cfg["tokens"]["access_token"]


def do_auth(code=None):
    """Run OAuth2 flow. If code is provided, exchange it directly. Otherwise print the auth URL."""
    cfg = load_config()
    scope = " ".join(SCOPES)
    params = urllib.parse.urlencode({
        "client_id": cfg["client_id"],
        "response_type": "code",
        "redirect_uri": cfg["redirect_uri"],
        "scope": scope,
    })
    auth_url = f"https://accounts.spotify.com/authorize?{params}"

    if code:
        # Exchange the code directly
        pass
    else:
        print("Open this URL in your browser to authorize:")
        print(auth_url)
        print()
        code = input("After authorizing, paste the 'code' parameter from the redirect URL: ").strip()

    if not code:
        print("No code provided.", file=sys.stderr)
        sys.exit(1)

    auth = base64.b64encode(f"{cfg['client_id']}:{cfg['client_secret']}".encode()).decode()
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": cfg["redirect_uri"],
    }).encode()
    req = urllib.request.Request("https://accounts.spotify.com/api/token", data=data, headers={
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    })

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        cfg["tokens"] = {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "expires_at": int(time.time()) + result.get("expires_in", 3600),
        }
        save_config(cfg)
        print("Authorization successful! Tokens saved.")
    except urllib.error.HTTPError as e:
        print(f"Authorization failed: {e.code} {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "auth":
        code = sys.argv[2] if len(sys.argv) > 2 else None
        do_auth(code)
    elif len(sys.argv) > 1 and sys.argv[1] == "refresh":
        ok = refresh_token()
        print("Token refreshed." if ok else "Refresh failed.")
    else:
        print("Usage: auth.py auth [code]  |  auth.py refresh")
        print()
        print("  auth          Print auth URL, prompt for code")
        print("  auth <code>   Exchange an authorization code directly")
        print("  refresh       Refresh the access token")
