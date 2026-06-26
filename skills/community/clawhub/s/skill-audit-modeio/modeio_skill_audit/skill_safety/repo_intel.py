from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

GITHUB_API_BASE = "https://api.github.com"
GITHUB_REMOTE_RE = re.compile(
    r"(?:https?://github\.com/|git@github\.com:|ssh://git@github\.com/)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?$",
    re.IGNORECASE,
)

HIGH_RISK_TEXT_RULES: Sequence[Tuple[re.Pattern[str], str]] = [
    (
        re.compile(
            r"\b(prompt[-_\s]+injection)\b.{0,80}\b(demo|attack|exploit|payload|proof[- ]?of[- ]?concept|poc)\b|"
            r"\b(demo|attack|exploit|payload|proof[- ]?of[- ]?concept|poc)\b.{0,80}\b(prompt[-_\s]+injection)\b",
            re.IGNORECASE,
        ),
        "prompt injection attack/demo content",
    ),
    (
        re.compile(
            r"\b(malware|backdoor|stealer|token\s+exfil(?:tration)?|credential\s+theft|"
            r"ransomware|phishing(?:\s+kit)?)\b",
            re.IGNORECASE,
        ),
        "malware or credential-theft content",
    ),
    (
        re.compile(
            r"\b(supply[- ]?chain|dependency\s+confusion)\b.{0,80}\b(attack|exploit|malicious|poison)\b|"
            r"\b(attack|exploit|malicious|poison)\b.{0,80}\b(supply[- ]?chain|dependency\s+confusion)\b",
            re.IGNORECASE,
        ),
        "supply-chain attack content",
    ),
]


def _github_headers(accept: str) -> Dict[str, str]:
    headers = {
        "Accept": accept,
        "User-Agent": "skill-audit-skill-safety",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _http_get_json(url: str, timeout_seconds: float) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    request = Request(url, headers=_github_headers("application/vnd.github+json"))
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = response.read().decode("utf-8", errors="ignore")
    except HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except URLError as exc:
        return None, str(exc.reason)
    except OSError as exc:
        return None, str(exc)

    try:
        data = json.loads(payload)
    except ValueError:
        return None, "invalid JSON response"
    if not isinstance(data, dict):
        return None, "unexpected response payload"
    return data, None


def _http_get_text(url: str, timeout_seconds: float) -> Tuple[Optional[str], Optional[str]]:
    request = Request(url, headers=_github_headers("application/vnd.github.raw"))
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = response.read().decode("utf-8", errors="ignore")
    except HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except URLError as exc:
        return None, str(exc.reason)
    except OSError as exc:
        return None, str(exc)
    return payload, None


def _origin_remote_url(target_repo: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(target_repo), "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    return value or None


def github_repo_slug_from_remote(remote_url: str) -> Optional[str]:
    match = GITHUB_REMOTE_RE.search(remote_url.strip())
    if not match:
        return None
    slug = match.group(1).strip().strip("/")
    if not slug or "/" not in slug:
        return None
    return slug


def _fetch_repo_metadata(repo_slug: str, timeout_seconds: float) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    return _http_get_json(f"{GITHUB_API_BASE}/repos/{repo_slug}", timeout_seconds)


def _fetch_repo_readme(repo_slug: str, timeout_seconds: float) -> Tuple[Optional[str], Optional[str]]:
    return _http_get_text(f"{GITHUB_API_BASE}/repos/{repo_slug}/readme", timeout_seconds)


def _fetch_issue_mentions(repo_slug: str, timeout_seconds: float) -> Tuple[list[str], Optional[str]]:
    query = (
        f'"{repo_slug}" '
        "(prompt injection OR malware OR backdoor OR stealer OR dependency confusion OR supply chain attack)"
    )
    url = (
        f"{GITHUB_API_BASE}/search/issues?q={quote_plus(query)}"
        "&sort=updated&order=desc&per_page=5"
    )
    payload, error = _http_get_json(url, timeout_seconds)
    if payload is None:
        return [], error

    items = payload.get("items")
    if not isinstance(items, list):
        return [], None

    snippets: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        body = str(item.get("body") or "").strip()
        snippet = " ".join(part for part in [title, body[:320]] if part)
        snippet = re.sub(r"\s+", " ", snippet).strip()
        if snippet:
            snippets.append(snippet)
    return snippets, None


def _trim_snippet(text: str, start: int, end: int, radius: int = 80) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    snippet = text[left:right]
    return re.sub(r"\s+", " ", snippet).strip()


def _collect_osint_signals(sources: Sequence[Tuple[str, str]]) -> list[Dict[str, str]]:
    signals: list[Dict[str, str]] = []
    seen: set[Tuple[str, str, str]] = set()

    for source, text in sources:
        if not text:
            continue
        for pattern, label in HIGH_RISK_TEXT_RULES:
            for match in pattern.finditer(text):
                snippet = _trim_snippet(text, match.start(), match.end())
                term = re.sub(r"\s+", " ", match.group(0)).strip()
                dedupe_key = (source, label, snippet.lower())
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                signals.append(
                    {
                        "source": source,
                        "label": label,
                        "term": term[:180],
                        "snippet": snippet[:240],
                    }
                )
                if len(signals) >= 10:
                    return signals
    return signals


def run_github_osint_precheck(target_repo: Path, timeout_seconds: float = 6.0) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "enabled": True,
        "executed": False,
        "decision": "unavailable",
        "reason": "precheck not executed",
        "repository": None,
        "remote_url": None,
        "sources_checked": [],
        "signals": [],
        "warnings": [],
    }

    remote_url = _origin_remote_url(target_repo)
    if not remote_url:
        result["decision"] = "not_applicable"
        result["reason"] = "origin remote not found"
        return result

    repo_slug = github_repo_slug_from_remote(remote_url)
    result["remote_url"] = remote_url
    result["repository"] = repo_slug
    if not repo_slug:
        result["decision"] = "not_applicable"
        result["reason"] = "origin remote is not a GitHub repository"
        return result

    result["executed"] = True
    timeout_seconds = max(1.0, float(timeout_seconds))

    metadata, metadata_error = _fetch_repo_metadata(repo_slug, timeout_seconds)
    if metadata is None:
        result["decision"] = "unavailable"
        result["reason"] = f"github metadata unavailable: {metadata_error}"
        return result

    readme_text, readme_error = _fetch_repo_readme(repo_slug, timeout_seconds)
    issue_snippets, issue_error = _fetch_issue_mentions(repo_slug, timeout_seconds)

    if readme_error:
        result.setdefault("warnings", []).append(f"README fetch failed: {readme_error}")
    if issue_error:
        result.setdefault("warnings", []).append(f"Issue search failed: {issue_error}")

    description = str(metadata.get("description") or "")
    topics_value = metadata.get("topics")
    topics = [str(item) for item in topics_value] if isinstance(topics_value, list) else []
    issue_text = "\n".join(issue_snippets)

    sources: list[Tuple[str, str]] = [
        ("github.repo", repo_slug),
        ("github.description", description),
        ("github.topics", " ".join(topics)),
        ("github.readme", readme_text or ""),
        ("github.search_issues", issue_text),
    ]

    result["sources_checked"] = [source for source, text in sources if text.strip()]
    signals = _collect_osint_signals(sources)
    result["signals"] = signals

    if signals:
        result["decision"] = "reject"
        result["reason"] = "high-risk GitHub OSINT signals detected before installation"
    else:
        result["decision"] = "clear"
        result["reason"] = "no high-risk GitHub OSINT signals detected"

    return result
