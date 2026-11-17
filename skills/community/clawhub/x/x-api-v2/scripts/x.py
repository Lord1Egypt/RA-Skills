#!/usr/bin/env python3
"""X (Twitter) API v2 client: profiles, posts, threads, search, home timeline, bookmarks, likes and posting.

Usage:
    python3 x.py user USERNAME                       # Profile: bio, counts, verification
    python3 x.py timeline USERNAME [--max N] [--exclude retweets,replies]
    python3 x.py thread TWEET_URL_OR_ID              # The author's own posts in that conversation
    python3 x.py search "query" [--max N]            # Posts from the last 7 days
    python3 x.py tweet TWEET_URL_OR_ID
    python3 x.py tweets TWEET_URL_OR_ID [...]        # Up to 100 in one request
    python3 x.py home [--max N] [--exclude retweets,replies]      # Needs the sign-in
    python3 x.py bookmarks [--max N] [--contains TEXT] [--urls]   # Needs the sign-in
    python3 x.py likes USERNAME [--max N]            # Needs the sign-in
    python3 x.py post "text" [--yes]                 # Needs the sign-in; without --yes: preview only
    python3 x.py auth [--manual]                     # One-time sign-in (OAuth 2.0 with PKCE)
    python3 x.py auth --code CODE_OR_URL             # Finish a manual sign-in
    python3 x.py logout                              # Revoke the sign-in, delete the stored tokens

Global option --json (before or after the subcommand): stdout carries exactly one
JSON document (errors too, as {"error": {...}}); human-readable text goes to stderr.

The bearer token and the OAuth client come from config.json in the config folder (env
vars override it), the sign-in from tokens.json next to it. The folder is
$X_SKILL_CONFIG_DIR if set, else $OPENCLAW_STATE_DIR/x (unless only ~/.openclaw/x
exists yet), else ~/.openclaw/x. Standard library only.
"""

import argparse
import base64
import functools
import hashlib
import html
import http.client
import http.server
import json
import os
import re
import secrets
import signal
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

# --- Paths ---

def _exists(path: Path) -> bool:
    try:
        return path.exists()
    except OSError:  # unreadable parent: treat as absent rather than fail at import
        return False


# 1.0 kept the bearer token and the OAuth client in two files of their own. They are still
# read, so existing setups keep working; config.json and the env vars take precedence.
LEGACY_NAMES = ("credentials", "oauth2")


def _has_settings(folder: Path) -> bool:
    """True when the folder holds config, a sign-in, or 1.0's settings, not when it is merely there."""
    return any(_exists(folder / f"{name}.json") for name in ("config", "tokens", *LEGACY_NAMES))


def _config_dir() -> Path:
    """Where config and the sign-in live; OpenClaw's backups and Docker setups keep its home folder."""
    custom = os.environ.get("X_SKILL_CONFIG_DIR")
    if custom:
        return Path(custom).expanduser()
    default = Path.home() / ".openclaw" / "x"
    state = os.environ.get("OPENCLAW_STATE_DIR")
    if state:
        moved = Path(state).expanduser() / "x"
        # 1.0 always used the default folder: keep using it until its files move
        if _has_settings(moved) or not _has_settings(default):
            return moved
    return default


CONFIG_DIR = _config_dir()
CONFIG_FILE = CONFIG_DIR / "config.json"
TOKEN_FILE = CONFIG_DIR / "tokens.json"
PENDING_AUTH_FILE = CONFIG_DIR / "pending-auth.json"
LEGACY_CONFIG_FILES = tuple(CONFIG_DIR / f"{name}.json" for name in LEGACY_NAMES)

API_HOST = "https://api.x.com"
API_BASE = f"{API_HOST}/2"
AUTHORIZE_URL = "https://x.com/i/oauth2/authorize"
TOKEN_URL = f"{API_BASE}/oauth2/token"
REVOKE_URL = f"{API_BASE}/oauth2/revoke"
# Must match the callback URI registered for the app in the X Developer Console exactly
REDIRECT_URI = "http://localhost:8080/callback"
CALLBACK_PORT = 8080
SCOPES = ("tweet.read", "users.read", "like.read", "bookmark.read", "tweet.write", "offline.access")
AUTH_TIMEOUT = 300  # seconds to wait for the browser to come back
HTTP_TIMEOUT = 30
NEEDS_CONFIRMATION_EXIT = 3  # post without --yes only previews, then exits with this
MAX_BATCH = 100  # tweets per lookup request

TWEET_ID_RE = re.compile(r"^\d{1,20}$")
# x.com/NAME/status/ID, twitter.com (also mobile.) and the /i/status and /i/web/status forms
TWEET_URL_RE = re.compile(r"(?:^|[/.])(?:x|twitter)\.com/(?:i/web|[^/?#]+)/status(?:es)?/(\d{1,20})")
PROFILE_URL_RE = re.compile(r"^(?:https?://)?(?:www\.|mobile\.)?(?:x|twitter)\.com/([^/?#]+)")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
TWEET_FIELDS = "created_at,public_metrics,author_id"


# --- Errors ---

