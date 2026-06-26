#!/usr/bin/env python3
"""
Interactive setup wizard for YouTube Comment Moderator skill.
Walks creator through: channel ID, API key, OAuth, preferences.
"""

import json
import os
import sys
import re
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.parse import urlencode, parse_qs, urlparse
from urllib.error import HTTPError

CONFIG_PATH = "skills/youtube-comment-moderator/config.json"
OAUTH_PATH = "skills/youtube-comment-moderator/oauth.json"

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

# OAuth credentials from environment (each user creates their own)
# See references/oauth-setup.md for instructions
CLIENT_ID = os.environ.get("YT_MOD_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("YT_MOD_CLIENT_SECRET", "")

YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl"  # read + write comments
]

OAUTH_REDIRECT_PORT = 8976


def extract_channel_id(url_or_id):
    """Extract channel ID from a YouTube URL or return as-is if already an ID."""
    if url_or_id.startswith("UC") and len(url_or_id) == 24:
        return url_or_id
    
    # Try to extract from URL patterns
    patterns = [
        r"youtube\.com/channel/(UC[\w-]{22})",
        r"youtube\.com/@([\w.-]+)",
        r"youtube\.com/c/([\w.-]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            result = match.group(1)
            if result.startswith("UC"):
                return result
            # Handle @username - need API lookup
            return resolve_handle(result, url_or_id)
    
    return url_or_id


def resolve_handle(handle, original_input):
    """Resolve a YouTube handle/username to channel ID via API."""
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print(f"  Can't resolve @{handle} without YOUTUBE_API_KEY. Please provide channel ID directly.")
        return original_input
    
    # Try handle resolution
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&forHandle={handle}&key={api_key}"
    req = Request(url, headers={"User-Agent": "YT-Moderator/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        if data.get("items"):
            channel_id = data["items"][0]["id"]
            channel_name = data["items"][0]["snippet"]["title"]
            print(f"  Found: {channel_name} ({channel_id})")
            return channel_id
    except Exception as e:
        print(f"  Error resolving handle: {e}")
    
    return original_input


def get_channel_info(channel_id, api_key):
    """Get channel name and stats."""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={api_key}"
    req = Request(url, headers={"User-Agent": "YT-Moderator/1.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        if data.get("items"):
            item = data["items"][0]
            return {
                "name": item["snippet"]["title"],
                "subscribers": int(item["statistics"].get("subscriberCount", 0)),
                "videos": int(item["statistics"].get("videoCount", 0))
            }
    except Exception:
        pass
    return None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Tiny HTTP handler that captures the OAuth callback code."""
    auth_code = None
    error = None

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            OAuthCallbackHandler.auth_code = query["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"""<html><body style="font-family:system-ui;text-align:center;padding:60px">
                <h1>&#9989; Authorization successful!</h1>
                <p>You can close this tab and return to the terminal.</p>
                </body></html>""")
        else:
            OAuthCallbackHandler.error = query.get("error", ["unknown"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Authorization failed: {OAuthCallbackHandler.error}</h1></body></html>".encode())

    def log_message(self, format, *args):
        pass  # silence request logs


def find_free_port():
    """Find an available port for the OAuth callback server."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def is_headless():
    """Detect if we're running without a display (VPS, SSH, container)."""
    if os.environ.get("SSH_CLIENT") or os.environ.get("SSH_TTY"):
        return True
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        return True
    if os.environ.get("OPENCLAW_HEADLESS"):
        return True
    return False


def extract_code_from_url(url_or_code):
    """Extract the auth code from a full callback URL or bare code string."""
    url_or_code = url_or_code.strip()
    if "code=" in url_or_code:
        parsed = parse_qs(urlparse(url_or_code).query)
        if "code" in parsed:
            return parsed["code"][0]
    return url_or_code


def do_oauth():
    """Walk user through OAuth flow. Auto-detects headless vs desktop."""
    print("\n=== YouTube Authorization ===")
    print("This lets the moderator reply to and delete comments on your behalf.")
    print("You can skip this for read-only mode (classification + reports only).\n")
    
    skip = input("Skip OAuth for now? (y/n, default: n): ").strip().lower()
    if skip == "y":
        return None

    if not CLIENT_ID or not CLIENT_SECRET:
        print("  ❌ OAuth credentials not found in environment.")
        print("  Set YT_MOD_CLIENT_ID and YT_MOD_CLIENT_SECRET in your .env file.")
        print("  See references/oauth-setup.md for step-by-step instructions.")
        print("  Skipping OAuth for now.\n")
        return None
    
    headless = is_headless()
    port = OAUTH_REDIRECT_PORT
    redirect_uri = f"http://127.0.0.1:{port}/callback"
    
    # Build auth URL
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(YOUTUBE_SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    
    if headless:
        # Headless mode: user opens URL on their own machine, pastes redirect URL back
        print("  Headless environment detected (no local browser).\n")
        print("  1. Open this URL in a browser on your computer:\n")
        print(f"     {auth_url}\n")
        print("  2. Sign in and click 'Allow'")
        print("  3. Your browser will redirect to a localhost URL that won't load.")
        print("     That's expected! Copy the ENTIRE URL from your browser's address bar.")
        print("     It looks like: http://127.0.0.1:.../callback?code=4/0A...\n")
        
        pasted = input("  Paste the full URL here: ").strip()
        if not pasted:
            print("  No input provided, skipping OAuth")
            return None
        
        code = extract_code_from_url(pasted)
        if not code:
            print("  Couldn't extract auth code from input, skipping OAuth")
            return None
        
        print("  Got it! Exchanging for tokens...")
    else:
        # Desktop mode: spin up localhost server, open browser automatically
        server = HTTPServer(("127.0.0.1", port), OAuthCallbackHandler)
        OAuthCallbackHandler.auth_code = None
        OAuthCallbackHandler.error = None
        
        print(f"\nOpening browser for authorization...\n")
        try:
            webbrowser.open(auth_url)
            print("  If the browser didn't open, visit this URL manually:\n")
        except Exception:
            print("  Couldn't open browser. Visit this URL:\n")
        print(f"  {auth_url}\n")
        print("  Waiting for authorization (5 min timeout)...")
        
        # Wait for the callback
        server.timeout = 300
        while OAuthCallbackHandler.auth_code is None and OAuthCallbackHandler.error is None:
            server.handle_request()
        
        server.server_close()
        
        if OAuthCallbackHandler.error:
            print(f"\n  OAuth error: {OAuthCallbackHandler.error}")
            return None
        
        code = OAuthCallbackHandler.auth_code
        if not code:
            print("  No authorization code received, skipping OAuth")
            return None
        
        print("  Authorization code received! Exchanging for tokens...")
    
    # Exchange code for tokens
    token_data = urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }).encode()
    
    req = Request(GOOGLE_TOKEN_URL, data=token_data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    
    try:
        with urlopen(req, timeout=15) as resp:
            tokens = json.loads(resp.read())
        
        if "error" in tokens:
            print(f"OAuth error: {tokens.get('error_description', tokens['error'])}")
            return None
        
        oauth = {
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in", 3600),
            "scope": tokens.get("scope", "")
        }
        
        # Save tokens
        os.makedirs(os.path.dirname(OAUTH_PATH), exist_ok=True)
        with open(OAUTH_PATH, "w") as f:
            json.dump(oauth, f, indent=2)
        
        print(f"\n  OAuth successful! Tokens saved to {OAUTH_PATH}")
        return oauth
        
    except HTTPError as e:
        body = e.read().decode()
        print(f"Token exchange failed: {body[:200]}")
        return None


def generate_auth_url():
    """Generate OAuth URL for non-interactive use (agent-driven setup).
    Prints the URL and instructions. User opens URL, pastes redirect URL back.
    Then call: setup.py --exchange-code <CODE_OR_URL>
    """
    if not CLIENT_ID:
        print("Error: YT_MOD_CLIENT_ID not set in environment", file=sys.stderr)
        sys.exit(1)

    redirect_uri = f"http://127.0.0.1:{OAUTH_REDIRECT_PORT}/callback"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(YOUTUBE_SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    print(auth_url)
    return auth_url


def exchange_code(code_or_url):
    """Exchange an auth code (or full callback URL) for tokens. Non-interactive."""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: YT_MOD_CLIENT_ID and YT_MOD_CLIENT_SECRET required", file=sys.stderr)
        sys.exit(1)

    code = extract_code_from_url(code_or_url)
    redirect_uri = f"http://127.0.0.1:{OAUTH_REDIRECT_PORT}/callback"

    token_data = urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }).encode()

    req = Request(GOOGLE_TOKEN_URL, data=token_data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })

    try:
        with urlopen(req, timeout=15) as resp:
            tokens = json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode()
        print(f"Token exchange failed: {body[:300]}", file=sys.stderr)
        sys.exit(1)

    if "error" in tokens:
        print(f"OAuth error: {tokens.get('error_description', tokens['error'])}", file=sys.stderr)
        sys.exit(1)

    oauth = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expires_in": tokens.get("expires_in", 3600),
        "scope": tokens.get("scope", "")
    }

    os.makedirs(os.path.dirname(OAUTH_PATH), exist_ok=True)
    with open(OAUTH_PATH, "w") as f:
        json.dump(oauth, f, indent=2)

    print(f"OAuth tokens saved to {OAUTH_PATH}")
    return oauth


def create_config(channel_id, channel_name, mode="approval", voice_style="friendly, casual, helpful", faq=None):
    """Create config.json non-interactively."""
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    config = {
        "channel_id": channel_id,
        "channel_name": channel_name,
        "mode": mode,
        "auto_delete_spam": mode in ("auto", "approval"),
        "auto_reply_questions": mode == "auto",
        "auto_reply_praise": False,
        "voice_style": voice_style,
        "faq": faq or [],
        "blocked_patterns": [
            "check out my channel", "dm me for",
            "I made $", "work from home", "crypto", "forex"
        ]
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(json.dumps(config, indent=2))
    return config


def main():
    print("=" * 50)
    print("  YouTube Comment Moderator - Setup Wizard")
    print("=" * 50)
    
    # Load existing config if any
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        print(f"\nExisting config found for: {config.get('channel_name', 'unknown')}")
        reconfigure = input("Reconfigure? (y/n, default: n): ").strip().lower()
        if reconfigure != "y":
            print("Keeping existing config.")
            return
    
    # Step 1: API Key
    print("\n=== Step 1: YouTube API Key ===")
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    if api_key:
        print(f"  ✅ Found YOUTUBE_API_KEY in environment ({api_key[:8]}...)")
    else:
        print("  ❌ YOUTUBE_API_KEY not found in environment.")
        print("  Add it to your .env file. See references/oauth-setup.md for instructions.")
        sys.exit(1)
    
    # Step 2: Channel
    print("\n=== Step 2: Your YouTube Channel ===")
    channel_input = input("  Channel URL or ID (e.g. https://youtube.com/@YourChannel): ").strip()
    channel_id = extract_channel_id(channel_input)
    
    info = get_channel_info(channel_id, api_key)
    if info:
        print(f"\n  Channel: {info['name']}")
        print(f"  Subscribers: {info['subscribers']:,}")
        print(f"  Videos: {info['videos']}")
    else:
        print(f"  Warning: couldn't verify channel {channel_id}")
    
    channel_name = info["name"] if info else input("  Channel name: ").strip()
    
    # Step 3: Mode
    print("\n=== Step 3: Moderation Mode ===")
    print("  1. Monitor only — classify + daily report (no API write access needed)")
    print("  2. Approval — drafts replies, you approve before posting")
    print("  3. Full auto — auto-replies to questions, auto-deletes spam")
    mode_choice = input("  Choose mode (1/2/3, default: 2): ").strip() or "2"
    mode_map = {"1": "monitor", "2": "approval", "3": "auto"}
    mode = mode_map.get(mode_choice, "approval")
    
    # Step 4: Voice/style
    print("\n=== Step 4: Your Voice ===")
    print("  How do you typically reply to comments? (e.g. 'casual and friendly',")
    print("  'professional but warm', 'short and direct')")
    voice = input("  Your style: ").strip() or "friendly, casual, appreciative"
    
    # Step 5: FAQ
    print("\n=== Step 5: FAQ (optional) ===")
    print("  Add common questions and your preferred answers.")
    print("  Press Enter with empty question to finish.")
    faq = []
    while True:
        q = input("  Q: ").strip()
        if not q:
            break
        a = input("  A: ").strip()
        if a:
            faq.append({"q": q, "a": a})
    
    # Step 6: OAuth (if not monitor-only)
    oauth = None
    if mode != "monitor":
        oauth = do_oauth()
        if not oauth and mode == "auto":
            print("\n  No OAuth — falling back to approval mode")
            mode = "approval"
    
    # Build config
    config = {
        "channel_id": channel_id,
        "channel_name": channel_name,
        "youtube_api_key": api_key,
        "mode": mode,
        "check_interval_minutes": 30,
        "max_videos_per_check": 5,
        "max_comments_per_video": 100,
        "auto_delete_spam": mode in ("auto", "approval"),
        "auto_reply_questions": mode == "auto",
        "auto_reply_praise": False,
        "voice_style": voice,
        "faq": faq,
        "blocked_patterns": [
            "check out my channel",
            "dm me for",
            "I made $",
            "work from home",
            "crypto",
            "forex"
        ],
        "has_oauth": oauth is not None
    }
    
    # Save
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n{'=' * 50}")
    print(f"  Setup complete!")
    print(f"{'=' * 50}")
    print(f"\n  Channel: {channel_name} ({channel_id})")
    print(f"  Mode: {mode}")
    print(f"  OAuth: {'yes' if oauth else 'no (read-only)'}")
    print(f"  FAQ entries: {len(faq)}")
    print(f"  Config saved: {CONFIG_PATH}")
    
    if mode != "monitor" and not oauth:
        print(f"\n  ⚠️  Run setup again to add OAuth when ready for write access")
    
    print(f"\n  Test it:")
    print(f"  python3 skills/youtube-comment-moderator/scripts/fetch_comments.py --channel-id {channel_id} --max-videos 1")
    print(f"  python3 skills/youtube-comment-moderator/scripts/classify_comments.py")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Moderator Setup")
    parser.add_argument("--auth-url", action="store_true",
                        help="Print OAuth URL (non-interactive)")
    parser.add_argument("--exchange-code", metavar="CODE_OR_URL",
                        help="Exchange auth code for tokens (non-interactive)")
    parser.add_argument("--create-config", action="store_true",
                        help="Create config non-interactively")
    parser.add_argument("--channel-id", help="Channel ID for --create-config")
    parser.add_argument("--channel-name", help="Channel name for --create-config")
    parser.add_argument("--mode", default="approval",
                        choices=["monitor", "approval", "auto"])
    parser.add_argument("--voice", default="friendly, casual, helpful")
    args = parser.parse_args()

    if args.auth_url:
        generate_auth_url()
    elif args.exchange_code:
        exchange_code(args.exchange_code)
    elif args.create_config:
        if not args.channel_id:
            print("Error: --channel-id required", file=sys.stderr)
            sys.exit(1)
        create_config(args.channel_id, args.channel_name or args.channel_id,
                      args.mode, args.voice)
    else:
        main()
