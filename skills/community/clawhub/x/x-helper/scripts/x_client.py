"""
X Helper — X API v2 client. Pure stdlib, no dependencies.

Usage:
  python3 x_client.py auth authorize --client-id <ID> [--headless]
  python3 x_client.py auth status
  python3 x_client.py auth logout

  python3 x_client.py search posts <query> [--max N] [--archive]
  python3 x_client.py search users <query> [--max N]
  python3 x_client.py search news <query> [--max N]

  python3 x_client.py user get <username>
  python3 x_client.py user me
  python3 x_client.py user timeline <username> [--max N]
  python3 x_client.py user mentions <username> [--max N]
  python3 x_client.py user followers <username> [--max N]
  python3 x_client.py user following <username> [--max N]
  python3 x_client.py user liked <username> [--max N]

  python3 x_client.py tweet post <text> [--reply-to ID] [--media path]...
  python3 x_client.py tweet get <id>
  python3 x_client.py tweet delete <id>
  python3 x_client.py tweet like <id>
  python3 x_client.py tweet unlike <id>
  python3 x_client.py tweet retweet <id>
  python3 x_client.py tweet unretweet <id>
  python3 x_client.py tweet likers <id> [--max N]
  python3 x_client.py tweet retweeters <id> [--max N]
  python3 x_client.py tweet quote-tweets <id> [--max N]

  python3 x_client.py thread post --text1 <text> --text2 <text> [--text3 <text> ...] [--media path]...

  python3 x_client.py trends [--woeid N]
  python3 x_client.py trends list

  python3 x_client.py bookmark list [--max N]
  python3 x_client.py bookmark add <tweet-id>
  python3 x_client.py bookmark remove <tweet-id>

  python3 x_client.py article draft --title <title> --text <text>
  python3 x_client.py article publish <article-id>

  python3 x_client.py follow <username>
  python3 x_client.py unfollow <username>

  python3 x_client.py dm list [--max N]
  python3 x_client.py dm conversation <id> [--max N]
  python3 x_client.py dm send <username> <text> --confirm
  python3 x_client.py dm delete <event-id> --confirm

  python3 x_client.py list create <name> [--description <desc>]
  python3 x_client.py list get <id>
  python3 x_client.py list delete <id>
  python3 x_client.py list members <id> [--max N]
  python3 x_client.py list posts <id> [--max N]
  python3 x_client.py list followers <id> [--max N]
  python3 x_client.py list add-member <list-id> <username>
  python3 x_client.py list remove-member <list-id> <username>
  python3 x_client.py list follow <list-id>
  python3 x_client.py list unfollow <list-id>
  python3 x_client.py list my [--max N]

  python3 x_client.py block <username>
  python3 x_client.py unblock <username>
  python3 x_client.py blocked [--max N]

  python3 x_client.py mute <username>
  python3 x_client.py unmute <username>
  python3 x_client.py muted [--max N]
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import URLError


API_BASE = "https://api.x.com/2"
MAX_RETRY_WAIT = 120


# ── Auth ──────────────────────────────────────────────────────────────────

def _get_token():
    """Get the access token.

    The token comes ONLY from the user-set X_BEARER_TOKEN env var. The user
    manages this credential themselves (e.g. `export X_BEARER_TOKEN=...`);
    this skill never requests, stores, or refreshes tokens on the user's behalf.
    """
    token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not token:
        print("Authentication error: set the X_BEARER_TOKEN environment variable "
              "(user-provided). Run 'auth authorize' to obtain one, then export it.",
              file=sys.stderr)
        return None
    return token


def _require_confirm(args, action):
    """Abort unless the caller passed --confirm. Destructive/irreversible ops only."""
    if "--confirm" not in args:
        print(f"⚠️  {action} 是不可撤销的操作。请加上 --confirm 确认。", file=sys.stderr)
        sys.exit(1)


# ── API request with retry ────────────────────────────────────────────────

def _api_req(method, path, params=None, body=None, token=None):
    if token is None:
        token = _get_token()
        if not token:
            return {"error": True, "detail": "Not authenticated. Run 'auth authorize' first."}

    url = f"{API_BASE}{path}"
    if params:
        qs = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}?{qs}"

    headers = {"Authorization": f"Bearer {token}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
        method = method.upper()

    for attempt in range(3):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else {}
        except URLError as e:
            code = getattr(e, "code", 0)
            body_text = ""
            try:
                body_text = e.read().decode(errors="replace")
            except Exception:
                body_text = str(e)

            if code == 429:
                retry_after = MAX_RETRY_WAIT
                if hasattr(e, "headers"):
                    ra = e.headers.get("Retry-After")
                    if ra and ra.isdigit():
                        retry_after = min(int(ra), MAX_RETRY_WAIT)
                wait = min(retry_after * (attempt + 1), MAX_RETRY_WAIT)
                print(f"  Rate limited. Retrying in {wait}s... (attempt {attempt + 1}/3)",
                      file=sys.stderr)
                time.sleep(wait)
                continue

            try:
                err_data = json.loads(body_text)
            except (json.JSONDecodeError, TypeError):
                err_data = {"detail": body_text[:500]}
            err_data["http_code"] = code
            err_data["error"] = True
            if code == 401:
                err_data["detail"] = "Token expired. Re-authorize with 'auth authorize'."
            return err_data
        except Exception as e:
            return {"error": True, "detail": str(e)}

    return {"error": True, "detail": "Rate limited after 3 retries. Try again later."}


def _paginated_req(path, params, token, max_items=20):
    """Yield items from a paginated endpoint."""
    params = dict(params)
    params["max_results"] = min(params.get("max_results", 10), 100)
    gathered = 0
    while True:
        data = _api_req("GET", path, params=params, token=token)
        if data.get("error"):
            yield data
            return
        items = data.get("data", [])
        for item in items:
            yield item
            gathered += 1
            if max_items and gathered >= max_items:
                return
        meta = data.get("meta", {})
        next_token = meta.get("next_token")
        if not next_token:
            return
        params["pagination_token"] = next_token


def _fetch_all(path, params, token, max_results=20):
    """Fetch all items up to max_results with pagination."""
    items = []
    for item in _paginated_req(path, params, token, max_items=max_results):
        if isinstance(item, dict) and item.get("error"):
            print(f"Error: {item.get('detail', 'Unknown error')}", file=sys.stderr)
            sys.exit(1)
        items.append(item)
    return items


# ── Helpers ───────────────────────────────────────────────────────────────

def _resolve_user_id(username, token=None):
    data = _api_req("GET", f"/users/by/username/{username}", token=token)
    if data.get("error") or not data.get("data"):
        return None
    return data["data"]["id"]


def _format_time(iso_str):
    if not iso_str:
        return ""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str[:19]


def _fmt_tweet(t):
    text = (t.get("text", "") or "")[:280].replace("\n", " ")
    return (f"  [{t.get('id', '')}] @{t.get('author_username', '')} "
            f"· {_format_time(t.get('created_at', ''))}\n"
            f"  {text}\n"
            f"  ♥ {t.get('likes', 0)}  🔁 {t.get('retweets', 0)}  "
            f"💬 {t.get('replies', 0)}  ❝ {t.get('quotes', 0)}")


def _extract_tweets(data):
    tweets = data.get("data", [])
    users_map = {}
    if "includes" in data and "users" in data["includes"]:
        for u in data["includes"]["users"]:
            users_map[u["id"]] = u
    result = []
    for t in tweets:
        author = users_map.get(t.get("author_id", ""), {})
        pm = t.get("public_metrics") or {}
        result.append({
            "id": t["id"],
            "text": t.get("text", ""),
            "author_username": author.get("username", ""),
            "author_name": author.get("name", ""),
            "created_at": t.get("created_at", ""),
            "likes": pm.get("like_count", 0),
            "retweets": pm.get("retweet_count", 0),
            "replies": pm.get("reply_count", 0),
            "quotes": pm.get("quote_count", 0),
        })
    return result


def _get_me(token=None):
    data = _api_req("GET", "/users/me", token=token)
    u = data.get("data")
    if u:
        return u["id"], u["username"]
    return None, None


def _consume_flags(args):
    """Parse --key value and --flag from args list. Returns (flags_dict, positional_args)."""
    flags = {}
    positionals = []
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--") and "=" in a:
            k, v = a.split("=", 1)
            flags[k[2:]] = v
            i += 1
        elif a == "--archive":
            flags["archive"] = True
            i += 1
        elif a.startswith("--") and i + 1 < len(args) and not args[i + 1].startswith("--"):
            flags[a[2:]] = args[i + 1]
            i += 2
        elif a.startswith("--"):
            flags[a[2:]] = True
            i += 1
        else:
            positionals.append(a)
            i += 1
    return flags, positionals


# ── Auth commands ─────────────────────────────────────────────────────────

def cmd_auth(args):
    if not args:
        print("Usage: auth <authorize|status|logout>")
        return
    from x_auth import authorize, status, logout
    sub = args[0]
    if sub == "authorize":
        client_id = next((args[i+1] for i, a in enumerate(args)
                          if a == "--client-id" and i+1 < len(args)),
                         os.environ.get("X_CLIENT_ID", ""))
        client_secret = next((args[i+1] for i, a in enumerate(args)
                              if a == "--client-secret" and i+1 < len(args)),
                             os.environ.get("X_CLIENT_SECRET"))
        headless = "--headless" in args
        if not client_id:
            print("Error: CLIENT_ID required. Set X_CLIENT_ID env var or pass --client-id")
            sys.exit(1)
        authorize(client_id, client_secret, headless=headless)
    elif sub == "status":
        status()
    elif sub == "logout":
        logout()
    else:
        print(f"Unknown auth command: {sub}")


# ── Search ────────────────────────────────────────────────────────────────

def cmd_search_posts(args):
    flags, positionals = _consume_flags(args)
    query = " ".join(positionals)
    if not query:
        print("Error: search query required")
        sys.exit(1)
    max_results = int(flags.get("max", "10"))
    archive = flags.get("archive", False)
    endpoint = "/tweets/search/all" if archive else "/tweets/search/recent"
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    token = _get_token()
    data = _api_req("GET", endpoint, params=params, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    label = "Full archive" if archive else "Recent"
    print(f"{label} search results for: \"{query}\"")
    tweets = _extract_tweets(data)
    if not tweets:
        print("  No results found.")
        return
    for t in tweets:
        print()
        print(_fmt_tweet(t))


def cmd_search_users(args):
    flags, positionals = _consume_flags(args)
    query = " ".join(positionals)
    if not query:
        print("Error: search query required")
        sys.exit(1)
    max_results = int(flags.get("max", "10"))
    token = _get_token()
    users = _fetch_all("/users/search", {
        "query": query,
        "max_results": min(max_results, 20),
        "user.fields": "description,public_metrics,created_at",
    }, token, max_results)
    if not users:
        print("No users found.")
        return
    print(f"User search for: \"{query}\"")
    for u in users:
        desc = (u.get("description") or "")[:180].replace("\n", " ")
        m = u.get("public_metrics", {})
        print(f"\n  @{u['username']} — {u.get('name', '')}")
        if desc:
            print(f"  {desc}")
        print(f"  👥 {m.get('followers_count', 0)} followers · {m.get('following_count', 0)} following")


def cmd_search_news(args):
    flags, positionals = _consume_flags(args)
    query = " ".join(positionals)
    if not query:
        print("Error: search query required")
        sys.exit(1)
    max_results = int(flags.get("max", "10"))
    token = _get_token()
    data = _api_req("GET", "/news/search", params={
        "query": query, "max_results": min(max_results, 100),
        "news.fields": "name,summary,hook,category",
    }, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    stories = data.get("data", [])
    if not stories:
        print("No news found.")
        return
    print(f"News for: \"{query}\" ({len(stories)} stories)")
    for s in stories[:max_results]:
        print(f"\n  📰 {s.get('name', '')}")
        if s.get("category"):
            print(f"     [{s['category']}]")
        print(f"     {s.get('hook', s.get('summary', ''))[:200]}")


# ── User ──────────────────────────────────────────────────────────────────

def cmd_user_get(args):
    username = args[0] if args else ""
    if not username:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    data = _api_req("GET", f"/users/by/username/{username}", params={
        "user.fields": "description,public_metrics,created_at,location,url,profile_image_url",
    }, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    u = data.get("data")
    if not u:
        print(f"User @{username} not found.")
        return
    m = u.get("public_metrics", {})
    desc = u.get("description", "") or ""
    print(f"@{u['username']} — {u.get('name', '')}")
    if desc:
        print(f"  {desc}")
    print(f"  👥 {m.get('followers_count', 0)} followers · {m.get('following_count', 0)} following")
    print(f"  📝 {m.get('tweet_count', 0)} posts")
    print(f"  📅 Joined {_format_time(u.get('created_at', ''))}")
    if u.get("location"):
        print(f"  📍 {u['location']}")
    if u.get("url"):
        print(f"  🔗 {u['url']}")


def cmd_user_me(args):
    token = _get_token()
    data = _api_req("GET", "/users/me", params={
        "user.fields": "description,public_metrics,created_at",
    }, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    u = data.get("data")
    if not u:
        print("Could not fetch current user.")
        return
    m = u.get("public_metrics", {})
    desc = u.get("description", "") or ""
    print(f"@{u['username']} — {u.get('name', '')} (you)")
    if desc:
        print(f"  {desc}")
    print(f"  👥 {m.get('followers_count', 0)} followers · {m.get('following_count', 0)} following")
    print(f"  📝 {m.get('tweet_count', 0)} posts")
    print(f"  📅 Joined {_format_time(u.get('created_at', ''))}")


def cmd_user_timeline(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "10"))
    token = _get_token()
    uid = _resolve_user_id(args[0], token)
    if not uid:
        print(f"User @{args[0]} not found.")
        return
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics",
    }
    tweets = _extract_tweets(_api_req("GET", f"/users/{uid}/tweets", params=params, token=token))
    if not tweets:
        print(f"@{args[0]} has no recent posts.")
        return
    print(f"@{args[0]}'s recent posts:")
    for t in tweets:
        print()
        print(_fmt_tweet(t))


def cmd_user_mentions(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "10"))
    token = _get_token()
    uid = _resolve_user_id(args[0], token)
    if not uid:
        print(f"User @{args[0]} not found.")
        return
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    tweets = _extract_tweets(_api_req("GET", f"/users/{uid}/mentions", params=params, token=token))
    if not tweets:
        print(f"@{args[0]} has no mentions.")
        return
    print(f"@{args[0]}'s mentions:")
    for t in tweets:
        print()
        print(_fmt_tweet(t))


def _user_list_cmd(username, endpoint, label, args):
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "10"))
    token = _get_token()
    uid = _resolve_user_id(username, token)
    if not uid:
        print(f"User @{username} not found.")
        return
    users = _fetch_all(f"/users/{uid}/{endpoint}", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name,public_metrics",
    }, token, max_results)
    if not users:
        print(f"@{username} has no {label}.")
        return
    print(f"@{username}'s {label}:")
    for u in users:
        m = u.get("public_metrics", {})
        print(f"  @{u['username']} — {u.get('name', '')} ({m.get('followers_count', 0)} followers)")


def cmd_user_followers(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    _user_list_cmd(args[0], "followers", "followers", args)


def cmd_user_following(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    _user_list_cmd(args[0], "following", "following", args)


def cmd_user_liked(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "10"))
    token = _get_token()
    uid = _resolve_user_id(args[0], token)
    if not uid:
        print(f"User @{args[0]} not found.")
        return
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    tweets = _extract_tweets(_api_req("GET", f"/users/{uid}/liked_tweets", params=params, token=token))
    if not tweets:
        print(f"@{args[0]} hasn't liked recent posts.")
        return
    print(f"Posts liked by @{args[0]}:")
    for t in tweets:
        print()
        print(_fmt_tweet(t))


# ── Tweet ─────────────────────────────────────────────────────────────────

def _upload_media_files(media_paths, token):
    """Upload multiple media files. Returns list of media_id strings.

    ⚠️  Data transmitted: file contents + Bearer token sent to api.x.com over HTTPS.
    """
    if not media_paths:
        return []
    from x_media import upload as _media_upload
    ids = []
    for path in media_paths:
        try:
            media_id = _media_upload(path, token)
            if media_id:
                ids.append(media_id)
                print(f"  Uploaded {path} → media_id: {media_id}", file=sys.stderr)
            else:
                print(f"Error uploading {path}: no media_id returned", file=sys.stderr)
                sys.exit(1)
        except SystemExit:
            raise
        except Exception as e:
            print(f"Error uploading {path}: {e}", file=sys.stderr)
            sys.exit(1)
    return ids


def cmd_tweet_post(args):
    text_parts = []
    reply_to = None
    media_paths = []
    for i, a in enumerate(args):
        if a == "--reply-to" and i + 1 < len(args):
            reply_to = args[i + 1]
        elif a == "--media" and i + 1 < len(args):
            media_paths.append(args[i + 1])
        elif not a.startswith("--"):
            text_parts.append(a)
    text = " ".join(text_parts)
    if not text:
        print("Error: tweet text required")
        sys.exit(1)

    token = _get_token()
    media_ids = _upload_media_files(media_paths, token)

    body = {"text": text}
    if reply_to:
        body["reply"] = {"in_reply_to_tweet_id": reply_to}
    if media_ids:
        body["media"] = {"media_ids": media_ids}

    data = _api_req("POST", "/tweets", body=body, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    created = data.get("data", {})
    tid = created.get("id", "")
    print(f"Posted! ID: {tid}")
    print(f"https://x.com/i/status/{tid}")
    return tid


def cmd_tweet_get(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    params = {
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    tweets = _extract_tweets(_api_req("GET", f"/tweets/{args[0]}", params=params, token=token))
    if not tweets:
        print("Tweet not found.")
        return
    t = tweets[0]
    print(f"@{t['author_username']} ({t['author_name']}) · {_format_time(t['created_at'])}")
    print(f"  {t['text']}")
    print(f"  ♥ {t['likes']}  🔁 {t['retweets']}  💬 {t['replies']}  ❝ {t['quotes']}")
    print(f"  https://x.com/i/status/{args[0]}")


def cmd_tweet_delete(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    data = _api_req("DELETE", f"/tweets/{args[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Deleted tweet {args[0]}")


def cmd_tweet_like(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/likes", body={"tweet_id": args[0]}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Liked tweet {args[0]}")


def cmd_tweet_unlike(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/likes/{args[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Unliked tweet {args[0]}")


def cmd_tweet_retweet(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/retweets", body={"tweet_id": args[0]}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Retweeted tweet {args[0]}")


def cmd_tweet_unretweet(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/retweets/{args[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Unretweeted tweet {args[0]}")


def cmd_tweet_likers(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    users = _fetch_all(f"/tweets/{args[0]}/liking_users", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name,public_metrics",
    }, token, max_results)
    if not users:
        print("No likes yet.")
        return
    print("Liked by:")
    for u in users:
        m = u.get("public_metrics", {})
        print(f"  @{u['username']} — {u.get('name', '')} ({m.get('followers_count', 0)} followers)")


def cmd_tweet_retweeters(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    users = _fetch_all(f"/tweets/{args[0]}/retweeted_by", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name,public_metrics",
    }, token, max_results)
    if not users:
        print("No retweets yet.")
        return
    print("Retweeted by:")
    for u in users:
        m = u.get("public_metrics", {})
        print(f"  @{u['username']} — {u.get('name', '')} ({m.get('followers_count', 0)} followers)")


def cmd_tweet_quote_tweets(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "10"))
    token = _get_token()
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    tweets = _extract_tweets(_api_req("GET", f"/tweets/{args[0]}/quote_tweets",
                                       params=params, token=token))
    if not tweets:
        print("No quote tweets found.")
        return
    print(f"Quote tweets for {args[0]}:")
    for t in tweets:
        print()
        print(_fmt_tweet(t))


# ── Thread ────────────────────────────────────────────────────────────────

def cmd_thread_post(args):
    """Post a thread (multiple tweets, each replying to the previous)."""
    media_paths = []
    texts = []
    for i, a in enumerate(args):
        if a == "--media" and i + 1 < len(args):
            media_paths.append(args[i + 1])
        elif a.startswith("--text") and i + 1 < len(args):
            idx = a.replace("--text", "")
            idx = int(idx) if idx else 1
            texts.append((idx, args[i + 1]))

    texts.sort()
    if not texts:
        print("Error: use --text1, --text2, --text3 etc. for thread posts")
        sys.exit(1)

    token = _get_token()
    media_ids = _upload_media_files(media_paths, token)
    prev_id = None
    for idx, text in texts:
        if not text.strip():
            continue
        body = {"text": text}
        if prev_id:
            body["reply"] = {"in_reply_to_tweet_id": prev_id}
        if media_ids and idx == 1:
            body["media"] = {"media_ids": media_ids}
        data = _api_req("POST", "/tweets", body=body, token=token)
        if data.get("error"):
            print(f"Error on tweet {idx}: {data.get('detail', 'Unknown error')}")
            sys.exit(1)
        tid = data.get("data", {}).get("id", "")
        prev_id = tid
        print(f"  {idx}. Posted: {tid} → https://x.com/i/status/{tid}")


# ── Trends ────────────────────────────────────────────────────────────────

WOEIDS = [
    (1, "Worldwide"), (23424977, "United States"), (23424856, "Japan"),
    (23424975, "United Kingdom"), (23424781, "China"), (23424829, "Germany"),
    (23424819, "France"), (23424934, "Canada"), (23424768, "Brazil"),
    (23424900, "Mexico"), (23424848, "India"), (23424868, "South Korea"),
    (23424747, "Australia"), (23424908, "Nigeria"), (23424925, "Turkey"),
    (2295420, "Tokyo"), (2442047, "Los Angeles"), (2459115, "New York"),
    (44418, "London"), (2151849, "Shanghai"),
]


def cmd_trends(args):
    woeid = 1
    if "--woeid" in args:
        idx = args.index("--woeid")
        try:
            woeid = int(args[idx + 1])
        except (ValueError, IndexError):
            pass
    token = _get_token()
    data = _api_req("GET", f"/trends/by/woeid/{woeid}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    trends = data.get("data", [])
    if not trends:
        print("No trends found.")
        return
    loc = data.get("meta", {}).get("location", f"WOEID {woeid}")
    print(f"Trending in {loc}:")
    for i, t in enumerate(trends[:20], 1):
        vol = t.get("tweet_volume", "")
        vs = f" · {vol} posts" if vol else ""
        print(f"  {i}. {t.get('name', '')}{vs}")


def cmd_trends_list(args):
    print("Available locations (WOEID):")
    for woeid, name in WOEIDS:
        print(f"  {woeid}: {name}")


# ── Bookmarks ─────────────────────────────────────────────────────────────

def cmd_bookmark_list(args):
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    tweets = _extract_tweets(_api_req("GET", f"/users/{my_id}/bookmarks",
                                       params=params, token=token))
    if not tweets:
        print("No bookmarks.")
        return
    print("Your bookmarks:")
    for i, t in enumerate(tweets, 1):
        print(f"\n  {i}. [{t['id']}]")
        print(_fmt_tweet(t))


def cmd_bookmark_add(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/bookmarks",
                     body={"tweet_id": args[0]}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Bookmarked tweet {args[0]}")


def cmd_bookmark_remove(args):
    if not args:
        print("Error: tweet ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/bookmarks/{args[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Removed bookmark for tweet {args[0]}")


# ── Articles ──────────────────────────────────────────────────────────────

def cmd_article_draft(args):
    title = None
    text = None
    rich = False  # Use rich text (headers, bold/italic support)
    for i, a in enumerate(args):
        if a == "--title" and i + 1 < len(args):
            title = args[i + 1]
        if a == "--text" and i + 1 < len(args):
            text = args[i + 1]
        if a == "--rich":
            rich = True
    if not title or not text:
        print("Error: --title and --text required")
        sys.exit(1)

    if rich:
        # Parse simple markdown-like rich text
        blocks = []
        for para in text.split("\n\n"):
            para = para.strip()
            if not para:
                continue
            if para.startswith("## "):
                blocks.append({"text": para[3:], "type": "header-two",
                               "inline_style_ranges": []})
            elif para.startswith("# "):
                blocks.append({"text": para[2:], "type": "header-one",
                               "inline_style_ranges": []})
            elif para.startswith("- ") or para.startswith("* "):
                for line in para.split("\n"):
                    line = line.strip()
                    if line.startswith("- ") or line.startswith("* "):
                        blocks.append({"text": line[2:], "type": "unordered-list-item",
                                       "inline_style_ranges": []})
            else:
                # Parse inline formatting
                ranges = []
                clean = para
                if "**" in para:
                    # Bold
                    import re
                    for m in re.finditer(r"\*\*(.+?)\*\*", para):
                        ranges.append({
                            "offset": m.start(),
                            "length": m.end() - m.start() - 4,
                            "style": "bold"
                        })
                    clean = re.sub(r"\*\*(.+?)\*\*", r"\1", clean)
                if "*" in clean and "**" not in para:
                    import re
                    for m in re.finditer(r"\*(.+?)\*", clean):
                        ranges.append({
                            "offset": m.start(),
                            "length": m.end() - m.start() - 2,
                            "style": "italic"
                        })
                    clean = re.sub(r"\*(.+?)\*", r"\1", clean)
                blocks.append({"text": clean, "type": "unstyled",
                               "inline_style_ranges": ranges})

        body = {
            "title": title,
            "content_state": {
                "blocks": blocks,
                "entities": [],
            },
        }
    else:
        body = {
            "title": title,
            "content_state": {
                "blocks": [{"text": text, "type": "unstyled"}],
                "entities": [],
            },
        }

    token = _get_token()
    data = _api_req("POST", "/articles/draft", body=body, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    article = data.get("data", {})
    print(f"Draft created: {title}")
    print(f"Article ID: {article.get('id', '')}")


def cmd_article_publish(args):
    if not args:
        print("Error: article ID required")
        sys.exit(1)
    token = _get_token()
    data = _api_req("POST", f"/articles/{args[0]}/publish", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    post_id = data.get("data", {}).get("post_id", "")
    print(f"Article {args[0]} published! Post ID: {post_id}")


# ── Follow / Unfollow ─────────────────────────────────────────────────────

def cmd_follow(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    target_id = _resolve_user_id(args[0], token)
    if not target_id:
        print(f"User @{args[0]} not found.")
        return
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/following",
                     body={"target_user_id": target_id}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Now following @{args[0]}")


def cmd_unfollow(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    target_id = _resolve_user_id(args[0], token)
    if not target_id:
        print(f"User @{args[0]} not found.")
        return
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/following/{target_id}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Unfollowed @{args[0]}")


# ── DM ────────────────────────────────────────────────────────────────────

def cmd_dm_list(args):
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    params = {
        "max_results": min(max_results, 100),
        "dm_event.fields": "created_at,sender_id,participant_ids",
        "expansions": "sender_id,participant_ids",
        "user.fields": "username,name",
    }
    data = _api_req("GET", "/dm_events", params=params, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    events = data.get("data", [])
    if not events:
        print("No DM conversations.")
        return
    users_map = {}
    if "includes" in data and "users" in data["includes"]:
        for u in data["includes"]["users"]:
            users_map[u["id"]] = u
    print("Recent DMs:")
    for e in events[:max_results]:
        sender = users_map.get(e.get("sender_id", ""), {})
        text = e.get("text", "")[:120].replace("\n", " ")
        print(f"\n  [{e['id']}] @{sender.get('username', '')}: {text}")
        print(f"     {_format_time(e.get('created_at', ''))}")


def cmd_dm_conversation(args):
    if not args:
        print("Error: conversation ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    params = {
        "max_results": min(max_results, 100),
        "dm_event.fields": "created_at,sender_id",
        "expansions": "sender_id",
        "user.fields": "username,name",
    }
    data = _api_req("GET", f"/dm_conversations/{args[0]}/dm_events",
                     params=params, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    events = data.get("data", [])
    if not events:
        print("No messages in this conversation.")
        return
    users_map = {}
    if "includes" in data and "users" in data["includes"]:
        for u in data["includes"]["users"]:
            users_map[u["id"]] = u
    print("⚠️  以下为私信内容（非公开数据），请注意不要外泄。", file=sys.stderr)
    print(f"Conversation {args[0]}:")
    for e in events:
        sender = users_map.get(e.get("sender_id", ""), {})
        print(f"\n  @{sender.get('username', '')} · {_format_time(e.get('created_at', ''))}")
        print(f"  {e.get('text', '')}")


def cmd_dm_send(args):
    _require_confirm(args, "发送私信")
    flags, pos = _consume_flags(args)
    if len(pos) < 2:
        print("Error: dm send <username> <text> [--confirm]")
        sys.exit(1)
    username = pos[0]
    text = " ".join(pos[1:])
    token = _get_token()
    target_id = _resolve_user_id(username, token)
    if not target_id:
        print(f"User @{username} not found.")
        return
    data = _api_req("POST", "/dm_conversations",
                     body={
                         "conversation_type": "GroupDM",
                         "participant_ids": [target_id],
                         "message": {"text": text},
                     }, token=token)
    if data.get("error"):
        # Try DM with participant ID endpoint
        data = _api_req("POST",
                         f"/dm_conversations/with/{target_id}/messages",
                         body={"text": text}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"DM sent to @{username}")


def cmd_dm_delete(args):
    _require_confirm(args, "删除私信")
    flags, pos = _consume_flags(args)
    if not pos:
        print("Error: dm delete <event_id> [--confirm]")
        sys.exit(1)
    token = _get_token()
    data = _api_req("DELETE", f"/dm_events/{pos[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Deleted DM event {pos[0]}")


# ── Lists ─────────────────────────────────────────────────────────────────

def cmd_list_create(args):
    name = args[0] if args else ""
    if not name:
        print("Error: list name required")
        sys.exit(1)
    description = next((args[i+1] for i, a in enumerate(args)
                        if a == "--description" and i+1 < len(args)), "")
    token = _get_token()
    body = {"name": name, "description": description, "private": True}
    data = _api_req("POST", "/lists", body=body, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    lst = data.get("data", {})
    print(f"List created: {name} (ID: {lst.get('id', '')})")


def cmd_list_get(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    token = _get_token()
    data = _api_req("GET", f"/lists/{args[0]}",
                     params={"list.fields": "name,description,member_count,follower_count,owner_id"},
                     token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    lst = data.get("data", {})
    desc = lst.get("description", "") or ""
    print(f"List: {lst.get('name', '')} ({lst.get('id', '')})")
    if desc:
        print(f"  {desc}")
    print(f"  👥 {lst.get('member_count', 0)} members · {lst.get('follower_count', 0)} followers")


def cmd_list_delete(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    token = _get_token()
    data = _api_req("DELETE", f"/lists/{args[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Deleted list {args[0]}")


def cmd_list_members(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    users = _fetch_all(f"/lists/{args[0]}/members", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name,public_metrics",
    }, token, max_results)
    if not users:
        print("No members.")
        return
    print(f"List {args[0]} members:")
    for u in users:
        m = u.get("public_metrics", {})
        print(f"  @{u['username']} — {u.get('name', '')} ({m.get('followers_count', 0)} followers)")


def cmd_list_posts(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "10"))
    token = _get_token()
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name",
    }
    tweets = _extract_tweets(_api_req("GET", f"/lists/{args[0]}/tweets",
                                       params=params, token=token))
    if not tweets:
        print("No posts in this list.")
        return
    print(f"List {args[0]} posts:")
    for t in tweets:
        print()
        print(_fmt_tweet(t))


def cmd_list_followers(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    users = _fetch_all(f"/lists/{args[0]}/followers", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name,public_metrics",
    }, token, max_results)
    if not users:
        print("No followers.")
        return
    print(f"List {args[0]} followers:")
    for u in users:
        m = u.get("public_metrics", {})
        print(f"  @{u['username']} — {u.get('name', '')}")


def cmd_list_add_member(args):
    if len(args) < 2:
        print("Error: list add-member <list-id> <username>")
        sys.exit(1)
    list_id, username = args[0], args[1]
    token = _get_token()
    uid = _resolve_user_id(username, token)
    if not uid:
        print(f"User @{username} not found.")
        return
    data = _api_req("POST", f"/lists/{list_id}/members",
                     body={"user_id": uid}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Added @{username} to list {list_id}")


def cmd_list_remove_member(args):
    if len(args) < 2:
        print("Error: list remove-member <list-id> <username>")
        sys.exit(1)
    list_id, username = args[0], args[1]
    token = _get_token()
    uid = _resolve_user_id(username, token)
    if not uid:
        print(f"User @{username} not found.")
        return
    data = _api_req("DELETE", f"/lists/{list_id}/members/{uid}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Removed @{username} from list {list_id}")


def cmd_list_follow(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/followed_lists",
                     body={"list_id": args[0]}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Following list {args[0]}")


def cmd_list_unfollow(args):
    if not args:
        print("Error: list ID required")
        sys.exit(1)
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/followed_lists/{args[0]}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Unfollowed list {args[0]}")


def cmd_list_my(args):
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    my_id, my_username = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    lists = _fetch_all(f"/users/{my_id}/owned_lists", {
        "max_results": min(max_results, 100),
        "list.fields": "name,description,member_count,follower_count,private",
    }, token, max_results)
    if not lists:
        print("You don't own any lists.")
        return
    print("Your lists:")
    for lst in lists:
        priv = "🔒" if lst.get("private") else "🌍"
        desc = (lst.get("description") or "")[:100].replace("\n", " ")
        print(f"\n  {priv} {lst.get('name', '')} ({lst.get('id', '')})")
        if desc:
            print(f"     {desc}")
        print(f"     👥 {lst.get('member_count', 0)} members · {lst.get('follower_count', 0)} followers")


# ── Block ─────────────────────────────────────────────────────────────────

def cmd_block(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    target_id = _resolve_user_id(args[0], token)
    if not target_id:
        print(f"User @{args[0]} not found.")
        return
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/blocking",
                     body={"target_user_id": target_id}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Blocked @{args[0]}")


def cmd_unblock(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    target_id = _resolve_user_id(args[0], token)
    if not target_id:
        print(f"User @{args[0]} not found.")
        return
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/blocking/{target_id}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Unblocked @{args[0]}")


def cmd_blocked(args):
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    users = _fetch_all(f"/users/{my_id}/blocking", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name",
    }, token, max_results)
    if not users:
        print("No blocked users.")
        return
    print("Blocked users:")
    for u in users:
        print(f"  @{u['username']} — {u.get('name', '')}")


# ── Mute ──────────────────────────────────────────────────────────────────

def cmd_mute(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    target_id = _resolve_user_id(args[0], token)
    if not target_id:
        print(f"User @{args[0]} not found.")
        return
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("POST", f"/users/{my_id}/muting",
                     body={"target_user_id": target_id}, token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Muted @{args[0]}")


def cmd_unmute(args):
    if not args:
        print("Error: username required")
        sys.exit(1)
    token = _get_token()
    target_id = _resolve_user_id(args[0], token)
    if not target_id:
        print(f"User @{args[0]} not found.")
        return
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    data = _api_req("DELETE", f"/users/{my_id}/muting/{target_id}", token=token)
    if data.get("error"):
        print(f"Error: {data.get('detail', 'Unknown error')}")
        sys.exit(1)
    print(f"Unmuted @{args[0]}")


def cmd_muted(args):
    max_results = int(next((args[i+1] for i, a in enumerate(args)
                            if a == "--max" and i+1 < len(args)), "20"))
    token = _get_token()
    my_id, _ = _get_me(token)
    if not my_id:
        print("Error: could not identify current user")
        sys.exit(1)
    users = _fetch_all(f"/users/{my_id}/muting", {
        "max_results": min(max_results, 100),
        "user.fields": "username,name",
    }, token, max_results)
    if not users:
        print("No muted users.")
        return
    print("Muted users:")
    for u in users:
        print(f"  @{u['username']} — {u.get('name', '')}")


# ── Main dispatch ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "auth":
        cmd_auth(args)
    elif cmd == "search":
        if not args:
            print("Usage: search <posts|users|news> <query> [--max N] [--archive]")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "posts": cmd_search_posts,
            "users": cmd_search_users,
            "news": cmd_search_news,
        }.get(sub, lambda _: print(f"Unknown search type: {sub}"))(sub_args)
    elif cmd == "user":
        if not args:
            print("Usage: user <get|me|timeline|mentions|followers|following|liked> ...")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "get": cmd_user_get,
            "me": cmd_user_me,
            "timeline": cmd_user_timeline,
            "mentions": cmd_user_mentions,
            "followers": cmd_user_followers,
            "following": cmd_user_following,
            "liked": cmd_user_liked,
        }.get(sub, lambda _: print(f"Unknown user command: {sub}"))(sub_args)
    elif cmd == "tweet":
        if not args:
            print("Usage: tweet <post|get|delete|like|unlike|retweet|unretweet|likers|retweeters|quote-tweets> ...")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "post": cmd_tweet_post,
            "get": cmd_tweet_get,
            "delete": cmd_tweet_delete,
            "like": cmd_tweet_like,
            "unlike": cmd_tweet_unlike,
            "retweet": cmd_tweet_retweet,
            "unretweet": cmd_tweet_unretweet,
            "likers": cmd_tweet_likers,
            "retweeters": cmd_tweet_retweeters,
            "quote-tweets": cmd_tweet_quote_tweets,
            "quotes": cmd_tweet_quote_tweets,
        }.get(sub, lambda _: print(f"Unknown tweet command: {sub}"))(sub_args)
    elif cmd == "thread":
        if not args or args[0] != "post":
            print("Usage: thread post --text1 <tweet1> --text2 <tweet2> ... [--media path ...]")
            sys.exit(1)
        cmd_thread_post(args[1:])
    elif cmd == "trends":
        if args and args[0] == "list":
            cmd_trends_list(args[1:])
        else:
            cmd_trends(args)
    elif cmd == "bookmark":
        if not args:
            print("Usage: bookmark <list|add|remove> ...")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "list": cmd_bookmark_list,
            "add": cmd_bookmark_add,
            "remove": cmd_bookmark_remove,
        }.get(sub, lambda _: print(f"Unknown bookmark command: {sub}"))(sub_args)
    elif cmd == "article":
        if not args:
            print("Usage: article <draft|publish> ...")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "draft": cmd_article_draft,
            "publish": cmd_article_publish,
        }.get(sub, lambda _: print(f"Unknown article command: {sub}"))(sub_args)
    elif cmd == "follow":
        cmd_follow(args)
    elif cmd == "unfollow":
        cmd_unfollow(args)
    elif cmd == "dm":
        if not args:
            print("Usage: dm <list|conversation|send|delete> ...")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "list": cmd_dm_list,
            "conversation": cmd_dm_conversation,
            "send": cmd_dm_send,
            "delete": cmd_dm_delete,
        }.get(sub, lambda _: print(f"Unknown dm command: {sub}"))(sub_args)
    elif cmd == "list":
        if not args:
            print("Usage: list <create|get|delete|members|posts|followers|add-member|remove-member|follow|unfollow|my> ...")
            sys.exit(1)
        sub, sub_args = args[0], args[1:]
        {
            "create": cmd_list_create,
            "get": cmd_list_get,
            "delete": cmd_list_delete,
            "members": cmd_list_members,
            "posts": cmd_list_posts,
            "followers": cmd_list_followers,
            "add-member": cmd_list_add_member,
            "remove-member": cmd_list_remove_member,
            "follow": cmd_list_follow,
            "unfollow": cmd_list_unfollow,
            "my": cmd_list_my,
        }.get(sub, lambda _: print(f"Unknown list command: {sub}"))(sub_args)
    elif cmd == "block":
        if args and args[0] == "list":
            cmd_blocked(args[1:])
        else:
            cmd_block(args)
    elif cmd == "unblock":
        cmd_unblock(args)
    elif cmd == "blocked":
        cmd_blocked(args)
    elif cmd == "mute":
        if args and args[0] == "list":
            cmd_muted(args[1:])
        else:
            cmd_mute(args)
    elif cmd == "unmute":
        cmd_unmute(args)
    elif cmd == "muted":
        cmd_muted(args)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__.strip())
        sys.exit(1)


if __name__ == "__main__":
    main()