class ApiError(Exception):
    """An error response from X, reduced to one line."""

    def __init__(self, status: int, message: str, reason: str = ""):
        super().__init__(message)
        self.status = status
        self.reason = reason

    @property
    def code(self) -> str:
        """X's error type (e.g. usage-capped, invalid_request), or the HTTP status."""
        return self.reason or f"http_{self.status}"

    def __str__(self):
        reason = f" {self.reason}" if self.reason else ""
        return f"X API error {self.status}{reason}: {self.args[0]}"


def _problem_reason(problem: dict) -> str:
    """The last part of an X problem type, e.g. resource-not-found or usage-capped."""
    kind = problem.get("type") or ""
    return kind.rstrip("/").rsplit("/", 1)[-1] if kind.startswith("http") else ""


def _api_error(e: urllib.error.HTTPError) -> ApiError:
    try:
        body = json.loads(e.read().decode() or "{}")
    except (ValueError, OSError, http.client.HTTPException):
        body = {}
    finally:
        e.close()
    if not isinstance(body, dict):
        body = {}
    if isinstance(body.get("error"), str):  # OAuth endpoints: {"error": "invalid_request", ...}
        return ApiError(e.code, body.get("error_description") or body["error"], body["error"])
    first = (body.get("errors") or [{}])[0]
    if not isinstance(first, dict):
        first = {}
    message = (body.get("detail") or first.get("message") or first.get("detail")
               or body.get("title") or str(e.reason))
    reason = _problem_reason(body) or _problem_reason(first)
    if e.code == 429:
        reason = reason or "rate_limited"
        reset = e.headers.get("x-rate-limit-reset") if e.headers else None
        if reset and reset.isdigit():
            message += f" (the limit resets at {datetime.fromtimestamp(int(reset)):%H:%M:%S})"
    return ApiError(e.code, message, reason)


# --- Output (text or --json) ---

JSON_MODE = False
_JSON_OUT = sys.stdout  # the real stdout; in JSON mode sys.stdout points at stderr
_RESULT = None


def emit(obj):
    """Record the command's JSON result (written once, at exit, in JSON mode)."""
    global _RESULT
    _RESULT = obj


def _write_json(obj):
    tty = _JSON_OUT.isatty()
    _JSON_OUT.write(json.dumps(obj, ensure_ascii=False, indent=2 if tty else None,
                               separators=None if tty else (",", ":")) + "\n")
    _JSON_OUT.flush()


def _flush_result():
    """Write the recorded result as the single JSON document (JSON mode only)."""
    global _RESULT
    if JSON_MODE and _RESULT is not None:
        _write_json(_RESULT)
        _RESULT = None


def _fail(message: str, code: str = "error", exit_code: int = 1):
    if JSON_MODE:
        _write_json({"error": {"message": message, "code": code}})
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(exit_code)


def tweet_url(tweet_id: str, username: Optional[str] = None) -> str:
    return f"https://x.com/{username or 'i'}/status/{tweet_id}"


def _tweet_json(tweet: dict, username: Optional[str] = None) -> dict:
    """The tweet as X returns it, plus its link (and the author's username when known)."""
    out = dict(tweet)
    if username:
        out["author_username"] = username
    out["url"] = tweet_url(tweet.get("id", ""), username)
    return out


def format_tweet(tweet: dict, username: Optional[str] = None):
    print(f"🐦 {tweet.get('text', '')}")
    created = tweet.get("created_at", "")
    if created:
        try:
            print(f"   📅 {datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%fZ'):%Y-%m-%d %H:%M:%S}")
        except ValueError:
            print(f"   📅 {created}")
    metrics = tweet.get("public_metrics") or {}
    if metrics:
        print(f"   ❤️  {metrics.get('like_count', 0)}  🔁 {metrics.get('retweet_count', 0)}  "
              f"💬 {metrics.get('reply_count', 0)}")
    print(f"   {tweet_url(tweet.get('id', ''), username)}")
    print()


def format_user(user: dict):
    print(f"👤 {user.get('name', '')} (@{user.get('username', '')})")
    if user.get("verified"):
        print("   ✓ Verified")
    print(f"   ID: {user.get('id', '')}")
    if user.get("description"):
        print(f"   Bio: {user['description']}")
    metrics = user.get("public_metrics") or {}
    if metrics:
        print(f"   👥 {metrics.get('followers_count', 0):,} followers · "
              f"{metrics.get('following_count', 0):,} following · {metrics.get('tweet_count', 0):,} tweets")
    print(f"   https://x.com/{user.get('username', '')}")
    print()


# --- Configuration (config.json + env var overrides) ---

def _read_settings(path: Path) -> dict:
    """One settings file as a dict; {} with a warning when it exists but can't be read."""
    if not _exists(path):
        return {}
    try:
        if os.name == "posix" and path.stat().st_mode & 0o077:
            print(f"Warning: {path} is readable by other users; "
                  "restrict it to your account (file mode 600).", file=sys.stderr)
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        return data
    except (ValueError, OSError) as e:
        print(f"Warning: Failed to read {path}: {e}", file=sys.stderr)
        return {}


@functools.lru_cache(maxsize=None)
def _load_config() -> dict:
    """Bearer token and OAuth client: env vars, else config.json, else the 1.0 files."""
    cfg = {}
    for path in (*LEGACY_CONFIG_FILES, CONFIG_FILE):  # later files win
        cfg.update((k, v) for k, v in _read_settings(path).items() if isinstance(v, str) and v)
    return {
        "bearer_token": os.environ.get("X_BEARER_TOKEN") or cfg.get("bearer_token", ""),
        "client_id": os.environ.get("X_CLIENT_ID") or cfg.get("client_id", ""),
        "client_secret": os.environ.get("X_CLIENT_SECRET") or cfg.get("client_secret", ""),
    }


