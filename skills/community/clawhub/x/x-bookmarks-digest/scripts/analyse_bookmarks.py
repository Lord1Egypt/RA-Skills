#!/usr/bin/env python3
"""Categorise and score X bookmarks for digest generation."""

import argparse
import json
import re
import sys
from urllib.parse import urlparse

# Category keywords — matched against bookmark text (case-insensitive)
CATEGORY_SIGNALS = {
    "tool": [
        "cli", "tool", "utility", "command-line", "terminal", "sdk",
        "library", "framework", "package", "npm", "pip", "brew",
        "cargo", "gem", "crate", "binary", "executable",
    ],
    "project": [
        "github.com", "gitlab.com", "repo", "repository", "open source",
        "open-source", "oss", "just shipped", "just released", "v1", "v2",
        "launched", "release", "source code",
    ],
    "product": [
        "saas", "app", "platform", "startup", "launched", "product",
        "pricing", "beta", "waitlist", "sign up", "try it",
        "subscription", "freemium",
    ],
    "insight": [
        "tip", "trick", "pattern", "architecture", "design", "approach",
        "technique", "best practice", "lesson", "learned", "mistake",
        "how i", "how we", "thread", "here's what",
    ],
    "resource": [
        "article", "blog", "tutorial", "guide", "paper", "course",
        "video", "talk", "presentation", "documentation", "docs",
        "cheatsheet", "cheat sheet", "book",
    ],
}

# High-value domain signals (boost relevance)
HIGH_VALUE_DOMAINS = [
    "github.com", "gitlab.com", "arxiv.org", "huggingface.co",
    "news.ycombinator.com",
]

# Tech keywords that boost relevance for this user's stack
STACK_KEYWORDS = [
    "python", "typescript", "swift", "fastapi", "react", "postgresql",
    "docker", "cloudflare", "llm", "ai", "agent", "automation",
    "mcp", "claude", "anthropic", "openai", "gpt", "embedding",
    "rag", "vector", "duckdb", "sqlite", "hetzner", "caddy",
]


def extract_urls(text: str) -> list[str]:
    """Extract all URLs from text."""
    return re.findall(r'https?://[^\s<>"\')\]]+', text)


def extract_github_repos(urls: list[str]) -> list[str]:
    """Extract GitHub user/repo paths from URLs."""
    repos = []
    for url in urls:
        parsed = urlparse(url)
        if parsed.hostname in ("github.com", "www.github.com"):
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 2:
                repo = f"{parts[0]}/{parts[1]}"
                if repo not in repos:
                    repos.append(repo)
    return repos


def categorise(text: str, urls: list[str]) -> str:
    """Determine the primary category of a bookmark."""
    text_lower = text.lower()
    full_text = text_lower + " " + " ".join(urls).lower()

    scores = {}
    for category, keywords in CATEGORY_SIGNALS.items():
        score = sum(1 for kw in keywords if kw in full_text)
        if score > 0:
            scores[category] = score

    if not scores:
        return "other"

    return max(scores, key=scores.get)


def score_relevance(text: str, urls: list[str], category: str) -> int:
    """Score relevance 1-5 based on signals."""
    text_lower = text.lower()
    score = 2  # base score

    # GitHub repos boost
    github_repos = extract_github_repos(urls)
    if github_repos:
        score += 1

    # High-value domains
    for url in urls:
        parsed = urlparse(url)
        if parsed.hostname and any(d in parsed.hostname for d in HIGH_VALUE_DOMAINS):
            score += 1
            break

    # Stack-relevant keywords
    stack_hits = sum(1 for kw in STACK_KEYWORDS if kw in text_lower)
    if stack_hits >= 2:
        score += 1
    elif stack_hits >= 1:
        score += 0  # mild interest, no boost

    # Tool/project categories inherently more actionable
    if category in ("tool", "project"):
        score += 1

    return min(5, max(1, score))


def analyse_bookmark(bookmark: dict) -> dict:
    """Analyse a single bookmark and return enriched data."""
    text = bookmark.get("text", "")
    author = bookmark.get("author_username", bookmark.get("username", "unknown"))
    bm_id = bookmark.get("id", "")
    created = bookmark.get("created_at", "")

    # Handle nested author object (X API v2 format with expansions)
    if isinstance(bookmark.get("author"), dict):
        author = bookmark["author"].get("username", author)

    urls = extract_urls(text)
    # Also check entities.urls if present (X API v2)
    entities = bookmark.get("entities", {})
    if isinstance(entities, dict):
        for url_entity in entities.get("urls", []):
            expanded = url_entity.get("expanded_url", "")
            if expanded and expanded not in urls:
                urls.append(expanded)

    github_repos = extract_github_repos(urls)
    category = categorise(text, urls)
    relevance = score_relevance(text, urls, category)

    return {
        "id": bm_id,
        "text": text[:500],  # Truncate very long tweets
        "author": f"@{author}" if not author.startswith("@") else author,
        "created_at": created,
        "category": category,
        "relevance": relevance,
        "urls": urls,
        "github_repos": github_repos,
        "keywords": extract_keywords(text),
    }


def extract_keywords(text: str) -> list[str]:
    """Extract relevant tech keywords found in text."""
    text_lower = text.lower()
    return [kw for kw in STACK_KEYWORDS if kw in text_lower]


def main():
    parser = argparse.ArgumentParser(description="Analyse X bookmarks")
    parser.add_argument("--file", help="Read bookmarks from file instead of stdin")
    parser.add_argument("--min-relevance", type=int, default=1, help="Minimum relevance score to include (1-5)")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            bookmarks = json.load(f)
    else:
        raw = sys.stdin.read()
        if not raw.strip():
            print(json.dumps({"summary": {"total": 0, "new": 0, "high": 0, "medium": 0, "low": 0}, "bookmarks": []}))
            return
        bookmarks = json.loads(raw)

    if not isinstance(bookmarks, list):
        bookmarks = [bookmarks]

    analysed = []
    for bm in bookmarks:
        result = analyse_bookmark(bm)
        if result["relevance"] >= args.min_relevance:
            analysed.append(result)

    # Sort by relevance descending
    analysed.sort(key=lambda x: x["relevance"], reverse=True)

    high = sum(1 for b in analysed if b["relevance"] >= 4)
    medium = sum(1 for b in analysed if b["relevance"] == 3)
    low = sum(1 for b in analysed if b["relevance"] <= 2)

    output = {
        "summary": {
            "total": len(bookmarks),
            "new": len(analysed),
            "high": high,
            "medium": medium,
            "low": low,
        },
        "bookmarks": analysed,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
