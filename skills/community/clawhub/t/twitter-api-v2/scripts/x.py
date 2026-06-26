#!/usr/bin/env python3
"""X (Twitter) API CLI — Direct API v2 calls (stdlib only, no dependencies).

Usage:
    python3 x.py user <username>                              # Get user info
    python3 x.py timeline <username> [--max N] [--exclude ...]
    python3 x.py thread <tweet_url_or_id>
    python3 x.py search "query" [--max N]
    python3 x.py tweet <tweet_id>
    python3 x.py tweets <id1> <id2> ...                       # Batch lookup
    python3 x.py likes <username> [--max N]                   # User's liked tweets
    python3 x.py bookmarks [--max N] [--contains "..."]      # Requires OAuth
    python3 x.py post "text"                                  # Requires OAuth
    python3 x.py auth                                         # OAuth 2.0 setup
"""

import argparse
import http.server
import json
import os
import re
import sys
import urllib.request
import urllib.parse
import webbrowser
from datetime import datetime

CONFIG_DIR = os.path.expanduser("~/.openclaw/x")
CREDS_FILE = os.path.join(CONFIG_DIR, "credentials.json")
OAUTH2_FILE = os.path.join(CONFIG_DIR, "oauth2.json")
TOKENS_FILE = os.path.join(CONFIG_DIR, "tokens.json")
API_BASE = "https://api.x.com/2"

REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = ["tweet.read", "users.read", "bookmark.read", "tweet.write", "offline.access"]


def load_creds():
    """Load API credentials from file."""
    if not os.path.exists(CREDS_FILE):
        print(f"Error: Credentials file not found: {CREDS_FILE}", file=sys.stderr)
        print("Create it with your bearer_token. See SETUP.md", file=sys.stderr)
        sys.exit(1)
    with open(CREDS_FILE) as f:
        return json.load(f)


def load_oauth2_creds():
    """Load OAuth 2.0 client credentials."""
    if os.path.exists(OAUTH2_FILE):
        with open(OAUTH2_FILE) as f:
            return json.load(f)
    # Try legacy credentials.json format
    creds = load_creds()
    if "client_id" in creds:
        return creds
    print("Error: OAuth 2.0 client credentials not found.", file=sys.stderr)
    print("Add client_id and client_secret to oauth2.json. See SETUP.md", file=sys.stderr)
    sys.exit(1)


def save_tokens(tokens):
    """Save OAuth user tokens."""
    import time
    
    # Add issued_at timestamp if not present
    if "issued_at" not in tokens:
        tokens["issued_at"] = time.time()
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)


def load_tokens():
    """Load OAuth user tokens."""
    if not os.path.exists(TOKENS_FILE):
        print("Error: Not authenticated. Run: python3 x.py auth", file=sys.stderr)
        sys.exit(1)
    with open(TOKENS_FILE) as f:
        return json.load(f)


def refresh_access_token():
    """Refresh OAuth access token using refresh_token."""
    import time
    import base64
    
    tokens = load_tokens()
    refresh_token = tokens.get("refresh_token")
    
    if not refresh_token:
        print("Error: No refresh token available. Re-authenticate with: python3 x.py auth", file=sys.stderr)
        sys.exit(1)
    
    oauth = load_oauth2_creds()
    client_id = oauth["client_id"]
    client_secret = oauth.get("client_secret")
    
    # Token refresh request with Basic auth
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    # Create Basic auth header
    credentials = f"{client_id}:{client_secret}".encode()
    basic_auth = base64.b64encode(credentials).decode()
    
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        "https://api.x.com/2/oauth2/token",
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic_auth}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            new_tokens = json.loads(resp.read())
            new_tokens["issued_at"] = time.time()
            save_tokens(new_tokens)
            return new_tokens
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"Token refresh failed: {e.code} {err_body}", file=sys.stderr)
        print("Re-authenticate with: python3 x.py auth", file=sys.stderr)
        sys.exit(1)


