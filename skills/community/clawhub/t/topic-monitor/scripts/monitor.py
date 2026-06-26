#!/usr/bin/env python3
"""
Proactive Research Monitor

Checks topics due for monitoring, scores findings, and sends alerts.
Run via cron for automated monitoring.
"""

import os
import sys
import json
import hashlib
import argparse
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen

SCRIPT_DIR = Path(__file__).parent
VENDOR_DIR = SCRIPT_DIR / "_vendor"
sys.path.insert(0, str(SCRIPT_DIR))
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

from config import (
    load_config, load_state, save_state, get_settings,
    save_finding, queue_alert
)
from importance_scorer import score_result

try:
    import feedparser
except ImportError:  # pragma: no cover - handled at runtime
    feedparser = None


class FeedDiscoveryParser(HTMLParser):
    """Extract RSS/Atom alternate links from HTML."""

    def __init__(self):
        super().__init__()
        self.feed_links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "link":
            return
        attr_map = {k.lower(): v for k, v in attrs}
        rel = (attr_map.get("rel") or "").lower()
        href = attr_map.get("href")
        content_type = (attr_map.get("type") or "").lower()
        if not href:
            return
        if "alternate" in rel and content_type in (
            "application/rss+xml",
            "application/atom+xml",
            "application/xml",
            "text/xml",
        ):
            self.feed_links.append(href)