def _require_oauth(cfg: dict) -> str:
    """The OAuth client ID, or exit with an error."""
    if not cfg["client_id"]:
        _fail("Missing the OAuth client ID. Set X_CLIENT_ID (and X_CLIENT_SECRET), or add "
              f"client_id and client_secret to {CONFIG_FILE}. See SETUP.md.", "missing_oauth_client")
    return cfg["client_id"]


# --- Sign-in tokens ---

def _write_private(path: Path, data: dict):
    """Write JSON only the owner can read (0600), replacing the file atomically."""
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.unlink(missing_ok=True)
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def save_tokens(tokens: dict):
    _write_private(TOKEN_FILE, tokens)


def load_tokens() -> dict:
    if not _exists(TOKEN_FILE):
        _fail("Not signed in to X. Run: x.py auth", "not_signed_in")
    try:
        tokens = json.loads(TOKEN_FILE.read_text())
        if not isinstance(tokens, dict):
            raise ValueError("expected a JSON object")
        if not tokens.get("access_token"):
            raise ValueError("the sign-in data is incomplete")
        loose = os.name == "posix" and TOKEN_FILE.stat().st_mode & 0o077
    except (ValueError, OSError) as e:
        _fail(f"Cannot read {TOKEN_FILE} ({e}). Run: x.py auth", "not_signed_in")
    if loose:  # 1.0 stored the sign-in readable by other users; keep it owner-only from now on
        save_tokens(tokens)
    return tokens


def _expired(tokens: dict) -> bool:
    """True when the sign-in is past, or within a minute of, the lifetime X gave it (2 hours)."""
    # issued_at is 1.0's field too, so both versions can share the stored sign-in: 1.0 renews
    # a sign-in without it on every request
    issued = tokens.get("issued_at")
    if not issued or not tokens.get("expires_in"):
        return False  # unknown: X answers 401 when it has run out, which renews it too
    return time.time() >= float(issued) + float(tokens["expires_in"]) - 60


def _token_request(url: str, fields: dict, cfg: dict) -> dict:
    """POST a form to X's OAuth token or revoke endpoint, authenticated as the app."""
    client_id = _require_oauth(cfg)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    if cfg["client_secret"]:  # confidential client (Web App, Automated App or Bot)
        basic = base64.b64encode(f"{client_id}:{cfg['client_secret']}".encode()).decode()
        headers["Authorization"] = f"Basic {basic}"
    else:  # public client (Native App): the client ID goes in the form instead
        fields = dict(fields, client_id=client_id)
    data = urllib.parse.urlencode(fields).encode()
    return _open_json(urllib.request.Request(url, data=data, headers=headers))


def refresh_sign_in(tokens: dict) -> dict:
    """Renew the sign-in with its refresh token; updates `tokens` in place and on disk."""
    if not tokens.get("refresh_token"):
        _fail("The sign-in expired and can't be renewed (no refresh token). Run: x.py auth",
              "not_signed_in")
    try:
        new = _token_request(TOKEN_URL, {"grant_type": "refresh_token",
                                         "refresh_token": tokens["refresh_token"]}, _load_config())
    except ApiError as e:
        if e.status in (400, 401):
            _fail(f"X rejected the stored sign-in ({e.args[0]}). Run: x.py auth", "not_signed_in")
        raise
    if not new.get("access_token"):
        _fail("X returned no new sign-in. Run: x.py auth", "not_signed_in")
    new["issued_at"] = int(time.time())
    for key in ("refresh_token", "user"):  # keep what X doesn't send again
        if key in tokens and key not in new:
            new[key] = tokens[key]
    tokens.clear()
    tokens.update(new)
    save_tokens(tokens)
    return tokens


# --- API helpers ---

def _open_json(req: urllib.request.Request) -> dict:
    """Send a request and decode the JSON reply; raises ApiError for HTTP errors."""
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise _api_error(e) from None
    except http.client.HTTPException as e:  # e.g. IncompleteRead: the connection dropped mid-reply
        raise urllib.error.URLError(f"incomplete reply from X ({type(e).__name__})") from None
    try:
        return json.loads(raw) if raw else {}
    except ValueError:  # e.g. a proxy or captive portal answering with HTML
        raise urllib.error.URLError("the reply from X wasn't JSON") from None


def api_request(method: str, path: str, params: Optional[dict] = None, body=None,
                user: bool = False) -> dict:
    """Call the X API v2 as the app (bearer token) or, with user=True, as the signed-in account.

    Without a bearer token, app requests go out with the sign-in instead."""
    url = API_BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    bearer = "" if user else _load_config()["bearer_token"]
    tokens = None
    if not bearer:
        if not user and not _exists(TOKEN_FILE):
            _fail("No X credentials. Set X_BEARER_TOKEN, add bearer_token to "
                  f"{CONFIG_FILE}, or sign in with x.py auth. See SETUP.md.", "missing_credentials")
        tokens = load_tokens()
        if _expired(tokens):
            print("Renewing the X sign-in...", file=sys.stderr)
            refresh_sign_in(tokens)
    headers = {}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    for attempt in (1, 2):
        headers["Authorization"] = f"Bearer {tokens['access_token'] if tokens else bearer}"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            return _open_json(req)
        except ApiError as e:
            if e.status != 401 or not tokens or attempt == 2:
                raise
            refresh_sign_in(tokens)  # X ended the sign-in early: renew it once and retry


