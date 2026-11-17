#!/usr/bin/env python3
"""
Twitter Bookmarks to Markdown Exporter
Parses bookmarks.json (X GraphQL or legacy v1 format) into individual .md files.
"""

import json
import re
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.parent  # project root
OUT_DIR = SCRIPT_DIR / "output" / "bookmarks"
BOOKMARKS_FILE = SCRIPT_DIR / "bookmarks.json"


def slugify(text: str) -> str:
    """Convert text to filename-safe slug."""
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text.strip())
    text = re.sub(r"[\s-]+", "-", text.lower())
    return text[:80] or "untitled"


def expand_urls(text: str, urls: list) -> str:
    """Replace t.co short URLs with their expanded originals."""
    for u in urls:
        short = u.get("url", "")
        expanded = u.get("expanded_url", "")
        if short and expanded:
            text = text.replace(short, expanded)
    return text


def get_screen_name(user_result: dict) -> str:
    """Extract screen_name from user result (new API puts it in .core, legacy in .legacy)."""
    return (
        user_result.get("core", {}).get("screen_name")
        or user_result.get("legacy", {}).get("screen_name")
        or "unknown"
    )


def get_display_name(user_result: dict) -> str:
    """Extract display name from user result."""
    return (
        user_result.get("core", {}).get("name")
        or user_result.get("legacy", {}).get("name")
        or ""
    )


