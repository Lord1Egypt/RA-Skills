#!/usr/bin/env python3
"""
Unified literature search entry point.
Routes queries to arXiv, Semantic Scholar, PubMed, CrossRef, Baidu Scholar,
then deduplicates and ranks results.

Usage:
    python scripts/search.py --query "transformer attention mechanism" --max 10
    python scripts/search.py --query "transformer" --source arxiv,semantic_scholar --year-from 2022
    python scripts/search.py --query "cancer immunotherapy" --source pubmed
    python scripts/search.py --query "深度学习" --source baidu_scholar
    python scripts/search.py --doi "10.1038/nature14539" --bibtex
    python scripts/search.py --citations "paper_id" --source semantic_scholar
    python scripts/search.py --author "Yann LeCun" --source semantic_scholar
"""

import sys
import json
import argparse
import re
import concurrent.futures
from typing import Optional

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from arxiv_api import search as arxiv_search
from semantic_scholar_api import (
    search as s2_search,
    get_citations,
    get_references,
    search_author,
    get_author_papers,
    get_paper as s2_get_paper,
)
from pubmed_api import search as pubmed_search
from crossref_api import search as crossref_search, get_by_doi, get_bibtex
from baidu_scholar_api import search as baidu_scholar_search
from summarize import generate_batch_prompt

ALL_SOURCES = ["arxiv", "semantic_scholar", "pubmed", "crossref", "baidu_scholar"]

SOURCE_MAP = {
    "arxiv": arxiv_search,
    "semantic_scholar": s2_search,
    "pubmed": pubmed_search,
    "crossref": crossref_search,
    "baidu_scholar": baidu_scholar_search,
}

EN_ONLY_SOURCES = ["arxiv", "semantic_scholar", "pubmed"]

_CN_PATTERN = re.compile(r"[\u4e00-\u9fff]")


def _is_chinese_query(query: str) -> bool:
    """Detect if query contains Chinese characters."""
    return bool(_CN_PATTERN.search(query))


def _smart_sources(query: str, user_sources: str) -> list[str]:
    """Choose optimal sources based on query language and user preference."""
    if user_sources != "all" and user_sources:
        return [s.strip() for s in user_sources.split(",") if s.strip() in ALL_SOURCES]

    if _is_chinese_query(query):
        return ["baidu_scholar", "crossref"]
    return ALL_SOURCES


def normalize_result(paper: dict) -> dict:
    """Ensure all papers share a common key set."""
    return {
        "source": paper.get("source", "unknown"),
        "id": paper.get("id", ""),
        "title": paper.get("title", ""),
        "authors": paper.get("authors", []),
        "abstract": paper.get("abstract", ""),
        "year": paper.get("year") or (int(paper.get("published", "0")[:4]) if paper.get("published") else None),
        "published": paper.get("published", ""),
        "doi": paper.get("doi", ""),
        "url": paper.get("url", ""),
        "pdf_url": paper.get("pdf_url", ""),
        "citation_count": paper.get("citation_count"),
        "venue": paper.get("venue", "") or paper.get("container", "") or paper.get("source_journal", ""),
        "categories": paper.get("categories", []),
    }


def deduplicate(papers: list[dict]) -> list[dict]:
    """Remove duplicate papers, keeping the entry with most data.
    Dedup by DOI first, then by normalized title."""
    by_doi = {}
    by_title = {}
    unmerged = []

    for p in papers:
        if p["doi"]:
            existing = by_doi.get(p["doi"])
            if existing:
                if _score_richness(p) > _score_richness(existing):
                    by_doi[p["doi"]] = p
            else:
                by_doi[p["doi"]] = p
            continue

        title_key = p["title"].lower().strip().rstrip(".")
        if title_key and len(title_key) > 20:
            existing = by_title.get(title_key)
            if existing:
                if _score_richness(p) > _score_richness(existing):
                    by_title[title_key] = p
            else:
                by_title[title_key] = p
            continue

        unmerged.append(p)

    merged = list(by_doi.values()) + list(by_title.values()) + unmerged
    return merged


def _score_richness(p: dict) -> int:
    score = 0
    if p["abstract"]:
        score += 3
    if p["doi"]:
        score += 2
    if p["authors"]:
        score += min(len(p["authors"]), 5)
    if p["citation_count"]:
        score += 1
    if p["pdf_url"]:
        score += 1
    return score


