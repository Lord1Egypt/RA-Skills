#!/usr/bin/env python3
"""
YouTube Comment Moderator — main pipeline.
Fetches new comments, classifies with Gemini Flash, takes action via OAuth.
All state persisted in SQLite.

Usage:
  # Moderate a specific video (dry run)
  python3 scripts/moderate.py --video-id VIDEO_ID --dry-run

  # Moderate a channel's recent videos
  python3 scripts/moderate.py --channel-id UC... --max-videos 5

  # Full auto on configured channel
  python3 scripts/moderate.py

  # Show stats
  python3 scripts/moderate.py --stats

  # Show approval queue
  python3 scripts/moderate.py --queue
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError

# Sibling imports
sys.path.insert(0, os.path.dirname(__file__))
from db import (
    get_db, init_db, upsert_comment, mark_classified, log_action,
    update_action, get_pending_actions, get_stats, is_known,
    save_channel, update_last_check, upsert_video, mark_video_scanned,
    get_scanned_videos
)

API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
BASE_URL = "https://www.googleapis.com/youtube/v3"
OAUTH_PATH = os.environ.get("YT_MOD_OAUTH", "skills/youtube-comment-moderator/oauth.json")
CONFIG_PATH = os.environ.get("YT_MOD_CONFIG", "skills/youtube-comment-moderator/config.json")

CLIENT_ID = os.environ.get("YT_MOD_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("YT_MOD_CLIENT_SECRET", "")


# ── YouTube API helpers ──────────────────────────────────────────────

def yt_get(endpoint, params):
    params["key"] = API_KEY
    url = f"{BASE_URL}/{endpoint}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "YT-Moderator/2.0"})
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        print(f"  API error {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        return None


def get_oauth_token():
    """Load, test, and refresh OAuth token."""
    if not os.path.exists(OAUTH_PATH):
        return None
    with open(OAUTH_PATH) as f:
        oauth = json.load(f)

    token = oauth.get("access_token")
    if not token:
        return None

    # Quick validity check
    req = Request(
        f"{BASE_URL}/channels?part=id&mine=true",
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urlopen(req, timeout=10):
            return token
    except HTTPError:
        pass

    # Refresh
    refresh = oauth.get("refresh_token")
    if not refresh:
        return None
    data = urlencode({
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "refresh_token": refresh, "grant_type": "refresh_token"
    }).encode()
    req = Request(
        "https://oauth2.googleapis.com/token", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urlopen(req, timeout=15) as resp:
            tokens = json.loads(resp.read())
        oauth["access_token"] = tokens["access_token"]
        with open(OAUTH_PATH, "w") as f:
            json.dump(oauth, f, indent=2)
        return tokens["access_token"]
    except Exception as e:
        print(f"  OAuth refresh failed: {e}", file=sys.stderr)
        return None


def yt_post_oauth(endpoint, body, token):
    url = f"{BASE_URL}/{endpoint}"
    req = Request(url, data=json.dumps(body).encode(), headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        print(f"  OAuth error {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        return None


def yt_set_moderation(comment_id, status, token):
    """Set moderation status: published, heldForReview, rejected."""
    url = f"{BASE_URL}/comments/setModerationStatus?{urlencode({'id': comment_id, 'moderationStatus': status})}"
    req = Request(url, method="POST", headers={"Authorization": f"Bearer {token}"})
    try:
        with urlopen(req, timeout=15):
            return True
    except HTTPError as e:
        print(f"  Moderation error {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        return False


# ── Fetch ────────────────────────────────────────────────────────────

def get_channel_videos(channel_id, max_videos=10):
    data = yt_get("channels", {"part": "contentDetails,statistics", "id": channel_id})
    if not data or not data.get("items"):
        return []
    uploads = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    total_vids = int(data["items"][0].get("statistics", {}).get("videoCount", 0))
    if max_videos == -1:
        max_videos = max(total_vids, 500)  # -1 = all videos
        print(f"  Fetching all {total_vids} videos...")
    videos, page_token = [], None
    while len(videos) < max_videos:
        params = {"part": "snippet", "playlistId": uploads,
                  "maxResults": min(50, max_videos - len(videos))}
        if page_token:
            params["pageToken"] = page_token
        data = yt_get("playlistItems", params)
        if not data or not data.get("items"):
            break
        for item in data["items"]:
            videos.append({
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"]["title"],
                "published_at": item["snippet"].get("publishedAt")
            })
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return videos[:max_videos] if max_videos > 0 else videos


def get_channel_owner_id(video_id):
    data = yt_get("videos", {"part": "snippet", "id": video_id})
    if data and data.get("items"):
        return data["items"][0]["snippet"]["channelId"]
    return None


def fetch_comments(video_id, max_comments=200):
    comments, page_token = [], None
    while len(comments) < max_comments:
        params = {
            "part": "snippet", "videoId": video_id,
            "maxResults": min(100, max_comments - len(comments)),
            "order": "time", "textFormat": "plainText"
        }
        if page_token:
            params["pageToken"] = page_token
        data = yt_get("commentThreads", params)
        if not data or "items" not in data:
            break
        for item in data["items"]:
            s = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "video_id": video_id,
                "author": s["authorDisplayName"],
                "author_channel_id": s.get("authorChannelId", {}).get("value", ""),
                "text": s["textDisplay"],
                "like_count": s["likeCount"],
                "reply_count": item["snippet"]["totalReplyCount"],
                "published_at": s["publishedAt"],
            })
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return comments[:max_comments]


# ── Classify ─────────────────────────────────────────────────────────

def classify_batch(comments, channel_name="", batch_size=50):
    """Classify comments with Gemini Flash. Returns {comment_id: {category, confidence}}."""
    if not comments:
        return {}

    results = {}
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i + batch_size]
        lines = "\n".join(
            f'{j+1}. [id:{c["comment_id"]}] [{c["author"]}] (likes:{c["like_count"]}) {c["text"][:400]}'
            for j, c in enumerate(batch)
        )

        prompt = f"""Classify each YouTube comment on {channel_name}'s channel into exactly one category:
