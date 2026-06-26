#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

API_URL = "https://api.tavily.com/search"
DEFAULT_NOISY_DOMAINS = {
    "facebook.com",
    "m.facebook.com",
    "reddit.com",
    "www.reddit.com",
    "pinterest.com",
    "www.pinterest.com",
    "instagram.com",
    "www.instagram.com",
    "x.com",
    "twitter.com",
    "quora.com",
    "www.quora.com",
}
OFFICIAL_DOMAIN_HINTS = {
    "openclaw": ["docs.openclaw.ai", "github.com", "openclaw.ai", "clawhub.com", "clawhub.ai"],
    "wsl": ["learn.microsoft.com", "github.com", "ubuntu.com", "microsoft.com"],
    "ubuntu": ["ubuntu.com", "help.ubuntu.com", "documentation.ubuntu.com", "learn.microsoft.com"],
    "tavily": ["tavily.com", "docs.tavily.com"],
}
INTENT_KEYWORDS = {
    "release": ["release", "release notes", "changelog", "what's changed", "patch notes", "latest version", "更新", "更新日志", "发行说明"],
    "docs": ["docs", "documentation", "guide", "how to", "install", "setup", "configure", "配置", "教程", "安装"],
    "issue": ["error", "bug", "issue", "problem", "failed", "fix", "troubleshoot", "报错", "问题", "失败"],
    "news": ["news", "latest news", "today", "funding", "announcement", "动态", "新闻"],
}


def load_api_key(args: argparse.Namespace) -> str:
    if args.api_key:
        return args.api_key.strip()
    env_key = os.environ.get("TAVILY_API_KEY", "").strip()
    if env_key:
        return env_key
    skill_dir = Path(__file__).resolve().parent.parent
    candidates = [
        skill_dir / ".secrets" / "tavily.key",
    ]
    for path in candidates:
        if path.exists():
            value = path.read_text(encoding="utf-8").strip()
            if value:
                return value
    raise SystemExit(
        "Missing Tavily API key. Provide --api-key, set TAVILY_API_KEY, or put the key in .secrets/tavily.key"
    )


def extract_host(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower()
    except Exception:
        return ""


def extract_path(url: str) -> str:
    try:
        return (urlparse(url).path or "/").lower()
    except Exception:
        return "/"


def host_matches(host: str, domain: str) -> bool:
    domain = domain.lower()
    return host == domain or host.endswith("." + domain)


def infer_official_domains(query: str) -> list[str]:
    q = query.lower()
    domains: list[str] = []
    for keyword, hints in OFFICIAL_DOMAIN_HINTS.items():
        if keyword in q:
            for hint in hints:
                if hint not in domains:
                    domains.append(hint)
    return domains


def detect_intents(query: str, topic: str) -> set[str]:
    q = query.lower()
    intents: set[str] = set()
    if topic == "news":
        intents.add("news")
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in q for keyword in keywords):
            intents.add(intent)
    return intents


def build_payload(args: argparse.Namespace, api_key: str) -> dict:
    payload = {
        "api_key": api_key,
        "query": args.query,
        "topic": args.topic,
        "search_depth": args.search_depth,
        "max_results": args.max_results,
        "include_answer": args.include_answer,
        "include_raw_content": args.include_raw_content,
        "include_images": args.include_images,
    }
    include_domains = list(args.include_domains)
    if args.official_first:
        for domain in infer_official_domains(args.query):
            if domain not in include_domains:
                include_domains.append(domain)
    exclude_domains = list(args.exclude_domains)
    if args.exclude_noisy_default:
        for domain in sorted(DEFAULT_NOISY_DOMAINS):
            if domain not in exclude_domains:
                exclude_domains.append(domain)
    if args.days is not None:
        payload["days"] = args.days
    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains
    if args.country:
        payload["country"] = args.country
    if args.time_range:
        payload["time_range"] = args.time_range
    return payload


