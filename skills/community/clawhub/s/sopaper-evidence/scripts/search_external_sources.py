#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote_plus, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

from url_safety import assert_public_http_url, is_safe_public_http_url


QUERY_LINE_RE = re.compile(r"^- Query:\s*(.+)\s*$")
RESULT_LINK_RE = re.compile(
    r'<a[^>]+class="result__a"[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
REQUEST_TIMEOUT = 8
MAX_QUERIES = 16
SECONDARY_HOSTS = {
    "theaireport.net",
    "sourcegraph.com",
    "alphaxiv.org",
    "www.alphaxiv.org",
    "catalyzex.com",
    "www.catalyzex.com",
}
PRIMARY_HOSTS = {
    "arxiv.org",
    "openreview.net",
    "aclanthology.org",
    "github.com",
    "huggingface.co",
    "openai.com",
}
GENERIC_TOPIC_TERMS = {
    "a",
    "an",
    "and",
    "arxiv",
    "assistant",
    "assistants",
    "benchmark",
    "benchmarks",
    "dataset",
    "datasets",
    "documentation",
    "evaluation",
    "for",
    "github",
    "in",
    "of",
    "official",
    "on",
    "paper",
    "repo",
    "the",
    "theme",
    "topic",
    "work",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search external sources from a topic or query plan and emit a markdown source list."
    )
    parser.add_argument("--topic", help="Research topic used to build default queries.")
    parser.add_argument("--plan", help="Markdown search-plan file containing '- Query:' lines.")
    parser.add_argument("--output", required=True, help="Markdown output file.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum number of results. Default: 8")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    queries = collect_queries(args.topic, args.plan)
    if not queries:
        print("No queries available. Provide --topic or --plan.", file=sys.stderr)
        return 1

    topic_terms = extract_topic_terms([args.topic]) if args.topic else extract_topic_terms(queries)
    results = search_queries(queries, args.limit, topic_terms)
    output = render_source_list(args.topic or "Topic search", queries, results)
    path = Path(args.output).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")
    print(path)
    return 0


def collect_queries(topic: str | None, plan_path: str | None) -> list[str]:
    queries: list[str] = []
    if topic:
        queries.extend(
            [
                f"{topic} paper arxiv benchmark",
                f"{topic} benchmark dataset",
                f"{topic} github repo",
                f"{topic} official documentation",
            ]
        )
        queries.extend(expand_topic_queries(topic))
    if plan_path:
        text = Path(plan_path).expanduser().resolve().read_text(encoding="utf-8")
        queries.extend(match.group(1).strip() for match in QUERY_LINE_RE.finditer(text))
    deduped: list[str] = []
    seen: set[str] = set()
    for query in queries:
        if query not in seen:
            seen.add(query)
            deduped.append(query)
    return deduped[:MAX_QUERIES]


def search_queries(queries: list[str], limit: int, topic_terms: set[str]) -> list[dict[str, str]]:
    seen_url: set[str] = set()
    best_by_title: dict[str, dict[str, str]] = {}

    for query in queries:
        for result in search_sources(query):
            if should_skip_result(result["url"]):
                continue
            overlap = result_overlap(result["title"], result["url"], topic_terms)
            result_tokens = tokenize_text(result["title"]) | tokenize_text(canonicalize_url(result["url"]))
            if "code" in topic_terms and "code" not in result_tokens:
                continue
            if not query_semantic_gate(query, result["title"], result["url"], overlap, topic_terms):
                continue
            if topic_terms and overlap < minimum_overlap(result["url"], result["title"]):
                continue
            canonical = canonicalize_url(result["url"])
            if canonical in seen_url:
                continue
            seen_url.add(canonical)
            enriched = result | {
                "query": query,
                "score": result_score(result["url"], result["title"], overlap),
            }
            title_key = canonicalize_title(result["title"])
            current = best_by_title.get(title_key)
            if current is None or enriched["score"] > current["score"]:
                best_by_title[title_key] = enriched

    ranked = sorted(best_by_title.values(), key=lambda item: (-item["score"], item["title"]))
    return ranked[:limit]


def search_sources(query: str) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    results.extend(search_openalex(query))
    results.extend(search_github_repositories(query))
    return results


def expand_topic_queries(topic: str) -> list[str]:
    lowered = topic.lower()
    queries: list[str] = []
    if any(
        token in lowered
        for token in ["openclaw", "manipulation", "robot", "robotic", "embodied", "long-horizon"]
    ):
        queries.extend(
            [
                f"{topic} RLBench",
                f"{topic} CALVIN benchmark",
                f"{topic} ManiSkill benchmark",
                f"{topic} RoboCasa benchmark",
                f"{topic} long-horizon manipulation benchmark",
                f"{topic} embodied manipulation evaluation",
                "long-horizon manipulation benchmark",
                "robotic manipulation benchmark",
                "RLBench manipulation benchmark",
                "CALVIN long-horizon manipulation benchmark",
                "ManiSkill manipulation benchmark",
                "RoboCasa manipulation benchmark",
            ]
        )
    if any(token in lowered for token in ["browser", "browsing", "web agent", "browser agent"]):
        queries.extend(
            [
                f"{topic} BrowseComp",
                f"{topic} WebArena benchmark",
                f"{topic} browsing agents benchmark",
            ]
        )
    if any(token in lowered for token in ["retrieval", "citation", "rag", "code assistant", "code assistants"]):
        queries.extend(
            [
                f"{topic} code retrieval benchmark",
                f"{topic} citation benchmark",
                f"{topic} grounded generation retrieval benchmark",
                "code information retrieval benchmark",
                "code retrieval benchmark",
                "code retrieval evaluation benchmark",
                "citation-grounded QA benchmark",
                "citation-grounded code benchmark",
                "code assistant retrieval benchmark",
                "grounded generation citation benchmark",
            ]
        )
    return queries


def extract_topic_terms(queries: list[str]) -> set[str]:
    terms: set[str] = set()
    for query in queries:
        for token in tokenize_text(query):
            if len(token) < 3 or token in GENERIC_TOPIC_TERMS:
                continue
            terms.add(token)
    return terms


def result_overlap(title: str, url: str, topic_terms: set[str]) -> int:
    haystack_tokens = tokenize_text(title) | tokenize_text(canonicalize_url(url))
    matched = {term for term in topic_terms if term in haystack_tokens}
    return len(matched)


def minimum_overlap(url: str, title: str) -> int:
    host = urlparse(url).netloc.lower()
    if "github.com" in host:
        return 1
    lowered = title.lower()
    if any(token in lowered for token in ["benchmark", "evaluation", "dataset", "leaderboard"]):
        return 1
    return 2


def query_semantic_gate(query: str, title: str, url: str, overlap: int, topic_terms: set[str]) -> bool:
    query_tokens = tokenize_text(query)
    title_tokens = tokenize_text(title) | tokenize_text(canonicalize_url(url))
    benchmark_tokens = {"benchmark", "evaluation", "leaderboard", "dataset"}
    repo_tokens = {"repo", "github", "implementation"}
    host = urlparse(url).netloc.lower()

    if query_tokens & benchmark_tokens and not (title_tokens & benchmark_tokens):
        return False
    if query_tokens & repo_tokens and "github.com" not in host:
        return False
    if "github.com" in host:
        if len(title) > 260:
            return False
        if query_tokens & benchmark_tokens and overlap < 2:
            return False
        if "code" in topic_terms and "code" not in title_tokens:
            return False
        if "citation" in topic_terms and "citation" not in title_tokens and "grounded" not in title_tokens:
            return False
    return True


def search_openalex(query: str) -> list[dict[str, str]]:
    url = "https://api.openalex.org/works?" + urlencode(
        {
            "search": query,
            "per-page": 8,
            "filter": "type:article|preprint|dataset",
            "select": "display_name,primary_location,locations,ids",
        }
    )
    assert_public_http_url(url)
    request = Request(
        url,
        headers={
            "User-Agent": (
                "SopaperEvidence/0.6 (+https://github.com/sheepxux/SoPaper-Evidence)"
            )
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    results: list[dict[str, str]] = []
    for item in payload.get("results", []):
        title = clean_text(item.get("display_name", ""))
        if not title:
            continue
        url = choose_openalex_url(item)
        if not url:
            continue
        results.append({"title": title, "url": url})
    return results


def choose_openalex_url(item: dict) -> str | None:
    primary = item.get("primary_location") or {}
    for candidate in [
        primary.get("landing_page_url"),
        primary.get("pdf_url"),
    ]:
        if candidate and is_safe_public_http_url(candidate):
            return candidate

    for location in item.get("locations", []):
        for candidate in [
            location.get("landing_page_url"),
            location.get("pdf_url"),
        ]:
            if candidate and is_safe_public_http_url(candidate):
                return candidate

    ids = item.get("ids") or {}
    for key in ["doi", "arxiv", "openalex"]:
        candidate = ids.get(key)
        if candidate and is_safe_public_http_url(candidate):
            return candidate
    return None


def search_github_repositories(query: str) -> list[dict[str, str]]:
    url = "https://api.github.com/search/repositories?" + urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": 5,
        }
    )
    assert_public_http_url(url)
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": (
                "SopaperEvidence/0.6 (+https://github.com/sheepxux/SoPaper-Evidence)"
            ),
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except Exception:
        return []

    results: list[dict[str, str]] = []
    for item in payload.get("items", []):
        title = clean_text(item.get("full_name", ""))
        description = clean_text(item.get("description", ""))
        href = item.get("html_url", "")
        combined = title if not description else f"{title}: {description}"
        if combined and is_safe_public_http_url(href):
            results.append({"title": combined, "url": href})
    return results