spam, question, praise, hate, neutral, constructive.

Rules:
- spam: promotional links, scam offers, bot-like text, crypto/forex schemes, coordinated spam (same phrase across users), self-promo
- question: genuine question about video content, creator, or topic
- praise: positive feedback, compliments, encouragement
- hate: hateful, abusive, harassing, threatening, or low-effort attacks on creator
- neutral: generic reactions, timestamps, observations, personal anecdotes
- constructive: thoughtful criticism, corrections, experience-based feedback with substance

Return ONLY a JSON array: [{{"index": 1, "category": "...", "confidence": 85}}]

Comments:
{lines}"""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
        body = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
        })
        req = Request(url, data=body.encode(), headers={"Content-Type": "application/json"})

        try:
            with urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            classifications = json.loads(text)

            for c in classifications:
                idx = c["index"] - 1
                if 0 <= idx < len(batch):
                    cid = batch[idx]["comment_id"]
                    results[cid] = {
                        "category": c["category"],
                        "confidence": c.get("confidence", 80)
                    }
        except Exception as e:
            print(f"  Classification error (batch {i//batch_size+1}): {e}", file=sys.stderr)

        if i + batch_size < len(comments):
            time.sleep(1)

    return results


# ── Reply drafting ───────────────────────────────────────────────────

THANK_OPTIONS = [
    "Thank you! Really appreciate that.",
    "Thanks so much! Glad you enjoyed it.",
    "Appreciate the kind words!",
    "Thank you! More coming soon.",
    "That means a lot, thank you!",
]


def draft_reply(comment, category, config):
    """Draft a reply. Simple templates for praise, Gemini for questions."""
    if category == "praise":
        idx = int(hashlib.md5(comment["comment_id"].encode()).hexdigest(), 16) % len(THANK_OPTIONS)
        return THANK_OPTIONS[idx]

    if category != "question":
        return None

    voice = config.get("voice_style", "friendly, casual, helpful")
    faq = config.get("faq", [])
    faq_text = "\n".join(f"Q: {f['q']}\nA: {f['a']}" for f in faq) if faq else "No FAQ."

    prompt = f"""Reply to a YouTube comment as the channel owner.
