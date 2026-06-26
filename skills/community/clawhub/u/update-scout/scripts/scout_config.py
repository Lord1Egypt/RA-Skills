"""
scout - scout_config.py
Shared constants and GitHub API helper used by all scout scripts.
"""

import json
import os
import urllib.request
from typing import Union

DEFAULT_CONFIG_DIR = os.path.expanduser("~/.config/scout")
DEFAULT_WATCHLIST_PATH = os.path.join(DEFAULT_CONFIG_DIR, "watchlist.json")
DEFAULT_SKIP_PATH = os.path.join(DEFAULT_CONFIG_DIR, "skip_list.json")


def github_request(url: str) -> Union[dict, list]:
    """Make an authenticated (if GITHUB_TOKEN set) GitHub API request."""
    headers = {"User-Agent": "scout-skill/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())