def _data(reply: dict, not_found: str):
    """The reply's data, or exit with X's explanation (or `not_found`) when it has none."""
    if reply.get("data"):
        return reply["data"]
    problem = (reply.get("errors") or [{}])[0]
    if not isinstance(problem, dict):
        problem = {}
    _fail(problem.get("detail") or not_found, _problem_reason(problem) or "not_found")


def _usernames(reply: dict) -> dict:
    """author_id -> username from a reply's expanded users."""
    return {u.get("id"): u.get("username") for u in (reply.get("includes") or {}).get("users", [])}


def extract_tweet_id(url_or_id: str) -> str:
    """The numeric ID from a post URL (x.com or twitter.com) or a bare ID."""
    s = url_or_id.strip()
    if TWEET_ID_RE.match(s):
        return s
    m = TWEET_URL_RE.search(s)
    if not m:
        _fail(f"Not a post URL or ID: {url_or_id}", "invalid_tweet")
    return m.group(1)


def parse_username(value: str) -> str:
    """A username from NAME, @NAME or a profile URL."""
    name = value.strip()
    m = PROFILE_URL_RE.match(name)
    if m:
        name = m.group(1)
    name = name.lstrip("@")
    if not USERNAME_RE.match(name):
        _fail(f"Not an X username: {value}", "invalid_username")
    return name


def _lookup_user(username: str, fields: Optional[str] = None) -> dict:
    params = {"user.fields": fields} if fields else None
    return _data(api_request("GET", f"/users/by/username/{username}", params),
                 f"User @{username} not found.")


def _signed_in_account() -> dict:
    """{id, username, name} of the signed-in account, looked up once and kept with the sign-in."""
    account = load_tokens().get("user")
    if isinstance(account, dict) and account.get("id"):
        return account
    me = _data(api_request("GET", "/users/me", user=True), "Could not read the signed-in account.")
    account = {"id": me["id"], "username": me.get("username"), "name": me.get("name")}
    tokens = load_tokens()  # fresh copy: the request may have renewed the sign-in
    tokens["user"] = account
    save_tokens(tokens)
    return account


def _print_tweets(tweets: list, username: Optional[str] = None, empty: str = "No posts found."):
    for tweet in tweets:
        format_tweet(tweet, username)
    if not tweets:
        print(empty)


# --- Commands: reading ---

def cmd_user(args):
    username = parse_username(args.username)
    user = _lookup_user(username, "created_at,description,public_metrics,verified")
    emit(dict(user, url=f"https://x.com/{user.get('username', username)}"))
    format_user(user)


def cmd_timeline(args):
    username = parse_username(args.username)
    user = _lookup_user(username)
    params = {"max_results": args.max, "tweet.fields": "created_at,public_metrics,referenced_tweets"}
    if args.exclude:
        params["exclude"] = args.exclude
    tweets = api_request("GET", f"/users/{user['id']}/tweets", params).get("data") or []
    emit([_tweet_json(t, username) for t in tweets])
    _print_tweets(tweets, username)


def cmd_thread(args):
    tweet_id = extract_tweet_id(args.tweet)
    root = _data(api_request("GET", f"/tweets/{tweet_id}", {"tweet.fields": "author_id,conversation_id"}),
                 "Post not found (deleted, protected, or a wrong ID).")
    conversation = root.get("conversation_id", tweet_id)
    params = {
        "query": f"conversation_id:{conversation} from:{root['author_id']}",
        "max_results": 100,
        "tweet.fields": "created_at,public_metrics,referenced_tweets",
    }
    tweets = api_request("GET", "/tweets/search/recent", params).get("data") or []
    tweets.sort(key=lambda t: int(t.get("id", 0)))  # search answers newest first
    emit([_tweet_json(t) for t in tweets])
    if tweets:
        print(f"🧵 Thread (conversation_id: {conversation})\n")
    _print_tweets(tweets, empty="No thread found (or it is older than 7 days).")


def cmd_search(args):
    params = {"query": args.query, "max_results": args.max, "tweet.fields": TWEET_FIELDS}
    tweets = api_request("GET", "/tweets/search/recent", params).get("data") or []
    emit([_tweet_json(t) for t in tweets])
    _print_tweets(tweets, empty="No results found.")


def cmd_tweet(args):
    tweet_id = extract_tweet_id(args.tweet_id)
    reply = api_request("GET", f"/tweets/{tweet_id}",
                        {"tweet.fields": TWEET_FIELDS, "expansions": "author_id", "user.fields": "username"})
    tweet = _data(reply, "Post not found (deleted, protected, or a wrong ID).")
    username = _usernames(reply).get(tweet.get("author_id"))
    emit(_tweet_json(tweet, username))
    format_tweet(tweet, username)