def search_duckduckgo(query: str) -> list[dict[str, str]]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    assert_public_http_url(url)
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except Exception:
        return []
    if "anomaly-modal__title" in raw or "bots use DuckDuckGo too" in raw:
        return []
    results: list[dict[str, str]] = []
    for match in RESULT_LINK_RE.finditer(raw):
        href = extract_result_url(match.group("href"))
        title = clean_text(re.sub(r"<[^>]+>", " ", match.group("title")))
        if title and href and is_safe_public_http_url(href):
            results.append({"title": title, "url": href})
    return results


def render_source_list(topic: str, queries: list[str], results: list[dict[str, str]]) -> str:
    lines = [
        "# Topic Search Source List",
        "",
        f"- Topic: {topic}",
        "",
        "## Queries",
        "",
    ]
    for query in queries:
        lines.append(f"- Query: {query}")

    lines.extend(["", "## Results", ""])
    if not results:
        lines.append("- No results found.")
    for result in results:
        host = urlparse(result["url"]).netloc
        lines.append(f"- [{escape_brackets(result['title'])}]({result['url']})")
        lines.append(f"  - Source host: {host}")
        lines.append(f"  - Found via query: {result['query']}")
    lines.append("")
    return "\n".join(lines)


def extract_result_url(href: str) -> str:
    if href.startswith("//"):
        href = "https:" + href
    href = html.unescape(href)
    parsed = urlparse(href)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        uddg = parse_qs(parsed.query).get("uddg")
        if uddg:
            return unquote(uddg[0])
    return href


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.netloc.lower()}{parsed.path.rstrip('/')}"


