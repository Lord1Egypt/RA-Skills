#!/usr/bin/env python3
"""YouTube search, video details and playlist management via the YouTube Data API v3.

Usage:
    python3 youtube.py search "query" [--max N] [--order relevance|date|...]
    python3 youtube.py video VIDEO_URL_OR_ID [...]  # Full description, duration, counts, chapters
    python3 youtube.py auth [--manual] [--port N]  # One-time Google sign-in
    python3 youtube.py auth --code CODE_OR_URL     # Finish a manual sign-in
    python3 youtube.py list                        # List your playlists
    python3 youtube.py create "Name" [--privacy private|unlisted|public] [--description TEXT]
    python3 youtube.py edit PLAYLIST_ID [--title T] [--description D] [--privacy P]
    python3 youtube.py add PLAYLIST_ID VIDEO_URL_OR_ID [...]
    python3 youtube.py videos PLAYLIST_ID
    python3 youtube.py remove ITEM_ID [...] [--yes]  # Without --yes: preview only
    python3 youtube.py delete PLAYLIST_ID [--yes]  # Without --yes: preview only
    python3 youtube.py logout                      # Revoke the sign-in, delete the tokens

Global option --json (before or after the subcommand): stdout carries exactly one
JSON document (errors too, as {"error": {...}}); human-readable text goes to stderr.

Credentials live in config.json in the config folder (env vars override it), OAuth
tokens in tokens.json next to it. The folder is $YOUTUBE_SKILL_CONFIG_DIR if set,
else $OPENCLAW_STATE_DIR/youtube (unless only ~/.openclaw/youtube exists yet), else
~/.openclaw/youtube. Standard library only.
"""

import argparse
import base64
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
from pathlib import Path
from typing import Optional

# --- Paths ---

def _exists(path: Path) -> bool:
    try:
        return path.exists()
    except OSError:  # unreadable parent: treat as absent rather than fail at import
        return False


def _has_settings(folder: Path) -> bool:
    """A config, a sign-in, or a sign-in in progress (auth --manual, then auth --code)."""
    return any(_exists(folder / name) for name in ("config.json", "tokens.json", "pending-auth.json"))


def _config_dir() -> Path:
    """Where config and tokens live; ~/.openclaw is kept by OpenClaw's backups and Docker setups."""
    custom = os.environ.get("YOUTUBE_SKILL_CONFIG_DIR")
    if custom:
        return Path(custom).expanduser()
    legacy = Path.home() / ".openclaw" / "youtube"
    state = os.environ.get("OPENCLAW_STATE_DIR")
    if state:
        moved = Path(state).expanduser() / "youtube"
        # Before 1.2.0 the folder was always ~/.openclaw/youtube: keep using it until its files
        # move. An empty folder at the new place (created ahead, say) doesn't count.
        if _has_settings(moved) or not _has_settings(legacy):
            return moved
    return legacy


CONFIG_DIR = _config_dir()
CONFIG_FILE = CONFIG_DIR / "config.json"
TOKEN_FILE = CONFIG_DIR / "tokens.json"
PENDING_AUTH_FILE = CONFIG_DIR / "pending-auth.json"

API_BASE = "https://www.googleapis.com/youtube/v3"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
SCOPES = "https://www.googleapis.com/auth/youtube"
AUTH_CALLBACK_PORT = 8923
AUTH_TIMEOUT = 300  # seconds to wait for the browser to come back
HTTP_TIMEOUT = 30
NEEDS_CONFIRMATION_EXIT = 3  # a delete or remove run without --yes only previews, then exits with this

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
# videos.list durations: PT1H2M3S, and P1DT2H3M4S once a video is a day or longer
DURATION_RE = re.compile(r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$")
# A chapter line in a description: "0:00 Intro", "1:02:03 - Outro", "(12:34) Demo"
CHAPTER_RE = re.compile(r"^\s*[(\[]?((?:\d{1,2}:)?\d{1,2}:\d{2})[)\]]?\s*[-–—:|]?\s+(\S.*?)\s*$")
# playlistItems.insert errors that concern one video; anything else stops `add`
VIDEO_ERRORS = {"videoNotFound", "invalidResourceId"}


# --- Errors ---

class ApiError(Exception):
    """An error response from a Google endpoint, reduced to one line."""

    def __init__(self, status: int, message: str, reason: str = ""):
        super().__init__(message)
        self.status = status
        self.reason = reason

    @property
    def code(self) -> str:
        """Google's reason (e.g. playlistNotFound, invalid_grant), or the HTTP status."""
        return self.reason or f"http_{self.status}"

    def __str__(self):
        reason = f" {self.reason}" if self.reason else ""
        return f"API error {self.status}{reason}: {self.args[0]}"


def _api_error(e: urllib.error.HTTPError) -> ApiError:
    try:
        body = json.loads(e.read().decode() or "{}")
    except (ValueError, OSError, http.client.HTTPException):
        body = {}
    finally:
        e.close()
    err = body.get("error", {}) if isinstance(body, dict) else {}
    if isinstance(err, str):  # OAuth endpoints: {"error": "invalid_grant", "error_description": ...}
        return ApiError(e.code, body.get("error_description") or err, err)
    if not isinstance(err, dict):
        err = {}
    first = (err.get("errors") or [{}])[0]
    reason = first.get("reason", "") if isinstance(first, dict) else ""
    return ApiError(e.code, err.get("message") or str(e.reason), reason)


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


def _abort(partial: dict, e: "ApiError"):
    """Stop a run part-way: the JSON lists what already happened, plus the error."""
    if JSON_MODE:
        _write_json(dict(partial, ok=False, error={"message": str(e), "code": e.code}))
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)