def cmd_tweets(args):
    ids = list(dict.fromkeys(extract_tweet_id(t) for t in args.tweet_ids))
    if len(ids) > MAX_BATCH:
        _fail(f"At most {MAX_BATCH} posts per request ({len(ids)} given).", "usage", 2)
    reply = api_request("GET", "/tweets", {"ids": ",".join(ids), "tweet.fields": TWEET_FIELDS,
                                           "expansions": "author_id", "user.fields": "username"})
    found = {t["id"]: t for t in reply.get("data") or []}
    usernames = _usernames(reply)
    results = []
    for tweet_id in ids:
        tweet = found.get(tweet_id)
        if tweet:
            username = usernames.get(tweet.get("author_id"))
            results.append(_tweet_json(tweet, username))
            format_tweet(tweet, username)
        else:
            print(f"❌ {tweet_id}: not found (deleted, protected, or a wrong ID)", file=sys.stderr)
            results.append({"id": tweet_id, "found": False,
                            "error": {"message": "Post not found (deleted, protected, or a wrong ID)",
                                      "code": "not_found"}})
    emit(results)
    if len(found) < len(ids):
        _flush_result()
        sys.exit(1)


# --- Commands: the signed-in account ---

def cmd_likes(args):
    username = parse_username(args.username)
    user = _lookup_user(username)
    params = {"max_results": args.max, "tweet.fields": TWEET_FIELDS}
    tweets = api_request("GET", f"/users/{user['id']}/liked_tweets", params, user=True).get("data") or []
    emit([_tweet_json(t) for t in tweets])
    if tweets:
        print(f"❤️  Liked by @{username}\n")
    _print_tweets(tweets, empty="No liked posts found.")


HOME_MAX = 3200  # X serves at most the latest 3,200 posts (or 7 days) of the home timeline
PAGE_MAX = 100  # posts per page of a list endpoint


def _full_text(tweet: dict, included: dict, users: dict) -> str:
    """A post's untruncated text: a long post's note_tweet, and for a repost the original's full text."""
    for ref in tweet.get("referenced_tweets") or []:
        original = included.get(ref.get("id")) if isinstance(ref, dict) and ref.get("type") == "retweeted" else None
        if original:
            name = (users.get(original.get("author_id")) or {}).get("username")
            text = (original.get("note_tweet") or {}).get("text") or original.get("text", "")
            return f"RT @{name}: {text}" if name else text
    return (tweet.get("note_tweet") or {}).get("text") or tweet.get("text", "")


def cmd_home(args):
    account = _signed_in_account()
    params = {
        "max_results": min(args.max, PAGE_MAX),
        "tweet.fields": "created_at,public_metrics,author_id,note_tweet,referenced_tweets,conversation_id",
        # referenced_tweets.id: X truncates a repost's own text; the original carries it in full
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id",
        "user.fields": "username,name",
    }
    if args.exclude:
        params["exclude"] = args.exclude
    tweets, users, included = [], {}, {}
    while len(tweets) < args.max:
        reply = api_request("GET", f"/users/{account['id']}/timelines/reverse_chronological",
                            params, user=True)
        tweets += reply.get("data") or []
        users.update({u.get("id"): u for u in (reply.get("includes") or {}).get("users", [])})
        included.update({t.get("id"): t for t in (reply.get("includes") or {}).get("tweets", [])
                         if isinstance(t, dict)})
        token = (reply.get("meta") or {}).get("next_token")
        if not token or not reply.get("data"):
            break
        params = dict(params, pagination_token=token,
                      max_results=max(1, min(args.max - len(tweets), PAGE_MAX)))
    tweets = tweets[:args.max]

    results = []
    for tweet in tweets:
        author = users.get(tweet.get("author_id")) or {}
        post = _tweet_json(tweet, author.get("username"))
        if author.get("name"):
            post["author_name"] = author["name"]
        post["full_text"] = _full_text(tweet, included, users)
        results.append(post)
    emit(results)
    if tweets:
        print(f"🏠 Home timeline of @{account.get('username')}\n")
    for tweet in tweets:
        author = users.get(tweet.get("author_id")) or {}
        if author:
            print(f"👤 {author.get('name', '')} (@{author.get('username', '')})")
        format_tweet(dict(tweet, text=_full_text(tweet, included, users)), author.get("username"))
    if not tweets:
        print("No posts in the home timeline.")


def _bookmark_text(tweet: dict, included: dict) -> str:
    """Everything --contains looks at: the text, a long post's full text, and article titles and text."""
    parts = [tweet.get("text", ""), (tweet.get("note_tweet") or {}).get("text", "")]
    sources = [tweet] + [included.get(ref.get("id")) for ref in tweet.get("referenced_tweets") or []
                         if isinstance(ref, dict)]
    for source in filter(None, sources):  # quoted and replied-to posts often carry the article
        if source is not tweet:
            parts.append(source.get("text", ""))
        article = source.get("article")
        if isinstance(article, dict):
            parts += [article.get("title", ""), (article.get("plain_text") or "")[:12000]]
    return "\n".join(p for p in parts if p).lower()


def _links(tweet: dict) -> list:
    return [u.get("expanded_url") or u.get("url") for u in (tweet.get("entities") or {}).get("urls", [])]


