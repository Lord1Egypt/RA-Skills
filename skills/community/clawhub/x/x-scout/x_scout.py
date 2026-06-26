#!/usr/bin/env python3
"""
X-Scout -- Twitter/X Intelligence Scraper

Modes:
  --search "query"    Search tweets by keyword
  --profile @handle   Scrape profile posts
  --comments <url>    Pull replies to a tweet
  --intel <url>       Full intel: tweet + video + comments + transcription

Options:
  --limit N           Max results (default: 20)
  --since YYYY-MM-DD  Date filter (default: 180 days ago)
  --no-methods        Skip method detection
  --no-transcribe     Skip video transcription
  --json              Output as JSON
  --timeout N         Scraper timeout in seconds (default: 90)
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency management
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    cmd = [sys.executable, "-m", "pip", "install", "-q", "requests"]
    try:
        subprocess.check_call(cmd + ["--break-system-packages"])
    except subprocess.CalledProcessError:
        subprocess.check_call(cmd)
    import requests

# Load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    # Look for .env in script directory
    _script_dir = Path(__file__).parent
    _env_file = _script_dir / ".env"
    if _env_file.exists():
        load_dotenv(_env_file)
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------
VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Config -- all from environment variables, no hardcoded secrets
# ---------------------------------------------------------------------------

# TwitterAPI.io (primary data source)
TWITTERAPI_BASE = "https://api.twitterapi.io/twitter"
TWITTERAPI_KEY = os.environ.get("TWITTERAPI_KEY", "")

# OpenRouter (Grok classification for method detection)
OPENROUTER_BASE = "https://openrouter.ai/api/v1"
GROK_MODEL = "x-ai/grok-4.1-fast"

# Cerebras (fast query simplification)
CEREBRAS_API_URL = "https://api.cerebras.ai/v1/chat/completions"
CEREBRAS_MODEL = "llama3.1-8b"
CEREBRAS_KEYS = [k.strip() for k in os.environ.get("CEREBRAS_API_KEYS", "").split(",") if k.strip()]
_cerebras_key_idx = 0

# Deepgram (video transcription)
DEEPGRAM_KEY = os.environ.get("DEEPGRAM_API_KEY", "")

# Install ID for analytics
INSTALL_ID = os.environ.get("XS_INSTALL_ID", "")
if not INSTALL_ID:
    # Try config file
    _config_path = Path.home() / ".x-scout" / "config.json"
    if _config_path.exists():
        try:
            INSTALL_ID = json.loads(_config_path.read_text()).get("install_id", "")
        except Exception:
            pass
    if not INSTALL_ID:
        INSTALL_ID = uuid.uuid4().hex[:16]

# Analytics endpoint
ANALYTICS_URL = "https://clawagents.dev/reddit-rank/v1/xs/usage"


# ---------------------------------------------------------------------------
# Analytics: phone-home on every run
# ---------------------------------------------------------------------------
def _report_usage(mode, query=None, results_count=0, error=None):
    """Silent phone-home to track CLI usage. Never blocks, never fails loudly."""
    try:
        requests.post(
            ANALYTICS_URL,
            json={
                "tool": "x-scout",
                "version": VERSION,
                "install_id": INSTALL_ID,
                "mode": mode,
                "query_hash": hashlib.sha256(query.encode()).hexdigest()[:12] if query else None,
                "results": results_count,
                "error": str(error)[:200] if error else None,
                "ts": int(time.time()),
            },
            timeout=3,
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Key helpers
# ---------------------------------------------------------------------------
def get_openrouter_key():
    """Get OpenRouter API key from env."""
    return os.environ.get("OPENROUTER_API_KEY", "") or None


# ---------------------------------------------------------------------------
# TwitterAPI.io: primary data source
# ---------------------------------------------------------------------------
def twitterapi_search(query, limit=20, query_type="Latest", timeout=30):
    """Search tweets via TwitterAPI.io. Returns list of raw tweet dicts or None on error."""
    url = TWITTERAPI_BASE + "/tweet/advanced_search"
    headers = {"X-API-Key": TWITTERAPI_KEY}
    params = {"query": query, "queryType": query_type, "cursor": ""}

    all_tweets = []
    pages = 0
    max_pages = max(1, (limit + 19) // 20)

    while pages < max_pages:
        pages += 1
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        except requests.exceptions.Timeout:
            print("WARN: TwitterAPI.io search timed out", file=sys.stderr)
            break
        except requests.exceptions.ConnectionError as e:
            print("WARN: TwitterAPI.io connection error: {}".format(e), file=sys.stderr)
            break

        if resp.status_code == 401:
            print("WARN: TwitterAPI.io auth failed (401) -- check API key", file=sys.stderr)
            return None
        if resp.status_code != 200:
            print("WARN: TwitterAPI.io returned {}: {}".format(resp.status_code, resp.text[:200]), file=sys.stderr)
            return None

        data = resp.json()
        tweets = data.get("tweets", [])
        if not tweets:
            break

        all_tweets.extend(tweets)
        if len(all_tweets) >= limit:
            break

        next_cursor = data.get("next_cursor")
        if not next_cursor or not data.get("has_next_page"):
            break
        params["cursor"] = next_cursor

    print("TwitterAPI.io: {} tweets from {} page(s)".format(len(all_tweets), pages), file=sys.stderr)
    return all_tweets[:limit] if all_tweets else None


def twitterapi_profile(username, timeout=15):
    """Get user profile via TwitterAPI.io. Returns raw dict or None."""
    url = TWITTERAPI_BASE + "/user/info"
    headers = {"X-API-Key": TWITTERAPI_KEY}
    try:
        resp = requests.get(url, headers=headers, params={"userName": username}, timeout=timeout)
    except Exception as e:
        print("WARN: TwitterAPI.io profile error: {}".format(e), file=sys.stderr)
        return None

    if resp.status_code != 200:
        print("WARN: TwitterAPI.io profile returned {}".format(resp.status_code), file=sys.stderr)
        return None

    return resp.json().get("data", resp.json())


def twitterapi_replies(tweet_id, limit=50, timeout=30):
    """Get replies to a tweet via TwitterAPI.io. Returns list of tweet dicts or None."""
    url = TWITTERAPI_BASE + "/tweet/replies"
    headers = {"X-API-Key": TWITTERAPI_KEY}
    params = {"tweetId": str(tweet_id), "cursor": ""}

    all_replies = []
    pages = 0
    max_pages = max(1, (limit + 19) // 20)

    while pages < max_pages:
        pages += 1
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        except Exception as e:
            print("WARN: TwitterAPI.io replies error: {}".format(e), file=sys.stderr)
            break

        if resp.status_code != 200:
            print("WARN: TwitterAPI.io replies returned {}".format(resp.status_code), file=sys.stderr)
            break

        data = resp.json()
        tweets = data.get("tweets", [])
        if not tweets:
            break

        all_replies.extend(tweets)
        if len(all_replies) >= limit:
            break

        next_cursor = data.get("next_cursor")
        if not next_cursor or not data.get("has_next_page"):
            break
        params["cursor"] = next_cursor

    return all_replies[:limit] if all_replies else None


def twitterapi_get_tweet(tweet_id, timeout=15):
    """Get a single tweet by ID via TwitterAPI.io. Returns raw dict or None."""
    url = TWITTERAPI_BASE + "/tweet/detail"
    headers = {"X-API-Key": TWITTERAPI_KEY}
    try:
        resp = requests.get(url, headers=headers, params={"tweetId": str(tweet_id)}, timeout=timeout)
    except Exception as e:
        print("WARN: TwitterAPI.io tweet detail error: {}".format(e), file=sys.stderr)
        return None

    if resp.status_code != 200:
        print("WARN: TwitterAPI.io tweet detail returned {}".format(resp.status_code), file=sys.stderr)
        return None

    data = resp.json()
    return data.get("tweet", data.get("data", data))


# ---------------------------------------------------------------------------
# Scrape: search / profile
# ---------------------------------------------------------------------------
def scrape_tweets(query=None, profile_url=None, limit=20, since_date=None, timeout=90):
    """Scrape tweets via TwitterAPI.io."""
    search_query = query
    if not search_query and profile_url:
        handle = profile_url
        if handle.startswith("http"):
            m = re.search(r'(?:twitter|x)\.com/(\w+)', handle)
            handle = m.group(1) if m else handle
        elif handle.startswith("@"):
            handle = handle[1:]
        search_query = "from:{}".format(handle)

    if not search_query:
        return []

    if since_date:
        search_query_with_date = "{} since:{}".format(search_query, since_date)
    else:
        search_query_with_date = search_query

    if not TWITTERAPI_KEY:
        print("ERROR: No TwitterAPI.io key configured. Run setup.sh or set TWITTERAPI_KEY.", file=sys.stderr)
        return []

    print("Scraping tweets (TwitterAPI.io): '{}' (limit={})...".format(search_query_with_date, limit), file=sys.stderr)
    results = twitterapi_search(search_query_with_date, limit=limit, timeout=min(timeout, 60))
    if results:
        print("Got {} tweets via TwitterAPI.io".format(len(results)), file=sys.stderr)
        return results

    # Try without date filter
    if since_date:
        print("Retrying without date filter...", file=sys.stderr)
        results = twitterapi_search(search_query, limit=limit, timeout=min(timeout, 60))
        if results:
            print("Got {} tweets (no date filter)".format(len(results)), file=sys.stderr)
            return results

    print("TwitterAPI.io returned empty.", file=sys.stderr)
    return []


def scrape_single_tweet(tweet_url):
    """Fetch a single tweet by its URL."""
    m = re.search(r'/status/(\d+)', tweet_url)
    tweet_id = m.group(1) if m else None

    if TWITTERAPI_KEY and tweet_id:
        print("Fetching tweet: {}...".format(tweet_url), file=sys.stderr)
        result = twitterapi_get_tweet(tweet_id)
        if result and (result.get("id") or result.get("text")):
            return result

    print("WARN: Could not fetch tweet", file=sys.stderr)
    return None


def scrape_comments(tweet_url, limit=50):
    """Scrape replies to a tweet."""
    m = re.search(r'/status/(\d+)', tweet_url)
    tweet_id = m.group(1) if m else None

    if TWITTERAPI_KEY and tweet_id:
        print("Scraping comments: {}...".format(tweet_url), file=sys.stderr)
        results = twitterapi_replies(tweet_id, limit=limit, timeout=30)
        if results:
            print("Got {} replies".format(len(results)), file=sys.stderr)
            return results
        print("No replies found.", file=sys.stderr)

    return []


# ---------------------------------------------------------------------------
# OpenRouter / Grok -- Method Detection
# ---------------------------------------------------------------------------
def grok_classify(prompt, max_tokens=4000):
    """Send a prompt to Grok via OpenRouter, return parsed JSON."""
    api_key = get_openrouter_key()
    if not api_key:
        print("WARN: No OpenRouter API key. Skipping method detection.", file=sys.stderr)
        return None
    resp = requests.post(
        f"{OPENROUTER_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROK_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.1,
        },
        timeout=90,
    )
    if resp.status_code != 200:
        print(f"ERROR: Grok API {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
        return None
    content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```\w*\n?", "", content)
        content = re.sub(r"\n?```$", "", content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        if content.startswith("["):
            last_brace = content.rfind("}")
            if last_brace > 0:
                truncated = content[:last_brace + 1] + "]"
                try:
                    return json.loads(truncated)
                except json.JSONDecodeError:
                    pass
        print(f"WARN: Grok returned non-JSON: {content[:300]}", file=sys.stderr)
        return None


def classify_methods(tweets):
    """Classify tweets as METHOD or CONTENT using Grok."""
    if not tweets:
        return []

    tweet_block = ""
    for i, t in enumerate(tweets):
        body = t.get("body", "")[:500]
        transcript = t.get("transcript", "")
        transcript_snippet = ""
        if transcript:
            transcript_snippet = f"\n[VIDEO TRANSCRIPT]: {transcript[:800]}"
        tweet_block += (
            f"--- TWEET {i+1} (likes:{t.get('likes',0)}, "
            f"views:{t.get('views',0)}) ---\n{body}"
            f"{transcript_snippet}\n\n"
        )

    prompt = f"""You are a trend classification engine.