def _playlist_json(p: dict) -> dict:
    s = p.get("snippet", {})
    return {
        "id": p["id"], "title": s.get("title", ""), "description": s.get("description", ""),
        "privacy": p.get("status", {}).get("privacyStatus"),
        "item_count": p.get("contentDetails", {}).get("itemCount"),
        "channel": s.get("channelTitle"), "channel_id": s.get("channelId"),
        "published_at": s.get("publishedAt"),
        "url": f"https://youtube.com/playlist?list={p['id']}",
    }


# --- Configuration (config.json + env var overrides) ---

def _load_config() -> dict:
    """Load config from config.json with env var overrides."""
    cfg = {}
    if CONFIG_FILE.exists():
        try:
            if os.name == "posix" and CONFIG_FILE.stat().st_mode & 0o077:
                print(f"Warning: {CONFIG_FILE} is readable by other users; "
                      "restrict it to your account (file mode 600).", file=sys.stderr)
            cfg = json.loads(CONFIG_FILE.read_text())
            if not isinstance(cfg, dict):
                raise ValueError("expected a JSON object")
        except (ValueError, OSError) as e:
            print(f"Warning: Failed to read {CONFIG_FILE}: {e}", file=sys.stderr)
            cfg = {}

    # Env vars override config.json
    api_key = os.environ.get("YOUTUBE_API_KEY") or cfg.get("api_key", "")
    client_id = os.environ.get("YOUTUBE_CLIENT_ID") or cfg.get("client_id", "")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET") or cfg.get("client_secret", "")

    return {
        "api_key": api_key,
        "client_id": client_id,
        "client_secret": client_secret,
    }


def _require_oauth(cfg: dict) -> tuple:
    """Return (client_id, client_secret) or exit with error."""
    cid = cfg.get("client_id", "")
    csec = cfg.get("client_secret", "")
    if not cid or not csec:
        _fail("Missing client_id/client_secret for OAuth. Set YOUTUBE_CLIENT_ID + "
              f"YOUTUBE_CLIENT_SECRET env vars, or add them to {CONFIG_FILE}", "missing_oauth_client")
    return cid, csec


# --- Token Management ---

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
    if not TOKEN_FILE.exists():
        _fail("Not signed in to YouTube. Run: youtube.py auth", "not_signed_in")
    try:
        tokens = json.loads(TOKEN_FILE.read_text())
        if not isinstance(tokens, dict):
            raise ValueError("expected a JSON object")
        if not tokens.get("access_token"):
            raise ValueError("the sign-in data is incomplete")
        return tokens
    except (ValueError, OSError) as e:
        _fail(f"Cannot read {TOKEN_FILE} ({e}). Run: youtube.py auth", "not_signed_in")


def refresh_access_token(tokens: dict) -> dict:
    """Renew the expired sign-in; updates `tokens` in place and on disk."""
    if not tokens.get("refresh_token"):
        _fail("No refresh token stored. Run: youtube.py auth", "not_signed_in")
    client_id, client_secret = _require_oauth(_load_config())
    try:
        new = _post_form(TOKEN_URL, {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": tokens["refresh_token"],
            "grant_type": "refresh_token",
        })
    except ApiError as e:
        if e.reason != "invalid_grant":
            _fail(f"Token refresh failed: {e}", e.code)
        hint = ""
        if tokens.get("refresh_token_expires_in"):
            hint = ("\nGoogle gave this sign-in a limited lifetime, usually because the OAuth consent "
                    "screen is in Testing mode (7 days). Publish the app to stay signed in (see SETUP.md).")
        _fail("Google rejected the stored sign-in (expired or revoked). Run: youtube.py auth" + hint, e.code)
    if not new.get("access_token"):
        _fail("Google returned no new sign-in token. Run: youtube.py auth", "not_signed_in")
    tokens["access_token"] = new["access_token"]
    if new.get("refresh_token"):
        tokens["refresh_token"] = new["refresh_token"]
    save_tokens(tokens)
    return tokens


# --- API Helpers ---

def _open_json(req: urllib.request.Request) -> dict:
    """Send a request and decode the JSON reply; raises ApiError for HTTP errors."""
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise _api_error(e) from None
    except http.client.HTTPException as e:  # e.g. IncompleteRead: the connection dropped mid-reply
        raise urllib.error.URLError(f"incomplete reply from Google ({type(e).__name__})") from None
    try:
        return json.loads(raw) if raw else {}
    except ValueError:  # e.g. a proxy or captive portal answering with HTML
        raise urllib.error.URLError("the reply from Google wasn't JSON") from None