def cmd_bookmarks(args):
    account = _signed_in_account()
    params = {
        "max_results": args.max,
        "tweet.fields": "created_at,public_metrics,entities,note_tweet,article,display_text_range,"
                        "context_annotations,card_uri,referenced_tweets,text",
        "expansions": "article.cover_media,article.media_entities,entities.note.mentions.username,"
                      "attachments.media_keys,referenced_tweets.id,referenced_tweets.id.author_id",
        "media.fields": "url,type,alt_text,height,width,duration_ms,preview_image_url,variants",
        "user.fields": "username,name,verified",
    }
    reply = api_request("GET", f"/users/{account['id']}/bookmarks", params, user=True)
    bookmarks = reply.get("data") or []
    if args.contains:
        included = {t.get("id"): t for t in (reply.get("includes") or {}).get("tweets", [])
                    if isinstance(t, dict)}
        needle = args.contains.lower()
        bookmarks = [t for t in bookmarks if needle in _bookmark_text(t, included)]

    if args.urls:
        links = [link for t in bookmarks for link in _links(t)]
        emit(links)
        for link in links:
            print(link)
        return
    emit([_tweet_json(t) for t in bookmarks])
    if bookmarks:
        print("🔖 Your bookmarks\n")
    for tweet in bookmarks:
        format_tweet(tweet)
        if _links(tweet):
            print("   🔗 Links:")
            for link in _links(tweet):
                print(f"      {link}")
            print()
    if not bookmarks:
        print(f"No bookmarks matched: {args.contains}" if args.contains else "No bookmarks found.")


def _needs_confirmation(what: str, preview: dict):
    """Stop after a preview: post only runs with --yes."""
    if JSON_MODE:
        _write_json(dict(preview, ok=False, needs_confirmation=True, dry_run=True))
    print(f"\nNothing was {what}. Show this to the user and, after a clear yes, "
          "run the same command with --yes.", file=sys.stderr)
    sys.exit(NEEDS_CONFIRMATION_EXIT)


def cmd_post(args):
    text = args.text
    if not text.strip():
        _fail("Nothing to post: the text is empty.", "usage", 2)
    # The account the post goes to, also for a 1.0 sign-in that never stored it; fails when not signed in
    account = _signed_in_account().get("username")
    if not account:
        _fail("X didn't name the signed-in account, so nothing can be posted. Run: x.py auth",
              "unknown_account")
    print(f"{'Posting' if args.yes else 'Would post'} as @{account} ({len(text)} characters):")
    for line in text.splitlines() or [""]:
        print(f"  │ {line}")
    if not args.yes:
        _needs_confirmation("posted", {"text": text, "characters": len(text), "account": account})

    posted = _data(api_request("POST", "/tweets", body={"text": text}, user=True),
                   "X did not confirm the post.")
    url = tweet_url(posted["id"], account)
    print(f"✅ Posted! {url}")
    emit({"ok": True, "posted": True, "id": posted["id"], "text": posted.get("text", text),
          "account": account, "url": url})


# --- Commands: signing in and out ---

def _pkce_pair() -> tuple:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def cmd_auth(args):
    cfg = _load_config()
    client_id = _require_oauth(cfg)

    if args.code:
        _finish_manual_auth(args.code, cfg)
        return

    # One sign-in attempt = one state + PKCE verifier, kept on disk so `auth --code` can finish it
    state = secrets.token_urlsafe(24)
    verifier, challenge = _pkce_pair()
    _write_private(PENDING_AUTH_FILE, {"state": state, "code_verifier": verifier,
                                       "redirect_uri": REDIRECT_URI})
    auth_url = AUTHORIZE_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })

    if args.manual:
        print("Open this URL in a browser and approve access:\n")
        print(f"{auth_url}\n")
        print(f"X then sends the browser to {REDIRECT_URI}?state=...&code=...")
        print("That page may not load, which is expected. Copy the full address from the address bar")
        print('and run: x.py auth --code "<address>"')
        emit({"ok": True, "auth_url": auth_url, "redirect_uri": REDIRECT_URI,
              "next": 'x.py auth --code "<address>"'})
        return

    # Short-lived localhost server that catches the browser coming back from X
    result = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        timeout = 10  # don't hang on browser preconnects that never send a request

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            code = qs.get("code", [None])[0]
            error = qs.get("error", [None])[0]
            if parsed.path != "/callback" or (not code and not error):
                self._reply(404, "Waiting for the X sign-in response.")
                return
            if qs.get("state", [None])[0] != state:
                self._reply(400, "This sign-in response belongs to a different attempt and was ignored.")
                return
            result["code"], result["error"] = code, error
            self._reply(200, "Signed in to X. You can close this tab." if code
                        else f"Sign-in failed: {html.escape(error)}")

        def _reply(self, status, text):
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<html><body><h2>{text}</h2></body></html>".encode())

        def log_message(self, *_):
            pass  # keep the terminal quiet

    try:
        server = http.server.HTTPServer(("127.0.0.1", CALLBACK_PORT), CallbackHandler)
    except OSError as e:
        _fail(f"Cannot listen on port {CALLBACK_PORT} for the sign-in callback ({e.strerror}). "
              "Free the port, or sign in with: x.py auth --manual")

    print("Opening the browser for the X sign-in...\n")
    print(f"If the browser doesn't open, visit:\n{auth_url}\n")
    print(f"Waiting up to {AUTH_TIMEOUT // 60} minutes for the callback on {REDIRECT_URI} ...", flush=True)
    webbrowser.open(auth_url)

    deadline = time.monotonic() + AUTH_TIMEOUT
    with server:
        while not result and time.monotonic() < deadline:
            server.timeout = max(1.0, deadline - time.monotonic())
            server.handle_request()

    if result.get("error"):
        _fail(f"X sign-in failed: {result['error']}", result["error"])
    if not result.get("code"):
        _fail('No callback received. Finish manually: x.py auth --code "<redirect address>"')
    _exchange_code(result["code"], cfg, verifier)


