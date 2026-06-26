"""Load Tekan API credentials.

Reads from ~/.tekan/credentials.json (set by auth.py login).
"""

import json
import sys
from pathlib import Path
from typing import Optional

CRED_FILE = Path.home() / ".tekan" / "credentials.json"


def _load_from_file() -> Optional[dict]:
    """Read uid, api_key, and access_token from the local credentials file."""
    if not CRED_FILE.exists():
        return None
    try:
        data = json.loads(CRED_FILE.read_text())
        uid = data.get("uid", "").strip()
        api_key = data.get("api_key", "").strip()
        if uid and api_key:
            result = {"uid": uid, "api_key": api_key}
            access_token = data.get("access_token", "").strip()
            if access_token:
                result["access_token"] = access_token
            return result
    except (json.JSONDecodeError, OSError):
        pass
    return None


def load_config() -> dict:
    """Return a dict with uid and api_key, or exit with a helpful error message."""
    creds = _load_from_file()
    if creds:
        return creds

    print(
        "Error: Tekan credentials not found.\n\n"
        "Log in with the auth module:\n"
        "  python scripts/auth.py login   # opens browser for authorization\n",
        file=sys.stderr,
    )
    sys.exit(1)
