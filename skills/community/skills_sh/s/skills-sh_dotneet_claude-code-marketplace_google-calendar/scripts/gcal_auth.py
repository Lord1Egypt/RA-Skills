#!/usr/bin/env python3
import argparse
import os
import pathlib
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Authenticate Google Calendar API and store token.")
    parser.add_argument(
        "--credentials",
        help="Path to OAuth client credentials JSON (Desktop app).",
        default=os.environ.get(
            "GCAL_CREDENTIALS",
            os.path.expanduser("~/.config/google-calendar/credentials.json"),
        ),
    )
    parser.add_argument(
        "--token",
        help="Path to store OAuth token JSON.",
        default=os.environ.get(
            "GCAL_TOKEN_PATH",
            os.path.expanduser("~/.config/google-calendar/token.json"),
        ),
    )
    parser.add_argument(
        "--scopes",
        nargs="*",
        default=DEFAULT_SCOPES,
        help="OAuth scopes (space separated).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use console-based auth flow (prints a URL).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="Local server port for auth (0 = auto).",
    )
    return parser.parse_args()


def ensure_parent(path: str) -> None:
    parent = pathlib.Path(path).expanduser().resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    args = parse_args()

    credentials_path = pathlib.Path(args.credentials).expanduser().resolve()
    if not credentials_path.exists():
        print(f"Credentials file not found: {credentials_path}", file=sys.stderr)
        return 2

    ensure_parent(args.token)

    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), scopes=args.scopes)
    if args.no_browser:
        creds = flow.run_console()
    else:
        creds = flow.run_local_server(port=args.port)

    token_path = pathlib.Path(args.token).expanduser().resolve()
    token_path.write_text(creds.to_json())
    print(f"Token saved to: {token_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