def _finish_manual_auth(code_or_url: str, cfg: dict):
    """Finish a sign-in with the code, or the whole redirect address, from the browser."""
    pending = _read_settings(PENDING_AUTH_FILE)
    if not pending.get("code_verifier"):
        _fail("No sign-in in progress. Run: x.py auth --manual, then pass the result to --code.")

    code = code_or_url.strip()
    if "code=" in code or "error=" in code:  # a pasted redirect address
        query = urllib.parse.urlparse(code).query or code.lstrip("?")
        qs = urllib.parse.parse_qs(query)
        if qs.get("error"):
            _fail(f"X sign-in failed: {qs['error'][0]}", qs["error"][0])
        if qs.get("state", [None])[0] != pending.get("state"):
            _fail("That address belongs to a different sign-in attempt. Run: x.py auth --manual")
        code = qs.get("code", [""])[0]
    _exchange_code(code, cfg, pending["code_verifier"])


def _exchange_code(code: str, cfg: dict, verifier: str):
    """Trade the authorization code for the sign-in and store it owner-only."""
    try:
        tokens = _token_request(TOKEN_URL, {"grant_type": "authorization_code", "code": code,
                                            "redirect_uri": REDIRECT_URI, "code_verifier": verifier}, cfg)
    except ApiError as e:
        _fail(f"Signing in failed: {e}", e.code)
    if not tokens.get("access_token"):
        _fail("X returned no sign-in. Run: x.py auth", "not_signed_in")
    tokens["issued_at"] = int(time.time())
    save_tokens(tokens)
    PENDING_AUTH_FILE.unlink(missing_ok=True)

    account = None
    try:
        account = _signed_in_account()
    except (ApiError, urllib.error.URLError, socket.timeout) as e:  # signed in all the same
        print(f"Warning: couldn't read the signed-in account yet ({e}).", file=sys.stderr)
    username = (account or {}).get("username")
    print(f"✅ Signed in to X{f' as @{username}' if username else ''}. Tokens saved to {TOKEN_FILE}")
    if not tokens.get("refresh_token"):
        print("⚠️  X sent no refresh token, so the sign-in ends after 2 hours. "
              "Check that the app may ask for offline.access.")
    emit({"ok": True, "token_file": str(TOKEN_FILE), "account": username,
          "scopes": (tokens.get("scope") or "").split(),
          "has_refresh_token": bool(tokens.get("refresh_token"))})


def cmd_logout(_args):
    """Revoke the sign-in at X, then delete the stored tokens."""
    if not _exists(TOKEN_FILE):
        print("Not signed in; nothing to do.")
        emit({"ok": True, "revoked": False, "tokens_deleted": False, "was_signed_in": False})
        return
    tokens = load_tokens()
    cfg = _load_config()
    revoked = False
    for kind in ("refresh_token", "access_token"):
        if not tokens.get(kind):
            continue
        try:
            _token_request(REVOKE_URL, {"token": tokens[kind], "token_type_hint": kind}, cfg)
            revoked = True
        except ApiError as e:
            if e.status not in (400, 401):  # 400/401: the sign-in was already invalid
                _fail(f"Could not revoke the sign-in ({e}); {TOKEN_FILE} was kept. Try again, or "
                      "revoke the app under Connected apps in X's settings.", e.code)
    print("✅ Revoked the sign-in at X." if revoked else "The stored sign-in was already invalid at X.")
    TOKEN_FILE.unlink(missing_ok=True)
    PENDING_AUTH_FILE.unlink(missing_ok=True)
    print(f"✅ Deleted {TOKEN_FILE}")
    emit({"ok": True, "revoked": revoked, "tokens_deleted": True, "was_signed_in": True})


# --- CLI ---

def _int_between(low: int, high: int):
    def parse(value: str) -> int:
        n = int(value)
        if not low <= n <= high:
            raise argparse.ArgumentTypeError(f"must be between {low} and {high}")
        return n
    return parse


def _exclude_list(value: str) -> str:
    kinds = [k.strip() for k in value.split(",") if k.strip()]
    if not kinds or any(k not in ("retweets", "replies") for k in kinds):
        raise argparse.ArgumentTypeError("use retweets, replies, or retweets,replies")
    return ",".join(dict.fromkeys(kinds))


