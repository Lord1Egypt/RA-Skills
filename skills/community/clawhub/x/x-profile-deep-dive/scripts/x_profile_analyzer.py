#!/usr/bin/env python3
"""
x_profile_analyzer.py — Deep-analyze an X/Twitter user profile using tweety-ns.

Usage:
    python3 x_profile_analyzer.py --handle karpathy --cookies cookies.json
    python3 x_profile_analyzer.py --handle dotey --tweet-pages 3 --output out.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse

from tweety_utils import (
    load_cookies_file,
    create_app,
    login_app,
    _flatten_tweets,
    _safe_int,
    _safe_str,
    _iso,
    DEFAULT_COOKIES_PATH,
    DEFAULT_SESSION_DIR,
)


def log(msg, quiet=False):
    if not quiet:
        sys.stderr.write(f"[x_profile_analyzer] {msg}\n")


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

def _extract_location(loc):
    if loc is None:
        return ""
    if isinstance(loc, str):
        return loc
    if isinstance(loc, dict):
        return loc.get("location", str(loc))
    if hasattr(loc, "location"):
        return str(loc.location)
    return str(loc)


def extract_profile(user):
    return {
        "username": _safe_str(getattr(user, "username", "")),
        "name": _safe_str(getattr(user, "name", "")),
        "bio": _safe_str(getattr(user, "description", "")),
        "location": _extract_location(getattr(user, "location", "")),
        "website": _safe_str(getattr(user, "profile_url", "")),
        "created_at": _iso(getattr(user, "created_at", None)),
        "followers_count": _safe_int(getattr(user, "followers_count", 0)),
        "following_count": _safe_int(getattr(user, "friends_count", 0)),
        "tweet_count": _safe_int(getattr(user, "statuses_count", 0)),
        "verified": bool(getattr(user, "verified", False)),
        "profile_image_url": _safe_str(getattr(user, "profile_image_url", "")),
    }


def extract_tweet(t):
    # URLs
    urls = []
    if hasattr(t, "urls") and t.urls:
        for u in t.urls:
            url_str = u.url if hasattr(u, "url") else str(u)
            if url_str:
                urls.append(url_str)

    # Hashtags
    hashtags = []
    if hasattr(t, "hashtags") and t.hashtags:
        for h in t.hashtags:
            tag = h.text if hasattr(h, "text") else str(h)
            if tag:
                hashtags.append(tag)

    # Mentions
    mentions = []
    if hasattr(t, "user_mentions") and t.user_mentions:
        for m in t.user_mentions:
            screen_name = getattr(m, "screen_name", None) or getattr(m, "username", None)
            if screen_name:
                mentions.append(f"@{screen_name}")
    if not mentions:
        # Fallback: extract from text
        text = t.text or ""
        mentions = re.findall(r"@(\w+)", text)
        mentions = [f"@{m}" for m in mentions]

    return {
        "id": str(t.id) if t.id else "",
        "text": t.text or "",
        "created_at": _iso(getattr(t, "created_on", None)),
        "likes": _safe_int(t.likes),
        "retweets": _safe_int(t.retweet_counts),
        "replies": _safe_int(t.reply_counts),
        "views": _safe_int(t.views),
        "is_retweet": bool(getattr(t, "is_retweet", False)),
        "is_quote": bool(getattr(t, "is_quoted", False)),
        "is_reply": bool(getattr(t, "is_reply", False)),
        "has_media": bool(t.media) if hasattr(t, "media") else False,
        "urls": urls,
        "url": str(t.url) if hasattr(t, "url") and t.url else "",
        "hashtags": hashtags,
        "mentions": mentions,
    }


def compute_tweet_stats(tweets_data):
    """Compute aggregate statistics from extracted tweet dicts."""
    total = len(tweets_data)
    if total == 0:
        return {
            "total_fetched": 0,
            "original_count": 0,
            "retweet_count": 0,
            "reply_count": 0,
            "avg_likes": 0,
            "avg_retweets": 0,
            "avg_replies": 0,
            "avg_views": 0,
            "top_tweet_id": "",
            "earliest_date": "",
            "latest_date": "",
            "tweets_per_day": 0,
            "top_hashtags": [],
            "top_mentions": [],
            "top_urls_domains": [],
            "engagement_trend": "stable",
        }

    retweet_count = sum(1 for t in tweets_data if t["is_retweet"])
    reply_count = sum(1 for t in tweets_data if t["is_reply"])
    original_count = total - retweet_count - reply_count

    total_likes = sum(t["likes"] for t in tweets_data)
    total_retweets = sum(t["retweets"] for t in tweets_data)
    total_replies = sum(t["replies"] for t in tweets_data)
    total_views = sum(t["views"] for t in tweets_data)

    avg_likes = round(total_likes / total, 1)
    avg_retweets = round(total_retweets / total, 1)
    avg_replies = round(total_replies / total, 1)
    avg_views = round(total_views / total, 1)

    # Top tweet by engagement (likes + retweets)
    top_tweet = max(tweets_data, key=lambda t: t["likes"] + t["retweets"])

    # Date range
    dates = []
    for t in tweets_data:
        if t["created_at"]:
            try:
                dates.append(datetime.fromisoformat(t["created_at"]))
            except (ValueError, TypeError):
                pass

    earliest_date = ""
    latest_date = ""
    tweets_per_day = 0.0
    if dates:
        dates.sort()
        earliest_date = dates[0].isoformat()
        latest_date = dates[-1].isoformat()
        span_days = (dates[-1] - dates[0]).total_seconds() / 86400
        if span_days > 0:
            tweets_per_day = round(total / span_days, 1)

    # Top hashtags
    hashtag_counter = Counter()
    for t in tweets_data:
        for h in t["hashtags"]:
            hashtag_counter[h] += 1
    top_hashtags = hashtag_counter.most_common(10)

    # Top mentions
    mention_counter = Counter()
    for t in tweets_data:
        for m in t["mentions"]:
            mention_counter[m] += 1
    top_mentions = mention_counter.most_common(10)

    # Top URL domains
    domain_counter = Counter()
    for t in tweets_data:
        for url in t["urls"]:
            try:
                domain = urlparse(url).netloc
                # Skip t.co links
                if domain and domain != "t.co":
                    domain_counter[domain] += 1
            except Exception:
                pass
    top_urls_domains = domain_counter.most_common(10)

    # Engagement trend: compare first half vs second half
    engagement_trend = "stable"
    if total >= 4:
        mid = total // 2
        # Tweets are typically newest-first, so first half = newer tweets
        first_half = tweets_data[:mid]
        second_half = tweets_data[mid:]
        eng_first = sum(t["likes"] + t["retweets"] for t in first_half) / len(first_half)
        eng_second = sum(t["likes"] + t["retweets"] for t in second_half) / len(second_half)
        if eng_second > 0:
            ratio = eng_first / eng_second
            if ratio > 1.3:
                engagement_trend = "rising"
            elif ratio < 0.7:
                engagement_trend = "declining"

    return {
        "total_fetched": total,
        "original_count": original_count,
        "retweet_count": retweet_count,
        "reply_count": reply_count,
        "avg_likes": avg_likes,
        "avg_retweets": avg_retweets,
        "avg_replies": avg_replies,
        "avg_views": avg_views,
        "top_tweet_id": top_tweet["id"],
        "earliest_date": earliest_date,
        "latest_date": latest_date,
        "tweets_per_day": tweets_per_day,
        "top_hashtags": top_hashtags,
        "top_mentions": top_mentions,
        "top_urls_domains": top_urls_domains,
        "engagement_trend": engagement_trend,
    }


def extract_following(user):
    return {
        "username": _safe_str(getattr(user, "username", "")),
        "name": _safe_str(getattr(user, "name", "")),
        "followers_count": _safe_int(getattr(user, "followers_count", 0)),
        "bio_snippet": _safe_str(getattr(user, "description", ""))[:100],
    }


def extract_follower(user):
    return {
        "username": _safe_str(getattr(user, "username", "")),
        "name": _safe_str(getattr(user, "name", "")),
        "followers_count": _safe_int(getattr(user, "followers_count", 0)),
    }


def compute_followings_stats(followings_data):
    total = len(followings_data)
    if total == 0:
        return {
            "total_fetched": 0,
            "avg_followers": 0,
            "categories_hint": [],
        }

    avg_followers = round(sum(f["followers_count"] for f in followings_data) / total)

    # Simple category inference from bio snippets
    category_keywords = {
        "AI researchers": ["AI", "machine learning", "deep learning", "neural", "NLP", "ML", "research"],
        "tech founders": ["founder", "CEO", "co-founder", "startup", "entrepreneur"],
        "engineers": ["engineer", "developer", "programming", "software", "code", "dev"],
        "journalists": ["journalist", "reporter", "editor", "news", "writer"],
        "investors": ["investor", "VC", "venture", "capital", "fund"],
        "crypto": ["crypto", "bitcoin", "web3", "blockchain", "defi"],
        "scientists": ["professor", "PhD", "scientist", "university", "academic"],
        "designers": ["design", "UX", "UI", "creative"],
    }

    category_counts = Counter()
    for f in followings_data:
        bio = f.get("bio_snippet", "").lower()
        for cat, keywords in category_keywords.items():
            if any(kw.lower() in bio for kw in keywords):
                category_counts[cat] += 1

    categories_hint = [cat for cat, _ in category_counts.most_common(5) if category_counts[cat] >= 2]

    return {
        "total_fetched": total,
        "avg_followers": avg_followers,
        "categories_hint": categories_hint,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Deep-analyze an X/Twitter user profile")
    parser.add_argument("--handle", required=True, help="Twitter username to analyze")
    parser.add_argument(
        "--cookies",
        default=os.path.expanduser(DEFAULT_COOKIES_PATH),
        help="Cookie file path",
    )
    parser.add_argument(
        "--session-dir",
        default=os.path.expanduser(DEFAULT_SESSION_DIR),
        help="tweety session directory",
    )
    parser.add_argument("--tweet-pages", type=int, default=2, help="Number of tweet pages to fetch (each ~20 tweets)")
    parser.add_argument("--following-pages", type=int, default=1, help="Number of following pages (each ~70 users)")
    parser.add_argument("--follower-pages", type=int, default=1, help="Number of follower pages (each ~70 users)")
    parser.add_argument("--output", default=None, help="Output JSON file path (default: stdout)")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages on stderr")
    args = parser.parse_args()

    handle = args.handle.lstrip("@")
    quiet = args.quiet

    # Load cookies
    log(f"Loading cookies from {args.cookies}", quiet)
    cookies_dict = load_cookies_file(args.cookies)

    # Create app and login
    log("Creating session and logging in...", quiet)
    app = create_app(args.session_dir)
    login_app(app, cookies_dict)
    log("Login successful", quiet)

    # 1. Fetch user profile
    log(f"Fetching profile for @{handle}...", quiet)
    try:
        user_info = app.get_user_info(handle)
    except Exception as e:
        err_str = str(e).lower()
        if "not found" in err_str or "does not exist" in err_str or "suspend" in err_str:
            sys.stderr.write(f"Error: user @{handle} not found: {e}\n")
            sys.exit(3)
        raise
    profile = extract_profile(user_info)
    log(f"Profile fetched: {profile['name']} (@{profile['username']})", quiet)

    # 2. Fetch tweets
    log(f"Fetching tweets (pages={args.tweet_pages})...", quiet)
    tweets_data = []
    try:
        raw_tweets = app.get_tweets(handle, pages=args.tweet_pages, wait_time=2)
        flat = _flatten_tweets(list(raw_tweets))
        tweets_data = [extract_tweet(t) for t in flat]
        log(f"Fetched {len(tweets_data)} tweets", quiet)
    except Exception as e:
        sys.stderr.write(f"Warning: error fetching tweets: {e}\n")

    tweet_stats = compute_tweet_stats(tweets_data)

    # Compute data range days
    data_range_days = 0
    if tweet_stats["earliest_date"] and tweet_stats["latest_date"]:
        try:
            d1 = datetime.fromisoformat(tweet_stats["earliest_date"])
            d2 = datetime.fromisoformat(tweet_stats["latest_date"])
            data_range_days = round((d2 - d1).total_seconds() / 86400, 1)
        except Exception:
            pass

    # 3. Fetch followings
    log(f"Fetching followings (pages={args.following_pages})...", quiet)
    followings_data = []
    try:
        raw_followings = app.get_user_followings(handle, pages=args.following_pages, wait_time=2)
        followings_data = [extract_following(u) for u in raw_followings]
        log(f"Fetched {len(followings_data)} followings", quiet)
    except Exception as e:
        sys.stderr.write(f"Warning: error fetching followings: {e}\n")

    followings_stats = compute_followings_stats(followings_data)

    # 4. Fetch followers
    log(f"Fetching followers (pages={args.follower_pages})...", quiet)
    followers_sample = []
    try:
        raw_followers = app.get_user_followers(handle, pages=args.follower_pages, wait_time=2)
        followers_sample = [extract_follower(u) for u in raw_followers]
        log(f"Fetched {len(followers_sample)} followers", quiet)
    except Exception as e:
        sys.stderr.write(f"Warning: error fetching followers: {e}\n")

    # 5. Assemble output
    result = {
        "profile": profile,
        "tweets": tweets_data,
        "tweet_stats": tweet_stats,
        "followings": followings_data,
        "followings_stats": followings_stats,
        "followers_sample": followers_sample,
        "metadata": {
            "analyzed_at": datetime.now(timezone.utc).astimezone().isoformat(),
            "script_version": "1.0",
            "tweet_pages_fetched": args.tweet_pages,
            "data_range_days": data_range_days,
        },
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
            f.write("\n")
        log(f"Output written to {args.output}", quiet)
    else:
        print(output_json)

    log("Done.", quiet)


if __name__ == "__main__":
    main()