Voice: {voice}
Channel: {config.get('channel_name', '')}

FAQ:
{faq_text}

Comment by @{comment['author']}:
"{comment['text']}"

Short reply (1-3 sentences). If unsure, say "Great question! I'll cover that soon." Match the voice.
Reply:"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 200}
    })
    req = Request(url, data=body.encode(), headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"].strip().strip('"')
    except Exception as e:
        print(f"  Reply draft error: {e}", file=sys.stderr)
        return None


# ── Action execution ─────────────────────────────────────────────────

CATEGORY_ACTION_MAP = {
    "spam": "delete",
    "hate": "delete",
    "question": "reply",
    "praise": "thank",
    "constructive": "flag_review",
    "neutral": "skip",
}


def execute_actions(conn, comments_with_class, config, token, dry_run=False):
    """Execute moderation actions. Returns summary dict."""
    mode = config.get("mode", "approval")
    results = {"replied": 0, "deleted": 0, "flagged": 0, "drafted": 0, "skipped": 0, "errors": 0}
    report = []

    for comment, cls_info in comments_with_class:
        cid = comment["comment_id"]
        category = cls_info["category"]
        confidence = cls_info.get("confidence", 80)
        intended = CATEGORY_ACTION_MAP.get(category, "skip")

        reply_text = None
        if intended in ("reply", "thank"):
            reply_text = draft_reply(comment, category, config)

        # Store classification
        action_label = "pending"

        if intended == "delete":
            if mode == "auto" and not dry_run and token:
                if config.get("auto_delete_spam", True):
                    ok = yt_set_moderation(cid, "rejected", token)
                    action_label = "deleted" if ok else "delete_failed"
                    log_action(conn, cid, action_label, success=ok,
                              error=None if ok else "API call failed")
                    results["deleted" if ok else "errors"] += 1
                else:
                    action_label = "flagged_for_review"
                    results["flagged"] += 1
            else:
                action_label = "flagged_for_review" if not dry_run else "would_delete"
                results["flagged" if not dry_run else "skipped"] += 1

        elif intended in ("reply", "thank") and reply_text:
            if mode == "auto" and not dry_run and token:
                resp = yt_post_oauth("comments?part=snippet", {
                    "snippet": {"parentId": cid, "textOriginal": reply_text}
                }, token)
                action_label = "replied" if resp else "reply_failed"
                log_action(conn, cid, action_label, detail=reply_text,
                          success=resp is not None,
                          error=None if resp else "API call failed")
                results["replied" if resp else "errors"] += 1
            else:
                action_label = "reply_drafted"
                results["drafted"] += 1

        elif intended == "flag_review":
            action_label = "flagged_for_review"
            results["flagged"] += 1

        else:
            action_label = "skipped"
            results["skipped"] += 1

        mark_classified(conn, cid, category, confidence, action_label, reply_text)

        icon = {"spam": "🗑", "question": "❓", "praise": "👍", "hate": "🚫",
                "neutral": "➖", "constructive": "🔧"}.get(category, "?")
        line = f"  {icon} [{category}] @{comment['author']}: {comment['text'][:100]}"
        if action_label not in ("skipped", "pending"):
            line += f" → {action_label}"
        if reply_text and action_label in ("replied", "reply_drafted"):
            line += f'\n    💬 "{reply_text[:120]}"'
        report.append(line)

    conn.commit()
    return results, report


# ── Commands ─────────────────────────────────────────────────────────

def cmd_moderate(args, config):
    """Main moderation pipeline."""
    conn = get_db()
    init_db(conn)

    channel_id = args.channel_id or config.get("channel_id", "")
    if not channel_id and not args.video_id:
        print("Error: provide --video-id or --channel-id (or set in config)", file=sys.stderr)
        sys.exit(1)

    # OAuth
    token = None
    if not args.dry_run:
        token = get_oauth_token()
        if not token:
            print("Warning: no OAuth token, running dry-run", file=sys.stderr)
            args.dry_run = True

    # Collect videos
    if args.video_id:
        videos = [{"video_id": args.video_id, "title": args.video_id}]
    else:
        max_v = -1 if args.all_videos else args.max_videos
        videos = get_channel_videos(channel_id, max_v)
        # Skip already fully-scanned videos when doing --all-videos
        if args.all_videos:
            scanned = get_scanned_videos(conn, channel_id)
            before = len(videos)
            videos = [v for v in videos if v["video_id"] not in scanned]
            if before != len(videos):
                print(f"  Skipping {before - len(videos)} already-scanned videos")
        print(f"Processing {len(videos)} videos")

    if not videos:
        print("No videos to process")
        return

    # Get owner ID for whitelisting
    owner_ids = set()
    owner_id = get_channel_owner_id(videos[0]["video_id"])
    if owner_id:
        owner_ids.add(owner_id)

    # Fetch comments, insert into DB, collect new ones
    new_comments = []
    for vi, video in enumerate(videos):
        vid = video["video_id"]
        # Track video in DB
        upsert_video(conn, vid, channel_id or vid,
                     title=video.get("title"),
                     published_at=video.get("published_at"))

        comments = fetch_comments(vid, args.max_comments)
        new_in_video = 0
        for c in comments:
            # Skip owner comments
            if c.get("author_channel_id") in owner_ids:
                cid_channel = channel_id or vid
                upsert_comment(conn, c, cid_channel)
                mark_classified(conn, c["comment_id"], "owner", 100, "skipped")
                continue
            ch = channel_id or vid
            is_new = upsert_comment(conn, c, ch)
            if is_new:
                new_comments.append(c)
                new_in_video += 1
        if new_in_video:
            print(f"  {video['title'][:60]} -- {new_in_video} new / {len(comments)} total")

        # Mark video as fully scanned
        mark_video_scanned(conn, vid)

        if (vi + 1) % 10 == 0:
            conn.commit()
            print(f"  ... {vi+1}/{len(videos)} videos processed")
    conn.commit()

    if not new_comments:
        stats = get_stats(conn, channel_id)
        print(f"\nNo new comments. ({stats['total']} tracked)")
        update_last_check(conn, channel_id) if channel_id else None
        conn.commit()
        conn.close()
        return

    print(f"\n{len(new_comments)} new comments to classify")

    # Classify
    channel_name = config.get("channel_name", "")
    classifications = classify_batch(new_comments, channel_name)

    # Pair comments with classifications
    paired = []
    for c in new_comments:
        cls_info = classifications.get(c["comment_id"], {"category": "neutral", "confidence": 50})
        paired.append((c, cls_info))

    # Execute
    results, report = execute_actions(conn, paired, config, token, args.dry_run)

    if channel_id:
        update_last_check(conn, channel_id)
        conn.commit()

    # Print report
    mode_label = "DRY RUN" if args.dry_run else config.get("mode", "approval").upper()
    print(f"\n{'='*60}")
    print(f"  Moderation Report ({mode_label})")
    print(f"{'='*60}")
    print(f"  New: {len(new_comments)}  Replied: {results['replied']}  Drafted: {results['drafted']}  Deleted: {results['deleted']}  Flagged: {results['flagged']}  Skipped: {results['skipped']}")
    print(f"{'='*60}\n")
    for line in report:
        print(line)

    conn.close()


def cmd_stats(args, config):
    """Show moderation stats."""
    conn = get_db()
    init_db(conn)
    channel_id = args.channel_id or config.get("channel_id")
    stats = get_stats(conn, channel_id)
    # Fall back to unfiltered if channel filter returns nothing
    if stats["total"] == 0 and channel_id:
        stats = get_stats(conn)

    print(f"\n{'='*40}")
    print(f"  Moderation Stats")
    print(f"{'='*40}")
    print(f"  Total comments: {stats['total']}")
    print(f"  Classified: {stats['classified']}")
    print(f"\n  By classification:")
    for k, v in sorted(stats["by_classification"].items(), key=lambda x: -x[1]):
        print(f"    {k:15s}: {v}")
    print(f"\n  By action:")
    for k, v in sorted(stats["by_action"].items(), key=lambda x: -x[1]):
        print(f"    {k:15s}: {v}")
    conn.close()


def cmd_queue(args, config):
    """Show pending approval queue."""
    conn = get_db()
    init_db(conn)
    channel_id = args.channel_id or config.get("channel_id")
    pending = get_pending_actions(conn, channel_id)

    if not pending:
        print("Approval queue is empty.")
        conn.close()
        return

    print(f"\n{len(pending)} items pending:\n")
    for row in pending:
        icon = {"spam": "🗑", "question": "❓", "praise": "👍", "hate": "🚫",
                "constructive": "🔧"}.get(row["classification"], "?")
        print(f"  {icon} [{row['classification']}] @{row['author']}: {row['text'][:100]}")
        print(f"    Action: {row['action']}  ID: {row['comment_id']}")
        if row["reply_draft"]:
            print(f'    Draft: "{row["reply_draft"][:120]}"')
        print()
    conn.close()


def cmd_approve(args, config):
    """Approve and execute all pending items (or specific comment_id)."""
    conn = get_db()
    init_db(conn)

    token = get_oauth_token()
    if not token:
        print("Error: OAuth required for approvals", file=sys.stderr)
        sys.exit(1)

    channel_id = args.channel_id or config.get("channel_id")
    pending = get_pending_actions(conn, channel_id)

    if args.comment_id:
        pending = [r for r in pending if r["comment_id"] == args.comment_id]

    if not pending:
        print("Nothing to approve.")
        conn.close()
        return

    approved = 0
    for row in pending:
        cid = row["comment_id"]
        if row["action"] == "reply_drafted" and row["reply_draft"]:
            resp = yt_post_oauth("comments?part=snippet", {
                "snippet": {"parentId": cid, "textOriginal": row["reply_draft"]}
            }, token)
            if resp:
                update_action(conn, cid, "replied", row["reply_draft"])
                log_action(conn, cid, "replied", detail=row["reply_draft"])
                print(f"  ✅ Replied to @{row['author']}")
                approved += 1
            else:
                print(f"  ❌ Failed to reply to {cid}")

        elif row["action"] == "flagged_for_review" and row["classification"] in ("spam", "hate"):
            ok = yt_set_moderation(cid, "rejected", token)
            if ok:
                update_action(conn, cid, "deleted")
                log_action(conn, cid, "deleted")
                print(f"  ✅ Deleted @{row['author']}'s {row['classification']}")
                approved += 1
            else:
                print(f"  ❌ Failed to delete {cid}")

        elif row["action"] == "flagged_for_review":
            # Constructive: mark as reviewed
            update_action(conn, cid, "reviewed")
            log_action(conn, cid, "reviewed")
            print(f"  ✅ Marked reviewed: @{row['author']}")
            approved += 1

    conn.commit()
    conn.close()
    print(f"\nApproved {approved}/{len(pending)} items")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="YouTube Comment Moderator")
    parser.add_argument("--video-id", help="Moderate a specific video")
    parser.add_argument("--channel-id", help="Channel ID to moderate")
    parser.add_argument("--max-videos", type=int, default=5)
    parser.add_argument("--all-videos", action="store_true", help="Process all videos in channel")
    parser.add_argument("--max-comments", type=int, default=200)
    parser.add_argument("--dry-run", action="store_true", help="Classify only, no writes")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--queue", action="store_true", help="Show approval queue")
    parser.add_argument("--approve", action="store_true", help="Approve pending items")
    parser.add_argument("--comment-id", help="Approve specific comment")
    parser.add_argument("--config", default=CONFIG_PATH)
    args = parser.parse_args()

    if not API_KEY:
        print("Error: YOUTUBE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Load config (optional, for channel defaults)
    config = {}
    cfg_path = args.config
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            config = json.load(f)

    if args.stats:
        cmd_stats(args, config)
    elif args.queue:
        cmd_queue(args, config)
    elif args.approve:
        cmd_approve(args, config)
    else:
        if not GEMINI_KEY:
            print("Error: GEMINI_API_KEY not set", file=sys.stderr)
            sys.exit(1)
        cmd_moderate(args, config)


if __name__ == "__main__":
    main()
