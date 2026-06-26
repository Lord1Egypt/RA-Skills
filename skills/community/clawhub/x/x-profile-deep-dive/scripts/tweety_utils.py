"""tweety_utils.py — Shared tweety-ns helpers for X/Twitter scripts."""

import json
import os
import sys


DEFAULT_COOKIES_PATH = os.path.expanduser(os.getenv("TWITTER_COOKIES_PATH", "~/.openclaw/workspace/config/twitter_cookies.json"))
DEFAULT_SESSION_DIR = os.path.expanduser(os.getenv("TWITTER_SESSION_DIR", "~/.openclaw/workspace/config/tw_session"))


def load_cookies_file(cookies_path):
    """Load cookies dict from a JSON file."""
    if not os.path.exists(cookies_path):
        sys.stderr.write(f"Error: cookie file not found: {cookies_path}\n")
        sys.exit(1)
    with open(cookies_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_app(session_dir):
    """Create a tweety Twitter client with session storage."""
    from tweety import Twitter

    os.makedirs(session_dir, exist_ok=True)
    session_path = os.path.join(session_dir, "tw_session")
    return Twitter(session_path)


def login_app(app, cookies_dict):
    """Login to Twitter via cookies. Exits on failure."""
    try:
        app.load_cookies(cookies_dict)
    except Exception as e:
        sys.stderr.write(f"Error: login failed: {e}\n")
        sys.exit(2)


def _flatten_tweets(items):
    """Flatten a list that may contain Tweet and SelfThread objects.

    SelfThread objects wrap a thread of tweets; we extract the individual
    Tweet objects from them.
    """
    result = []
    for item in items:
        if hasattr(item, "tweets") and not hasattr(item, "id"):
            # SelfThread — expand into individual tweets
            result.extend(item.tweets)
        else:
            result.append(item)
    return result


def _safe_int(val):
    """Convert a value to int, returning 0 for non-numeric values."""
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def _safe_str(val, default=""):
    """Convert a value to string, returning default for None."""
    if val is None:
        return default
    return str(val)


def _iso(dt):
    """Convert a datetime to ISO format string."""
    if dt is None:
        return ""
    try:
        return dt.isoformat()
    except Exception:
        return str(dt)
