"""Thin wrapper around OpenClaw's `gog` CLI for Gmail access.

`gog` owns OAuth + token refresh; this module just shells out to it.
Replaces what would otherwise be an IMAP layer.

Prerequisites on the user's machine (via OpenClaw):
    brew install steipete/tap/gogcli
    gog auth credentials ~/path/to/client_secret.json
    gog auth add you@gmail.com --services gmail
"""

from __future__ import annotations

import base64
import json
import shutil
import subprocess


class GogError(RuntimeError):
    pass


def is_gog_installed() -> bool:
    return shutil.which("gog") is not None


def verify_auth(account: str) -> bool:
    """Check that `gog auth list` contains the given account.

    Tolerant of two shapes gog has used in practice:
    - `[{"email": ...}, ...]` (bare list)
    - `{"accounts": [{"email": ...}, ...]}` (wrapped — current)
    """
    try:
        result = subprocess.run(
            ["gog", "auth", "list", "--json"],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return False
    if result.returncode != 0:
        return False
    try:
        data = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return False
    if isinstance(data, dict):
        accounts = data.get("accounts") or data.get("items") or []
    else:
        accounts = data
    return any(isinstance(a, dict) and a.get("email") == account for a in accounts)


class GogClient:
    def __init__(self, account: str):
        if not account:
            raise ValueError("account is required")
        self.account = account

    def list_unread(
        self,
        query: str = "in:inbox is:unread",
        max_results: int = 20,
    ) -> list[dict]:
        """Return a list of message refs. Uses `gog gmail messages search`.

        Tolerates both observed shapes:
        - `[{...}, ...]` (bare list)
        - `{"messages": [{...}, ...], "nextPageToken": "..."}` (wrapped — current gog)
        """
        args = [
            "gog", "gmail", "messages", "search", query,
            "--account", self.account,
            "--max", str(max_results),
            "--json",
        ]
        data = self._run_json(args, expect_list=True)
        return _unwrap_list(data, keys=("messages", "items", "results"))

    def search(self, query: str, max_results: int = 20) -> list[dict]:
        return self.list_unread(query=query, max_results=max_results)

    def fetch_mime(self, message_id: str) -> bytes:
        """Fetch raw RFC-822 bytes via `gog gmail get --format raw`.

        Tolerates shapes:
        - `{"raw": "<b64>"}` (bare)
        - `{"message": {"raw": "<b64>", ...}, "headers": {...}}` (wrapped — current gog)
        """
        args = [
            "gog", "gmail", "get", message_id,
            "--account", self.account,
            "--format", "raw",
            "--json",
        ]
        data = self._run_json(args)
        raw = data.get("raw")
        if not raw and isinstance(data.get("message"), dict):
            raw = data["message"].get("raw")
        if not raw:
            raise GogError(f"no `raw` field in response for {message_id}")
        # Gmail API returns url-safe base64 without padding; add back
        pad_len = (-len(raw)) % 4
        return base64.urlsafe_b64decode(raw + ("=" * pad_len))

    def mark_read(self, message_id: str) -> None:
        """Remove the UNREAD label so repeats don't resurface on the next poll."""
        args = [
            "gog", "gmail", "messages", "modify", message_id,
            "--account", self.account,
            "--remove-label", "UNREAD",
            "--json",
        ]
        self._run_json(args)

    def _run_json(self, args: list[str], *, expect_list: bool = False):
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=False)
        except FileNotFoundError as exc:
            raise GogError(f"gog CLI not found on PATH: {exc}") from exc
        if result.returncode != 0:
            raise GogError(
                f"gog failed (rc={result.returncode}): {result.stderr or result.stdout}"
            )
        try:
            payload = json.loads(result.stdout or ("[]" if expect_list else "{}"))
        except json.JSONDecodeError as exc:
            raise GogError(f"gog returned invalid JSON: {exc}") from exc
        return payload


def _unwrap_list(data, *, keys: tuple[str, ...]) -> list:
    """Return a list from either a bare-list response or a wrapped object.

    `gog` wraps collection endpoints differently across versions:
    - `gog gmail messages search --json` → {"messages": [...]}
    - `gog auth list --json`             → {"accounts": [...]}
    Older docs showed bare lists. Accept both.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []
