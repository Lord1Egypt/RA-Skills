#!/usr/bin/env python3
"""Refresh the WHOOP access token using the stored refresh token."""

import json
import time
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as _cfg

CREDS_PATH = _cfg.creds_path()
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"


def load_creds():
    if not CREDS_PATH.exists():
        print(f"ERROR: Credentials file not found at {CREDS_PATH}", file=sys.stderr)
        print("Run scripts/auth.py first to complete the initial OAuth flow.", file=sys.stderr)
        sys.exit(1)
    with open(CREDS_PATH) as f:
        return json.load(f)


def save_creds(creds):
    CREDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDS_PATH, "w") as f:
        json.dump(creds, f, indent=2)


def refresh(creds):
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "refresh_token",
        "refresh_token": creds["refresh_token"],
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "scope": "offline read:recovery read:cycles read:workout read:sleep read:profile read:body_measurement",
    })
    resp.raise_for_status()
    return resp.json()


def main():
    creds = load_creds()

    # Check if refresh is actually needed
    expires_at = creds.get("expires_at", 0)
    if expires_at - time.time() > 60 and "--force" not in sys.argv:
        print("Token is still valid, skipping refresh. Use --force to override.")
        return

    print("Refreshing WHOOP access token...")
    data = refresh(creds)

    creds["access_token"] = data["access_token"]
    creds["refresh_token"] = data.get("refresh_token", creds["refresh_token"])
    creds["expires_at"] = int(time.time()) + data.get("expires_in", 3600)

    save_creds(creds)
    print(f"Token refreshed. Expires at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creds['expires_at']))}")


if __name__ == "__main__":
    main()
