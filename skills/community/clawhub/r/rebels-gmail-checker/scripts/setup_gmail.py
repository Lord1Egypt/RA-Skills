#!/usr/bin/env python3
"""One-time setup script for Gmail API OAuth credentials.

Saves credentials to <DATA_DIR>/gmail.json with a refresh token.
Requires: google-auth-oauthlib, google-api-python-client

DATA_DIR resolution order:
  1. $SKILL_DATA_DIR          (set by agent platform)
  2. ~/.config/gmail-checker   (XDG default)

Usage:
  python3 setup_gmail.py              # interactive, opens browser
  python3 setup_gmail.py --no-browser # prints URL for manual auth (headless/SSH)

See references/setup.md for full setup guide.
"""

import json
import os
import sys
import webbrowser

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# --- Path resolution (same logic as check_gmail.py) ---
DATA_DIR = os.path.expanduser(
    os.environ.get("SKILL_DATA_DIR", "~/.config/gmail-checker")
)
CREDS_PATH = os.path.join(DATA_DIR, "gmail.json")


def check_dependencies():
    missing = []
    try:
        import google_auth_oauthlib  # noqa: F401
    except ImportError:
        missing.append("google-auth-oauthlib")
    try:
        import googleapiclient  # noqa: F401
    except ImportError:
        missing.append("google-api-python-client")
    if missing:
        print("Missing required packages. Install with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)


def save_credentials(creds_data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CREDS_PATH, "w") as f:
        json.dump(creds_data, f, indent=2)
    os.chmod(CREDS_PATH, 0o600)
    print(f"\nCredentials saved to {CREDS_PATH}")


def run_browser_flow(client_id, client_secret):
    """Open browser for OAuth (works on desktop/laptop)."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    print("\nOpening browser for Google authorization...")
    print("(If no browser opens, re-run with --no-browser)\n")

    try:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True, timeout_seconds=120)
    except Exception as e:
        print(f"\nOAuth flow failed: {e}")
        print("Make sure your Gmail address is added as a Test User in the OAuth consent screen.")
        sys.exit(1)

    return creds


def run_console_flow(client_id, client_secret):
    """Manual auth flow for headless machines (Pi, SSH, containers)."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    auth_url, _ = flow.authorization_url(prompt="consent")

    print("\n" + "=" * 60)
    print("Open this URL in a browser on any device:")
    print(auth_url)
    print("=" * 60)
    print("\nAfter authorizing, you'll get an authorization code.")
    print("Paste it here and press Enter.")

    code = input("\nAuthorization code: ").strip()
    if not code:
        print("Error: No code provided.")
        sys.exit(1)

    try:
        flow.fetch_token(code=code)
        return flow.credentials
    except Exception as e:
        print(f"\nToken exchange failed: {e}")
        print("Make sure the code is correct and hasn't expired.")
        sys.exit(1)


def main():
    check_dependencies()

    args = sys.argv[1:]
    no_browser = "--no-browser" in args

    print("Gmail Checker — OAuth Setup")
    print("=" * 35)
    print(f"Data directory: {DATA_DIR}")
    if no_browser:
        print("Mode: console (no browser — for headless/SSH)")

    if os.path.exists(CREDS_PATH):
        print(f"\nCredentials already exist at {CREDS_PATH}")
        overwrite = input("Overwrite? [y/N] ").strip().lower()
        if overwrite != "y":
            print("Aborted.")
            return

    print("\nPaste your Google OAuth credentials (from Google Cloud Console > Credentials):")
    print("  Application type: Desktop app\n")

    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    if not client_id or not client_secret:
        print("Error: Client ID and Client Secret are required.")
        sys.exit(1)

    if no_browser:
        creds = run_console_flow(client_id, client_secret)
    else:
        creds = run_browser_flow(client_id, client_secret)

    save_credentials({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": creds.refresh_token,
    })

    print("Setup complete! Test with:")
    print("  python3 scripts/check_gmail.py")


if __name__ == "__main__":
    main()
