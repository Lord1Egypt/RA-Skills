#!/usr/bin/env python3
"""Slack Thread/Channel Reader — Compact LLM-friendly output.

Usage:
  slack-thread.sh <slack-thread-link>
  slack-thread.sh <channel-id> <thread-ts>
  slack-thread.sh <slack-channel-link>
  slack-thread.sh <channel-id> [--from DATE] [--to DATE] [--limit N] [--with-threads] [--thread-limit N] [--desc]

Output: one message per line, oldest first (asc, default), minimal whitespace.

Link type behavior:
  /archives/CHANNEL                      → channel history
  /archives/CHANNEL/pTS                  → full thread (ts as parent)
  /archives/CHANNEL/pTS?thread_ts=...    → single reply only

Options:
  --desc             descending order (newest→oldest)
  --limit N          number of channel history messages (default 0=all)
  --from YYYY-MM-DD  messages after this date only (channel mode)
  --to YYYY-MM-DD    messages before this date only (channel mode)
  --with-threads     include thread replies inline in channel mode
  --thread-limit N   max replies per thread (0=all)
"""

import json, sys, re, time, threading, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# --- Config ---

CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"
USER_CACHE_FILE = Path.home() / ".cache" / "slack-reader" / "users.json"
USER_CACHE_TTL = 86400  # user cache expiry: 24 hours

MAX_RETRIES = 3          # rate limit retry count
MAX_WORKERS_USERS = 5    # parallel user info lookups
MAX_WORKERS_THREADS = 8  # parallel thread reply fetches
HTTP_TIMEOUT = 30        # HTTP request timeout (seconds)


def load_token():
    """Read Slack Bot Token from openclaw.json."""
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)["channels"]["slack"]["botToken"]
    except FileNotFoundError:
        print(f"Config not found: {CONFIG_FILE}", file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Invalid config {CONFIG_FILE}: {e}", file=sys.stderr)
        sys.exit(1)


class SlackClient:
    """Slack Web API client with automatic rate limit (429) retry.

    When parallel workers hit 429 simultaneously, _rate_wait_until shares the
    wait-until timestamp across workers to prevent thundering herd on retry.
    """

    def __init__(self, token):
        self.token = token
        self._rate_lock = threading.Lock()
        self._rate_wait_until = 0.0

    def api(self, method, params):
        # If another worker hit rate limit, wait for the remaining time
        with self._rate_lock:
            wait = self._rate_wait_until - time.time()
        if wait > 0:
            time.sleep(wait)

        url = f"https://slack.com/api/{method}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
        for attempt in range(MAX_RETRIES):
            try:
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                    return json.loads(resp.read())
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    retry_after = int(e.headers.get("Retry-After", "5"))
                    with self._rate_lock:
                        self._rate_wait_until = time.time() + retry_after
                    time.sleep(retry_after)
                    continue
                raise
        print(f"Rate limit exceeded after {MAX_RETRIES} retries", file=sys.stderr)
        sys.exit(1)


def parse_slack_link(link):
    """Parse a Slack link and return (channel, msg_ts, thread_ts) tuple.

    - Channel link:  (channel, None, None)
    - Thread link:   (channel, ts, None)        ← ts is the parent message
    - Reply link:    (channel, reply_ts, thread_ts) ← thread_ts is parent, reply_ts is child
    """
    # Extract thread_ts from query string (present means reply link)
    thread_ts = None
    qs = re.search(r'[?&]thread_ts=([^&]+)', link)
    if qs:
        thread_ts = qs.group(1)

    # Extract channel and message ts from path
    # pTS format: p + 10 digits (seconds) + 6 digits (microseconds) → "seconds.microseconds"
    m = re.search(r'/archives/([^/]+)/p(\d+)', link)
    if m:
        raw_ts = m.group(2)
        return m.group(1), f"{raw_ts[:10]}.{raw_ts[10:]}", thread_ts

    # Channel link (no ts)
    m = re.search(r'/archives/([^/?]+)', link)
    if m:
        return m.group(1), None, None

    return None, None, None


def parse_date_to_ts(date_str):
    """Convert a YYYY-MM-DD date string to a Slack ts (Unix timestamp string)."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return str(dt.timestamp())
    except ValueError:
        print(f"Invalid date format: {date_str} (expected YYYY-MM-DD)", file=sys.stderr)
        sys.exit(1)


# --- User cache ---
# Locally cache user ID → real name mappings to minimize API calls

def _load_user_cache():
    """Load user map from cache file. Returns empty dict if TTL expired."""
    if not USER_CACHE_FILE.exists():
        return {}
    try:
        with open(USER_CACHE_FILE) as f:
            data = json.load(f)
        if time.time() - data.get("_ts", 0) > USER_CACHE_TTL:
            return {}
        return data.get("users", {})
    except (json.JSONDecodeError, KeyError):
        return {}


def _save_user_cache(user_map):
    """Merge newly fetched user info into existing cache and save.

    Preserves existing cache _ts to prevent TTL reset.
    Sets a new _ts if cache is expired or missing.
    """
    USER_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing_ts = 0
    existing_users = {}
    if USER_CACHE_FILE.exists():
        try:
            with open(USER_CACHE_FILE) as f:
                data = json.load(f)
            existing_ts = data.get("_ts", 0)
            if time.time() - existing_ts <= USER_CACHE_TTL:
                existing_users = data.get("users", {})
            else:
                existing_ts = 0  # expired, start fresh
        except (json.JSONDecodeError, KeyError):
            pass
    existing_users.update(user_map)
    with open(USER_CACHE_FILE, "w") as f:
        json.dump({"_ts": existing_ts or time.time(), "users": existing_users}, f, ensure_ascii=False)


def _resolve_single_user(client, uid):
    """Fetch a single user's real name via users.info API."""
    try:
        data = client.api("users.info", {"user": uid})
        if data.get("ok"):
            u = data["user"]
            return uid, u.get("real_name") or u.get("name", uid)
    except Exception:
        pass
    return uid, uid


def resolve_users(user_ids, client):
    """Resolve user IDs to real names. Cache first, parallel API calls for uncached."""
    unique_ids = {uid for uid in set(user_ids) if uid}
    cached = _load_user_cache()
    result = {}
    uncached = []
    for uid in unique_ids:
        if uid in cached:
            result[uid] = cached[uid]
        else:
            uncached.append(uid)
    if uncached:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS_USERS) as pool:
            futures = {pool.submit(_resolve_single_user, client, uid): uid for uid in uncached}
            for future in as_completed(futures):
                uid, name = future.result()
                result[uid] = name
        _save_user_cache(result)
    return result


