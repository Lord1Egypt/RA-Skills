#!/usr/bin/env python3
"""
twitter_trend_radar.py

Read-only X/Twitter trend radar powered by the local `bird` CLI.

- Searches X for launch-signal tweets with links.
- Extracts outbound domains.
- Checks RDAP domain registration age when possible.
- Scores early product/SEO opportunities.
- Outputs Markdown or JSON.

No third-party Python dependencies required.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

DEFAULT_LAUNCH_PHRASES = [
    "just launched",
    "introducing",
    "built this",
    "made this",
    "made a site",
    "shipped",
    "launch day",
    "now live",
    "new app",
    "new tool",
    "new game",
    "try it",
    "play online",
]

NOISY_DOMAINS = {
    "x.com", "twitter.com", "t.co", "youtube.com", "youtu.be", "github.com",
    "producthunt.com", "linkedin.com", "instagram.com", "facebook.com", "reddit.com",
    "medium.com", "substack.com", "notion.site", "notion.so", "figma.com",
    "discord.gg", "discord.com", "telegram.me", "t.me", "apple.com", "google.com",
    "chromewebstore.google.com", "apps.apple.com", "play.google.com", "steamcommunity.com",
}

URL_RE = re.compile(r"https?://[^\s<>)\]}\"']+", re.IGNORECASE)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_date_days_ago(days: int) -> str:
    return (utc_now() - dt.timedelta(days=days)).date().isoformat()


def normalize_domain(url_or_domain: str) -> Optional[str]:
    s = url_or_domain.strip()
    if not s:
        return None
    if "://" not in s:
        s = "https://" + s
    try:
        parsed = urllib.parse.urlparse(s)
        host = (parsed.hostname or "").lower().strip(".")
        if host.startswith("www."):
            host = host[4:]
        return host or None
    except Exception:
        return None


def is_noisy_domain(domain: str) -> bool:
    if domain in NOISY_DOMAINS:
        return True
    return any(domain.endswith("." + d) for d in NOISY_DOMAINS)


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        if isinstance(value, str):
            value = value.replace(",", "").strip()
            if value.endswith("K"):
                return int(float(value[:-1]) * 1000)
            if value.endswith("M"):
                return int(float(value[:-1]) * 1_000_000)
        return int(value)
    except Exception:
        return default


def find_first(d: Any, keys: Iterable[str]) -> Any:
    """Recursively find the first value for any candidate key in nested dict/list JSON."""
    if isinstance(d, dict):
        for key in keys:
            if key in d:
                return d[key]
        for v in d.values():
            found = find_first(v, keys)
            if found is not None:
                return found
    elif isinstance(d, list):
        for item in d:
            found = find_first(item, keys)
            if found is not None:
                return found
    return None


def flatten_candidate_tweets(obj: Any) -> List[dict]:
    """Try to normalize many possible bird JSON shapes into tweet-like dicts."""
    candidates: List[dict] = []

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            text = find_first(x, ["text", "full_text", "content", "tweetText"])
            tweet_id = find_first(x, ["id", "id_str", "tweet_id", "rest_id"])
            if text and (tweet_id or find_first(x, ["url", "permalink", "tweet_url"])):
                candidates.append(x)
                return
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(obj)
    # Deduplicate by id/text hash.
    seen = set()
    out = []
    for c in candidates:
        text = str(find_first(c, ["text", "full_text", "content", "tweetText"]) or "")
        tid = str(find_first(c, ["id", "id_str", "tweet_id", "rest_id"]) or "")
        key = tid or hashlib.sha1(text.encode("utf-8")).hexdigest()
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def extract_urls_from_tweet(tweet: dict) -> List[str]:
    urls = set()
    # Regex over full JSON catches expanded_url/url fields even if schema shifts.
    blob = json.dumps(tweet, ensure_ascii=False)
    for m in URL_RE.findall(blob):
        clean = m.replace("\\/", "/").rstrip(".,;:!?)\"'")
        urls.add(clean)

    text = str(find_first(tweet, ["text", "full_text", "content", "tweetText"]) or "")
    for m in URL_RE.findall(text):
        urls.add(m.rstrip(".,;:!?)\"'"))
    return sorted(urls)


def parse_created_at(value: Any) -> Optional[str]:
    if not value:
        return None
    s = str(value)
    # Common Twitter format: Wed Oct 10 20:19:24 +0000 2018
    for fmt in ["%a %b %d %H:%M:%S %z %Y", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]:
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except Exception:
            pass
    return s[:10] if re.match(r"\d{4}-\d{2}-\d{2}", s) else None


def normalize_tweet(tweet: dict) -> dict:
    text = str(find_first(tweet, ["text", "full_text", "content", "tweetText"]) or "")
    user = find_first(tweet, ["username", "screen_name", "userName", "handle"])
    created_at = parse_created_at(find_first(tweet, ["created_at", "createdAt", "time", "date"] ))
    tweet_url = find_first(tweet, ["url", "permalink", "tweet_url"])
    tid = find_first(tweet, ["id_str", "tweet_id", "rest_id", "id"])
    if not tweet_url and user and tid:
        handle = str(user).lstrip("@")
        tweet_url = f"https://x.com/{handle}/status/{tid}"

    likes = safe_int(find_first(tweet, ["favorite_count", "like_count", "likes", "favoriteCount", "likeCount"]), 0)
    reposts = safe_int(find_first(tweet, ["retweet_count", "repost_count", "retweets", "reposts", "retweetCount"]), 0)
    replies = safe_int(find_first(tweet, ["reply_count", "replies", "replyCount"]), 0)

    return {
        "id": str(tid or hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]),
        "text": text,
        "user": str(user or ""),
        "created_at": created_at,
        "url": str(tweet_url or ""),
        "likes": likes,
        "reposts": reposts,
        "replies": replies,
        "links": extract_urls_from_tweet(tweet),
    }


def run_bird_search(query: str, limit: int, bird_args: List[str], cache_dir: Path, ttl_seconds: int, dry_run: bool = False) -> List[dict]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_key = hashlib.sha1((query + "|" + str(limit) + "|" + " ".join(bird_args)).encode("utf-8")).hexdigest()
    cache_path = cache_dir / f"bird_{cache_key}.json"
    if cache_path.exists() and time.time() - cache_path.stat().st_mtime < ttl_seconds:
        try:
            return json.loads(cache_path.read_text("utf-8"))
        except Exception:
            pass

    cmd = ["bird", *bird_args, "search", query, "-n", str(limit), "--json"]
    if dry_run:
        print("DRY RUN:", " ".join(cmd), file=sys.stderr)
        return []

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except FileNotFoundError:
        raise SystemExit("bird CLI not found. Install bird and make sure it is on PATH.")
    except subprocess.TimeoutExpired:
        print(f"Warning: bird search timed out for query: {query}", file=sys.stderr)
        return []

    if proc.returncode != 0:
        print(f"Warning: bird search failed for query: {query}\n{proc.stderr.strip()}", file=sys.stderr)
        return []

    raw = proc.stdout.strip()
    if not raw:
        return []

    try:
        parsed = json.loads(raw)
        tweets = [normalize_tweet(t) for t in flatten_candidate_tweets(parsed)]
    except Exception:
        # Fallback: parse URLs from text output.
        tweets = [{
            "id": hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16],
            "text": raw,
            "user": "",
            "created_at": None,
            "url": "",
            "likes": 0,
            "reposts": 0,
            "replies": 0,
            "links": sorted(set(URL_RE.findall(raw))),
        }]

    cache_path.write_text(json.dumps(tweets, ensure_ascii=False, indent=2), "utf-8")
    return tweets


def rdap_lookup(domain: str, cache_dir: Path, ttl_seconds: int = 86400 * 7) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"rdap_{hashlib.sha1(domain.encode()).hexdigest()}.json"
    if cache_path.exists() and time.time() - cache_path.stat().st_mtime < ttl_seconds:
        try:
            return json.loads(cache_path.read_text("utf-8"))
        except Exception:
            pass

    url = f"https://rdap.org/domain/{urllib.parse.quote(domain)}"
    info: Dict[str, Any] = {"domain": domain, "created_at": None, "age_days": None, "rdap_ok": False}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "twitter-trend-radar/1.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
        events = data.get("events", []) if isinstance(data, dict) else []
        created = None
        for e in events:
            if e.get("eventAction") in {"registration", "registered", "domain registration"}:
                created = e.get("eventDate")
                break
        if created:
            created_date = dt.datetime.fromisoformat(created.replace("Z", "+00:00")).date()
            info.update({
                "created_at": created_date.isoformat(),
                "age_days": (utc_now().date() - created_date).days,
                "rdap_ok": True,
            })
    except Exception as e:
        info["error"] = str(e)[:160]

    cache_path.write_text(json.dumps(info, ensure_ascii=False, indent=2), "utf-8")
    return info


def build_queries(topic: str, days: int, min_likes: int, phrases: List[str]) -> List[str]:
    since = iso_date_days_ago(days)
    queries = []
    for phrase in phrases:
        if topic:
            q = f'"{phrase}" "{topic}" filter:links min_faves:{min_likes} since:{since}'
        else:
            q = f'"{phrase}" filter:links min_faves:{min_likes} since:{since}'
        queries.append(q)
    return queries


def launch_phrase_score(text: str, phrases: List[str]) -> int:
    lower = text.lower()
    score = 0
    for p in phrases:
        if p.lower() in lower:
            score += 8
    return min(score, 24)


def suggested_pages(domain: str, topic: str) -> List[str]:
    base = domain.split(".")[0].replace("-", " ")
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-") or "product"
    pages = [f"/{slug}", f"/{slug}-alternatives", f"/{slug}-review", f"/{slug}-pricing"]
    if any(w in topic.lower() for w in ["game", "browser", "play", "chameleon"]):
        pages = [f"/{slug}", f"/{slug}-online", f"/{slug}-unblocked", f"/{slug}-how-to-play", f"/{slug}-alternatives"]
    return pages


@dataclass
class Opportunity:
    domain: str
    score: int
    mentions: int
    max_likes: int
    total_engagement: int
    domain_age_days: Optional[int]
    domain_created_at: Optional[str]
    tweets: List[dict]
    links: List[str]
    suggested_pages: List[str]
    reasons: List[str]


def score_domain(domain: str, tweets: List[dict], links: List[str], rdap: dict, topic: str, phrases: List[str]) -> Opportunity:
    likes = [safe_int(t.get("likes")) for t in tweets]
    reposts = [safe_int(t.get("reposts")) for t in tweets]
    replies = [safe_int(t.get("replies")) for t in tweets]
    max_likes = max(likes or [0])
    total_engagement = sum(likes) + 2 * sum(reposts) + sum(replies)
    mentions = len(tweets)
    age_days = rdap.get("age_days")

    score = 0
    reasons = []

    if max_likes >= 1000:
        score += 28; reasons.append("strong X engagement: 1K+ likes")
    elif max_likes >= 300:
        score += 22; reasons.append("good X engagement: 300+ likes")
    elif max_likes >= 100:
        score += 16; reasons.append("early X engagement: 100+ likes")
    elif max_likes >= 20:
        score += 10; reasons.append("some X engagement")

    if mentions >= 3:
        score += 18; reasons.append("multiple matching tweets mention this domain")
    elif mentions == 2:
        score += 10; reasons.append("repeated signal across tweets")

    if isinstance(age_days, int):
        if age_days <= 30:
            score += 25; reasons.append(f"very fresh domain: {age_days} days old")
        elif age_days <= 180:
            score += 18; reasons.append(f"fresh domain: {age_days} days old")
        elif age_days <= 365:
            score += 10; reasons.append(f"domain under 1 year old: {age_days} days")
    else:
        reasons.append("domain age unknown; verify manually")

    phrase_points = sum(launch_phrase_score(t.get("text", ""), phrases) for t in tweets)
    if phrase_points:
        p = min(phrase_points, 20)
        score += p
        reasons.append("contains launch-signal wording")

    if links:
        score += 5

    score = min(score, 100)
    return Opportunity(
        domain=domain,
        score=score,
        mentions=mentions,
        max_likes=max_likes,
        total_engagement=total_engagement,
        domain_age_days=age_days,
        domain_created_at=rdap.get("created_at"),
        tweets=sorted(tweets, key=lambda x: safe_int(x.get("likes")), reverse=True)[:3],
        links=sorted(set(links))[:5],
        suggested_pages=suggested_pages(domain, topic),
        reasons=reasons,
    )


def generate_report(opps: List[Opportunity], topic: str, days: int, min_likes: int) -> str:
    now = utc_now().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Twitter Trend Radar: {topic or 'launch signals'}",
        "",
        f"Generated: {now}",
        f"Window: last {days} days",
        f"Minimum likes filter: {min_likes}",
        "",
        "## Summary",
        "",
        f"Found {len(opps)} candidate domains.",
        "",
    ]
    if not opps:
        lines += [
            "No candidates found. Try lowering `--min-likes`, increasing `--days`, or using a broader topic.",
            "",
        ]
        return "\n".join(lines)

    lines += ["## Top opportunities", ""]
    for i, o in enumerate(opps, 1):
        lines += [
            f"### {i}. {o.domain} — Score {o.score}/100",
            "",
            f"- Mentions: {o.mentions}",
            f"- Max likes: {o.max_likes}",
            f"- Total weighted engagement: {o.total_engagement}",
            f"- Domain created: {o.domain_created_at or 'unknown'}",
            f"- Domain age: {str(o.domain_age_days) + ' days' if o.domain_age_days is not None else 'unknown'}",
            "- Reasons: " + ("; ".join(o.reasons) if o.reasons else "n/a"),
            "- Suggested pages: " + ", ".join(f"`{p}`" for p in o.suggested_pages),
            "",
            "Top tweets:",
        ]
        for t in o.tweets:
            text = re.sub(r"\s+", " ", t.get("text", "")).strip()
            if len(text) > 240:
                text = text[:237] + "..."
            lines += [
                f"- {t.get('url') or '(tweet url unavailable)'}",
                f"  - Likes: {t.get('likes', 0)}, reposts: {t.get('reposts', 0)}, replies: {t.get('replies', 0)}",
                f"  - Text: {text}",
            ]
        if o.links:
            lines += ["", "Links:"]
            for link in o.links:
                lines.append(f"- {link}")
        lines.append("")

    lines += [
        "## Next steps",
        "",
        "1. Manually open the top domains and verify the product/game is real and new.",
        "2. Check Google SERP, Google Suggest, Reddit, YouTube, Product Hunt, and GitHub for demand confirmation.",
        "3. Prioritize pages where the keyword has weak SERP competition and clear user intent.",
        "4. Generate landing-page briefs for the highest-confidence candidates.",
        "",
        "## Notes",
        "",
        "This report uses bird CLI and X/Twitter web search behavior. Results are approximate and can vary by account, location, search ranking, and rate limits.",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="X/Twitter trend radar using bird CLI")
    parser.add_argument("--topic", default="", help="Topic to combine with launch phrases, e.g. 'browser game' or 'AI agent'.")
    parser.add_argument("--days", type=int, default=30, help="Search window in days.")
    parser.add_argument("--min-likes", type=int, default=20, help="Minimum likes filter used in X search query.")
    parser.add_argument("--limit", type=int, default=30, help="Tweets per query.")
    parser.add_argument("--max-queries", type=int, default=8, help="Maximum launch phrase queries to run.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Write report to file.")
    parser.add_argument("--cache-dir", default=".cache/twitter-trend-radar")
    parser.add_argument("--cache-ttl", type=int, default=3600, help="Bird search cache TTL seconds.")
    parser.add_argument("--bird-arg", action="append", default=[], help="Extra arg passed before bird subcommand, e.g. --bird-arg='--chrome-profile' --bird-arg='Default'.")
    parser.add_argument("--phrase", action="append", help="Override/add launch phrases. If provided, only these phrases are used.")
    parser.add_argument("--dry-run", action="store_true", help="Print bird commands without executing.")
    args = parser.parse_args()

    phrases = args.phrase if args.phrase else DEFAULT_LAUNCH_PHRASES
    queries = build_queries(args.topic, args.days, args.min_likes, phrases)[: args.max_queries]
    cache_dir = Path(args.cache_dir)

    all_tweets: List[dict] = []
    for q in queries:
        tweets = run_bird_search(q, args.limit, args.bird_arg, cache_dir, args.cache_ttl, dry_run=args.dry_run)
        all_tweets.extend(tweets)
        time.sleep(1.5)  # Conservative pacing to avoid rate limits.

    # Deduplicate tweets.
    seen_ids = set()
    deduped = []
    for t in all_tweets:
        if t["id"] not in seen_ids:
            seen_ids.add(t["id"])
            deduped.append(t)

    by_domain: Dict[str, Dict[str, Any]] = {}
    for t in deduped:
        for link in t.get("links", []):
            domain = normalize_domain(link)
            if not domain or is_noisy_domain(domain):
                continue
            by_domain.setdefault(domain, {"tweets": [], "links": []})
            by_domain[domain]["tweets"].append(t)
            by_domain[domain]["links"].append(link)

    opportunities: List[Opportunity] = []
    for domain, data in by_domain.items():
        rdap = rdap_lookup(domain, cache_dir)
        opportunities.append(score_domain(domain, data["tweets"], data["links"], rdap, args.topic, phrases))

    opportunities.sort(key=lambda o: (o.score, o.max_likes, o.mentions), reverse=True)

    if args.format == "json":
        result = json.dumps({
            "topic": args.topic,
            "days": args.days,
            "min_likes": args.min_likes,
            "generated_at": utc_now().isoformat(),
            "opportunities": [asdict(o) for o in opportunities],
        }, ensure_ascii=False, indent=2)
    else:
        result = generate_report(opportunities, args.topic, args.days, args.min_likes)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result, "utf-8")
        print(f"Wrote {out}")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