def should_skip_result(url: str) -> bool:
    if not is_safe_public_http_url(url):
        return True
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    return (
        "duckduckgo.com" in host
        or parsed.path.endswith(".pdf")
        or "researchgate.net" in host
        or "semanticscholar.org" in host
        or "bing.com" in host
    )


def result_score(url: str, title: str, overlap: int) -> int:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    score = 0
    score += overlap * 4
    if host in PRIMARY_HOSTS:
        score += 10
    if host in SECONDARY_HOSTS:
        score -= 3
    if "github.com" in host:
        score += 2
    if "arxiv.org" in host or "openreview.net" in host or "aclanthology.org" in host:
        score += 4
    lowered_title = title.lower()
    if any(token in lowered_title for token in ["benchmark", "dataset", "evaluation", "agents", "retrieval"]):
        score += 2
    if any(token in lowered_title for token in ["blog", "news", "report"]):
        score -= 2
    return score


def canonicalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def tokenize_text(value: str) -> set[str]:
    return {normalize_token(token) for token in re.findall(r"[a-z0-9]+", value.lower())}


def normalize_token(token: str) -> str:
    if len(token) > 4 and token.endswith("s"):
        return token[:-1]
    return token


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def escape_brackets(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]")


if __name__ == "__main__":
    raise SystemExit(main())
