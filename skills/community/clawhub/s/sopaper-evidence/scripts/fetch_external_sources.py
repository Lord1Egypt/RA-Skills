#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from url_safety import assert_public_http_url, is_safe_public_http_url


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s)>]+")


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta: dict[str, str] = {}
        self.in_script = False
        self.in_style = False
        self.in_paragraph = False
        self.current_paragraph: list[str] = []
        self.paragraphs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value or "" for key, value in attrs}
        lowered = tag.lower()
        if lowered == "title":
            self.in_title = True
        if lowered == "meta":
            name = attr_map.get("name", "").lower()
            prop = attr_map.get("property", "").lower()
            content = attr_map.get("content", "").strip()
            if name and content:
                self.meta[name] = content
            if prop and content:
                self.meta[prop] = content
        if lowered == "script":
            self.in_script = True
        if lowered == "style":
            self.in_style = True
        if lowered in {"p", "li", "article", "section", "main", "div"}:
            self.in_paragraph = True

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered == "title":
            self.in_title = False
        if lowered == "script":
            self.in_script = False
        if lowered == "style":
            self.in_style = False
        if lowered in {"p", "li", "article", "section", "main", "div"}:
            self.flush_paragraph()
            self.in_paragraph = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.in_script or self.in_style:
            return
        if self.in_paragraph:
            cleaned = clean_text(data)
            if cleaned:
                self.current_paragraph.append(cleaned)

    def flush_paragraph(self) -> None:
        if not self.current_paragraph:
            return
        paragraph = clean_text(" ".join(self.current_paragraph))
        self.current_paragraph = []
        if len(paragraph) >= 50:
            self.paragraphs.append(paragraph)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch external URLs from markdown/text files or direct URL arguments and generate "
            "structured source-note drafts."
        )
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Markdown/text files and/or direct URLs.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for generated source-note markdown files.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP timeout in seconds. Default: 15",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    urls = collect_urls(args.inputs)
    if not urls:
        print("No external URLs found.", file=sys.stderr)
        return 1

    for index, url in enumerate(urls, start=1):
        try:
            note = fetch_note(url, timeout=args.timeout)
        except Exception as exc:  # pragma: no cover
            note = render_failure_note(url, str(exc))

        slug = slugify(note["title"] or guess_title_from_url(url))
        path = output_dir / f"{index:02d}-{slug}.md"
        path.write_text(render_note(note), encoding="utf-8")
        print(path)

    return 0


