#!/usr/bin/env python3
"""
Save or verify Videoinu access key.

The token is stored at ~/.videoinu/credentials.json so scripts
can read it without needing environment variables.

Usage:
    # Save token
    python3 auth.py save "your-access-key-here"

    # Show current auth status (does NOT print the token)
    python3 auth.py status

    # Verify token works by calling the API
    python3 auth.py verify

    # Remove saved token
    python3 auth.py logout

Output (JSON):
    { "status": "saved", "credentials_path": "~/.videoinu/credentials.json" }
"""

import argparse
import json
import os
import sys
import stat

CREDENTIALS_DIR = os.path.expanduser("~/.videoinu")
CREDENTIALS_PATH = os.path.join(CREDENTIALS_DIR, "credentials.json")


def save_token(token: str):
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    data = {"access_key": token}
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump(data, f, indent=2)
    # Restrict permissions: owner read/write only
    os.chmod(CREDENTIALS_PATH, stat.S_IRUSR | stat.S_IWUSR)
    print(json.dumps({
        "status": "saved",
        "credentials_path": CREDENTIALS_PATH,
        "hint": "Scripts will now auto-read this token. You can also override with VIDEOINU_ACCESS_KEY env var.",
    }, indent=2))


def show_status():
    env_key = os.environ.get("VIDEOINU_ACCESS_KEY", "")
    file_key = ""
    if os.path.isfile(CREDENTIALS_PATH):
        try:
            with open(CREDENTIALS_PATH) as f:
                file_key = json.load(f).get("access_key", "")
        except (json.JSONDecodeError, OSError):
            pass

    active_source = None
    if env_key:
        active_source = "environment variable (VIDEOINU_ACCESS_KEY)"
    elif file_key:
        active_source = f"credentials file ({CREDENTIALS_PATH})"

    print(json.dumps({
        "authenticated": bool(env_key or file_key),
        "source": active_source,
        "env_var_set": bool(env_key),
        "credentials_file_exists": bool(file_key),
    }, indent=2))


def verify_token():
    sys.path.insert(0, os.path.dirname(__file__))
    from _common import require_access_key, api_get, BASE_URL
    require_access_key()
    # A lightweight call to check auth - list graphs with page_size=1
    try:
        data = api_get("/graph/list", params={"page": 1, "page_size": 1})
        print(json.dumps({
            "status": "verified",
            "base_url": BASE_URL,
            "message": "Access key is valid.",
        }, indent=2))
    except SystemExit:
        # api_get already printed error
        pass


def logout():
    if os.path.isfile(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)
        print(json.dumps({"status": "logged_out", "message": "Credentials removed."}))
    else:
        print(json.dumps({"status": "no_credentials", "message": "No saved credentials found."}))


def main():
    parser = argparse.ArgumentParser(description="Manage Videoinu authentication")
    sub = parser.add_subparsers(dest="command")

    save_p = sub.add_parser("save", help="Save access key")
    save_p.add_argument("token", help="Access key (JWT token)")

    sub.add_parser("status", help="Show auth status")
    sub.add_parser("verify", help="Verify token works")
    sub.add_parser("logout", help="Remove saved credentials")

    args = parser.parse_args()

    if args.command == "save":
        save_token(args.token)
    elif args.command == "status":
        show_status()
    elif args.command == "verify":
        verify_token()
    elif args.command == "logout":
        logout()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