# --- Channel info ---

def fetch_channel_name(channel, client):
    """Fetch channel name via conversations.info API. Returns None on failure."""
    try:
        data = client.api("conversations.info", {"channel": channel})
        if data.get("ok"):
            return data["channel"].get("name")
    except Exception:
        pass
    return None


# --- Fetch (deduplicated, sorted) ---

def fetch_reply(channel, thread_ts, reply_ts, client):
    """Fetch a single reply from a thread.

    Narrows the range with oldest=latest=reply_ts in conversations.replies
    to retrieve only the target reply without fetching unnecessary messages.
    Filters by ts comparison since the API always includes the parent message.
    """
    params = {"channel": channel, "ts": thread_ts, "oldest": reply_ts, "latest": reply_ts, "inclusive": "true", "limit": 1}
    data = client.api("conversations.replies", params)
    if not data.get("ok"):
        print(f"API error: {data.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)
    for msg in data.get("messages", []):
        if msg["ts"] == reply_ts:
            return msg
    return None


def fetch_thread(channel, ts, client):
    """Fetch all messages in a thread (including parent).

    - Cursor-based pagination for complete collection
    - conversations.replies duplicates parent at [0] on every page → deduplicated via seen_ts
    - Result: descending order (newest→oldest)
    """
    all_messages = []
    seen_ts = set()
    cursor = None
    while True:
        params = {"channel": channel, "ts": ts, "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = client.api("conversations.replies", params)
        if not data.get("ok"):
            print(f"API error: {data.get('error', 'unknown')}", file=sys.stderr)
            sys.exit(1)
        for msg in data.get("messages", []):
            if msg["ts"] not in seen_ts:
                seen_ts.add(msg["ts"])
                all_messages.append(msg)
        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break
    all_messages.sort(key=lambda m: float(m["ts"]), reverse=True)  # default desc, reversed to asc in main
    return all_messages


def fetch_channel(channel, client, limit=0, oldest=None, latest=None):
    """Fetch channel history (newest→oldest, API default order).

    limit=0 fetches all, limit>0 fetches that many messages.
    oldest/latest: Slack ts strings for date filtering (conversations.history API params).
    Paginates in batches of 200.
    """
    all_messages = []
    cursor = None
    while True:
        remaining = limit - len(all_messages) if limit > 0 else 200
        if limit > 0 and remaining <= 0:
            break
        batch = min(remaining, 200)
        params = {"channel": channel, "limit": batch}
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        if cursor:
            params["cursor"] = cursor
        data = client.api("conversations.history", params)
        if not data.get("ok"):
            print(f"API error: {data.get('error', 'unknown')}", file=sys.stderr)
            sys.exit(1)
        msgs = data.get("messages", [])
        all_messages.extend(msgs)
        cursor = data.get("response_metadata", {}).get("next_cursor", "")
        if not cursor or not msgs:
            break
    return all_messages


def _fetch_thread_replies(channel, thread_ts, client, thread_limit):
    """Worker function to fetch replies for an individual thread in channel mode.

    Excludes the parent message since it's already in the channel history.
    If thread_limit > 0, returns only the newest N replies.
    Catches all exceptions including SystemExit to skip only the failed thread.
    """
    try:
        replies = fetch_thread(channel, thread_ts, client)
        replies = [r for r in replies if r.get("ts") != thread_ts]
        if thread_limit > 0:
            replies = replies[:thread_limit]
        return thread_ts, replies, None
    except BaseException as e:
        print(f"[warn] Thread fetch failed {thread_ts}: {e}", file=sys.stderr)
        return thread_ts, [], str(e)


def fetch_threads_parallel(channel, messages, client, thread_limit):
    """Fetch thread replies in parallel for messages with reply_count > 0.

    Up to MAX_WORKERS_THREADS concurrent requests.
    Returns: {thread_ts: [reply_messages]} dict
    Prints a summary to stderr if any threads failed.
    """
    threaded = [m for m in messages if m.get("reply_count", 0) > 0]
    if not threaded:
        return {}
    thread_replies = {}
    failed = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS_THREADS) as pool:
        futures = {
            pool.submit(_fetch_thread_replies, channel, m["thread_ts"], client, thread_limit): m
            for m in threaded
        }
        for future in as_completed(futures):
            t_ts, replies, err = future.result()
            if err:
                failed.append(t_ts)
            if replies:
                thread_replies[t_ts] = replies
    if failed:
        print(f"[warn] {len(failed)}/{len(threaded)} threads failed: {', '.join(failed)}", file=sys.stderr)
    return thread_replies


# --- Formatting (compact, LLM-friendly) ---

def collect_user_ids(messages):
    """Collect all user IDs from messages (senders + reaction participants)."""
    ids = []
    for m in messages:
        if m.get("user"):
            ids.append(m["user"])
        for r in m.get("reactions", []):
            ids.extend(r.get("users", []))
    return ids


def replace_mentions(text, user_map):
    """Replace <@U12345> mentions with @real_name."""
    for uid, name in user_map.items():
        text = text.replace(f"<@{uid}>", f"@{name}")
    return text


def format_ts(ts_val):
    """Convert Slack ts (float string) to ISO 8601 format."""
    return datetime.fromtimestamp(float(ts_val)).strftime("%Y-%m-%dT%H:%M:%S")


def fmt_reactions(msg, user_map):
    """Format reactions as [:emoji:name1,name2]."""
    reactions = msg.get("reactions", [])
    if not reactions:
        return ""
    parts = []
    for r in reactions:
        names = ",".join(user_map.get(uid, uid) for uid in r.get("users", []))
        parts.append(f":{r['name']}:{names}")
    return " [" + "|".join(parts) + "]"


def fmt_files(msg):
    """Format attachments as 📎filename path.

    Strips https://*.slack.com/files/ prefix from permalink to save tokens.
    Full URL reconstruction: https://{workspace}.slack.com/files/ + path
    """
    files = msg.get("files", [])
    if not files:
        return ""
    parts = []
    for f in files:
        name = f.get("name", f.get("title", "file"))
        link = f.get("permalink", "")
        if link:
            # https://*.slack.com/files/USER_ID/FILE_ID/encoded_filename → USER_ID/FILE_ID
            short = re.sub(r'https://[^/]+\.slack\.com/files/', '', link)
            short = "/".join(short.split("/")[:2])  # keep only USER_ID/FILE_ID
            parts.append(f"\U0001f4ce{name} {short}")
        else:
            parts.append(f"\U0001f4ce{name}")
    return " " + " ".join(parts)


def fmt_msg(msg, user_map, indent=""):
    """Format a single message as one line.

    Format: [ISO-time|ts] username: text 📎attachments [:emoji:names]
    - ts: Slack message unique ID (unique within channel)
    - Multiline text is collapsed to single spaces
    - Bot messages have no user field, falls back to username then bot_profile
    """
    user = user_map.get(msg.get("user", "")) or msg.get("username") or msg.get("bot_profile", {}).get("name") or "bot"
    text = re.sub(r'\s+', ' ', msg.get("text", "")).strip()
    text = replace_mentions(text, user_map)
    ts_str = format_ts(msg.get("ts", 0))
    msg_ts = msg.get("ts", "")
    return f"{indent}[{ts_str}|{msg_ts}] {user}: {text}{fmt_files(msg)}{fmt_reactions(msg, user_map)}"


def fmt_participants(messages, user_map):
    """Summarize message senders. Preserves order of appearance. Includes bots."""
    seen = []
    for m in messages:
        uid = m.get("user", "")
        name = user_map.get(uid) or m.get("username") or m.get("bot_profile", {}).get("name")
        if name and name not in seen:
            seen.append(name)
    return f"[participants] {', '.join(seen)} ({len(seen)})"


def format_thread(messages, user_map, channel=None, channel_name=None, asc=False):
    """Thread mode output format.

    Header: [thread] ch:channelID(#name) parent:parentTs replies:N range:start~end
    Participants: [participants] name1, name2 (N)
    Body: messages (oldest→newest if asc=True)
    """
    if not messages:
        return "(empty)"
    parent = next((m for m in messages if m.get("thread_ts") == m.get("ts")), None)
    reply_count = parent.get("reply_count", len(messages) - 1) if parent else len(messages)
    parent_ts = parent.get("ts", "") if parent else ""
    tss = [float(m["ts"]) for m in messages]
    d0 = datetime.fromtimestamp(min(tss)).strftime("%Y-%m-%d")
    d1 = datetime.fromtimestamp(max(tss)).strftime("%Y-%m-%d")
    date_range = f"{d0}~{d1}" if d0 != d1 else d0
    ch_label = f" ch:{channel}" if channel else ""
    if channel_name:
        ch_label = f" ch:{channel}(#{channel_name})"
    lines = [f"[thread]{ch_label} parent:{parent_ts} replies:{reply_count} range:{date_range}"]
    lines.append(fmt_participants(messages, user_map))
    if asc:
        messages = list(reversed(messages))
    for msg in messages:
        lines.append(fmt_msg(msg, user_map))
    return "\n".join(lines)


def format_channel(messages, user_map, thread_replies=None, asc=False):
    """Channel mode output format.

    Appends [thread replies:N latest:time] tag to messages with threads.
    With --with-threads, displays replies inline with 1-space indentation.
    """
    messages = sorted(messages, key=lambda m: float(m["ts"]), reverse=not asc)
    lines = []
    for msg in messages:
        rc = msg.get("reply_count", 0)
        if rc:
            latest_reply = msg.get("latest_reply")
            latest_str = f" latest:{format_ts(latest_reply)}" if latest_reply else ""
            tag = f" [thread replies:{rc}{latest_str}]"
        else:
            tag = ""
        lines.append(fmt_msg(msg, user_map) + tag)
        # Display replies inline if fetched with --with-threads
        thread_ts = msg.get("thread_ts")
        if thread_replies and thread_ts and thread_ts == msg.get("ts") and thread_ts in thread_replies:
            replies = thread_replies[thread_ts]
            if asc:
                replies = list(reversed(replies))  # fetch_thread returns desc, reverse to asc
            for reply in replies:
                lines.append(fmt_msg(reply, user_map, indent=" "))
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: slack-thread.sh <link-or-channel> [thread-ts] [--from DATE] [--to DATE] [--limit N] [--with-threads] [--thread-limit N] [--desc]", file=sys.stderr)
        sys.exit(1)

    # --- Option parsing ---
    limit = 0
    with_threads = False
    thread_limit = 0
    desc = False
    oldest = None
    latest = None
    args = list(sys.argv[1:])

    if "--from" in args:
        idx = args.index("--from")
        if idx + 1 >= len(args) or args[idx + 1].startswith("-"):
            print("--from requires a date (YYYY-MM-DD)", file=sys.stderr)
            sys.exit(1)
        oldest = parse_date_to_ts(args[idx + 1])
        args = args[:idx] + args[idx + 2:]
    if "--to" in args:
        idx = args.index("--to")
        if idx + 1 >= len(args) or args[idx + 1].startswith("-"):
            print("--to requires a date (YYYY-MM-DD)", file=sys.stderr)
            sys.exit(1)
        # --to date is inclusive through end of day (23:59:59)
        latest = parse_date_to_ts(args[idx + 1])
        latest = str(float(latest) + 86400)  # next day 00:00:00
        args = args[:idx] + args[idx + 2:]
    if "--desc" in args:
        desc = True
        args.remove("--desc")
    if "--with-threads" in args:
        with_threads = True
        args.remove("--with-threads")
    if "--thread-limit" in args:
        idx = args.index("--thread-limit")
        try:
            thread_limit = int(args[idx + 1]) if idx + 1 < len(args) else 0
        except ValueError:
            print(f"--thread-limit requires a number, got: {args[idx + 1]}", file=sys.stderr)
            sys.exit(1)
        args = args[:idx] + args[idx + 2:]
    if "--limit" in args:
        idx = args.index("--limit")
        try:
            limit = int(args[idx + 1]) if idx + 1 < len(args) else 0
        except ValueError:
            print(f"--limit requires a number, got: {args[idx + 1]}", file=sys.stderr)
            sys.exit(1)
        args = args[:idx] + args[idx + 2:]
    if len(args) >= 3 and args[2].isdigit():
        limit = int(args[2])
        args = args[:2]

    # --- Input parsing ---
    # URL → parse_slack_link, otherwise treat as positional args
    channel, ts, thread_ts = None, None, None
    if args[0].startswith("http"):
        channel, ts, thread_ts = parse_slack_link(args[0])
        if not channel:
            print(f"Bad link: {args[0]}", file=sys.stderr)
            sys.exit(1)
        if len(args) >= 2 and args[1].isdigit():
            limit = int(args[1])
    else:
        channel = args[0]
        if len(args) >= 2 and not args[1].startswith("-"):
            ts = args[1]

    if (oldest or latest) and ts:
        print("[warn] --from/--to is only for channel mode, ignored for thread/reply", file=sys.stderr)

    token = load_token()
    client = SlackClient(token)

    # --- Execute: fetch channel name and data in parallel ---

    with ThreadPoolExecutor(max_workers=2) as pool:
        name_future = pool.submit(fetch_channel_name, channel, client)

        if ts and thread_ts:
            data_future = pool.submit(fetch_reply, channel, thread_ts, ts, client)
        elif ts:
            data_future = pool.submit(fetch_thread, channel, ts, client)
        else:
            data_future = pool.submit(fetch_channel, channel, client, limit, oldest, latest)

        channel_name = name_future.result()
        data = data_future.result()

    if ts and thread_ts:
        # Reply mode: fetch single reply (child ts) from thread (parent thread_ts)
        msg = data
        if not msg:
            print("(empty)")
            return
        user_map = resolve_users(collect_user_ids([msg]), client)
        ch_label = f"{channel}(#{channel_name})" if channel_name else channel
        print(f"[reply] ch:{ch_label} thread:{thread_ts}")
        print(fmt_msg(msg, user_map))
    elif ts:
        # Thread mode: fetch full thread with ts as parent
        messages = data
        if not messages:
            print("(empty)")
            return
        user_map = resolve_users(collect_user_ids(messages), client)
        print(format_thread(messages, user_map, channel, channel_name, not desc))
    else:
        # Channel mode: fetch channel history (optionally includes thread replies)
        messages = data
        if not messages:
            print("(empty)")
            return
        thread_replies = {}
        if with_threads:
            thread_replies = fetch_threads_parallel(channel, messages, client, thread_limit)
        all_msgs = list(messages)
        for replies in thread_replies.values():
            all_msgs.extend(replies)
        user_map = resolve_users(collect_user_ids(all_msgs), client)
        thread_info = f" threads:{len(thread_replies)}" if thread_replies else ""
        ch_label = f"{channel}(#{channel_name})" if channel_name else channel
        print(f"[channel] ch:{ch_label} msgs:{len(messages)}{thread_info}")
        print(fmt_participants(all_msgs, user_map))
        print(format_channel(messages, user_map, thread_replies, not desc))


if __name__ == "__main__":
    main()