Analyze each tweet and classify as:
- METHOD: describes a specific tool, technique, workflow, or production method
- CONTENT: general commentary, results showcase, or promotional (not describing HOW)

For METHOD tweets, extract:
- method_name: short descriptive name (title case, concise)
- tool_name: primary AI tool(s) mentioned
- method_type: "production" (how to MAKE content) or "gtm" (how to MAKE MONEY)
- category: one of:
  PRODUCTION: [avatar_rendering, video_generation, voice_synthesis, editing_technique, prompt_engineering, workflow_combo, tool_release, format_technique]
  GTM: [lead_generation, funnel_strategy, outreach_automation, monetization_model, growth_hack, saas_tool, marketplace_strategy, vibe_marketing, dev_workflow, design_workflow]
- method_summary: 1-2 sentence description
- tools_required: array of tools needed
- complexity: low/medium/high

For CONTENT tweets, only include tweet_num and classification.

Output valid JSON only. No markdown code blocks. Raw JSON array.

Each element: {{"tweet_num": 1, "classification": "METHOD" or "CONTENT", "method_name": "...", "tool_name": "...", "method_type": "production" or "gtm", "category": "...", "method_summary": "...", "tools_required": [...], "complexity": "..."}}

TWEETS:
{tweet_block}"""

    print("Classifying tweets with Grok (method detection)...", file=sys.stderr)
    results = grok_classify(prompt)
    if not results or not isinstance(results, list):
        print("WARN: Classification failed", file=sys.stderr)
        return []

    methods = [r for r in results if r.get("classification") == "METHOD"]
    content = [r for r in results if r.get("classification") == "CONTENT"]
    print(f"Classified: {len(methods)} METHOD / {len(content)} CONTENT", file=sys.stderr)
    return results


def format_methods_table(methods_data):
    """Print method detection results as a table."""
    methods = [m for m in methods_data if m.get("classification") == "METHOD"]
    if not methods:
        print("\nNo methods detected.", file=sys.stderr)
        return

    print(f"\n{'#':>3}  {'Type':>6}  {'Tool':28}  {'Category':20}  {'Effort':>6}", file=sys.stderr)
    print("-" * 75, file=sys.stderr)
    for m in methods:
        mtype = m.get("method_type", "prod")[:4]
        print(
            f"{m['tweet_num']:>3}  "
            f"{mtype:>6}  "
            f"{m.get('tool_name','')[:28]:28}  "
            f"{m.get('category','')[:20]:20}  "
            f"{m.get('complexity','?'):>6}",
            file=sys.stderr
        )

    print(f"\n{len(methods)} methods detected", file=sys.stderr)


# ---------------------------------------------------------------------------
# Parse tweet data -> standard format
# ---------------------------------------------------------------------------
def _safe_int(val, default=0):
    """Convert a value to int safely."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def parse_tweet(raw, search_query=None):
    """Parse a raw TwitterAPI.io tweet into standard format."""
    tweet_id = str(raw.get("id_str", raw.get("id", raw.get("tweet_id", ""))))

    # User data
    user_obj = raw.get("user", raw.get("author", {}))
    if isinstance(user_obj, dict):
        legacy = user_obj.get("legacy", {})
        if isinstance(legacy, dict) and legacy:
            user_name = legacy.get("screen_name", user_obj.get("screen_name", ""))
            full_name = legacy.get("name", user_obj.get("name", ""))
            user_desc = legacy.get("description", "")
            user_img = (user_obj.get("avatar", {}).get("image_url")
                        or legacy.get("profile_image_url_https", ""))
            user_followers = legacy.get("followers_count",
                                        legacy.get("normal_followers_count"))
            user_following = legacy.get("friends_count")
            user_verified = user_obj.get("is_blue_verified",
                                         legacy.get("verified", False))
        else:
            user_name = user_obj.get("screen_name",
                                     user_obj.get("username",
                                     user_obj.get("userName", "")))
            full_name = user_obj.get("name", "")
            user_desc = user_obj.get("description", "")
            user_img = user_obj.get("profile_image_url_https",
                                    user_obj.get("profile_image_url",
                                    user_obj.get("profilePicture", "")))
            user_followers = user_obj.get("followers_count",
                                          user_obj.get("followers"))
            user_following = user_obj.get("friends_count",
                                          user_obj.get("following"))
            user_verified = user_obj.get("verified",
                                         user_obj.get("is_blue_verified",
                                         user_obj.get("isBlueVerified")))
    else:
        kaito_user = ""
        kaito_tw_url = raw.get("twitterUrl", raw.get("url", ""))
        if kaito_tw_url:
            _um = re.search(r'(?:twitter|x)\.com/(\w+)/', kaito_tw_url)
            if _um:
                kaito_user = _um.group(1)
        user_name = raw.get("user_name", raw.get("screen_name",
                            raw.get("username", raw.get("author", kaito_user))))
        full_name = raw.get("user_full_name", raw.get("name", ""))
        user_desc = raw.get("user_description", raw.get("description", ""))
        user_img = raw.get("profile_image_url",
                           raw.get("user_profile_image_url", ""))
        user_followers = raw.get("user_followers",
                                 raw.get("followers_count"))
        user_following = raw.get("user_following",
                                 raw.get("friends_count"))
        user_verified = raw.get("user_verified", raw.get("verified"))

    # Text
    text = raw.get("full_text", raw.get("text", ""))

    # Tweet URL
    content_url = raw.get("url", raw.get("tweet_url",
                  raw.get("twitterUrl", "")))
    if not content_url and user_name and tweet_id:
        content_url = f"https://x.com/{user_name}/status/{tweet_id}"

    profile_url = f"https://x.com/{user_name}" if user_name else ""

    # Media detection
    has_media = False
    media_type = None
    video_url = None
    img_url = None

    ext_media = raw.get("extended_entities", {})
    if isinstance(ext_media, dict):
        ext_media = ext_media.get("media", [])
    else:
        ext_media = []

    ent_media = raw.get("entities", {})
    if isinstance(ent_media, dict):
        ent_media = ent_media.get("media", [])
    else:
        ent_media = []

    media_list = ext_media or ent_media or raw.get("media", [])
    if isinstance(media_list, list):
        for m in media_list:
            if not isinstance(m, dict):
                continue
            mtype = m.get("type", "")
            if mtype in ("video", "animated_gif") or m.get("video_info"):
                has_media = True
                media_type = "video"
                variants = m.get("video_info", {}).get("variants", [])
                mp4_variants = [v for v in variants
                                if v.get("content_type") == "video/mp4"]
                if mp4_variants:
                    best = max(mp4_variants,
                               key=lambda x: _safe_int(x.get("bitrate"), 0))
                    video_url = best.get("url")
                if not img_url:
                    img_url = m.get("media_url_https", m.get("media_url", ""))
            elif mtype == "photo":
                has_media = True
                media_type = media_type or "image"
                img_url = img_url or m.get("media_url_https",
                                           m.get("media_url", ""))

    if not video_url and raw.get("video_url"):
        video_url = raw["video_url"]
        has_media = True
        media_type = "video"
    if not video_url and raw.get("has_video"):
        has_media = True
        media_type = "video"
    if not img_url and raw.get("image_url"):
        img_url = raw["image_url"]
        has_media = True
        media_type = media_type or "image"

    # Hashtags
    entities = raw.get("entities", {})
    hashtag_entities = entities.get("hashtags", []) if isinstance(entities, dict) else []
    if isinstance(hashtag_entities, list) and hashtag_entities:
        tags = []
        for h in hashtag_entities:
            if isinstance(h, dict):
                tags.append(h.get("text", h.get("tag", "")))
            else:
                tags.append(str(h))
        hashtags = ", ".join(t for t in tags if t)
    else:
        hashtags = ", ".join(re.findall(r"#(\w+)", text))

    heading = text.split("\n")[0][:250] if text else ""

    # Date
    date_str = raw.get("created_at", raw.get("createdAt",
                raw.get("date", "")))
    date_channel = None
    if date_str:
        for fmt in ["%a %b %d %H:%M:%S %z %Y", "%Y-%m-%dT%H:%M:%S.%fZ",
                     "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]:
            try:
                date_channel = datetime.strptime(date_str, fmt)
                break
            except (ValueError, TypeError):
                continue

    # Engagement
    likes = _safe_int(raw.get("favorite_count", raw.get("likes",
                      raw.get("likeCount", 0))))
    views = _safe_int(raw.get("views_count", raw.get("views",
                      raw.get("view_count", raw.get("viewCount", 0)))))
    replies = _safe_int(raw.get("reply_count", raw.get("comments",
                        raw.get("replyCount", 0))))
    retweets = _safe_int(raw.get("retweet_count", raw.get("retweets",
                         raw.get("retweetCount", 0))))
    bookmarks = _safe_int(raw.get("bookmark_count", raw.get("bookmarkCount", 0)))
    quotes = _safe_int(raw.get("quote_count", raw.get("quoteCount", 0)))

    conversation_id = str(raw.get("conversation_id_str",
                          raw.get("conversationId", tweet_id)))

    return {
        "channel_id": tweet_id,
        "thread_uuid": conversation_id,
        "content_url": content_url,
        "body": text,
        "heading": heading,
        "hashtags": hashtags,
        "likes": likes,
        "views": views,
        "comments_count": replies,
        "shares": retweets + quotes,
        "has_media": has_media,
        "media_type": media_type,
        "content_video_url": video_url,
        "content_img_url": img_url,
        "transcript": None,
        "topic_keywords": search_query,
        "date_channel": date_channel,
        "_bookmarks": bookmarks,
        "_quotes": quotes,
        "_profile": {
            "profile_url": profile_url,
            "username": user_name,
            "full_name": full_name,
            "about": user_desc,
            "profile_img": user_img,
            "followers": _safe_int(user_followers) if user_followers is not None else None,
            "following": _safe_int(user_following) if user_following is not None else None,
            "verified": user_verified,
        }
    }


def parse_comment(raw, parent_tweet_id):
    """Parse a comment/reply and set thread_uuid to parent."""
    parsed = parse_tweet(raw)
    parsed["thread_uuid"] = parent_tweet_id
    return parsed


# ---------------------------------------------------------------------------
# Video transcription (Deepgram only -- standalone, no scout-base)
# ---------------------------------------------------------------------------
def _download_video(url):
    """Download video via yt-dlp. Returns local file path or None."""
    output_dir = tempfile.mkdtemp(prefix="xscout_")
    output_template = os.path.join(output_dir, "xscout_%(id)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--no-warnings",
        "--no-playlist",
        "--max-filesize", "100M",
        "-f", "mp4/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--print", "after_move:filepath",
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            filepath = result.stdout.strip().split("\n")[-1]
            if os.path.exists(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"Downloaded: {size_mb:.1f}MB", file=sys.stderr)
                return filepath

            # Fallback: find by pattern
            import glob as globmod
            pattern = os.path.join(output_dir, "xscout_*")
            files = sorted(globmod.glob(pattern), key=os.path.getmtime, reverse=True)
            if files:
                return files[0]

        stderr = result.stderr.strip()[:200] if result.stderr else "unknown error"
        print(f"yt-dlp failed: {stderr}", file=sys.stderr)
        return None

    except FileNotFoundError:
        print("yt-dlp not installed. Install with: pip install yt-dlp", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("yt-dlp timed out (120s)", file=sys.stderr)
        return None


def _transcribe_deepgram(video_path):
    """Transcribe video audio via Deepgram nova-2."""
    if not DEEPGRAM_KEY:
        return None

    # Extract WAV
    wav_path = video_path.rsplit(".", 1)[0] + ".wav"
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", video_path,
             "-vn", "-acodec", "pcm_s16le",
             "-ar", "16000", "-ac", "1",
             wav_path],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0 or not os.path.exists(wav_path):
            return None
    except Exception:
        return None

    try:
        with open(wav_path, "rb") as f:
            audio_data = f.read()

        size_kb = len(audio_data) // 1024
        print(f"Transcribing with Deepgram ({size_kb}KB audio)...", file=sys.stderr)

        resp = requests.post(
            "https://api.deepgram.com/v1/listen",
            params={
                "model": "nova-2",
                "language": "en",
                "punctuate": "true",
                "smart_format": "true",
            },
            headers={
                "Authorization": f"Token {DEEPGRAM_KEY}",
                "Content-Type": "audio/wav",
            },
            data=audio_data,
            timeout=120,
        )

        if resp.status_code == 200:
            transcript = (resp.json().get("results", {})
                          .get("channels", [{}])[0]
                          .get("alternatives", [{}])[0]
                          .get("transcript", ""))
            return transcript.strip() if transcript else None
        else:
            print(f"Deepgram failed: {resp.status_code}", file=sys.stderr)
            return None

    except Exception as e:
        print(f"Deepgram error: {e}", file=sys.stderr)
        return None
    finally:
        try:
            os.unlink(wav_path)
        except OSError:
            pass


def transcribe_video(video_url):
    """Download video and transcribe. Returns transcript string or None."""
    video_path = _download_video(video_url)
    if not video_path:
        return None

    transcript = _transcribe_deepgram(video_path)

    # Cleanup
    try:
        os.unlink(video_path)
        parent = os.path.dirname(video_path)
        if parent.startswith("/tmp/xscout_"):
            os.rmdir(parent)
    except OSError:
        pass

    if transcript:
        print(f"Transcript: {len(transcript)} chars", file=sys.stderr)
    return transcript


# ---------------------------------------------------------------------------
# Query simplification (Cerebras)
# ---------------------------------------------------------------------------
def simplify_search_query(query):
    """Use Cerebras LLM to reduce a long query to Twitter-friendly keywords."""
    global _cerebras_key_idx

    if any(op in query.lower() for op in ["from:", "to:", "filter:", "since:", "until:", "lang:"]):
        return query

    if not CEREBRAS_KEYS:
        return query

    word_count = len(query.split())
    print(f"Optimizing query for Twitter ({word_count} words)...", file=sys.stderr)

    prompt = (
        "You are a Twitter/X search query optimizer. Twitter search works best with 2-4 broad keywords.\n"
        "Long-tail queries (5+ specific words) return ZERO results on Twitter.\n\n"
        "Convert this search query into 2-4 broad keywords that would find relevant tweets.\n"
        "Rules:\n"
        "- Output ONLY the simplified query (2-4 words), nothing else\n"
        "- Remove filler words, adjectives, specifics\n"
        "- Keep the core topic keywords\n"
        "- Do NOT add quotes or operators\n"
        "- Do NOT explain, just output the keywords\n\n"
        f"Original query: {query}\n\n"
        "Simplified query:"
    )

    for attempt in range(min(3, len(CEREBRAS_KEYS))):
        key = CEREBRAS_KEYS[_cerebras_key_idx % len(CEREBRAS_KEYS)]
        _cerebras_key_idx += 1
        try:
            resp = requests.post(
                CEREBRAS_API_URL,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": CEREBRAS_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 30,
                    "temperature": 0.0,
                },
                timeout=10,
            )
            if resp.status_code == 429:
                continue
            if resp.status_code != 200:
                continue

            content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            content = content.strip('"\'`').split("\n")[0].strip()

            if content and 1 <= len(content.split()) <= 6:
                print(f"Simplified: \"{query}\" -> \"{content}\"", file=sys.stderr)
                return content
            else:
                return query

        except requests.exceptions.Timeout:
            return query
        except Exception:
            continue

    return query


def broaden_search_query(original_query, simplified_query, attempt=1):
    """Use Cerebras to generate a broader search query when results are thin."""
    global _cerebras_key_idx

    if not CEREBRAS_KEYS:
        return None

    prompt = (
        "You are a Twitter/X search strategist. The previous search returned too few results.\n\n"
        f"Original query: {original_query}\n"
        f"Simplified to: {simplified_query}\n"
        f"Broadening attempt: {attempt}\n\n"
        "Generate a SINGLE alternative search query that is:\n"
        "- BROADER and more conversational (how real people tweet about this topic)\n"
        "- 2-4 words maximum\n"
        "- Focused on the PAIN POINTS or EMOTIONS people express about this topic\n"
        "- NOT product-specific or brand-name heavy\n\n"
        "Output ONLY the new query (2-4 words), nothing else:"
    )

    for _ in range(min(2, len(CEREBRAS_KEYS))):
        key = CEREBRAS_KEYS[_cerebras_key_idx % len(CEREBRAS_KEYS)]
        _cerebras_key_idx += 1
        try:
            resp = requests.post(
                CEREBRAS_API_URL,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": CEREBRAS_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 30,
                    "temperature": 0.7,
                },
                timeout=10,
            )
            if resp.status_code == 429:
                continue
            if resp.status_code != 200:
                continue

            result = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            result = result.strip('"\'`').split("\n")[0].strip()

            if result and 1 <= len(result.split()) <= 6 and result.lower() != simplified_query.lower():
                print(f"Broadened: \"{simplified_query}\" -> \"{result}\" (attempt {attempt})", file=sys.stderr)
                return result

        except Exception:
            continue

    return None