def rank(papers: list[dict]) -> list[dict]:
    """Sort papers by citation count (desc), then year (desc)."""
    def sort_key(p):
        citations = p.get("citation_count") or 0
        year = p.get("year") or 0
        return (-citations, -year)
    return sorted(papers, key=sort_key)


def search_multi(
    query: str,
    sources: list[str],
    max_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> list[dict]:
    """Concurrently search multiple sources."""
    all_results = []

    per_source = max(5, max_results // len(sources) + 2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources)) as executor:
        futures = {}
        for src in sources:
            if src not in SOURCE_MAP:
                continue
            kwargs = {"query": query, "max_results": min(per_source, 20)}
            if year_from:
                kwargs["year_from"] = year_from
            if year_to:
                kwargs["year_to"] = year_to

            futures[executor.submit(SOURCE_MAP[src], **kwargs)] = src

        for future in concurrent.futures.as_completed(futures):
            src = futures[future]
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                print(f"[WARN] Source '{src}' failed: {e}", file=sys.stderr)

    normalized = [normalize_result(p) for p in all_results]
    deduped = deduplicate(normalized)
    ranked = rank(deduped)

    return ranked[:max_results]


def main():
    parser = argparse.ArgumentParser(description="Unified literature search")
    parser.add_argument("--query", "-q", type=str, help="Search query")
    parser.add_argument("--source", "-s", type=str, default="all",
                        help=f"Comma-separated sources: {','.join(ALL_SOURCES)} or 'all'")
    parser.add_argument("--max", "-n", type=int, default=10, help="Max results (default 10)")
    parser.add_argument("--year-from", type=int, help="Filter from year")
    parser.add_argument("--year-to", type=int, help="Filter to year")
    parser.add_argument("--doi", type=str, help="Look up paper by DOI")
    parser.add_argument("--bibtex", action="store_true", help="Get BibTeX for DOI (use with --doi)")
    parser.add_argument("--citations", type=str, help="Get citations of a paper by S2 paper ID")
    parser.add_argument("--references", type=str, help="Get references of a paper by S2 paper ID")
    parser.add_argument("--author", type=str, help="Search for author and their papers")
    parser.add_argument("--summarize", action="store_true", help="Output structured per-paper summary blocks for AI review")
    parser.add_argument("--json", action="store_true", default=True, help="Output JSON")

    args = parser.parse_args()

    # DOI lookup
    if args.doi:
        if args.bibtex:
            bib = get_bibtex(args.doi)
            if bib:
                print(bib)
                return
            else:
                print(json.dumps({"error": "BibTeX not available for this DOI"}, ensure_ascii=False))
                return

        paper = get_by_doi(args.doi)
        if paper:
            print(json.dumps(normalize_result(paper), ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": f"No results for DOI: {args.doi}"}, ensure_ascii=False))
        return

    # Citations
    if args.citations:
        results = get_citations(args.citations, max_results=args.max)
        normalized = [normalize_result(p) for p in results]
        print(json.dumps(normalized, ensure_ascii=False, indent=2))
        return

    # References
    if args.references:
        results = get_references(args.references, max_results=args.max)
        normalized = [normalize_result(p) for p in results]
        print(json.dumps(normalized, ensure_ascii=False, indent=2))
        return

    # Author search
    if args.author:
        authors = search_author(args.author)
        if authors:
            top_author = authors[0]
            author_id = top_author.get("authorId", "")
            papers = get_author_papers(author_id, max_results=args.max)
            normalized = [normalize_result(p) for p in papers]
            print(json.dumps({
                "author": {"name": top_author.get("name", ""), "id": author_id,
                           "paperCount": top_author.get("paperCount"),
                           "citationCount": top_author.get("citationCount")},
                "papers": normalized,
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": f"No author found: {args.author}"}, ensure_ascii=False))
        return

    # Multi-source search
    if not args.query:
        print(json.dumps({"error": "No query provided. Use --query or --doi or --citations or --author."}, ensure_ascii=False))
        sys.exit(1)

    sources = _smart_sources(args.query, args.source)
    if not sources:
        print(json.dumps({"error": f"No valid sources. Available: {','.join(ALL_SOURCES)}"}, ensure_ascii=False))
        sys.exit(1)

    results = search_multi(
        query=args.query,
        sources=sources,
        max_results=args.max,
        year_from=args.year_from,
        year_to=args.year_to,
    )

    if args.summarize:
        output = generate_batch_prompt(results, args.query)
        print(output)
    else:
        print(json.dumps({
            "query": args.query,
            "sources": sources,
            "count": len(results),
            "results": results,
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