def api_request(method, endpoint, params=None, body=None, use_user_token=False):
    """Make authenticated API request to X API v2."""
    import time
    
    creds = load_creds()
    
    if use_user_token:
        tokens = load_tokens()
        
        # Check if token is expired and refresh if needed
        issued_at = tokens.get("issued_at", 0)
        expires_in = tokens.get("expires_in", 7200)
        expires_at = issued_at + expires_in
        
        if time.time() >= expires_at - 60:  # Refresh 60s before expiry
            print("🔄 Access token expired, refreshing...", file=sys.stderr)
            tokens = refresh_access_token()
        
        token = tokens.get("access_token")
    else:
        token = creds.get("bearer_token")
    
    if not token:
        print("Error: No authentication token available.", file=sys.stderr)
        sys.exit(1)
    
    if params:
        url = f"{API_BASE}{endpoint}?{urllib.parse.urlencode(params, doseq=True)}"
    else:
        url = f"{API_BASE}{endpoint}"
    
    headers = {"Authorization": f"Bearer {token}"}
    data = None
    
    if body:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                return {}
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode() if hasattr(e, "read") else ""
        print(f"API Error {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)


def extract_tweet_id(url_or_id):
    """Extract tweet ID from URL or return as-is."""
    m = re.search(r"(?:x\.com|twitter\.com)/[^/]+/status/(\d+)", url_or_id)
    if m:
        return m.group(1)
    if re.match(r"^\d+$", url_or_id):
        return url_or_id
    return url_or_id


def format_tweet(tweet, username=None):
    """Format a tweet for display."""
    text = tweet.get("text", "")
    created = tweet.get("created_at", "")
    tid = tweet.get("id", "")
    metrics = tweet.get("public_metrics", {})
    
    print(f"🐦 {text}")
    if created:
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            print(f"   📅 {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            print(f"   📅 {created}")
    
    if metrics:
        likes = metrics.get("like_count", 0)
        rts = metrics.get("retweet_count", 0)
        replies = metrics.get("reply_count", 0)
        print(f"   ❤️  {likes}  🔁 {rts}  💬 {replies}")
    
    if username:
        print(f"   https://x.com/{username}/status/{tid}")
    else:
        print(f"   https://x.com/i/status/{tid}")
    print()


def format_user(user):
    """Format user info for display."""
    username = user.get("username", "")
    name = user.get("name", "")
    uid = user.get("id", "")
    desc = user.get("description", "")
    metrics = user.get("public_metrics", {})
    verified = user.get("verified", False)
    
    print(f"👤 {name} (@{username})")
    if verified:
        print("   ✓ Verified")
    print(f"   ID: {uid}")
    if desc:
        print(f"   Bio: {desc}")
    if metrics:
        followers = metrics.get("followers_count", 0)
        following = metrics.get("following_count", 0)
        tweets = metrics.get("tweet_count", 0)
        print(f"   👥 {followers:,} followers · {following:,} following · {tweets:,} tweets")
    print(f"   https://x.com/{username}")
    print()


# --- Commands ---

def cmd_auth(_args):
    """Perform OAuth 2.0 PKCE authentication flow."""
    oauth = load_oauth2_creds()
    client_id = oauth["client_id"]
    client_secret = oauth.get("client_secret")
    
    # Generate PKCE challenge
    import hashlib
    import base64
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("=")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    
    # Build authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": "state",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"https://twitter.com/i/oauth2/authorize?{urllib.parse.urlencode(auth_params)}"
    
    # Start local callback server
    auth_code = [None]
    
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/callback"):
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                auth_code[0] = qs.get("code", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Authenticated! You can close this tab.</h1>")
        
        def log_message(self, *a):
            pass
    
    server = http.server.HTTPServer(("127.0.0.1", 8080), Handler)
    server.timeout = 120
    
    print(f"Opening browser for authentication...\n{auth_url}\n")
    webbrowser.open(auth_url)
    print("Waiting for callback on localhost:8080...")
    server.handle_request()
    
    if not auth_code[0]:
        print("No auth code received.", file=sys.stderr)
        sys.exit(1)
    
    # Exchange code for tokens
    token_data = {
        "code": auth_code[0],
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }
    
    token_body = urllib.parse.urlencode(token_data).encode()
    
    # Prepare Basic Auth header with client_id:client_secret
    import base64
    credentials = f"{client_id}:{client_secret}".encode()
    auth_header = f"Basic {base64.b64encode(credentials).decode()}"
    
    token_req = urllib.request.Request(
        "https://api.twitter.com/2/oauth2/token",
        data=token_body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth_header,
        },
    )
    
    try:
        with urllib.request.urlopen(token_req) as resp:
            tokens = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if hasattr(e, "read") else ""
        print(f"Token exchange failed: HTTP {e.code}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Token exchange failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    save_tokens(tokens)
    print(f"✅ Authenticated! Tokens saved to {TOKENS_FILE}")


def cmd_user(args):
    """Get user info by username."""
    params = {
        "user.fields": "description,public_metrics,verified,created_at",
    }
    data = api_request("GET", f"/users/by/username/{args.username}", params)
    
    if "data" not in data:
        print(f"Error: User '{args.username}' not found.", file=sys.stderr)
        sys.exit(1)
    
    format_user(data["data"])


def cmd_timeline(args):
    """Get user's tweets by username."""
    # Look up user by username
    user_data = api_request("GET", f"/users/by/username/{args.username}")
    
    if "data" not in user_data:
        print(f"Error: User '{args.username}' not found.", file=sys.stderr)
        sys.exit(1)
    
    user_id = user_data["data"]["id"]
    
    # Get user's tweets
    params = {
        "max_results": min(args.max, 100),
        "tweet.fields": "created_at,public_metrics,referenced_tweets",
    }
    
    if args.exclude:
        params["exclude"] = args.exclude.split(",")
    
    data = api_request("GET", f"/users/{user_id}/tweets", params)
    
    if "data" not in data or not data["data"]:
        print("No tweets found.")
        return
    
    for tweet in data["data"]:
        format_tweet(tweet, args.username)


def cmd_thread(args):
    """Get conversation thread for a tweet."""
    tweet_id = extract_tweet_id(args.tweet)
    
    # Get root tweet
    params = {"tweet.fields": "author_id,conversation_id"}
    root = api_request("GET", f"/tweets/{tweet_id}", params)
    
    if "data" not in root:
        print("Error: Tweet not found.", file=sys.stderr)
        sys.exit(1)
    
    conv_id = root["data"].get("conversation_id", tweet_id)
    author_id = root["data"].get("author_id")
    
    # Search for thread
    search_params = {
        "query": f"conversation_id:{conv_id} from:{author_id}",
        "max_results": 100,
        "tweet.fields": "created_at,referenced_tweets",
    }
    
    results = api_request("GET", "/tweets/search/recent", search_params)
    
    if "data" not in results or not results["data"]:
        print("No thread found (or thread is older than 7 days).")
        return
    
    print(f"🧵 Thread (conversation_id: {conv_id})\n")
    for tweet in results["data"]:
        format_tweet(tweet)


def cmd_search(args):
    """Search tweets."""
    if args.max < 10 or args.max > 100:
        print("Error: --max must be between 10 and 100", file=sys.stderr)
        sys.exit(1)
    
    params = {
        "query": args.query,
        "max_results": args.max,
        "tweet.fields": "created_at,public_metrics,author_id",
    }
    
    results = api_request("GET", "/tweets/search/recent", params)
    
    if "data" not in results or not results["data"]:
        print("No results found.")
        return
    
    for tweet in results["data"]:
        format_tweet(tweet)


def cmd_tweet(args):
    """Get a single tweet by ID."""
    tweet_id = extract_tweet_id(args.tweet_id)
    
    params = {
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username",
    }
    
    data = api_request("GET", f"/tweets/{tweet_id}", params)
    
    if "data" not in data:
        print("Error: Tweet not found.", file=sys.stderr)
        sys.exit(1)
    
    tweet = data["data"]
    username = None
    
    if "includes" in data and "users" in data["includes"]:
        username = data["includes"]["users"][0]["username"]
    
    format_tweet(tweet, username)


def cmd_tweets(args):
    """Get multiple tweets by ID (batch lookup)."""
    ids = [extract_tweet_id(tid) for tid in args.tweet_ids]
    
    params = {
        "ids": ",".join(ids),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username",
    }
    
    data = api_request("GET", "/tweets", params)
    
    if "data" not in data or not data["data"]:
        print("No tweets found.")
        return
    
    # Build username map
    usernames = {}
    if "includes" in data and "users" in data["includes"]:
        for user in data["includes"]["users"]:
            usernames[user["id"]] = user["username"]
    
    for tweet in data["data"]:
        username = usernames.get(tweet.get("author_id"))
        format_tweet(tweet, username)


def cmd_likes(args):
    """Get user's liked tweets (requires OAuth 2.0 if querying others)."""
    # Note: liked_tweets endpoint requires user context for any user
    # Must use OAuth 2.0 or OAuth 1.0a
    
    # Look up user
    user_data = api_request("GET", f"/users/by/username/{args.username}")
    
    if "data" not in user_data:
        print(f"Error: User '{args.username}' not found.", file=sys.stderr)
        sys.exit(1)
    
    user_id = user_data["data"]["id"]
    
    # Get liked tweets (requires user context)
    params = {
        "max_results": min(args.max, 100),
        "tweet.fields": "created_at,public_metrics",
    }
    
    try:
        data = api_request("GET", f"/users/{user_id}/liked_tweets", params, use_user_token=True)
    except SystemExit:
        print("\nNote: This endpoint requires OAuth 2.0 user context.", file=sys.stderr)
        print("Run: python3 x.py auth", file=sys.stderr)
        sys.exit(1)
    
    if "data" not in data or not data["data"]:
        print("No liked tweets found.")
        return
    
    print(f"❤️  Liked by @{args.username}\n")
    for tweet in data["data"]:
        format_tweet(tweet)


def cmd_bookmarks(args):
    """Get user's bookmarked tweets (requires OAuth 2.0)."""
    # Get current user ID
    me = api_request("GET", "/users/me", use_user_token=True)
    
    if "data" not in me:
        print("Error: Could not get user info.", file=sys.stderr)
        sys.exit(1)
    
    user_id = me["data"]["id"]
    
    # Get bookmarks
    params = {
        "max_results": min(args.max, 100),
        "tweet.fields": "created_at,public_metrics,entities,note_tweet,article,display_text_range,context_annotations,card_uri,referenced_tweets,text",
        "expansions": "article.cover_media,article.media_entities,entities.note.mentions.username,attachments.media_keys,referenced_tweets.id,referenced_tweets.id.author_id",
        "media.fields": "url,type,alt_text,height,width,duration_ms,preview_image_url,variants",
        "user.fields": "username,name,verified",
    }
    
    data = api_request("GET", f"/users/{user_id}/bookmarks", params, use_user_token=True)
    
    if "data" not in data or not data["data"]:
        print("No bookmarks found.")
        return

    bookmarks = data["data"]

    # Resolve article content from referenced tweets when bookmark itself has no article
    includes = data.get("includes", {}) if isinstance(data, dict) else {}
    included_tweets = {
        t.get("id"): t
        for t in includes.get("tweets", []) or []
        if isinstance(t, dict) and t.get("id")
    }

    # referenced articles are resolved lazily when needed

    # Optional filter by phrase in article title/plain_text or tweet text
    if getattr(args, 'contains', None):
        needle = args.contains.lower()
        filtered = []
        for tweet in bookmarks:
            parts = [tweet.get('text', '')]
            note_text = tweet.get('note_tweet', {}).get('text')
            if note_text:
                parts.append(note_text)

            # Direct article on bookmark
            article = tweet.get('article', {})
            if isinstance(article, dict):
                parts.append(article.get('title', ''))
                parts.append((article.get('plain_text', '') or '')[:12000])

            # Article in referenced tweet (common for quote/reply bookmarks)
            refs = tweet.get('referenced_tweets', []) or []
            for ref in refs:
                ref_id = ref.get('id') if isinstance(ref, dict) else None
                ref_tweet = included_tweets.get(ref_id)
                if not ref_tweet:
                    continue
                parts.append(ref_tweet.get('text', ''))
                ref_article = ref_tweet.get('article', {})
                if isinstance(ref_article, dict):
                    parts.append(ref_article.get('title', ''))
                    parts.append((ref_article.get('plain_text', '') or '')[:12000])

            haystack = "\n".join(parts).lower()
            if needle in haystack:
                filtered.append(tweet)

        bookmarks = filtered

        if not bookmarks:
            print(f"No bookmarks matched: {args.contains}")
            return

    # If JSON output requested, print raw data
    if args.json:
        print(json.dumps(bookmarks, indent=2))
        return

    # If URL extraction requested, print URLs only
    if args.urls:
        for tweet in bookmarks:
            entities = tweet.get("entities", {})
            urls = entities.get("urls", [])
            for url in urls:
                expanded = url.get("expanded_url", url.get("url"))
                print(expanded)
        return
    
    print("🔖 Your bookmarks\n")
    for tweet in bookmarks:
        format_tweet(tweet)
        # Show expanded URLs if present
        entities = tweet.get("entities", {})
        urls = entities.get("urls", [])
        if urls:
            print("   🔗 Links:")
            for url in urls:
                expanded = url.get("expanded_url", url.get("url"))
                print(f"      {expanded}")
            print()



def cmd_post(args):
    """Post a tweet (requires OAuth 2.0)."""
    body = {"text": args.text}
    
    data = api_request("POST", "/tweets", body=body, use_user_token=True)
    
    if "data" not in data:
        print("Error: Failed to post tweet.", file=sys.stderr)
        sys.exit(1)
    
    tweet_id = data["data"]["id"]
    print(f"✅ Posted! https://x.com/i/status/{tweet_id}")


def main():
    parser = argparse.ArgumentParser(
        description="X (Twitter) API v2 CLI — Pure Python, zero dependencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get user profile
  x.py user steipete

  # Get user's latest tweets
  x.py timeline steipete --max 50 --exclude retweets

  # Search recent tweets
  x.py search "OpenClaw" --max 20

  # Get conversation thread
  x.py thread https://x.com/steipete/status/123456

  # Authenticate for bookmarks/posting (one-time)
  x.py auth

  # Get your bookmarks
  x.py bookmarks --max 100

  # Post a tweet
  x.py post "Hello from OpenClaw!"
        """
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    sub.add_parser("auth", help="authenticate with OAuth 2.0 (one-time setup)")

    p_user = sub.add_parser("user", help="get user profile info")
    p_user.add_argument("username", help="username (without @)")

    p_timeline = sub.add_parser("timeline", help="get user's recent tweets")
    p_timeline.add_argument("username", help="username (without @)")
    p_timeline.add_argument("--max", type=int, default=25, metavar="N", help="max results (5-100, default: 25)")
    p_timeline.add_argument("--exclude", metavar="TYPE", help="exclude: retweets, replies, or both (comma-separated)")

    p_thread = sub.add_parser("thread", help="get conversation thread")
    p_thread.add_argument("tweet", help="tweet URL or ID")

    p_search = sub.add_parser("search", help="search recent tweets (last 7 days)")
    p_search.add_argument("query", help="search query")
    p_search.add_argument("--max", type=int, default=10, metavar="N", help="max results (10-100, default: 10)")

    p_tweet = sub.add_parser("tweet", help="get single tweet by ID")
    p_tweet.add_argument("tweet_id", help="tweet URL or ID")

    p_tweets = sub.add_parser("tweets", help="get multiple tweets (batch lookup)")
    p_tweets.add_argument("tweet_ids", nargs="+", metavar="ID", help="tweet URLs or IDs")

    p_likes = sub.add_parser("likes", help="get user's liked tweets (requires OAuth)")
    p_likes.add_argument("username", help="username (without @)")
    p_likes.add_argument("--max", type=int, default=25, metavar="N", help="max results (1-100, default: 25)")

    p_bookmarks = sub.add_parser("bookmarks", help="get your bookmarks (requires OAuth)")
    p_bookmarks.add_argument("--max", type=int, default=25, metavar="N", help="max results (1-100, default: 25)")
    p_bookmarks.add_argument("--json", action="store_true", help="output raw JSON")
    p_bookmarks.add_argument("--urls", action="store_true", help="extract URLs only")
    p_bookmarks.add_argument("--contains", help="filter bookmarks by text/article title contains this phrase")

    p_post = sub.add_parser("post", help="post a tweet (requires OAuth)")
    p_post.add_argument("text", help="tweet text (max 280 chars)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "auth": cmd_auth,
        "user": cmd_user,
        "timeline": cmd_timeline,
        "thread": cmd_thread,
        "search": cmd_search,
        "tweet": cmd_tweet,
        "tweets": cmd_tweets,
        "likes": cmd_likes,
        "bookmarks": cmd_bookmarks,
        "post": cmd_post,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
