#!/usr/bin/env python3
"""
Scholarly research helper via OpenAlex API.

Core features:
- Search papers by topic
- Look up papers by DOI
- Inspect citation chains
- Discover open-access URLs and PDF URLs via Unpaywall
- Cache API responses locally
- Generate a concise Markdown literature review
- Hand off long review files to qqbot-send with <qqmedia>

Packaged as a reusable OpenClaw skill for academic paper search.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests


BASE = "https://api.openalex.org"
UNPAYWALL_BASE = "https://api.unpaywall.org/v2"
MAILTO = os.getenv("OPENALEX_MAILTO", "openclaw@example.com")

APP_DIR = Path.home() / ".openclaw" / "scholarly-research"
CACHE_DIR = APP_DIR / "cache"
OUTPUT_DIR = APP_DIR / "outputs"
CACHE_TTL_SECONDS = 24 * 60 * 60


def eprint(*args):
    print(*args, file=sys.stderr)


def normalize_doi(doi):
    doi = (doi or "").strip()
    doi = doi.removeprefix("https://doi.org/")
    doi = doi.removeprefix("http://doi.org/")
    doi = doi.removeprefix("doi:")
    return doi.strip()


def safe_filename(text, max_len=90):
    text = text or "untitled"
    text = re.sub(r"[\\/:*?\"<>|]+", "_", text)
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:max_len].rstrip() or "untitled")


def cache_key(url, params):
    raw = json.dumps({"url": url, "params": params or {}}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def read_cache(url, params):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{cache_key(url, params)}.json"

    if not path.exists():
        return None

    if time.time() - path.stat().st_mtime > CACHE_TTL_SECONDS:
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_cache(url, params, data):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{cache_key(url, params)}.json"

    try:
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def request_json(url, params=None, *, add_mailto=True, attempts=3, timeout=20):
    params = dict(params or {})

    if add_mailto:
        params["mailto"] = MAILTO

    cached = read_cache(url, params)
    if cached is not None:
        return cached

    for attempt in range(attempts):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code == 429:
                time.sleep(2 ** attempt)
                continue

            response.raise_for_status()
            data = response.json()
            write_cache(url, params, data)
            return data

        except requests.exceptions.RequestException as exc:
            if attempt == attempts - 1:
                eprint(f"Error: {exc}")
                return None
            time.sleep(1 + attempt)

    return None


def restore_abstract(inverted_index):
    if not inverted_index:
        return None

    try:
        max_pos = max(max(pos) for pos in inverted_index.values() if pos)
        words = [""] * (max_pos + 1)

        for word, positions in inverted_index.items():
            for pos in positions:
                words[pos] = word

        return " ".join(words).strip() or None

    except Exception:
        return None


def parse_work(work):
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    open_access = work.get("open_access") or {}

    authors = []
    for item in work.get("authorships", [])[:5]:
        author = item.get("author") or {}
        authors.append(author.get("display_name", "Unknown"))

    doi = normalize_doi((work.get("doi") or "").replace("https://doi.org/", ""))

    return {
        "title": work.get("display_name", "N/A"),
        "year": work.get("publication_year"),
        "authors": authors,
        "abstract": restore_abstract(work.get("abstract_inverted_index")),
        "citations": work.get("cited_by_count", 0),
        "doi": doi or None,
        "open_access": bool(open_access.get("is_oa", False)),
        "oa_url": open_access.get("oa_url"),
        "landing_url": location.get("landing_page_url"),
        "source": source.get("display_name"),
        "type": work.get("type"),
        "openalex_id": work.get("id"),
    }


def unpaywall_lookup(doi):
    doi = normalize_doi(doi)
    if not doi:
        return None

    return request_json(
        f"{UNPAYWALL_BASE}/{doi}",
        {"email": MAILTO},
        add_mailto=False,
        attempts=2,
        timeout=12,
    )


def add_oa_pdf_info(paper):
    if not paper or not paper.get("doi"):
        return paper

    data = unpaywall_lookup(paper["doi"])
    if not data:
        return paper

    best = data.get("best_oa_location") or {}

    if data.get("is_oa"):
        paper["open_access"] = True

    if best.get("url_for_pdf"):
        paper["pdf_url"] = best["url_for_pdf"]
    elif best.get("url"):
        paper["fulltext_url"] = best["url"]

    if best.get("license"):
        paper["license"] = best.get("license")

    return paper


def search_papers(query, limit=10, sort="relevance", years=None, oa_only=False):
    params = {
        "search": query,
        "per_page": min(limit, 50),
    }

    if sort == "citations":
        params["sort"] = "cited_by_count:desc"
    elif sort == "recent":
        params["sort"] = "publication_year:desc"

    filters = []
    if years:
        filters.append(f"publication_year:{years}")
    if oa_only:
        filters.append("open_access.is_oa:true")
    if filters:
        params["filter"] = ",".join(filters)

    data = request_json(f"{BASE}/works", params)
    if not data:
        return []

    papers = [parse_work(item) for item in data.get("results", [])]
    return [add_oa_pdf_info(paper) for paper in papers]


def lookup_doi(doi):
    doi = normalize_doi(doi)
    if not doi:
        return None

    data = request_json(f"{BASE}/works/https://doi.org/{doi}", {})
    if not data:
        return None

    return add_oa_pdf_info(parse_work(data))


def lookup_openalex_work(work_id):
    if not work_id:
        return None

    wid = work_id.split("/")[-1]
    data = request_json(f"{BASE}/works/{wid}", {})
    if not data:
        return None

    return add_oa_pdf_info(parse_work(data))


def citation_chain(doi, direction="cited_by", limit=10):
    doi = normalize_doi(doi)
    raw_work = request_json(f"{BASE}/works/https://doi.org/{doi}", {})

    if not raw_work:
        return {"cited_by": [], "references": []}

    result = {}
    work_id = (raw_work.get("id") or "").split("/")[-1]

    if direction in ("cited_by", "both"):
        data = request_json(
            f"{BASE}/works",
            {
                "filter": f"cites:{work_id}",
                "sort": "cited_by_count:desc",
                "per_page": min(limit, 50),
            },
        )
        result["cited_by"] = [
            add_oa_pdf_info(parse_work(item))
            for item in (data or {}).get("results", [])
        ]

    if direction in ("references", "both"):
        refs = []
        for ref_id in raw_work.get("referenced_works", [])[:limit]:
            paper = lookup_openalex_work(ref_id)
            if paper:
                refs.append(paper)
        result["references"] = refs

    return result


def format_authors(authors, max_authors=3):
    authors = authors or []
    shown = ", ".join(authors[:max_authors])
    if len(authors) > max_authors:
        shown += " et al."
    return shown


def format_paper(paper, idx=None):
    prefix = f"{idx}. " if idx else ""
    access = "🔓" if paper.get("open_access") else "🔒"
    year = f"({paper['year']})" if paper.get("year") else ""
    citations = f"[{paper['citations']} citations]" if paper.get("citations") else ""

    lines = [
        f"{prefix}{access} {paper.get('title', 'N/A')} {year} {citations}".strip()
    ]

    authors = format_authors(paper.get("authors"))
    if authors:
        lines.append(f"   Authors: {authors}")
    if paper.get("source"):
        lines.append(f"   Source: {paper['source']}")
    if paper.get("doi"):
        lines.append(f"   DOI: {paper['doi']}")
    if paper.get("oa_url"):
        lines.append(f"   OA URL: {paper['oa_url']}")
    if paper.get("pdf_url"):
        lines.append(f"   OA PDF: {paper['pdf_url']}")
    if paper.get("fulltext_url"):
        lines.append(f"   Full text: {paper['fulltext_url']}")
    if paper.get("abstract"):
        abstract = paper["abstract"][:300]
        if len(paper["abstract"]) > 300:
            abstract += "..."
        lines.append(f"   Abstract: {abstract}")

    return "\n".join(lines)


def query_variations(topic):
    topic = topic.strip()
    words = topic.split()

    variants = [topic]

    if len(words) > 1:
        variants.append(f'"{topic}"')

    if len(words) >= 6:
        mid = len(words) // 2
        variants.append(" ".join(words[:mid]))
        variants.append(" ".join(words[mid:]))

    deduped = []
    for item in variants:
        if item and item not in deduped:
            deduped.append(item)

    return deduped[:4]


def collect_review_papers(topic, target_count=20, years=None, oa_only=False):
    papers_by_key = {}
    queries = query_variations(topic)
    per_query = max(15, target_count // max(len(queries), 1) + 8)

    for query in queries:
        eprint(f"Searching: {query}")
        papers = search_papers(
            query=query,
            limit=per_query,
            sort="relevance",
            years=years,
            oa_only=oa_only,
        )

        for paper in papers:
            key = paper.get("doi") or paper.get("openalex_id") or paper.get("title")
            if key and key not in papers_by_key:
                papers_by_key[key] = paper

    ranked = sorted(
        papers_by_key.values(),
        key=lambda p: (p.get("citations", 0), p.get("year") or 0),
        reverse=True,
    )

    return ranked[:target_count]


def first_sentence(text, max_chars=260):
    if not text:
        return ""

    sentence = text.split(". ")[0].strip()
    if not sentence.endswith("."):
        sentence += "."

    if len(sentence) > max_chars:
        sentence = sentence[:max_chars].rstrip() + "..."

    return sentence


def make_review_markdown(topic, papers, years=None):
    pub_years = [p["year"] for p in papers if p.get("year")]
    total_citations = sum(p.get("citations", 0) for p in papers)
    oa_count = sum(1 for p in papers if p.get("open_access"))

    lines = []
    lines.append(f"# Literature Review: {topic}\n")
    lines.append("Generated by scholarly-research using OpenAlex.\n")

    lines.append("## Overview\n")
    lines.append(f"- Papers analyzed: {len(papers)}")
    if years:
        lines.append(f"- Search year filter: {years}")
    if pub_years:
        lines.append(f"- Publication years: {min(pub_years)}–{max(pub_years)}")
    lines.append(f"- Total citations: {total_citations:,}")
    lines.append(f"- Open-access papers: {oa_count}/{len(papers)}")
    lines.append("")

    lines.append("## Representative Papers\n")
    for i, paper in enumerate(papers, 1):
        authors = format_authors(paper.get("authors"), max_authors=2)
        year = f" ({paper['year']})" if paper.get("year") else ""
        source = f" — {paper['source']}" if paper.get("source") else ""
        doi = f" DOI: https://doi.org/{paper['doi']}" if paper.get("doi") else ""
        oa = "OA" if paper.get("open_access") else "Closed"

        lines.append(
            f"{i}. **{paper.get('title', 'N/A')}** — {authors}{year}{source}; "
            f"{paper.get('citations', 0)} citations; {oa}.{doi}"
        )

        summary = first_sentence(paper.get("abstract"))
        if summary:
            lines.append(f"   > {summary}")

        if paper.get("pdf_url"):
            lines.append(f"   PDF: {paper['pdf_url']}")
        elif paper.get("oa_url"):
            lines.append(f"   OA URL: {paper['oa_url']}")

        lines.append("")

    lines.append("## Bibliography\n")
    for i, paper in enumerate(sorted(papers, key=lambda p: p.get("year") or 0, reverse=True), 1):
        authors = format_authors(paper.get("authors"), max_authors=3)
        year = f" ({paper['year']})" if paper.get("year") else ""
        source = f" {paper['source']}." if paper.get("source") else ""
        doi = f" https://doi.org/{paper['doi']}" if paper.get("doi") else ""
        lines.append(f"{i}. {authors}{year}. *{paper.get('title', 'N/A')}*.{source}{doi}")

    lines.append("")
    lines.append("---")
    lines.append(f"{len(papers)} papers reviewed.")

    return "\n".join(lines)


def save_text(path, text):
    path = Path(path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def default_review_path(topic):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    name = safe_filename(topic, max_len=70).replace(" ", "_")
    return OUTPUT_DIR / f"review_{timestamp}_{name}.md"


def find_stage_media_script(explicit_path=None):
    candidates = []

    if explicit_path:
        candidates.append(Path(explicit_path))

    env_path = os.getenv("OPENCLAW_QQBOT_STAGE_MEDIA_SCRIPT") or os.getenv("QQBOT_STAGE_MEDIA_SCRIPT")
    if env_path:
        candidates.append(Path(env_path))

    candidates.append(Path.home() / ".openclaw" / "skills" / "qqbot-send" / "scripts" / "stage_media.py")

    for candidate in candidates:
        try:
            candidate = candidate.expanduser().resolve()
            if candidate.exists() and candidate.is_file():
                return candidate
        except Exception:
            continue

    return None


def stage_for_qqmedia(file_path, stage_media_script=None):
    script = find_stage_media_script(stage_media_script)
    source = Path(file_path).expanduser().resolve()

    if not script:
        raise RuntimeError(
            "stage_media.py not found. Set OPENCLAW_QQBOT_STAGE_MEDIA_SCRIPT "
            "or pass --stage-media-script."
        )

    result = subprocess.run(
        [sys.executable, str(script), str(source)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown staging error"
        raise RuntimeError(message)

    staged_path = result.stdout.strip().splitlines()[-1].strip()
    if not staged_path:
        raise RuntimeError("stage_media.py did not return a staged path")

    return staged_path


def output_qqmedia(file_path, stage_media_script=None):
    staged_path = stage_for_qqmedia(file_path, stage_media_script)
    print(f"<qqmedia>{staged_path}</qqmedia>")


def print_papers(papers):
    for i, paper in enumerate(papers, 1):
        print(format_paper(paper, i))
        print()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Search academic papers and generate concise literature reviews using OpenAlex."
    )

    sub = parser.add_subparsers(dest="cmd")

    search_cmd = sub.add_parser("search", help="Search papers by topic")
    search_cmd.add_argument("query")
    search_cmd.add_argument("--limit", "-l", type=int, default=10)
    search_cmd.add_argument("--sort", choices=["relevance", "citations", "recent"], default="relevance")
    search_cmd.add_argument("--years", help="Year range, e.g. 2020-2026")
    search_cmd.add_argument("--oa", action="store_true", help="Open-access papers only")
    search_cmd.add_argument("--json", action="store_true")

    doi_cmd = sub.add_parser("doi", help="Look up a paper by DOI")
    doi_cmd.add_argument("doi")
    doi_cmd.add_argument("--json", action="store_true")

    citations_cmd = sub.add_parser("citations", help="Inspect citation chain")
    citations_cmd.add_argument("doi")
    citations_cmd.add_argument("--direction", choices=["cited_by", "references", "both"], default="cited_by")
    citations_cmd.add_argument("--limit", "-l", type=int, default=10)
    citations_cmd.add_argument("--json", action="store_true")

    review_cmd = sub.add_parser("review", help="Generate a Markdown literature review")
    review_cmd.add_argument("topic")
    review_cmd.add_argument("--papers", "-n", type=int, default=20)
    review_cmd.add_argument("--years", help="Year range, e.g. 2020-2026")
    review_cmd.add_argument("--oa", action="store_true", help="Open-access papers only")
    review_cmd.add_argument("--output", "-o", help="Write review to file")
    review_cmd.add_argument("--json", action="store_true")
    review_cmd.add_argument("--qqmedia", action="store_true", help="Stage generated review with qqbot-send")
    review_cmd.add_argument("--stage-media-script", help="Path to qqbot-send scripts/stage_media.py")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "search":
        papers = search_papers(
            query=args.query,
            limit=args.limit,
            sort=args.sort,
            years=args.years,
            oa_only=args.oa,
        )

        if args.json:
            print(json.dumps(papers, indent=2, ensure_ascii=False))
        else:
            print(f"🔍 Found {len(papers)} results for: {args.query}\n")
            print_papers(papers)

        return 0

    if args.cmd == "doi":
        paper = lookup_doi(args.doi)

        if args.json:
            print(json.dumps(paper, indent=2, ensure_ascii=False))
        elif paper:
            print(format_paper(paper))
        else:
            print("❌ Not found")

        return 0

    if args.cmd == "citations":
        result = citation_chain(args.doi, args.direction, args.limit)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for name, papers in result.items():
                icon = "📥" if name == "cited_by" else "📤"
                print(f"\n{icon} {name.replace('_', ' ').title()} ({len(papers)}):\n")
                print_papers(papers)

        return 0

    if args.cmd == "review":
        eprint(f"📚 Review topic: {args.topic}")
        eprint(f"Target papers: {args.papers}")

        papers = collect_review_papers(
            topic=args.topic,
            target_count=args.papers,
            years=args.years,
            oa_only=args.oa,
        )

        if not papers:
            eprint("No papers found")
            return 1

        if args.json:
            payload = {
                "topic": args.topic,
                "paper_count": len(papers),
                "papers": papers,
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0

        markdown = make_review_markdown(args.topic, papers, args.years)

        if args.output:
            output_path = save_text(args.output, markdown)
            eprint(f"✅ Review written to {output_path}")
        elif args.qqmedia:
            output_path = save_text(default_review_path(args.topic), markdown)
            eprint(f"✅ Review written to {output_path}")
        else:
            print(markdown)
            return 0

        if args.qqmedia:
            try:
                output_qqmedia(output_path, args.stage_media_script)
            except RuntimeError as exc:
                eprint(f"QQ media handoff failed: {exc}")
                eprint(f"Review file remains available at: {output_path}")
                return 1

        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())