def call_tavily(payload: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Tavily HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error calling Tavily: {e}")


def clean_text(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = (parsed.path or "/").rstrip("/") or "/"
    return f"{host}{path}"


def dedupe_results(results: list[dict]) -> list[dict]:
    seen: set[str] = set()
    deduped: list[dict] = []
    for item in results:
        url = item.get("url") or ""
        key = normalize_url(url) if url else json.dumps(item, sort_keys=True, ensure_ascii=False)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def path_score(host: str, path: str, intents: set[str], official_domains: list[str], query: str) -> int:
    score = 0
    q = query.lower()
    if any(host_matches(host, d) for d in official_domains):
        score += 80

    if "docs.openclaw.ai" in host:
        score += 70
    if host == "github.com":
        if "/openclaw/openclaw/releases" in path:
            score += 130
        elif "/openclaw/openclaw/blob/" in path or "/openclaw/openclaw/tree/" in path:
            score += 70
        elif "/openclaw/openclaw/issues/" in path:
            score += 45 if "issue" in intents else 20
        elif "/orgs/community/discussions/" in path:
            score -= 35
        elif "/discussions/" in path:
            score -= 25
        elif "/openclaw/openclaw" in path:
            score += 60
        if "openclaw" in q:
            if "/openclaw/openclaw-ansible" in path:
                score -= 55
            elif "/openclaw/" in path and "/openclaw/openclaw" not in path:
                score -= 15
    if host.endswith("learn.microsoft.com"):
        score += 75 if ("docs" in intents or "issue" in intents or "release" in intents) else 40
    if host.endswith("ubuntu.com") or host.endswith("help.ubuntu.com") or host.endswith("documentation.ubuntu.com"):
        score += 65
    if host.endswith("tavily.com") or host.endswith("docs.tavily.com"):
        score += 70

    if "release" in intents:
        if any(token in path for token in ["/releases", "/release", "/changelog", "/patch", "/updates", "/release-notes"]):
            score += 50
        if any(token in path for token in ["/issues", "/discussion", "/discussions"]):
            score -= 25
    if "docs" in intents:
        if any(token in path for token in ["/docs", "/documentation", "/guide", "/install", "/setup", "/configure", "/config", "/help"]):
            score += 45
    if "issue" in intents:
        if any(token in path for token in ["/issues", "/troubleshoot", "/troubleshooting", "/faq", "/questions"]):
            score += 35
        if any(token in path for token in ["/releases", "/changelog"]):
            score += 10
    if "news" in intents:
        if any(token in path for token in ["/news", "/blog", "/updates", "/announcements"]):
            score += 30

    return score


def label_source(host: str, path: str, intents: set[str], official_domains: list[str]) -> str:
    if any(host_matches(host, d) for d in official_domains):
        if host == "github.com" and "/openclaw/openclaw/releases" in path:
            return "official-release"
        if host.startswith("docs.") or "/docs" in path or "/documentation" in path:
            return "official-docs"
        return "official"
    if any(host_matches(host, d) for d in DEFAULT_NOISY_DOMAINS):
        return "noisy"
    if host == "github.com" and "/issues/" in path:
        return "issue"
    if host == "github.com" and "/discussions/" in path:
        return "community"
    if "news" in intents:
        return "news"
    return "reference"


def score_item(item: dict, args: argparse.Namespace, official_domains: list[str], intents: set[str]) -> tuple:
    url = item.get("url") or ""
    host = extract_host(url)
    path = extract_path(url)
    noisy = args.exclude_noisy_default and any(host_matches(host, d) for d in DEFAULT_NOISY_DOMAINS)
    title = (item.get("title") or "").strip()
    content = (item.get("content") or "").strip()
    content_len = len(content)
    semantic = path_score(host, path, intents, official_domains, args.query)
    return (
        1 if noisy else 0,
        -semantic,
        0 if content_len > 0 else 1,
        -min(content_len, 500),
        len(title) == 0,
        host,
        path,
    )


def annotate_and_reorder_results(results: list[dict], args: argparse.Namespace) -> list[dict]:
    official_domains = infer_official_domains(args.query) if args.official_first else []
    intents = detect_intents(args.query, args.topic)
    deduped = dedupe_results(results)
    sorted_items = sorted(deduped, key=lambda item: score_item(item, args, official_domains, intents))
    annotated: list[dict] = []
    for item in sorted_items:
        cloned = dict(item)
        url = cloned.get("url") or ""
        host = extract_host(url)
        path = extract_path(url)
        cloned["_host"] = host
        cloned["_path"] = path
        cloned["_source_label"] = label_source(host, path, intents, official_domains)
        cloned["_path_score"] = path_score(host, path, intents, official_domains, args.query)
        annotated.append(cloned)
    return annotated


def print_text(result: dict, args: argparse.Namespace) -> None:
    answer = result.get("answer")
    if answer:
        print(f"Answer: {clean_text(answer, args.answer_max_chars)}\n")

    results = annotate_and_reorder_results(result.get("results") or [], args)
    if not results:
        print("No results.")
        return

    for i, item in enumerate(results[: args.show_results], start=1):
        title = item.get("title") or "(no title)"
        url = item.get("url") or ""
        content = clean_text(item.get("content") or "", args.snippet_max_chars)
        host = item.get("_host") or extract_host(url)
        source_label = item.get("_source_label") or "reference"
        path_score_value = item.get("_path_score", 0)
        print(f"[{i}] {title}")
        if url:
            print(url)
        if host:
            print(f"host: {host} | type: {source_label} | score: {path_score_value}")
        if content:
            print(content)
        print()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search the web with Tavily.")
    p.add_argument("query", help="Search query")
    p.add_argument("--api-key", help="Tavily API key (overrides env/file)")
    p.add_argument("--topic", default="general", choices=["general", "news"], help="Tavily topic")
    p.add_argument("--search-depth", default="advanced", choices=["basic", "advanced"], help="Search depth")
    p.add_argument("--max-results", type=int, default=10, help="Max results to request from Tavily")
    p.add_argument("--show-results", type=int, default=5, help="How many results to print after ranking")
    p.add_argument("--days", type=int, help="Limit news recency in days")
    p.add_argument("--country", help="Country code, when supported by Tavily")
    p.add_argument("--time-range", choices=["day", "week", "month", "year"], help="Time range hint")
    p.add_argument("--include-answer", action="store_true", help="Ask Tavily for synthesized answer")
    p.add_argument("--include-raw-content", action="store_true", help="Include raw page content when available")
    p.add_argument("--include-images", action="store_true", help="Include image results when available")
    p.add_argument("--include-domains", nargs="*", default=[], help="Only search these domains")
    p.add_argument("--exclude-domains", nargs="*", default=[], help="Exclude these domains")
    p.add_argument("--official-first", action="store_true", default=True, help="Prefer inferred official domains when query matches known products/topics (default: on)")
    p.add_argument("--no-official-first", dest="official_first", action="store_false", help="Disable inferred official-domain preference")
    p.add_argument("--exclude-noisy-default", action="store_true", default=True, help="Exclude common noisy social/content-farm domains by default")
    p.add_argument("--no-exclude-noisy-default", dest="exclude_noisy_default", action="store_false", help="Disable default noisy-domain exclusion")
    p.add_argument("--snippet-max-chars", type=int, default=320, help="Max characters per printed result snippet")
    p.add_argument("--answer-max-chars", type=int, default=240, help="Max characters for printed synthesized answer")
    p.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds")
    p.add_argument("--json", action="store_true", help="Print raw JSON")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    api_key = load_api_key(args)
    payload = build_payload(args, api_key)
    result = call_tavily(payload, timeout=args.timeout)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result, args)


if __name__ == "__main__":
    main()