def _post_form(url: str, fields: dict) -> dict:
    data = urllib.parse.urlencode(fields).encode()
    return _open_json(urllib.request.Request(url, data=data))


def _api_url(endpoint: str, params: dict) -> str:
    return f"{API_BASE}/{endpoint}?{urllib.parse.urlencode(params)}"


def api_request(method: str, url: str, tokens: dict, body=None, retry=True) -> dict:
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    else:
        data = None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        return _open_json(req)
    except ApiError as e:
        if e.status == 401 and retry:
            refresh_access_token(tokens)
            return api_request(method, url, tokens, body, retry=False)
        raise


def _paged(endpoint: str, params: dict, tokens: dict):
    """Yield every item of a list endpoint, following nextPageToken."""
    params = dict(params, maxResults=50)
    while True:
        data = api_request("GET", _api_url(endpoint, params), tokens)
        yield from data.get("items", [])
        if not data.get("nextPageToken"):
            return
        params["pageToken"] = data["nextPageToken"]


def extract_video_id(url_or_id: str) -> Optional[str]:
    """Return the 11-character video ID from a video URL or bare ID, or None."""
    s = url_or_id.strip()
    if VIDEO_ID_RE.match(s):
        return s
    parsed = urllib.parse.urlparse(s if "://" in s else f"https://{s}")
    host = (parsed.hostname or "").lower()
    path = [p for p in parsed.path.split("/") if p]
    candidate = ""
    if host == "youtu.be" and path:
        candidate = path[0]
    elif any(host == d or host.endswith("." + d) for d in ("youtube.com", "youtube-nocookie.com")):
        candidate = urllib.parse.parse_qs(parsed.query).get("v", [""])[0]
        if not candidate and len(path) >= 2 and path[0] in ("shorts", "embed", "live", "v", "e"):
            candidate = path[1]
    return candidate if VIDEO_ID_RE.match(candidate) else None


# --- Commands ---

def _pkce_pair() -> tuple:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def cmd_auth(args):
    cfg = _load_config()
    client_id, client_secret = _require_oauth(cfg)

    if args.code:
        _finish_manual_auth(args.code, client_id, client_secret)
        return

    # One sign-in attempt = one state + PKCE verifier, kept on disk so `auth --code` can finish it
    redirect_uri = f"http://127.0.0.1:{args.port}"
    state = secrets.token_urlsafe(24)
    verifier, challenge = _pkce_pair()
    _write_private(PENDING_AUTH_FILE, {
        "state": state, "code_verifier": verifier, "redirect_uri": redirect_uri,
    })
    auth_url = AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })

    if args.manual:
        print("Open this URL in a browser and approve access:\n")
        print(f"{auth_url}\n")
        print(f"Google then sends the browser to {redirect_uri}/?state=...&code=...")
        print("That page may not load, which is expected. Copy the full address from the address bar")
        print('and run: youtube.py auth --code "<address>"')
        emit({"ok": True, "auth_url": auth_url, "redirect_uri": redirect_uri,
              "next": 'youtube.py auth --code "<address>"'})
        return

    # Ephemeral localhost server that captures the callback
    result = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        timeout = 10  # don't hang on browser preconnects that never send a request

        def do_GET(self):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code = qs.get("code", [None])[0]
            error = qs.get("error", [None])[0]
            if code and qs.get("state", [None])[0] != state:
                self._reply(400, "This sign-in response belongs to a different attempt and was ignored.")
                return
            if not code and not error:
                self._reply(404, "Waiting for the Google sign-in response.")
                return
            result["code"], result["error"] = code, error
            if code:
                self._reply(200, "Authenticated! You can close this tab.")
            else:
                self._reply(200, f"Sign-in failed: {error}")

        def _reply(self, status, text):
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<html><body><h2>{text}</h2></body></html>".encode())

        def log_message(self, *_):
            pass  # Suppress server logs

    try:
        server = http.server.HTTPServer(("127.0.0.1", args.port), CallbackHandler)
    except OSError as e:
        _fail(f"Cannot listen on 127.0.0.1:{args.port} ({e.strerror}). Use --port N or --manual.")

    print("Opening browser for Google consent...\n")
    print(f"If the browser doesn't open, visit:\n{auth_url}\n")
    print(f"Waiting up to {AUTH_TIMEOUT // 60} minutes for the callback on {redirect_uri} ...", flush=True)
    webbrowser.open(auth_url)

    deadline = time.monotonic() + AUTH_TIMEOUT
    with server:
        while not result and time.monotonic() < deadline:
            server.timeout = max(1.0, deadline - time.monotonic())
            server.handle_request()

    if result.get("error"):
        _fail(f"Google sign-in failed: {result['error']}", result["error"])
    if not result.get("code"):
        _fail('No callback received. Finish manually: youtube.py auth --code "<redirect address>"')
    _exchange_code(result["code"], client_id, client_secret, redirect_uri, verifier)