def collect_urls(values: list[str]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value.startswith(("http://", "https://")):
            add_url(found, seen, value)
            continue

        path = Path(value).expanduser().resolve()
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for _, locator in MARKDOWN_LINK_RE.findall(text):
            add_url(found, seen, locator)
        for locator in BARE_URL_RE.findall(text):
            add_url(found, seen, locator)
    return found


def add_url(found: list[str], seen: set[str], url: str) -> None:
    cleaned = url.strip().rstrip(").,")
    if not is_safe_public_http_url(cleaned):
        return
    if cleaned not in seen:
        seen.add(cleaned)
        found.append(cleaned)


def fetch_note(url: str, *, timeout: int) -> dict[str, str]:
    assert_public_http_url(url)
    request = Request(
        url,
        headers={
            "User-Agent": "SopaperEvidenceBot/0.6 (+https://github.com/sheepxux/SoPaper-Evidence)"
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code in {301, 302, 303, 307, 308} and exc.headers.get("Location"):
            redirected = urljoin(url, exc.headers["Location"])
            assert_public_http_url(redirected)
            return fetch_note(redirected, timeout=timeout)
        raise

    parser = MetaParser()
    parser.feed(raw)
    parser.flush_paragraph()

    title = clean_text(
        parser.meta.get("citation_title")
        or parser.meta.get("og:title")
        or parser.title
        or guess_title_from_url(url)
    )
    description = clean_text(
        parser.meta.get("description")
        or parser.meta.get("og:description")
        or parser.meta.get("twitter:description")
    )
    source_type = guess_external_source_type(url, content_type)
    access_date = datetime.now(timezone.utc).date().isoformat()
    paragraphs = summarize_paragraphs(parser.paragraphs)
    task = infer_task(title, description, paragraphs)
    metrics = infer_metrics(description, paragraphs)
    relevance = infer_relevance(source_type, task, metrics)
    comparable = infer_comparable_scope(source_type)
    facts = build_candidate_facts(title, description, paragraphs, source_type)

    return {
        "title": title or guess_title_from_url(url),
        "url": url,
        "source_type": source_type,
        "access_date": access_date,
        "task": task,
        "metrics": metrics,
        "facts": facts,
        "relevance": relevance,
        "comparable": comparable,
        "limits": infer_limits(source_type, paragraphs),
        "verification": "fetched-primary-review-required",
    }


def render_failure_note(url: str, error: str) -> dict[str, str]:
    return {
        "title": guess_title_from_url(url),
        "url": url,
        "source_type": "other",
        "access_date": datetime.now(timezone.utc).date().isoformat(),
        "task": "TODO",
        "metrics": "TODO",
        "facts": [f"TODO: fetch failed with error: {error}"],
        "relevance": "TODO: retry fetch or review manually.",
        "comparable": "unknown",
        "limits": "fetch failed; source content not reviewed.",
        "verification": "fetch-failed",
    }


def render_note(note: dict[str, str]) -> str:
    return "\n".join(
        [
            "# Source Note",
            "",
            "## Title",
            "",
            f"- Title: {note['title']}",
            "",
            "## Source",
            "",
            f"- Source type: {note['source_type']}",
            f"- Locator: {note['url']}",
            f"- Access date: {note['access_date']}",
            f"- Task: {note['task']}",
            f"- Metrics: {note['metrics']}",
            f"- Verification status: {note['verification']}",
            "",
            "## Why it matters",
            "",
            f"- Relevance to our paper: {note['relevance']}",
            f"- Comparable to us: {note['comparable']}",
            "",
            "## Key facts",
            "",
            *[f"- Fact: {fact}" for fact in note["facts"]],
            "",
            "## Limits",
            "",
            f"- Limit: {note['limits']}",
            "",
            "## Reviewer risk",
            "",
            "- Risk: TODO",
            "- Risk: TODO",
            "",
        ]
    )


def guess_external_source_type(locator: str, content_type: str) -> str:
    parsed = urlparse(locator)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if any(token in host for token in ["sourcegraph.com", "theaireport.net"]) or "blog" in path:
        return "blog"
    if "arxiv.org" in host or "doi.org" in host:
        return "paper"
    if "github.com" in host or "gitlab.com" in host:
        return "repo"
    if any(token in host for token in ["readthedocs.io", "docs.", "documentation"]):
        return "official_doc"
    if any(token in host for token in ["paperswithcode.com", "huggingface.co"]):
        return "benchmark"
    if any(token in path for token in ["benchmark", "leaderboard", "eval"]):
        return "benchmark"
    if any(token in path for token in ["/dataset", "/datasets"]):
        return "dataset"
    if "html" in content_type.lower() or host:
        return "official_doc"
    return "other"


def guess_title_from_url(locator: str) -> str:
    parsed = urlparse(locator)
    if parsed.netloc:
        tail = parsed.path.rstrip("/").split("/")[-1]
        return (tail or parsed.netloc).replace("-", " ").replace("_", " ")
    return locator


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return cleaned[:50] or "source-note"


def clean_text(value: str) -> str:
    collapsed = re.sub(r"\s+", " ", html.unescape(value or "")).strip()
    return collapsed


def summarize_paragraphs(paragraphs: list[str]) -> list[str]:
    cleaned: list[str] = []
    for paragraph in paragraphs:
        normalized = clean_text(paragraph)
        lowered = normalized.lower()
        if len(normalized) < 80:
            continue
        if any(
            token in lowered
            for token in [
                "donate",
                "privacy policy",
                "cookie",
                "terms of use",
                "we gratefully acknowledge support",
                "all fields title author abstract",
                "sign up",
                "log in",
                "open science",
                "giving day",
                "javascript is disabled",
                "skip to content",
                "cookies are used",
            ]
        ):
            continue
        if lowered.startswith("abstract page for arxiv paper"):
            continue
        if normalized and normalized not in cleaned:
            cleaned.append(normalized)
        if len(cleaned) == 3:
            break
    return cleaned


def build_candidate_facts(title: str, description: str, paragraphs: list[str], source_type: str) -> list[str]:
    facts: list[str] = []
    if title:
        facts.append(f'Fetched page title: "{title}".')
    title_fact = synthesize_title_fact(title, source_type)
    if title_fact:
        facts.append(title_fact)
    evaluation_fact = synthesize_evaluation_fact(title, source_type)
    if evaluation_fact:
        facts.append(evaluation_fact)
    baseline_fact = synthesize_baseline_fact(title, source_type)
    if baseline_fact:
        facts.append(baseline_fact)
    if description and not description.lower().startswith("abstract page for arxiv paper"):
        facts.append(f"Meta description: {description}")
    extracted = extract_semantic_facts(title, description, paragraphs, source_type)
    facts.extend(extracted)
    metric_fact = synthesize_metric_fact(title, description, paragraphs)
    if metric_fact:
        facts.append(metric_fact)
    if source_type == "paper" and "arxiv.org" in title.lower():
        facts.append("Source host is arXiv, which is usually a primary paper distribution channel.")
    deduped: list[str] = []
    seen: set[str] = set()
    for fact in facts:
        normalized = clean_text(fact).lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(fact)
    return deduped[:4] if deduped else ["TODO: add reviewed facts from the fetched source."]


def extract_semantic_facts(
    title: str, description: str, paragraphs: list[str], source_type: str
) -> list[str]:
    facts: list[str] = []
    candidates = [description, *paragraphs]
    for paragraph in candidates:
        normalized = clean_text(paragraph)
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered.startswith("abstract page for arxiv paper"):
            continue
        if lowered.startswith("view a pdf of the paper titled"):
            continue
        if source_type in {"paper", "benchmark"} and any(
            token in lowered
            for token in [
                "benchmark",
                "dataset",
                "long-horizon",
                "robot manipulation",
                "tabletop manipulation",
                "retrieval",
                "citation",
                "grounded generation",
                "code understanding",
                "code generation",
                "translation",
            ]
        ):
            facts.append(f"Candidate benchmark/task fact: {trim_sentence(normalized)}")
        elif any(token in lowered for token in ["success rate", "accuracy", "precision", "recall", "f1", "metric"]):
            facts.append(f"Candidate metric fact: {trim_sentence(normalized)}")
        elif any(token in lowered for token in ["baseline", "compare", "comparison", "evaluate", "evaluation"]):
            facts.append(f"Candidate evaluation fact: {trim_sentence(normalized)}")
        if len(facts) >= 2:
            break
    return facts


def synthesize_title_fact(title: str, source_type: str) -> str:
    lowered = title.lower()
    if source_type in {"paper", "benchmark"}:
        if "benchmark" in lowered and any(token in lowered for token in ["browser", "browsing", "web"]):
            return "Candidate benchmark/task fact: This source appears to define a browser-agent or web-browsing benchmark."
        if "benchmark" in lowered and "long-horizon" in lowered and any(
            token in lowered for token in ["manipulation", "robot", "robotic"]
        ):
            return "Candidate benchmark/task fact: This source appears to define a long-horizon robotics manipulation benchmark."
        if "benchmark" in lowered and "retrieval" in lowered and "code" in lowered:
            return "Candidate benchmark/task fact: This source appears to define a code retrieval benchmark."
        if "benchmark" in lowered and any(token in lowered for token in ["code understanding", "code generation", "translation"]):
            return "Candidate benchmark/task fact: This source appears to define a multi-task code benchmark with retrieval relevance."
        if "benchmark" in lowered and "citation" in lowered:
            return "Candidate benchmark/task fact: This source appears to define a citation-grounded benchmark or evaluation setting."
        if "benchmark" in lowered:
            return "Candidate benchmark/task fact: This source appears to define a benchmark or evaluation setting."
    if source_type == "repo" and any(token in lowered for token in ["benchmark", "eval", "evaluation"]):
        return "Candidate evaluation fact: This repository likely contains evaluation or benchmark artifacts."
    return ""


def synthesize_evaluation_fact(title: str, source_type: str) -> str:
    lowered = title.lower()
    if source_type not in {"paper", "benchmark", "repo"}:
        return ""
    if any(token in lowered for token in ["long-horizon", "manipulation", "robot", "robotic"]):
        return "Candidate evaluation fact: This source likely defines task scope and evaluation setup for long-horizon robotics manipulation."
    if any(token in lowered for token in ["code retrieval", "code understanding", "code generation", "translation"]):
        return "Candidate evaluation fact: This source likely defines evaluation setup for code retrieval or closely related code tasks."
    if any(token in lowered for token in ["browser", "browsing", "web"]):
        return "Candidate evaluation fact: This source likely defines browsing-task setup or benchmark scope for web-agent evaluation."
    if "benchmark" in lowered:
        return "Candidate evaluation fact: This source likely defines benchmark scope or evaluation setup."
    return ""


def synthesize_metric_fact(title: str, description: str, paragraphs: list[str]) -> str:
    metrics = infer_metrics(description, paragraphs)
    if metrics != "TODO":
        return f"Candidate metric fact: This source likely reports or defines metrics related to {metrics}."
    lowered = " ".join([title, description, *paragraphs]).lower()
    if any(token in lowered for token in ["benchmark", "evaluation"]):
        return "Candidate metric fact: This source likely defines benchmark metrics that still need manual review."
    return ""


def synthesize_baseline_fact(title: str, source_type: str) -> str:
    lowered = title.lower()
    if source_type not in {"paper", "benchmark", "repo"}:
        return ""
    if any(token in lowered for token in ["manipulation", "robot", "robotic", "embodied"]):
        return "Candidate baseline fact: This source likely expects embodiment-matched or benchmark-aligned baselines for fair comparison."
    if any(token in lowered for token in ["code retrieval", "code understanding", "code generation", "translation"]):
        return "Candidate baseline fact: This source likely expects task-aligned code retrieval or code-task baselines for fair comparison."
    if any(token in lowered for token in ["browser", "browsing", "web"]):
        return "Candidate baseline fact: This source likely expects benchmark-aligned browsing-agent baselines for fair comparison."
    if "benchmark" in lowered:
        return "Candidate baseline fact: This source likely expects benchmark-aligned baselines for fair comparison."
    return ""


def infer_task(title: str, description: str, paragraphs: list[str]) -> str:
    base = " ".join([title, description, *paragraphs]).lower()
    if any(token in base for token in ["manipulation", "robot", "robotic", "embodied"]):
        return "robotics manipulation benchmark"
    if any(token in base for token in ["code retrieval", "code understanding", "code generation"]):
        return "code retrieval and code-task benchmark"
    if any(token in base for token in ["question answering", "qa"]):
        return "question answering"
    if "browser" in base or "web task" in base or "webarena" in base:
        return "browser agent evaluation"
    if "benchmark" in base:
        return "benchmark evaluation"
    if "documentation" in base or "docs" in base:
        return "documentation or API guidance"
    return "TODO"


def infer_metrics(description: str, paragraphs: list[str]) -> str:
    base = " ".join([description, *paragraphs]).lower()
    metrics: list[str] = []
    for token in [
        "success rate",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "citation",
        "completion",
        "latency",
        "pass@k",
        "execution",
        "retrieval",
    ]:
        if token in base:
            metrics.append(token)
    return ", ".join(metrics[:4]) if metrics else "TODO"


def infer_relevance(source_type: str, task: str, metrics: str) -> str:
    if source_type == "paper":
        return f"This fetched paper may support task framing for {task} and should be reviewed before upgrade."
    if source_type == "benchmark":
        return f"This fetched benchmark source may help define evaluation fit for {task} and related metrics such as {metrics}."
    if source_type == "repo":
        return "This fetched repository may help verify implementation scope or artifact availability."
    if source_type == "blog":
        return "This fetched blog or news page may provide discovery leads, but it should not anchor factual research claims."
    if source_type == "official_doc":
        return "This fetched documentation page may help verify definitions, interfaces, or evaluation concepts."
    return "TODO: explain why this fetched source matters for the current evidence pack."


def infer_comparable_scope(source_type: str) -> str:
    if source_type in {"paper", "benchmark"}:
        return "potentially comparable after manual review"
    if source_type in {"repo", "official_doc"}:
        return "contextual until manually reviewed"
    if source_type == "blog":
        return "discovery-only unless manually traced back to a primary source"
    return "unknown"


def infer_limits(source_type: str, paragraphs: list[str]) -> str:
    if source_type == "paper":
        return "Paper content still needs manual reading to confirm exact claims, task fit, and metric alignment."
    if source_type == "benchmark":
        return "Benchmark scope and task overlap still need manual review before using it for direct comparisons."
    if source_type == "repo":
        return "Repository metadata alone does not prove evaluation results or benchmark performance."
    if source_type == "blog":
        return "Blog content may summarize useful context, but it should be traced back to a primary source before use in evidence mapping."
    if source_type == "official_doc":
        return "Documentation content may define concepts, but it does not by itself validate comparative claims."
    return "TODO: state scope limits, benchmark mismatch risk, or unresolved verification gaps."


def trim_sentence(value: str) -> str:
    text = clean_text(value)
    if len(text) <= 220:
        return text
    return text[:217].rstrip() + "..."


if __name__ == "__main__":
    raise SystemExit(main())
