#!/usr/bin/env python3
"""Tekan Device Authorization CLI (OAuth 2.0 Device Flow).

Uses the remote Tekan OAuth service — no local server required.

  python auth.py login   — Full flow: init → open browser → poll → save credentials
  python auth.py poll    — Resume polling a previously started login (recovery only)
  python auth.py status  — Check current login state
  python auth.py logout  — Remove saved credentials

Usage:
    python auth.py login
    python auth.py status
    python auth.py logout
"""

import argparse
import json
import sys
import time
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

import requests
from typing import Optional

OAUTH_BASE_URL = "https://api.tekan.cn"
CLIENT_ID = "tkv-skill"
DEFAULT_SCOPE = "read:profile read:billing read:apikey"

CRED_FILE = Path.home() / ".tekan" / "credentials.json"
PENDING_FILE = Path.home() / ".tekan" / "pending_device.json"
LOGIN_TIMEOUT = 600  # 10 minutes, matching server-side expiry


# ---------------------------------------------------------------------------
# Credential file helpers
# ---------------------------------------------------------------------------

def _save_credentials(data: dict) -> None:
    """Persist user credentials returned by the OAuth APPROVED response."""
    CRED_FILE.parent.mkdir(parents=True, exist_ok=True)

    api_keys = data.get("api_keys", [])
    api_key = api_keys[0] if api_keys else ""

    creds = {
        "uid": data.get("uid", ""),
        "api_key": api_key,
        "email": data.get("email", ""),
        "name": data.get("name", ""),
        "team_id": data.get("team_id", ""),
        "role": data.get("role", ""),
        "charge_type": data.get("charge_type", ""),
        "remain_credit": data.get("remain_credit"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    if data.get("access_token"):
        creds["access_token"] = data["access_token"]
        creds["token_type"] = data.get("token_type", "Bearer")

    CRED_FILE.write_text(json.dumps(creds, indent=2))
    CRED_FILE.chmod(0o600)


def _load_credentials() -> Optional[dict]:
    if not CRED_FILE.exists():
        return None
    try:
        return json.loads(CRED_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _delete_credentials() -> bool:
    if CRED_FILE.exists():
        CRED_FILE.unlink()
        return True
    return False


def _mask_key(key: str) -> str:
    if len(key) <= 8:
        return "***"
    return key[:4] + "..." + key[-4:]


# ---------------------------------------------------------------------------
# API key fetching
# ---------------------------------------------------------------------------

def _fetch_api_key(access_token: str, app_key: str) -> dict:
    """Fetch API key info from /topview/apikey/get after successful authorization.

    Returns a dict with uid, apiKey, teamId (empty dict on failure).
    """
    try:
        resp = requests.get(
            f"{OAUTH_BASE_URL}/topview/apikey/get",
            params={"source": app_key},
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        body = resp.json()
        return body.get("data") or body.get("result") or body
    except requests.RequestException as e:
        print(f"Warning: could not fetch API key: {e}", file=sys.stderr)
        return {}


# ---------------------------------------------------------------------------
# Core polling logic (shared by login and poll)
# ---------------------------------------------------------------------------

def _poll_for_approval(token_endpoint: str, interval: int, app_key: str) -> None:
    """Poll token_endpoint until authorized (200), pending (428), or timeout.

    On success: fetches API key, saves credentials, cleans up pending file.
    On failure: prints error to stderr and calls sys.exit(1).
    """
    print("Waiting for authorization (Ctrl+C to cancel)...", file=sys.stderr)

    start = time.time()

    try:
        while time.time() - start < LOGIN_TIMEOUT:
            time.sleep(interval)
            elapsed = int(time.time() - start)
            print(f"  [{elapsed}s] checking...", file=sys.stderr, end="\r")

            try:
                resp = requests.get(token_endpoint, timeout=10)
                body = resp.json()
            except (requests.RequestException, ValueError):
                continue

            code = body.get("code", resp.status_code)

            if code == 428:
                continue

            if code == 200:
                token_data = body.get("data") or body

                access_token = token_data.get("token", "")
                apikey_data = {}
                if access_token:
                    apikey_data = _fetch_api_key(access_token, app_key)

                api_key = apikey_data.get("apiKey", "") or apikey_data.get("api_key", "")

                if not api_key:
                    PENDING_FILE.unlink(missing_ok=True)
                    recharge_url = "https://tekan.cn/subscription?action=recharge"
                    print()
                    print()
                    print("  Authorization succeeded, but no API key available.", file=sys.stderr)
                    print("  This usually means your account has 0 credits.", file=sys.stderr)
                    print(f"  [点击充值]({recharge_url})", file=sys.stderr)
                    print(f"  {recharge_url}", file=sys.stderr)
                    print("  After recharging, run `auth.py login` again.", file=sys.stderr)
                    print()
                    _try_open_browser(recharge_url)
                    sys.exit(1)

                merged = {
                    "uid": apikey_data.get("uid", token_data.get("thirdUid", str(token_data.get("userId", "")))),
                    "name": token_data.get("realName", ""),
                    "team_id": apikey_data.get("teamId", ""),
                    "access_token": access_token,
                    "api_keys": [api_key],
                }

                _save_credentials(merged)
                PENDING_FILE.unlink(missing_ok=True)

                print()
                print()
                print("  Logged in successfully!")
                print(f"  uid:         {merged['uid']}")
                print(f"  name:        {merged['name']}")
                print(f"  api_key:     {_mask_key(api_key)}")
                print(f"  Saved to:    {CRED_FILE}")
                print()
                return

            PENDING_FILE.unlink(missing_ok=True)
            print(
                f"\nUnexpected response (code={code}): {body.get('msg', resp.text)}",
                file=sys.stderr,
            )
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nPolling cancelled.", file=sys.stderr)
        sys.exit(130)

    print(
        f"\nTimeout: no authorization received within {LOGIN_TIMEOUT}s.",
        file=sys.stderr,
    )
    PENDING_FILE.unlink(missing_ok=True)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def _try_open_browser(url: str) -> None:
    """Best-effort browser open — silently ignored if unavailable."""
    try:
        webbrowser.open(url)
    except Exception:
        pass


def cmd_login(args) -> None:
    """Full login flow: init device code → open browser → poll until done."""
    try:
        resp = requests.post(
            f"{OAUTH_BASE_URL}/oauth/device/code",
            json={
                "client_id": CLIENT_ID,
                "scope": DEFAULT_SCOPE,
            },
            timeout=10,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: could not reach OAuth server: {e}", file=sys.stderr)
        sys.exit(1)

    body = resp.json()
    data = body.get("data") or body
    device_code = data["device_code"]
    verification_url = data["verification_uri_complete"]
    token_endpoint = data["token_endpoint"]
    interval = data.get("interval", 2)
    expires_in = data.get("expires_in", 600)
    app_key = data.get("app_key", "openclaw")

    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps({
        "device_code": device_code,
        "token_endpoint": token_endpoint,
        "interval": interval,
        "expires_in": expires_in,
        "app_key": app_key,
        "verification_uri_complete": verification_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }, indent=2))

    print()
    print(f"复制下方链接到浏览器中登录，登录后将解锁以下能力：")
    print(f"[点击登录]({verification_url})")
    print(f"{verification_url}")
    print()

    _try_open_browser(verification_url)

    _poll_for_approval(token_endpoint, interval, app_key)


def cmd_poll(args) -> None:
    """Resume polling a previously started login (recovery if login was interrupted)."""
    if not PENDING_FILE.exists():
        print(
            "Error: no pending login found. Run `auth.py login` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        pending = json.loads(PENDING_FILE.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: could not read pending device file: {e}", file=sys.stderr)
        sys.exit(1)

    _poll_for_approval(
        pending["token_endpoint"],
        pending.get("interval", 2),
        pending.get("app_key", "openclaw"),
    )


def cmd_logout(args) -> None:
    if _delete_credentials():
        print(f"Logged out. Removed {CRED_FILE}")
    else:
        print("Not logged in (no credentials file found).")


def cmd_status(args) -> None:
    creds = _load_credentials()
    if creds is None:
        print("Not logged in.")
        print("Run: python auth.py login")
        sys.exit(1)

    uid = creds.get("uid", "(unknown)")
    api_key = creds.get("api_key", "")
    email = creds.get("email", "")
    name = creds.get("name", "")
    charge_type = creds.get("charge_type", "")
    created_at = creds.get("created_at", "(unknown)")

    print("Logged in")
    print(f"  uid:         {uid}")
    if name:
        print(f"  name:        {name}")
    if email:
        print(f"  email:       {email}")
    print(f"  api_key:     {_mask_key(api_key)}")
    if charge_type:
        print(f"  charge_type: {charge_type}")
    print(f"  authorized:  {created_at}")
    print(f"  file:        {CRED_FILE}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Tekan Device Authorization — log in via browser and save credentials.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Subcommands:
  login   Full flow: open browser → wait for authorization → save credentials
  poll    Resume a previously interrupted login (recovery only)
  logout  Remove saved credentials
  status  Show current login state

Examples:
  python auth.py login     # complete login flow (opens browser, waits, saves)
  python auth.py status    # check if logged in
  python auth.py logout    # remove credentials
""",
    )
    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    sub.add_parser("login",  help="Open browser for authorization, wait, save credentials")
    sub.add_parser("poll",   help="Resume a previously interrupted login")
    sub.add_parser("logout", help="Remove saved credentials")
    sub.add_parser("status", help="Show current login state")

    args = parser.parse_args()

    handlers = {
        "login": cmd_login,
        "poll": cmd_poll,
        "logout": cmd_logout,
        "status": cmd_status,
    }
    handlers[args.subcommand](args)


if __name__ == "__main__":
    main()