def _finish_manual_auth(code_or_url: str, client_id: str, client_secret: str):
    """Finish a sign-in with the code, or the whole redirect address, from the browser."""
    pending = {}
    if PENDING_AUTH_FILE.exists():
        try:
            pending = json.loads(PENDING_AUTH_FILE.read_text())
        except (ValueError, OSError):
            pass
    if not isinstance(pending, dict):
        pending = {}
    if not pending.get("redirect_uri"):
        _fail("No sign-in in progress. Run: youtube.py auth --manual, then pass the result to --code.")

    code = code_or_url.strip()
    if "code=" in code or "error=" in code:  # a pasted redirect address
        query = urllib.parse.urlparse(code).query or code.lstrip("?")
        qs = urllib.parse.parse_qs(query)
        if qs.get("error"):
            _fail(f"Google sign-in failed: {qs['error'][0]}", qs["error"][0])
        if qs.get("state", [None])[0] != pending.get("state"):
            _fail("That address belongs to a different sign-in attempt. Run: youtube.py auth --manual")
        code = qs.get("code", [""])[0]
    _exchange_code(code, client_id, client_secret, pending["redirect_uri"], pending.get("code_verifier"))


def _exchange_code(code: str, client_id: str, client_secret: str, redirect_uri: str,
                   verifier: Optional[str] = None):
    """Exchange authorization code for tokens."""
    fields = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    if verifier:
        fields["code_verifier"] = verifier
    try:
        tokens = _post_form(TOKEN_URL, fields)
    except ApiError as e:
        _fail(f"Token exchange failed: {e}", e.code)
    tokens["obtained_at"] = int(time.time())
    save_tokens(tokens)
    PENDING_AUTH_FILE.unlink(missing_ok=True)
    print(f"✅ Authenticated! Tokens saved to {TOKEN_FILE}")
    if not tokens.get("refresh_token"):
        print("⚠️  Google sent no refresh token; you'll need to run auth again within the hour.")
    elif tokens.get("refresh_token_expires_in"):
        days = round(tokens["refresh_token_expires_in"] / 86400)
        print(f"⚠️  Google limited this sign-in to {days} days, usually because the OAuth consent "
              "screen is in Testing mode. Publish the app to stay signed in (see SETUP.md).")
    emit({"ok": True, "token_file": str(TOKEN_FILE),
          "has_refresh_token": bool(tokens.get("refresh_token")),
          "refresh_token_expires_in": tokens.get("refresh_token_expires_in")})


def cmd_create(args):
    tokens = load_tokens()
    body = {
        "snippet": {
            "title": args.name,
            "description": args.description,
        },
        "status": {"privacyStatus": args.privacy},
    }
    result = api_request("POST", _api_url("playlists", {"part": "snippet,status"}), tokens, body)
    pid = result["id"]
    title = result["snippet"]["title"]
    print(f"✅ Created playlist: {title} ({result['status']['privacyStatus']})")
    print(f"   ID: {pid}")
    print(f"   URL: https://youtube.com/playlist?list={pid}")
    emit({"ok": True, "playlist": _playlist_json(result)})


def cmd_list(_args):
    tokens = load_tokens()
    params = {"part": "snippet,contentDetails,status", "mine": "true"}
    count, out = 0, []
    for count, p in enumerate(_paged("playlists", params, tokens), 1):
        out.append(_playlist_json(p))
        items = p["contentDetails"]["itemCount"]
        privacy = p.get("status", {}).get("privacyStatus", "?")
        print(f"  📋 {p['snippet']['title']} ({items} videos, {privacy})")
        print(f"     ID: {p['id']}")
        print(f"     https://youtube.com/playlist?list={p['id']}")
        print()
    if not count:
        print("No playlists yet.")
    emit(out)