def main():
    # Quiet broken pipe behavior when piping to `head` etc.
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    # Always write UTF-8, even under an ASCII or legacy locale (minimal containers, some
    # consoles), and keep stdout and stderr in order when both go to one pipe (as agents read them)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace", line_buffering=True)
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")

    json_opt = argparse.ArgumentParser(add_help=False)
    json_opt.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                          help="print exactly one JSON document to stdout (text goes to stderr)")
    parser = argparse.ArgumentParser(
        description="X (Twitter) API v2 client, Python standard library only",
        parents=[json_opt],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  x.py user XDevelopers
  x.py timeline XDevelopers --max 20 --exclude retweets,replies
  x.py search "from:XDevelopers -is:retweet" --max 10
  x.py thread https://x.com/XDevelopers/status/1234567890
  x.py auth                     (one-time sign-in for bookmarks, likes and posting)
  x.py bookmarks --max 50
  x.py home --max 20 --exclude replies
  x.py post "Hello from OpenClaw!"   (preview; add --yes to post)
""")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers = []

    def add(name, **kw):
        p = sub.add_parser(name, parents=[json_opt], **kw)
        subparsers.append(p)
        return p

    p = add("user", help="profile: bio, counts, verification")
    p.add_argument("username", help="username, @username or profile URL")

    p = add("timeline", help="a user's recent posts")
    p.add_argument("username", help="username, @username or profile URL")
    p.add_argument("--max", type=_int_between(5, 100), default=25, metavar="N",
                   help="number of posts, 5-100 (default: 25)")
    p.add_argument("--exclude", type=_exclude_list, metavar="KINDS",
                   help="leave out retweets, replies, or both (retweets,replies)")

    p = add("thread", help="the author's own posts in a conversation (last 7 days)")
    p.add_argument("tweet", help="post URL or ID")

    p = add("search", help="search posts from the last 7 days")
    p.add_argument("query", help="search query (X API v2 operators work)")
    p.add_argument("--max", type=_int_between(10, 100), default=10, metavar="N",
                   help="number of posts, 10-100 (default: 10)")

    p = add("tweet", help="one post by URL or ID")
    p.add_argument("tweet_id", help="post URL or ID")

    p = add("tweets", help=f"several posts in one request (up to {MAX_BATCH})")
    p.add_argument("tweet_ids", nargs="+", metavar="ID", help="post URLs or IDs")

    p = add("home", help="the signed-in account's home timeline, newest first (needs the sign-in)")
    p.add_argument("--max", type=_int_between(1, HOME_MAX), default=25, metavar="N",
                   help=f"number of posts, 1-{HOME_MAX} (default: 25; more than 100 pages through)")
    p.add_argument("--exclude", type=_exclude_list, metavar="KINDS",
                   help="leave out retweets, replies, or both (retweets,replies)")

    p = add("bookmarks", help="the signed-in account's bookmarks")
    p.add_argument("--max", type=_int_between(1, 100), default=25, metavar="N",
                   help="number of bookmarks, 1-100 (default: 25)")
    p.add_argument("--contains", metavar="TEXT",
                   help="only bookmarks whose text or article contains TEXT (case-insensitive)")
    p.add_argument("--urls", action="store_true", help="list only the links in the bookmarks")

    p = add("likes", help="posts an account liked (needs the sign-in)")
    p.add_argument("username", help="username, @username or profile URL")
    p.add_argument("--max", type=_int_between(1, 100), default=25, metavar="N",
                   help="number of posts, 1-100 (default: 25)")

    p = add("post", help="publish a post as the signed-in account (preview without --yes)")
    p.add_argument("text", help="the text of the post")
    p.add_argument("--yes", action="store_true",
                   help="really post it (without it, only shows what would be posted)")

    p = add("auth", help="sign in with X (OAuth 2.0 with PKCE, opens the browser)")
    p.add_argument("--manual", action="store_true",
                   help="print the sign-in URL and exit instead of waiting for the browser")
    p.add_argument("--code", metavar="CODE_OR_URL",
                   help="finish a manual sign-in: the redirect address (or just its code)")

    add("logout", help="revoke the sign-in at X and delete the stored tokens")

    global JSON_MODE, _JSON_OUT
    _JSON_OUT = sys.stdout
    words = sys.argv[1:]
    argv = words[:words.index("--") if "--" in words else None]
    if any(len(a) >= 3 and "--json".startswith(a) for a in argv):  # argparse also accepts --j, --js, --jso
        JSON_MODE = True  # set early so argparse usage errors are reported as JSON too
        sys.stdout = sys.stderr
        for p in (parser, *subparsers):  # a bad value for a subcommand option errors in its subparser
            p.error = lambda msg: _fail(msg, "usage", 2)
    args = parser.parse_args(words)
    JSON_MODE = getattr(args, "json", False) or JSON_MODE
    if JSON_MODE and sys.stdout is _JSON_OUT:
        sys.stdout = sys.stderr
    if not args.command:
        if JSON_MODE:
            _fail("No command given.", "usage", 2)
        parser.print_help()
        return

    cmds = {
        "user": cmd_user, "timeline": cmd_timeline, "thread": cmd_thread, "search": cmd_search,
        "tweet": cmd_tweet, "tweets": cmd_tweets, "bookmarks": cmd_bookmarks, "home": cmd_home, "likes": cmd_likes,
        "post": cmd_post, "auth": cmd_auth, "logout": cmd_logout,
    }
    try:
        cmds[args.command](args)
        _flush_result()
    except ApiError as e:
        _fail(str(e), e.code)
    except (urllib.error.URLError, socket.timeout) as e:
        _fail(f"Network error: {getattr(e, 'reason', e)}", "network_error")
    except OSError as e:  # e.g. a config folder that can't be written; dropped connections have no filename
        if e.filename:
            _fail(f"Cannot use {e.filename}: {e.strerror or e}. Check the config folder "
                  "or set X_SKILL_CONFIG_DIR.", "filesystem_error")
        _fail(f"Network error: {e}", "network_error")
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