def hash_url(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def normalize_text_list(values: Optional[List[str]]) -> List[str]:
    if not values:
        return []
    out = []
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            out.append(text)
    return out


def normalize_feed_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if "github.com" in url and "/releases" not in url and url.count("/") >= 4:
        parts = url.rstrip("/").split("/")
        if len(parts) >= 5:
            owner = parts[-2]
            repo = parts[-1]
            return f"https://github.com/{owner}/{repo}/releases.atom"
    return url


def github_release_feed_url(repo: str) -> str:
    repo = repo.strip().strip("/")
    return f"https://github.com/{repo}/releases.atom"


def parse_http_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except Exception:
        return None


def discover_feed_urls(url: str, timeout: int = 15) -> List[str]:
    """Try to discover RSS/Atom feeds from a regular webpage URL."""
    url = (url or "").strip()
    if not url:
        return []

    if url.endswith((".rss", ".xml", ".atom")) or url.endswith("/feed"):
        return [url]

    request = Request(
        url,
        headers={
            "User-Agent": "topic-monitor/1.5 (+feed-discovery)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            final_url = response.geturl()
            body = response.read(250_000)
    except Exception:
        return []

    lowered_type = content_type.lower()
    if "rss" in lowered_type or "atom" in lowered_type or "xml" in lowered_type:
        return [final_url]

    try:
        html = body.decode("utf-8", errors="ignore")
    except Exception:
        return []

    parser = FeedDiscoveryParser()
    parser.feed(html)
    discovered = [urljoin(final_url, href) for href in parser.feed_links]

    common_guesses = [
        urljoin(final_url, "/feed"),
        urljoin(final_url, "/rss"),
        urljoin(final_url, "/rss.xml"),
        urljoin(final_url, "/atom.xml"),
        urljoin(final_url, "/feeds/posts/default"),
    ]

    seen = set()
    ordered = []
    for candidate in discovered + common_guesses:
        candidate = candidate.strip()
        if candidate and candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)
    return ordered


def is_duplicate(url: str, state: Dict, dedup_hours: int = 72) -> bool:
    url_hash = hash_url(url)
    dedup_map = state.get("deduplication", {}).get("url_hash_map", {})
    if url_hash not in dedup_map:
        return False
    last_seen = datetime.fromisoformat(dedup_map[url_hash])
    return (datetime.now() - last_seen) < timedelta(hours=dedup_hours)


def mark_as_seen(url: str, state: Dict):
    if "deduplication" not in state:
        state["deduplication"] = {"url_hash_map": {}}
    state["deduplication"]["url_hash_map"][hash_url(url)] = datetime.now().isoformat()


def get_topic_state(state: Dict, topic_id: str) -> Dict:
    if "topics" not in state:
        state["topics"] = {}
    if topic_id not in state["topics"]:
        state["topics"][topic_id] = {}
    return state["topics"][topic_id]


def get_feed_state(state: Dict, topic_id: str) -> Dict:
    topic_state = get_topic_state(state, topic_id)
    if "feeds" not in topic_state:
        topic_state["feeds"] = {}
    return topic_state["feeds"]


def feed_cache_headers(state: Dict, topic_id: str, feed_url: str) -> Dict[str, str]:
    feed_state = get_feed_state(state, topic_id).get(feed_url, {})
    headers = {"User-Agent": "topic-monitor/1.5 (+feedparser)"}
    if feed_state.get("etag"):
        headers["If-None-Match"] = feed_state["etag"]
    if feed_state.get("modified"):
        headers["If-Modified-Since"] = feed_state["modified"]
    return headers


def update_feed_cache(state: Dict, topic_id: str, feed_url: str, parsed_feed):
    cache = get_feed_state(state, topic_id).setdefault(feed_url, {})
    if getattr(parsed_feed, "etag", None):
        cache["etag"] = parsed_feed.etag
    response_headers = getattr(parsed_feed, "headers", {}) or {}
    if response_headers.get("etag"):
        cache["etag"] = response_headers.get("etag")
    if response_headers.get("last-modified"):
        cache["modified"] = response_headers.get("last-modified")
    cache["last_checked"] = datetime.now().isoformat()
    if getattr(parsed_feed, "status", None) is not None:
        cache["last_status"] = parsed_feed.status
    href = getattr(parsed_feed.feed, "link", None) if getattr(parsed_feed, "feed", None) else None
    if href:
        cache["site_url"] = href
    title = getattr(parsed_feed.feed, "title", None) if getattr(parsed_feed, "feed", None) else None
    if title:
        cache["feed_title"] = title


def iso_from_struct_time(struct_time_value) -> Optional[str]:
    if not struct_time_value:
        return None
    try:
        return datetime(*struct_time_value[:6], tzinfo=timezone.utc).isoformat()
    except Exception:
        return None


def entry_to_result(entry: Dict, feed_url: str, topic: Dict, feed_title: str = "") -> Dict:
    title = entry.get("title", "Untitled")
    summary = entry.get("summary", "") or entry.get("description", "")
    link = entry.get("link", feed_url)
    published = (
        iso_from_struct_time(entry.get("published_parsed"))
        or iso_from_struct_time(entry.get("updated_parsed"))
        or entry.get("published")
        or entry.get("updated")
        or ""
    )
    tags = ", ".join(tag.get("term", "") for tag in entry.get("tags", []) if tag.get("term"))
    source_label = feed_title or topic.get("name", "Feed")

    result = {
        "title": title,
        "url": link,
        "snippet": re.sub(r"\s+", " ", summary).strip(),
        "published_date": published,
        "source": "feed",
        "feed_url": feed_url,
        "feed_title": feed_title,
        "source_label": source_label,
        "tags": tags,
    }

    if "github.com" in feed_url and "/releases.atom" in feed_url:
        repo = feed_url.split("github.com/")[-1].split("/releases.atom")[0]
        result["source"] = "github_release"
        result["github_repo"] = repo
        result["title"] = f"{repo} release: {title}"
        if not result["snippet"]:
            result["snippet"] = f"New GitHub release published for {repo}."
    return result


def search_topic(topic: Dict, dry_run: bool = False, verbose: bool = False) -> List[Dict]:
    query = topic.get("query", "")
    if not query:
        return []

    web_search_plus = Path(os.environ.get(
        "WEB_SEARCH_PLUS_PATH",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "web-search-plus",
            "scripts",
            "search.py",
        ),
    ))

    if web_search_plus.exists():
        import subprocess
        try:
            safe_query = re.sub(r'[\x00-\x1f\x7f]', '', query)[:500]
            if verbose:
                print(f"   🔍 Searching via web-search-plus: {safe_query}")
            result = subprocess.run(
                ["python3", str(web_search_plus), "--query", safe_query, "--max-results", "5"],
                capture_output=True,
                text=True,
                timeout=45,
                env={k: v for k, v in os.environ.items() if k in (
                    "PATH", "HOME", "LANG", "TERM",
                    "SERPER_API_KEY", "TAVILY_API_KEY", "EXA_API_KEY",
                    "YOU_API_KEY", "SEARXNG_INSTANCE_URL", "WSP_CACHE_DIR",
                )},
            )
            if result.returncode == 0:
                stdout = result.stdout.strip()
                json_start = stdout.find('{')
                if json_start >= 0:
                    data = json.loads(stdout[json_start:])
                    results = data.get("results", [])
                    if verbose:
                        print(f"   ✅ Got {len(results)} search results from {data.get('provider', 'unknown')}")
                    for item in results:
                        item.setdefault("source", "web_search")
                    return results
            elif verbose and result.stderr:
                print(f"   ⚠️ web-search-plus error: {result.stderr[:200]}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            print(f"⚠️ web-search-plus timed out for query: {query}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ web-search-plus failed: {e}", file=sys.stderr)
    elif verbose:
        print(f"   ⚠️ web-search-plus not found at {web_search_plus}", file=sys.stderr)

    if dry_run:
        return [{
            "title": f"[Mock] Result for: {query}",
            "url": f"https://example.com/mock-{hashlib.md5(query.encode()).hexdigest()[:8]}",
            "snippet": f"This is a mock/test result for query: {query}. Run without --dry-run to use real search.",
            "published_date": datetime.now().isoformat(),
            "source": "web_search",
        }]
    return []


def fetch_feed_results(topic: Dict, state: Dict, dry_run: bool = False, verbose: bool = False) -> List[Dict]:
    if feedparser is None:
        if verbose:
            print("   ⚠️ feedparser is not installed; skipping feeds", file=sys.stderr)
        return []

    topic_id = topic.get("id")
    explicit_feeds = [normalize_feed_url(url) for url in normalize_text_list(topic.get("feeds", []))]
    github_feeds = [github_release_feed_url(repo) for repo in normalize_text_list(topic.get("github_repos", []))]
    all_feeds = []
    for feed in explicit_feeds + github_feeds:
        if feed and feed not in all_feeds:
            all_feeds.append(feed)

    if not all_feeds:
        return []

    results = []
    for feed_url in all_feeds:
        headers = feed_cache_headers(state, topic_id, feed_url)
        if verbose:
            print(f"   📰 Fetching feed: {feed_url}")
        parsed = feedparser.parse(feed_url, request_headers=headers)
        update_feed_cache(state, topic_id, feed_url, parsed)

        status = getattr(parsed, "status", None)
        if status == 304:
            if verbose:
                print("   ⏭️  Feed not modified (304)")
            continue

        if getattr(parsed, "bozo", False) and not getattr(parsed, "entries", []):
            if verbose:
                print(f"   ⚠️ feed parse issue for {feed_url}: {getattr(parsed, 'bozo_exception', 'unknown')}", file=sys.stderr)
            continue

        feed_title = parsed.feed.get("title", "") if getattr(parsed, "feed", None) else ""
        entries = getattr(parsed, "entries", [])[:10]
        if verbose:
            print(f"   ✅ Got {len(entries)} feed entries")
        for entry in entries:
            results.append(entry_to_result(entry, feed_url, topic, feed_title=feed_title))
    return results


def collect_results(topic: Dict, state: Dict, dry_run: bool = False, verbose: bool = False) -> List[Dict]:
    results = []
    results.extend(search_topic(topic, dry_run=dry_run, verbose=verbose))
    results.extend(fetch_feed_results(topic, state, dry_run=dry_run, verbose=verbose))
    return results


def passes_topic_filters(result: Dict, topic: Dict) -> (bool, str):
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    content = f"{title}\n{snippet}".lower()

    exclude_keywords = [k.lower() for k in normalize_text_list(topic.get("exclude_keywords", []))]
    for keyword in exclude_keywords:
        if keyword in content:
            return False, f"excluded_by_{keyword}"

    required_keywords = [k.lower() for k in normalize_text_list(topic.get("required_keywords", []))]
    missing = [keyword for keyword in required_keywords if keyword not in content]
    if missing:
        return False, f"missing_required_{','.join(missing)}"

    return True, ""


def should_check_topic(topic: Dict, state: Dict, force: bool = False) -> bool:
    if force:
        return True
    topic_state = state.get("topics", {}).get(topic.get("id"), {})
    last_check_str = topic_state.get("last_check")
    if not last_check_str:
        return True
    last_check = datetime.fromisoformat(last_check_str)
    now = datetime.now()
    frequency = topic.get("frequency", "daily")
    if frequency == "hourly":
        return (now - last_check) >= timedelta(hours=1)
    if frequency == "daily":
        return (now - last_check) >= timedelta(days=1)
    if frequency == "weekly":
        return (now - last_check) >= timedelta(weeks=1)
    return False


def check_rate_limits(topic: Dict, state: Dict, settings: Dict) -> bool:
    topic_id = topic.get("id")
    max_per_day = settings.get("max_alerts_per_day", 5)
    max_per_topic_per_day = settings.get("max_alerts_per_topic_per_day", 2)
    topic_state = state.get("topics", {}).get(topic_id, {})
    alerts_today = topic_state.get("alerts_today", 0)
    if alerts_today >= max_per_topic_per_day:
        return False
    total_alerts_today = sum(s.get("alerts_today", 0) for s in state.get("topics", {}).values())
    return total_alerts_today < max_per_day


def sentiment_shifted(topic: Dict, state: Dict, new_sentiment: str) -> bool:
    if not topic.get("alert_on_sentiment_shift"):
        return False
    history = get_topic_state(state, topic.get("id")).get("sentiment_history", [])
    if not history:
        return False
    previous = history[-1].get("sentiment")
    return bool(previous and previous != new_sentiment)


def record_sentiment(topic: Dict, state: Dict, result: Dict, sentiment: str):
    topic_state = get_topic_state(state, topic.get("id"))
    history = topic_state.setdefault("sentiment_history", [])
    history.append({
        "timestamp": datetime.now().isoformat(),
        "sentiment": sentiment,
        "url": result.get("url", ""),
        "title": result.get("title", ""),
    })
    if len(history) > 50:
        del history[:-50]
    topic_state["last_sentiment"] = sentiment


def build_alert_message(topic: Dict, result: Dict, priority: str, score: float, reason: str, sentiment: str, sentiment_shift: bool) -> str:
    emoji_map = {"high": "🔥", "medium": "📌", "low": "📝"}
    source = result.get("source", "web_search")
    source_label = {
        "web_search": "🌐 Web",
        "feed": "📰 Feed",
        "github_release": "🚀 GitHub Release",
    }.get(source, "🌐 Web")
    lines = [f"{emoji_map.get(priority, '📌')} **{topic.get('name', 'Research Alert')}** {topic.get('emoji', '🔍')}", ""]
    lines.append(f"**{result.get('title', 'Untitled')}**")
    lines.append("")
    snippet = result.get("snippet", "")
    if snippet:
        if len(snippet) > 320:
            snippet = snippet[:317] + "..."
        lines.append(snippet)
        lines.append("")
    context = topic.get("context", "")
    if context:
        lines.append(f"💡 _Context: {context}_")
        lines.append("")
    lines.append(f"{source_label}: {result.get('feed_title') or result.get('source_label') or result.get('url', '')}")
    if result.get("url"):
        lines.append(f"🔗 {result['url']}")
    lines.append(f"📊 _Score: {score:.2f} | {reason}_")
    lines.append(f"🙂 _Sentiment: {sentiment}_")
    if sentiment_shift:
        lines.append("🔄 _Sentiment shift detected_")
    return "\n".join(lines)


def send_alert(topic: Dict, result: Dict, priority: str, score: float, reason: str, sentiment: str, sentiment_shift: bool = False, dry_run: bool = False):
    channels = topic.get("channels", [])
    message = build_alert_message(topic, result, priority, score, reason, sentiment, sentiment_shift)

    if dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - Would send alert:")
        print(f"Channels: {', '.join(channels)}")
        print(f"Priority: {priority.upper()}")
        print()
        print(message)
        print(f"{'='*60}\n")
        return None

    alert_ids = []
    for channel in channels:
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
            "channel": channel,
            "topic_id": topic.get("id"),
            "topic_name": topic.get("name"),
            "title": result.get("title", ""),
            "snippet": result.get("snippet", ""),
            "url": result.get("url", ""),
            "score": score,
            "reason": reason,
            "message": message,
            "context": topic.get("context", ""),
            "sentiment": sentiment,
            "sentiment_shift": sentiment_shift,
            "source": result.get("source", "web_search"),
            "feed_url": result.get("feed_url", ""),
            "github_repo": result.get("github_repo", ""),
        }
        alert_id = queue_alert(alert_data)
        alert_ids.append(alert_id)
        print(f"📢 ALERT_QUEUED: {json.dumps({'id': alert_id, 'channel': channel, 'priority': priority, 'topic': topic.get('name'), 'sentiment': sentiment})}")
    return alert_ids


def monitor_topic(topic: Dict, state: Dict, settings: Dict, dry_run: bool = False, verbose: bool = False):
    topic_id = topic.get("id")
    topic_name = topic.get("name")
    if verbose:
        print(f"\n🔍 Checking topic: {topic_name} ({topic_id})")

    results = collect_results(topic, state, dry_run=dry_run, verbose=verbose)
    if verbose:
        print(f"   Found {len(results)} total results across all sources")

    dedup_hours = settings.get("deduplication_window_hours", 72)
    high_priority = []
    medium_priority = []

    for result in results:
        url = result.get("url", "") or result.get("feed_url", "")
        if not url:
            continue

        if is_duplicate(url, state, dedup_hours):
            if verbose:
                print(f"   ⏭️  Skipping duplicate: {url}")
            continue

        passes, filter_reason = passes_topic_filters(result, topic)
        if not passes:
            if verbose:
                print(f"   🚫 Filtered out: {filter_reason} - {result.get('title', '')[:60]}")
            mark_as_seen(url, state)
            continue

        priority, score, reason, sentiment = score_result(result, topic, settings)
        sentiment_shift = sentiment_shifted(topic, state, sentiment)

        # alert_on override: if the result source matches alert_on config, force high priority
        alert_on = normalize_text_list(topic.get("alert_on", []))
        result_source = result.get("source", "")
        if alert_on and result_source in alert_on:
            priority = "high"
            score = max(score, 0.9)
            reason = f"alert_on:{result_source}"
            if verbose:
                print(f"   🚨 alert_on match: {result_source} → forced HIGH priority")

        if sentiment_shift and priority == "medium":
            priority = "high"
            reason = f"{reason} + sentiment_shift"
        elif sentiment_shift and priority == "low":
            priority = "medium"
            reason = f"{reason} + sentiment_shift"

        if verbose:
            print(f"   {priority.upper():6} ({score:.2f}) [{sentiment}] - {result.get('title', '')[:55]}...")

        if priority == "high":
            high_priority.append((result, score, reason, sentiment, sentiment_shift))
        elif priority == "medium":
            medium_priority.append((result, score, reason, sentiment, sentiment_shift))

        mark_as_seen(url, state)
        if not dry_run:
            record_sentiment(topic, state, result, sentiment)

    for result, score, reason, sentiment, sentiment_shift in high_priority:
        if check_rate_limits(topic, state, settings):
            send_alert(topic, result, "high", score, reason, sentiment, sentiment_shift, dry_run=dry_run)
            if not dry_run:
                topic_state = get_topic_state(state, topic_id)
                topic_state["alerts_today"] = topic_state.get("alerts_today", 0) + 1
        elif verbose:
            print("   ⚠️ Rate limit reached, skipping alert")

    date_str = datetime.now().strftime("%Y-%m-%d")
    for result, score, reason, sentiment, sentiment_shift in medium_priority:
        if not dry_run:
            save_finding(topic_id, date_str, {
                "result": result,
                "score": score,
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
                "sentiment": sentiment,
                "sentiment_shift": sentiment_shift,
            })
        if verbose:
            print(f"   💾 Saved to digest: {result.get('title', '')[:50]}...")

    if not dry_run:
        topic_state = get_topic_state(state, topic_id)
        topic_state["last_check"] = datetime.now().isoformat()
        topic_state["last_results_count"] = len(results)
        topic_state["findings_count"] = topic_state.get("findings_count", 0) + len(medium_priority)


def main():
    parser = argparse.ArgumentParser(description="Monitor research topics")
    parser.add_argument("--dry-run", action="store_true", help="Don't send alerts or save state")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--topic", help="Check specific topic by ID")
    parser.add_argument("--force", action="store_true", help="Force check even if not due")
    parser.add_argument("--frequency", choices=["hourly", "daily", "weekly"], help="Only check topics with this frequency")
    parser.add_argument("--discover-feed", metavar="URL", help="Discover RSS/Atom feed links for a URL and exit")
    args = parser.parse_args()

    if args.discover_feed:
        for item in discover_feed_urls(args.discover_feed):
            print(item)
        return

    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    state = load_state()
    settings = get_settings()
    topics = config.get("topics", [])
    if not topics:
        print("⚠️ No topics configured", file=sys.stderr)
        sys.exit(0)

    topics_to_check = []
    for topic in topics:
        if args.topic and topic.get("id") != args.topic:
            continue
        if args.frequency and topic.get("frequency") != args.frequency:
            continue
        if should_check_topic(topic, state, force=args.force):
            topics_to_check.append(topic)

    if not topics_to_check:
        if args.verbose:
            print("✅ No topics due for checking")
        sys.exit(0)

    print(f"🔍 Monitoring {len(topics_to_check)} topic(s)...")
    for topic in topics_to_check:
        try:
            monitor_topic(topic, state, settings, dry_run=args.dry_run, verbose=args.verbose)
        except Exception as e:
            print(f"❌ Error monitoring {topic.get('name')}: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()

    if not args.dry_run:
        save_state(state)
        print("✅ State saved")
    print("✅ Monitoring complete")


if __name__ == "__main__":
    main()