def cmd_add(args):
    tokens = load_tokens()
    failed, results = 0, []
    for vid in (v.strip() for v in args.videos):  # main() pads bare IDs that start with -
        video_id = extract_video_id(vid)
        if not video_id:
            print(f"  ❌ Not a YouTube video URL or ID: {vid}", file=sys.stderr)
            results.append({"input": vid, "ok": False, "video_id": None,
                            "error": {"message": "Not a YouTube video URL or ID", "code": "invalid_video"}})
            failed += 1
            continue
        body = {
            "snippet": {
                "playlistId": args.playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        }
        try:
            result = api_request("POST", _api_url("playlistItems", {"part": "snippet"}), tokens, body)
        except ApiError as e:
            if e.reason not in VIDEO_ERRORS:
                _abort({"playlist_id": args.playlist_id, "results": results}, e)
            print(f"  ❌ {video_id}: {e}", file=sys.stderr)
            results.append({"input": vid, "ok": False, "video_id": video_id,
                            "error": {"message": e.args[0], "code": e.reason or str(e.status)}})
            failed += 1
            continue
        print(f"  ✅ Added: {result['snippet']['title']} ({video_id})")
        print(f"     Item ID: {result['id']}")
        results.append({"input": vid, "ok": True, "video_id": video_id, "item_id": result["id"],
                        "title": result["snippet"].get("title", ""),
                        "url": f"https://youtube.com/watch?v={video_id}"})
    emit({"ok": not failed, "playlist_id": args.playlist_id, "results": results})
    if failed:
        _flush_result()
        sys.exit(1)


def cmd_videos(args):
    tokens = load_tokens()
    params = {"part": "snippet", "playlistId": args.playlist_id}
    count, out = 0, []
    for count, item in enumerate(_paged("playlistItems", params, tokens), 1):
        s = item["snippet"]
        vid = s["resourceId"]["videoId"]
        channel = s.get("videoOwnerChannelTitle")
        out.append({"item_id": item["id"], "video_id": vid, "position": s.get("position"),
                    "title": s.get("title", ""), "description": s.get("description", ""),
                    "channel": channel, "channel_id": s.get("videoOwnerChannelId"),
                    "published_at": s.get("publishedAt"), "playlist_id": s.get("playlistId"),
                    "url": f"https://youtube.com/watch?v={vid}"})
        print(f"  {count}. {s['title']}" + (f"  ({channel})" if channel else ""))
        print(f"     https://youtube.com/watch?v={vid}")
        print(f"     Item ID: {item['id']} (for removal)")
        print()
    if not count:
        print("Playlist is empty.")
    emit(out)


def _needs_confirmation(what: str, preview=None):
    """Stop after a preview: destructive commands only run with --yes."""
    if JSON_MODE:
        _write_json(dict(preview or {}, ok=False, needs_confirmation=True, dry_run=True))
    print(f"\nNothing was {what}. Show this to the user and, after a clear yes, "
          "run the same command with --yes.", file=sys.stderr)
    sys.exit(NEEDS_CONFIRMATION_EXIT)


def _playlist_titles(playlist_ids: list, tokens: dict) -> dict:
    titles = {}
    for i in range(0, len(playlist_ids), 50):
        params = {"part": "snippet", "id": ",".join(playlist_ids[i:i + 50]), "maxResults": 50}
        for p in api_request("GET", _api_url("playlists", params), tokens).get("items", []):
            titles[p["id"]] = p["snippet"]["title"]
    return titles


def cmd_remove(args):
    tokens = load_tokens()

    # Show exactly what goes before anything is removed. Lookups by ID page too
    # (5 results by default), so ask for the whole batch of up to 50.
    found = {}
    for i in range(0, len(args.item_ids), 50):
        params = {"part": "snippet", "id": ",".join(args.item_ids[i:i + 50]), "maxResults": 50}
        for item in api_request("GET", _api_url("playlistItems", params), tokens).get("items", []):
            found[item["id"]] = item["snippet"]
    titles = _playlist_titles(sorted({s["playlistId"] for s in found.values()}), tokens)
    n = len(args.item_ids)
    entries_label = f"{n} playlist entr{'y' if n == 1 else 'ies'}"
    print(f"Removing {entries_label}:" if args.yes else f"Would remove {entries_label}:")
    for item_id in args.item_ids:
        s = found.get(item_id)
        if s:
            playlist = titles.get(s["playlistId"], s["playlistId"])
            print(f"  - \"{s['title']}\" from \"{playlist}\"  [{item_id}]")
        else:
            print(f"  - unknown entry (not found, or not visible yet)  [{item_id}]")
    entries = []
    for item_id in args.item_ids:
        s = found.get(item_id)
        entries.append({"item_id": item_id, "found": bool(s),
                        "video_id": s["resourceId"]["videoId"] if s else None,
                        "title": s["title"] if s else None,
                        "playlist_id": s["playlistId"] if s else None,
                        "playlist_title": titles.get(s["playlistId"]) if s else None})
    if not args.yes:
        _needs_confirmation("removed", {"items": entries})

    for entry in entries:
        try:
            api_request("DELETE", _api_url("playlistItems", {"id": entry["item_id"]}), tokens)
        except ApiError as e:
            _abort({"items": entries}, e)
        entry["removed"] = True
        print(f"  ✅ Removed item {entry['item_id']}")
    emit({"ok": True, "items": entries})


def cmd_delete(args):
    tokens = load_tokens()

    # Show exactly what goes before anything is deleted
    params = {"part": "snippet,contentDetails,status", "id": args.playlist_id}
    items = api_request("GET", _api_url("playlists", params), tokens).get("items", [])
    pj = _playlist_json(items[0]) if items else {"id": args.playlist_id, "found": False}
    if items:
        p = items[0]
        label = (f"\"{p['snippet']['title']}\" ({p['contentDetails']['itemCount']} videos, "
                 f"{p['status']['privacyStatus']})")
    else:
        label = "unknown playlist (not found, or not visible yet)"
    print(f"Deleting playlist {label}  [{args.playlist_id}]" if args.yes
          else f"Would delete playlist {label}  [{args.playlist_id}]")
    if not args.yes:
        _needs_confirmation("deleted", {"playlist": pj})

    api_request("DELETE", _api_url("playlists", {"id": args.playlist_id}), tokens)
    print(f"  ✅ Deleted playlist {args.playlist_id}")
    emit({"ok": True, "deleted": True, "playlist": pj})


def cmd_logout(_args):
    """Revoke the sign-in at Google, then delete the local tokens."""
    if not TOKEN_FILE.exists():
        print("Not signed in; nothing to do.")
        emit({"ok": True, "revoked": False, "tokens_deleted": False, "was_signed_in": False})
        return
    tokens = load_tokens()
    token = tokens.get("refresh_token") or tokens.get("access_token")
    revoked = False
    if token:
        try:
            _post_form(REVOKE_URL, {"token": token})
            print("✅ Revoked the sign-in at Google.")
            revoked = True
        except ApiError as e:
            if e.reason != "invalid_token":
                _fail(f"Could not revoke the sign-in ({e}); {TOKEN_FILE} was kept. Try again, or "
                      "remove the app at https://myaccount.google.com/permissions", e.code)
            print("The stored sign-in was already invalid at Google.")
    TOKEN_FILE.unlink(missing_ok=True)
    PENDING_AUTH_FILE.unlink(missing_ok=True)
    print(f"✅ Deleted {TOKEN_FILE}")
    emit({"ok": True, "revoked": revoked, "tokens_deleted": True, "was_signed_in": True})


def cmd_edit(args):
    if args.title is None and args.description is None and args.privacy is None:
        _fail("Nothing to change. Pass --title, --description and/or --privacy.", "usage", 2)
    tokens = load_tokens()

    # 1. Fetch current playlist details (title is required for updates).
    #    A playlist created moments ago takes a few seconds to become readable.
    url_get = _api_url("playlists", {"part": "snippet,status", "id": args.playlist_id})
    for attempt in range(4):
        if attempt:
            time.sleep(3)
        data = api_request("GET", url_get, tokens)
        if data.get("items"):
            break
    else:
        _fail(f"Playlist {args.playlist_id} not found.", "playlistNotFound")

    playlist = data["items"][0]
    snippet = playlist["snippet"]
    status = playlist["status"]

    # 2. Update fields locally
    if args.title is not None:
        snippet["title"] = args.title
    if args.description is not None:
        snippet["description"] = args.description
    if args.privacy is not None:
        status["privacyStatus"] = args.privacy

    # 3. An update replaces the whole part, so send back every writable field
    #    (omitted ones are cleared); thumbnails/channelId etc. are read-only
    body = {
        "id": args.playlist_id,
        "snippet": {
            "title": snippet["title"],
            "description": snippet.get("description", ""),
        },
        "status": {"privacyStatus": status["privacyStatus"]},
    }
    for key in ("tags", "defaultLanguage"):
        if snippet.get(key):
            body["snippet"][key] = snippet[key]
    if status.get("podcastStatus"):
        body["status"]["podcastStatus"] = status["podcastStatus"]

    # 4. Send Update
    result = api_request("PUT", _api_url("playlists", {"part": "snippet,status"}), tokens, body)

    print(f"✅ Updated playlist: {result['snippet']['title']}")
    print(f"   Privacy: {result['status']['privacyStatus']}")
    emit({"ok": True, "playlist": _playlist_json(result)})


def _duration_seconds(iso: str) -> Optional[int]:
    m = DURATION_RE.match(iso or "")
    if not m or not any(m.groups()):
        return None
    days, hours, minutes, seconds = (int(g or 0) for g in m.groups())
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def _format_duration(seconds: int) -> str:
    """H:MM:SS, or M:SS under an hour."""
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"


def _chapters(description: str, duration: Optional[int] = None) -> list:
    """Chapters as YouTube finds them: timestamped lines from 0:00 on, ascending, at least three,
    each at least 10 seconds long (the last one too, when the video's length is known)."""
    chapters = []
    for line in description.splitlines():
        m = CHAPTER_RE.match(line)
        if not m:
            continue
        start = 0
        for part in m.group(1).split(":"):
            start = start * 60 + int(part)
        if not chapters and start:
            continue  # the list starts at 0:00
        if chapters and start <= chapters[-1]["start_seconds"]:
            break  # a timestamp out of order ends the list
        chapters.append({"timestamp": m.group(1), "start_seconds": start, "title": m.group(2)})
    starts = [c["start_seconds"] for c in chapters] + ([duration] if duration else [])
    if len(chapters) < 3 or any(b - a < 10 for a, b in zip(starts, starts[1:])):
        return []  # YouTube shows no chapters for such a list
    return chapters


def _count(value) -> Optional[int]:
    """Statistics arrive as strings; hidden like counts and disabled comments are missing."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _video_json(item: dict) -> dict:
    s, stats = item.get("snippet", {}), item.get("statistics", {})
    description = s.get("description", "")  # videos.list sends plain text; only search escapes
    seconds = _duration_seconds(item.get("contentDetails", {}).get("duration", ""))
    duration = _format_duration(seconds) if seconds is not None else None
    if s.get("liveBroadcastContent") in ("live", "upcoming"):  # P0D until the stream is over
        duration, seconds = s["liveBroadcastContent"], None
    return {
        "video_id": item["id"], "title": s.get("title", ""), "description": description,
        "channel": s.get("channelTitle", ""), "channel_id": s.get("channelId"),
        "published_at": s.get("publishedAt"), "duration": duration, "duration_seconds": seconds,
        "view_count": _count(stats.get("viewCount")), "like_count": _count(stats.get("likeCount")),
        "comment_count": _count(stats.get("commentCount")),
        "url": f"https://youtube.com/watch?v={item['id']}", "chapters": _chapters(description, seconds),
    }


def cmd_video(args):
    video_ids = []
    for url_or_id in args.videos:
        video_id = extract_video_id(url_or_id)
        if not video_id:
            _fail(f"Not a YouTube video URL or ID: {url_or_id}", "invalid_video")
        if video_id not in video_ids:
            video_ids.append(video_id)

    # API key if configured, otherwise the OAuth sign-in (same quota either way)
    cfg = _load_config()
    if not cfg["api_key"] and not TOKEN_FILE.exists():
        _fail(code="missing_credentials", message="video needs an API key (YOUTUBE_API_KEY or api_key in "
              f"{CONFIG_FILE}) or a sign-in (youtube.py auth). See SETUP.md.")
    tokens = None if cfg["api_key"] else load_tokens()
    found = {}
    for i in range(0, len(video_ids), 50):  # videos.list takes up to 50 IDs per call
        params = {"part": "snippet,contentDetails,statistics", "id": ",".join(video_ids[i:i + 50])}
        if tokens:
            data = api_request("GET", _api_url("videos", params), tokens)
        else:
            data = _open_json(urllib.request.Request(_api_url("videos", dict(params, key=cfg["api_key"]))))
        found.update((item["id"], item) for item in data.get("items", []))

    results = [_video_json(found[v]) if v in found else
               {"video_id": v, "found": False,
                "error": {"message": "Video not found (deleted, private, or a wrong ID)", "code": "videoNotFound"}}
               for v in video_ids]
    emit(results)
    for r in results:
        if "error" in r:
            print(f"❌ {r['video_id']}: {r['error']['message']}", file=sys.stderr)
            continue
        print(f"📺 {r['title']}")
        print(f"   Channel: {r['channel']}")
        print(f"   Published: {(r['published_at'] or '')[:10]}")
        print(f"   Duration: {r['duration'] or 'unknown'}")
        if r["view_count"] is not None:
            print(f"   Views: {r['view_count']:,}")
        print(f"   URL: {r['url']}")
        if not JSON_MODE:  # the JSON carries the description; don't repeat it on stderr
            print(f"\nDescription:\n{r['description'] or '(none)'}\n")
            print("─" * 80)
            print()
    if len(found) < len(video_ids):
        _flush_result()
        sys.exit(1)


def cmd_search(args):
    params = {
        "part": "snippet",
        "q": args.query,
        "type": "video",
        "maxResults": args.max,
        "order": args.order,
    }

    if args.duration:
        params["videoDuration"] = args.duration

    if args.hd:
        params["videoDefinition"] = "high"

    if args.channel:
        params["channelId"] = args.channel

    if args.after:
        # Basic validation for RFC 3339 (YYYY-MM-DD or full timestamp)
        val = args.after.strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", val):
            val += "T00:00:00Z"
        # If it doesn't match YYYY-MM-DD, assume user provided valid RFC 3339 or let API error out
        params["publishedAfter"] = val

    # API key if configured, otherwise the OAuth sign-in (same quota either way)
    cfg = _load_config()
    if cfg["api_key"]:
        url = _api_url("search", dict(params, key=cfg["api_key"]))
        data = _open_json(urllib.request.Request(url))
    elif TOKEN_FILE.exists():
        data = api_request("GET", _api_url("search", params), load_tokens())
    else:
        _fail(code="missing_credentials", message="Search needs an API key (YOUTUBE_API_KEY or api_key in "
              f"{CONFIG_FILE}) or a sign-in (youtube.py auth). See SETUP.md.")

    items = data.get("items", [])
    for item in items:  # search returns titles HTML-escaped (Father&#39;s); descriptions arrive as plain text
        snippet = item.get("snippet", {})
        snippet["title"] = html.unescape(snippet.get("title", ""))
    emit([{"id": item["id"].get("videoId"), "video_id": item["id"].get("videoId"),
           "title": item["snippet"].get("title", ""),
           "description": item["snippet"].get("description", ""),
           "channel": item["snippet"].get("channelTitle", ""),
           "channel_id": item["snippet"].get("channelId"),
           "published_at": item["snippet"].get("publishedAt"),
           "url": f"https://youtube.com/watch?v={item['id'].get('videoId')}"} for item in items])
    for item in items:
        s = item["snippet"]
        vid = item["id"].get("videoId", "?")
        print(f"  📺 {s['title']}")
        print(f"     Channel: {s['channelTitle']}  |  {s['publishedAt'][:10]}")
        print(f"     https://youtube.com/watch?v={vid}")
        print()
    if not items:
        print("No results.")


# --- CLI ---

def _int_between(low: int, high: int):
    def parse(value: str) -> int:
        n = int(value)
        if not low <= n <= high:
            raise argparse.ArgumentTypeError(f"must be between {low} and {high}")
        return n
    return parse


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
                          help="Print exactly one JSON document to stdout (text goes to stderr)")
    parser = argparse.ArgumentParser(description="YouTube search and playlist manager",
                                     parents=[json_opt])
    sub = parser.add_subparsers(dest="command")
    subparsers = []
    _add_parser = sub.add_parser

    def add_parser(*a, **kw):
        p = _add_parser(*a, parents=[json_opt], **kw)
        subparsers.append(p)
        return p
    sub.add_parser = add_parser

    p_auth = sub.add_parser("auth", help="Sign in with Google (opens browser)")
    p_auth.add_argument("--code", help="Finish a manual sign-in: the code or the full redirect address")
    p_auth.add_argument("--manual", action="store_true",
                        help="Print the consent URL and exit instead of waiting for the browser")
    p_auth.add_argument("--port", type=_int_between(1, 65535), default=AUTH_CALLBACK_PORT,
                        help=f"Local callback port (default: {AUTH_CALLBACK_PORT})")

    p_create = sub.add_parser("create", help="Create a playlist")
    p_create.add_argument("name", help="Playlist name")
    p_create.add_argument("--privacy", default="private",
                          choices=["public", "unlisted", "private"])
    p_create.add_argument("--description", default="", help="Playlist description")

    sub.add_parser("list", help="List your playlists")

    p_add = sub.add_parser("add", help="Add videos to a playlist")
    p_add.add_argument("playlist_id")
    p_add.add_argument("videos", nargs="+", help="Video URLs or IDs")

    p_vids = sub.add_parser("videos", help="List videos in a playlist")
    p_vids.add_argument("playlist_id")

    p_rm = sub.add_parser("remove", help="Remove videos from a playlist")
    p_rm.add_argument("item_ids", nargs="+", metavar="item_id",
                      help="Playlist item ID(s), as shown by `videos`")
    p_rm.add_argument("--yes", action="store_true",
                      help="Really remove them (without it, only shows what would be removed)")

    p_del = sub.add_parser("delete", help="Delete an entire playlist")
    p_del.add_argument("playlist_id", help="Playlist ID to delete")
    p_del.add_argument("--yes", action="store_true",
                       help="Really delete it (without it, only shows what would be deleted)")

    sub.add_parser("logout", help="Revoke the Google sign-in and delete the stored tokens")

    p_edit = sub.add_parser("edit", help="Edit a playlist (title, description, privacy)")
    p_edit.add_argument("playlist_id")
    p_edit.add_argument("--title")
    p_edit.add_argument("--description")
    p_edit.add_argument("--privacy", choices=["public", "unlisted", "private"])

    p_search = sub.add_parser("search", help="Search YouTube")
    p_search.add_argument("query")
    p_search.add_argument("--max", type=_int_between(1, 50), default=5,
                          help="Max results, 1-50 (default: 5)")
    p_search.add_argument("--order", default="relevance",
                          choices=["relevance", "date", "rating", "title", "videoCount", "viewCount"],
                          help="Sort order (default: relevance)")
    p_search.add_argument("--duration", choices=["any", "long", "medium", "short"],
                          help="Video duration (short <4m, medium 4-20m, long >20m)")
    p_search.add_argument("--hd", action="store_true", help="High definition (HD) only")
    p_search.add_argument("--after", help="Published after (YYYY-MM-DD)")
    p_search.add_argument("--channel", help="Filter by Channel ID")

    p_video = sub.add_parser("video", help="Get full details of one or more videos")
    p_video.add_argument("videos", nargs="+", metavar="VIDEO_URL_OR_ID",
                         help="Video URLs or IDs (watch, youtu.be, Shorts, embed, live, or bare 11-char ID)")

    global JSON_MODE, _JSON_OUT
    _JSON_OUT = sys.stdout
    words = sys.argv[1:]
    command_at = next((i for i, a in enumerate(words) if not a.startswith("-")), len(words))
    if words[command_at:command_at + 1] in (["video"], ["add"]):
        # 1 in 64 video IDs starts with "-", which argparse would take for an option. A leading
        # space keeps such a bare ID positional; extract_video_id strips it again.
        words[command_at + 1:] = [" " + a if a.startswith("-") and VIDEO_ID_RE.match(a) else a
                                  for a in words[command_at + 1:]]
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
        "auth": cmd_auth, "create": cmd_create, "list": cmd_list,
        "add": cmd_add, "videos": cmd_videos, "remove": cmd_remove,
        "delete": cmd_delete, "edit": cmd_edit, "search": cmd_search,
        "video": cmd_video, "logout": cmd_logout,
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
                  "or set YOUTUBE_SKILL_CONFIG_DIR.", "filesystem_error")
        _fail(f"Network error: {e}", "network_error")
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