def parse_created_at(created_at_raw: str) -> str:
    if not created_at_raw:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        return datetime.strptime(created_at_raw, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
    except ValueError:
        return datetime.now().strftime("%Y-%m-%d")


def extract_media_urls(result: dict) -> list:
    """Extract image/video URLs from extended_entities or entities."""
    media_items = (
        result.get("legacy", {}).get("extended_entities", {}).get("media", [])
        or result.get("legacy", {}).get("entities", {}).get("media", [])
    )
    urls = []
    for m in media_items:
        media_type = m.get("type", "")
        if media_type == "photo":
            urls.append(("image", m.get("media_url_https", m.get("media_url", ""))))
        elif media_type in ("video", "animated_gif"):
            # Pick highest-bitrate variant
            variants = m.get("video_info", {}).get("variants", [])
            mp4s = [v for v in variants if v.get("content_type") == "video/mp4"]
            if mp4s:
                best = max(mp4s, key=lambda v: v.get("bitrate", 0))
                urls.append(("video", best.get("url", "")))
            thumb = m.get("media_url_https", "")
            if thumb:
                urls.append(("thumbnail", thumb))
    return urls


def extract_tweet_text(result: dict) -> tuple[str, str]:
    """
    Return (full_text, content_type) for a tweet result.
    content_type: 'note' | 'article' | 'tweet'
    URLs in text are expanded. t.co media placeholders are stripped.
    """
    legacy = result.get("legacy", {})
    entity_urls = legacy.get("entities", {}).get("urls", [])

    # Long-form note tweet (supersedes legacy.full_text)
    if "note_tweet" in result:
        note_result = result["note_tweet"].get("note_tweet_results", {}).get("result", {})
        text = note_result.get("text", legacy.get("full_text", ""))
        note_urls = note_result.get("entity_set", {}).get("urls", []) or entity_urls
        text = expand_urls(text, note_urls)
        return text, "note"

    # X Article (legacy.full_text is just a t.co link)
    if "article" in result:
        art = result["article"].get("article_results", {}).get("result", {})
        title = art.get("title", "")
        preview = art.get("preview_text", "")
        art_url = ""
        for u in entity_urls:
            if "x.com/i/article" in u.get("expanded_url", ""):
                art_url = u["expanded_url"]
                break
        text = f"{title}\n\n{preview}"
        if art_url:
            text += f"\n\n{art_url}"
        return text, "article"

    # Regular tweet
    full_text = legacy.get("full_text", "")
    full_text = expand_urls(full_text, entity_urls)
    # Strip trailing t.co media placeholder (already captured as media)
    full_text = re.sub(r"\s*https://t\.co/\S+$", "", full_text).strip()
    return full_text, "tweet"


def extract_quoted_tweet(result: dict) -> dict | None:
    """Extract quoted tweet data if present."""
    qr = result.get("quoted_status_result", {}).get("result", {})
    if not qr:
        return None
    # Unwrap limitedActionResults wrapper
    if qr.get("__typename") == "TweetWithVisibilityResults":
        qr = qr.get("tweet", qr)
    if qr.get("__typename") != "Tweet":
        return None

    user_result = qr.get("core", {}).get("user_results", {}).get("result", {})
    screen_name = get_screen_name(user_result)
    q_legacy = qr.get("legacy", {})
    q_id = q_legacy.get("id_str") or qr.get("rest_id", "")
    q_text, _ = extract_tweet_text(qr)
    return {
        "author": screen_name,
        "url": f"https://x.com/{screen_name}/status/{q_id}" if q_id else "",
        "text": q_text,
    }


def unwrap_result(result: dict) -> dict:
    """Unwrap limitedActionResults or TweetWithVisibilityResults wrappers."""
    if result.get("__typename") in ("TweetWithVisibilityResults", "limitedActionResults"):
        return result.get("tweet", result)
    return result


def extract_tweet_entries(data: dict) -> list:
    """Extract tweet result objects from GraphQL or legacy v1 JSON structure."""
    # GraphQL format (current Twitter/X API)
    try:
        instructions = data["data"]["bookmark_timeline_v2"]["timeline"]["instructions"]
        items = []
        for instruction in instructions:
            for entry in instruction.get("entries", []):
                result = (
                    entry.get("content", {})
                    .get("itemContent", {})
                    .get("tweet_results", {})
                    .get("result", {})
                )
                result = unwrap_result(result)
                if result.get("__typename") == "Tweet":
                    items.append(result)
        if items:
            return items
    except (KeyError, TypeError):
        pass

    # Legacy v1 format
    tweets = data.get("globalObjects", {}).get("tweets", {})
    users = data.get("globalObjects", {}).get("users", {})
    if tweets:
        items = []
        for tweet in tweets.values():
            user_id = tweet.get("user_id_str", "")
            tweet["_v1_user"] = users.get(user_id, {})
            items.append(tweet)
        return items

    return []


def extract_bookmark_data(item: dict) -> dict:
    """Extract all fields from a tweet result (GraphQL or legacy v1)."""
    legacy = item.get("legacy", {})
    user_result = item.get("core", {}).get("user_results", {}).get("result", {})

    # Legacy v1 fallback
    if not user_result:
        user_result = {"legacy": item.get("_v1_user", {})}

    screen_name = get_screen_name(user_result)
    display_name = get_display_name(user_result)
    id_str = legacy.get("id_str") or item.get("rest_id") or item.get("id_str", "")
    tweet_url = f"https://x.com/{screen_name}/status/{id_str}" if id_str else ""
    saved_at = parse_created_at(legacy.get("created_at", ""))

    full_text, content_type = extract_tweet_text(item)
    media = extract_media_urls(item)
    quoted = extract_quoted_tweet(item)

    # Title: first non-empty line, cap at 100 chars
    first_line = next((l.strip() for l in full_text.splitlines() if l.strip()), "")
    if len(first_line) > 100:
        title = first_line[:100] + "..."
    else:
        title = first_line or "Untitled"

    # Stats
    stats = {
        "likes": legacy.get("favorite_count", 0),
        "retweets": legacy.get("retweet_count", 0),
        "replies": legacy.get("reply_count", 0),
        "bookmarks": legacy.get("bookmark_count", 0),
        "views": item.get("views", {}).get("count", ""),
    }

    return {
        "title": title,
        "url": tweet_url,
        "author": screen_name,
        "display_name": display_name,
        "saved_at": saved_at,
        "content_type": content_type,
        "content": full_text,
        "media": media,
        "quoted": quoted,
        "stats": stats,
    }


def bookmark_to_markdown(b: dict) -> str:
    """Convert bookmark data to Markdown string."""
    # Escape quotes in title for YAML
    safe_title = b["title"].replace('"', '\\"')
    lines = [
        "---",
        f'title: "{safe_title}"',
        f'url: "{b["url"]}"',
        f'author: "@{b["author"]}"',
        f'saved_at: "{b["saved_at"]}"',
        f'type: "{b["content_type"]}"',
        "---",
        "",
        f"# {b['title']}",
        "",
    ]

    # Metadata block
    meta = [f"**Author:** {b['display_name']} (@{b['author']})  "]
    meta.append(f"**Date:** {b['saved_at']}  ")
    meta.append(f"**URL:** {b['url']}  ")
    stats = b["stats"]
    stat_parts = []
    if stats.get("likes"):
        stat_parts.append(f"❤️ {stats['likes']}")
    if stats.get("retweets"):
        stat_parts.append(f"🔁 {stats['retweets']}")
    if stats.get("replies"):
        stat_parts.append(f"💬 {stats['replies']}")
    if stats.get("bookmarks"):
        stat_parts.append(f"🔖 {stats['bookmarks']}")
    if stats.get("views"):
        stat_parts.append(f"👁 {stats['views']}")
    if stat_parts:
        meta.append(f"**Stats:** {' · '.join(stat_parts)}  ")
    lines.extend(meta)
    lines.append("")

    # Main content
    lines.append(b["content"])

    # Media
    if b["media"]:
        lines.append("")
        for kind, url in b["media"]:
            if url:
                if kind == "image":
                    lines.append(f"![image]({url})")
                elif kind == "video":
                    lines.append(f"[Video]({url})")
                elif kind == "thumbnail":
                    lines.append(f"![thumbnail]({url})")

    # Quoted tweet
    if b["quoted"]:
        q = b["quoted"]
        lines.append("")
        lines.append("> **Quoted tweet** by @" + q["author"])
        if q["url"]:
            lines.append(f"> {q['url']}")
        for qline in q["text"].splitlines():
            lines.append(f"> {qline}")

    lines.append("")
    return "\n".join(lines)


def load_all_json_objects(filepath: Path) -> list:
    """Load one or more concatenated JSON objects from a file."""
    objects = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    decoder = json.JSONDecoder()
    pos = 0
    content = content.strip()
    while pos < len(content):
        while pos < len(content) and content[pos] in " \t\n\r":
            pos += 1
        if pos >= len(content):
            break
        obj, pos = decoder.raw_decode(content, pos)
        objects.append(obj)
    return objects


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        pages = load_all_json_objects(BOOKMARKS_FILE)
    except FileNotFoundError:
        print(f"❌ bookmarks.json not found at {BOOKMARKS_FILE}. Export from browser first.")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in bookmarks.json: {e}")
        return

    print(f"Loaded {len(pages)} page(s) from bookmarks.json")
    items = []
    for page in pages:
        items.extend(extract_tweet_entries(page))
    if not items:
        print("❌ No bookmarks found. Check that bookmarks.json matches the expected format.")
        return

    print(f"Processing {len(items)} bookmarks...")

    exported = 0
    for i, item in enumerate(items, 1):
        try:
            bookmark = extract_bookmark_data(item)
            filename = f"{i:04d}-{slugify(bookmark['title'])}.md"
            filepath = OUT_DIR / filename
            filepath.write_text(bookmark_to_markdown(bookmark), encoding="utf-8")
            print(f"  Created: {filename}")
            exported += 1
        except Exception as e:
            print(f"  ⚠️  Skipped item {i}: {e}")

    print(f"\n✅ Exported {exported}/{len(items)} bookmarks to {OUT_DIR}")


if __name__ == "__main__":
    main()