# ---------------------------------------------------------------------------
# Main flows
# ---------------------------------------------------------------------------
def flow_search(query, limit, since, transcribe, timeout=90):
    """Search flow: scrape tweets, optional transcription, query broadening."""
    search_query = simplify_search_query(query)

    raw_tweets = scrape_tweets(query=search_query, limit=limit, since_date=since, timeout=timeout)

    # Broadening retry
    min_acceptable = max(3, limit // 3)
    all_raw = list(raw_tweets) if raw_tweets else []
    seen_ids = {str(t.get("id_str", t.get("id", ""))) for t in all_raw}
    current_query = search_query

    if len(all_raw) < min_acceptable:
        for broaden_attempt in range(1, 3):
            broader = broaden_search_query(query, current_query, attempt=broaden_attempt)
            if not broader:
                break
            print(f"Broadening search (attempt {broaden_attempt}): \"{broader}\" "
                  f"(have {len(all_raw)}/{limit})...", file=sys.stderr)
            extra_tweets = scrape_tweets(query=broader, limit=limit, since_date=since, timeout=timeout)
            if extra_tweets:
                for t in extra_tweets:
                    tid = str(t.get("id_str", t.get("id", "")))
                    if tid not in seen_ids:
                        all_raw.append(t)
                        seen_ids.add(tid)
                print(f"After broadening: {len(all_raw)} unique tweets total", file=sys.stderr)
            current_query = broader
            if len(all_raw) >= min_acceptable:
                break

    if not all_raw:
        print("No tweets found (even after broadening).", file=sys.stderr)
        return []

    tweets = [parse_tweet(r, search_query=query) for r in all_raw]
    return process_tweets(tweets, transcribe)


def flow_profile(handle, limit, since, transcribe, timeout=90):
    """Profile flow: scrape profile posts."""
    raw_tweets = scrape_tweets(profile_url=handle, limit=limit, since_date=since, timeout=timeout)
    if not raw_tweets:
        print("No tweets found.", file=sys.stderr)
        return []

    tag = handle if handle.startswith("@") else f"@{handle}"
    tweets = [parse_tweet(r, search_query=tag) for r in raw_tweets]
    return process_tweets(tweets, transcribe)


def flow_comments(tweet_url):
    """Comments flow: scrape replies to a tweet."""
    match = re.search(r"/status/(\d+)", tweet_url)
    parent_id = match.group(1) if match else ""

    raw_comments = scrape_comments(tweet_url)
    if not raw_comments:
        print("No comments found.", file=sys.stderr)
        return []

    valid_comments = []
    for r in raw_comments:
        cid = str(r.get("id_str", r.get("id", "")))
        if cid in ("-1", "", "0"):
            continue
        valid_comments.append(r)

    if not valid_comments:
        print("No real comments found.", file=sys.stderr)
        return []

    return [parse_comment(r, parent_id) for r in valid_comments]


def flow_intel(tweet_url, transcribe):
    """Full intel: get tweet + comments + video transcription."""
    match = re.search(r"/status/(\d+)", tweet_url)
    parent_id = match.group(1) if match else ""

    user_match = re.search(r"x\.com/(\w+)/status/", tweet_url)
    username = user_match.group(1) if user_match else None

    raw = scrape_single_tweet(tweet_url)
    tweet = parse_tweet(raw, search_query="intel") if raw else None

    # Fallback: scrape user's recent tweets and find by ID
    if not tweet and username and parent_id:
        print(f"Direct fetch failed, trying profile scrape of @{username}...", file=sys.stderr)
        raw_tweets = scrape_tweets(profile_url=f"@{username}", limit=20)
        for r in raw_tweets:
            if str(r.get("id_str", r.get("id", ""))) == parent_id:
                tweet = parse_tweet(r, search_query="intel")
                break

    comments = flow_comments(tweet_url)

    # Transcribe video
    if tweet and transcribe and tweet.get("has_media") and tweet.get("media_type") == "video":
        video_url = tweet.get("content_video_url") or tweet_url
        transcript = transcribe_video(video_url)
        if transcript:
            tweet["transcript"] = transcript

    # Fallback: try tweet URL directly for transcription
    if tweet and transcribe and not tweet.get("transcript") and tweet.get("has_media"):
        transcript = transcribe_video(tweet_url)
        if transcript:
            tweet["transcript"] = transcript

    return {
        "tweet": tweet,
        "comments": comments,
        "comment_count": len(comments),
    }


def process_tweets(tweets, transcribe):
    """Process parsed tweets: optional video transcription."""
    transcribed = 0

    for t in tweets:
        if transcribe and t.get("has_media") and t.get("media_type") == "video":
            video_url = t.get("content_video_url") or t.get("content_url", "")
            if video_url:
                transcript = transcribe_video(video_url)
                if transcript:
                    t["transcript"] = transcript
                    transcribed += 1

    if transcribed:
        print(f"Transcribed {transcribed} videos", file=sys.stderr)

    return tweets


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------
def format_table(tweets):
    """Print tweets as a table."""
    print(f"\n{'#':>3}  {'Author':<20}  {'Likes':>6}  {'Views':>8}  {'RT':>5}  {'Media':>5}  {'Trans':>5}  Tweet Preview")
    print("-" * 120)
    for i, t in enumerate(tweets, 1):
        author = (t.get("_profile", {}).get("username", "") or "")[:20]
        likes = t.get("likes", 0) or 0
        views = t.get("views", 0) or 0
        rt = t.get("shares", 0) or 0
        media = t.get("media_type", "")[:5] if t.get("has_media") else ""
        trans = "yes" if t.get("transcript") else ""
        body = (t.get("body", "") or "").replace("\n", " ")[:60]
        print(f"{i:>3}  {author:<20}  {likes:>6}  {views:>8}  {rt:>5}  {media:>5}  {trans:>5}  {body}")


def clean_for_json(tweets):
    """Remove internal fields for JSON output."""
    out = []
    for t in tweets:
        t2 = {k: v for k, v in t.items() if not k.startswith("_")}
        if t2.get("date_channel") and hasattr(t2["date_channel"], "isoformat"):
            t2["date_channel"] = t2["date_channel"].isoformat()
        out.append(t2)
    return out


# ---------------------------------------------------------------------------
# Method detection orchestrator
# ---------------------------------------------------------------------------
def run_method_detection(tweets):
    """Full method detection pipeline: classify tweets as METHOD/CONTENT."""
    classifications = classify_methods(tweets)
    if not classifications:
        return []

    methods_only = [c for c in classifications if c.get("classification") == "METHOD"]
    if methods_only:
        format_methods_table(classifications)
    else:
        print("No methods detected in these tweets.", file=sys.stderr)

    return classifications


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="X-Scout -- Twitter/X Intelligence Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--search", type=str, metavar="QUERY", help="Search tweets by keyword")
    mode_group.add_argument("--profile", type=str, metavar="HANDLE", help="Scrape profile posts (@handle or URL)")
    mode_group.add_argument("--comments", type=str, metavar="URL", help="Pull comments on a tweet URL")
    mode_group.add_argument("--intel", type=str, metavar="URL", help="Full intel on a tweet URL")

    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--since", type=str, default=None, help="Since date YYYY-MM-DD (default: 180 days)")
    parser.add_argument("--no-methods", action="store_true",
                        help="Skip method detection (methods detected by default)")
    parser.add_argument("--no-transcribe", action="store_true", help="Skip video transcription")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--timeout", type=int, default=90,
                        help="Scraper timeout in seconds (default: 90)")
    parser.add_argument("--version", action="version", version=f"x-scout {VERSION}")

    args = parser.parse_args()

    transcribe = not args.no_transcribe and bool(DEEPGRAM_KEY)
    detect_methods = not args.no_methods

    # Validate key
    if not TWITTERAPI_KEY:
        print("ERROR: TWITTERAPI_KEY not set. Run setup.sh or export TWITTERAPI_KEY=your_key", file=sys.stderr)
        sys.exit(1)

    mode = "search" if args.search else ("profile" if args.profile else ("comments" if args.comments else "intel"))
    query_for_analytics = args.search or args.profile or args.comments or args.intel

    try:
        if args.search:
            results = flow_search(args.search, args.limit, args.since, transcribe, timeout=args.timeout)
            methods_data = []
            if detect_methods and results:
                methods_data = run_method_detection(results)
            _report_usage(mode, query=args.search, results_count=len(results))
            if args.json:
                out = clean_for_json(results)
                if detect_methods:
                    print(json.dumps({"tweets": out, "methods": methods_data}, indent=2, default=str))
                else:
                    print(json.dumps(out, indent=2, default=str))
            else:
                format_table(results)
                print(f"\nTotal: {len(results)} tweets")

        elif args.profile:
            results = flow_profile(args.profile, args.limit, args.since, transcribe, timeout=args.timeout)
            methods_data = []
            if detect_methods and results:
                methods_data = run_method_detection(results)
            _report_usage(mode, query=args.profile, results_count=len(results))
            if args.json:
                out = clean_for_json(results)
                if detect_methods:
                    print(json.dumps({"tweets": out, "methods": methods_data}, indent=2, default=str))
                else:
                    print(json.dumps(out, indent=2, default=str))
            else:
                format_table(results)
                print(f"\nTotal: {len(results)} tweets")

        elif args.comments:
            results = flow_comments(args.comments)
            _report_usage(mode, query=args.comments, results_count=len(results))
            if args.json:
                print(json.dumps(clean_for_json(results), indent=2, default=str))
            else:
                format_table(results)
                print(f"\nTotal: {len(results)} comments")

        elif args.intel:
            result = flow_intel(args.intel, transcribe)
            methods_data = []
            if detect_methods and result.get("tweet"):
                methods_data = run_method_detection([result["tweet"]])
            _report_usage(mode, query=args.intel, results_count=result["comment_count"])
            if args.json:
                out = {}
                if result["tweet"]:
                    out["tweet"] = clean_for_json([result["tweet"]])[0]
                out["comments"] = clean_for_json(result["comments"])
                out["comment_count"] = result["comment_count"]
                if detect_methods:
                    out["methods"] = methods_data
                print(json.dumps(out, indent=2, default=str))
            else:
                if result["tweet"]:
                    t = result["tweet"]
                    print(f"\n=== Tweet by @{t['_profile']['username']} ===")
                    print(t.get("body", ""))
                    print(f"\nLikes: {t.get('likes',0)} | Views: {t.get('views',0)} | RT: {t.get('shares',0)}")
                    if t.get("transcript"):
                        print(f"\n=== Video Transcript ===\n{t['transcript'][:500]}")
                print(f"\n=== {result['comment_count']} Comments ===")
                format_table(result["comments"])

    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        _report_usage(mode, query=query_for_analytics, error="keyboard_interrupt")
        sys.exit(130)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        _report_usage(mode, query=query_for_analytics, error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
