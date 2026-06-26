from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import urllib.error
import urllib.request

from .config import Settings


@dataclass(slots=True)
class GroundingSnippet:
    source: str
    excerpt: str
    score: float = 0.0
    url: str | None = None


def ground_query(query: str, settings: Settings) -> list[GroundingSnippet]:
    remote = _query_contextual(query, settings)
    if remote:
        return remote
    return _query_local_runbooks(query, settings.runbook_docs_path)


def _query_contextual(query: str, settings: Settings) -> list[GroundingSnippet]:
    if not settings.contextual_api_key or not settings.contextual_agent_id:
        return []

    payload = {"query": query, "retrievals_only": True}
    request = urllib.request.Request(
        url=(
            f"{settings.contextual_base_url.rstrip('/')}/v1/agents/"
            f"{settings.contextual_agent_id}/query"
        ),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.contextual_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    retrievals = (
        payload.get("retrieval_contents")
        or payload.get("retrievals")
        or payload.get("results")
        or []
    )
    snippets: list[GroundingSnippet] = []
    for item in retrievals:
        excerpt = (
            item.get("content_text")
            or item.get("text")
            or item.get("excerpt")
            or ""
        ).strip()
        source = (
            item.get("document_name")
            or item.get("source_name")
            or item.get("title")
            or "Contextual retrieval"
        )
        if not excerpt:
            continue
        snippets.append(
            GroundingSnippet(
                source=str(source),
                excerpt=excerpt[:400],
                score=float(item.get("score", 0.0) or 0.0),
                url=str(item.get("url")) if item.get("url") else None,
            )
        )
    return snippets[:3]


def _query_local_runbooks(query: str, runbook_path: Path) -> list[GroundingSnippet]:
    if not runbook_path.exists():
        return []

    query_terms = set(_tokenize(query))
    scored: list[tuple[int, GroundingSnippet]] = []
    for path in sorted(runbook_path.glob("*.md")):
        content = path.read_text()
        content_terms = set(_tokenize(content))
        overlap = len(query_terms & content_terms)
        if overlap == 0:
            continue
        excerpt = _best_excerpt(content, query_terms)
        scored.append(
            (
                overlap,
                GroundingSnippet(
                    source=path.name,
                    excerpt=excerpt,
                    score=float(overlap),
                ),
            )
        )
    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored[:3]]


def _best_excerpt(content: str, query_terms: set[str]) -> str:
    paragraphs = [segment.strip() for segment in content.split("\n\n") if segment.strip()]
    if not paragraphs:
        return content[:240]

    ranked = sorted(
        paragraphs,
        key=lambda paragraph: len(query_terms & set(_tokenize(paragraph))),
        reverse=True,
    )
    return ranked[0][:400]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9-]+", text.lower())
