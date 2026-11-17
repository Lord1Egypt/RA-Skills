#!/usr/bin/env python3
"""
Literature synthesis formatter.
Takes search JSON results and outputs structured per-paper summary blocks
for AI-driven literature review generation.

Usage:
    python scripts/search.py -q "query" -n 5 --json | python scripts/summarize.py
    python scripts/summarize.py --file results.json
"""

import sys
import json
import argparse


def format_authors(authors: list[dict]) -> str:
    names = [a.get("name", "?") for a in authors if a.get("name")]
    if not names:
        return "Unknown"
    if len(names) <= 3:
        return ", ".join(names)
    return f"{names[0]} et al. ({len(names)} authors)"


def format_paper_block(paper: dict, index: int) -> str:
    title = paper.get("title", "Untitled")
    authors = format_authors(paper.get("authors", []))
    year = paper.get("year", "Unknown")
    doi = paper.get("doi", "")
    abstract = paper.get("abstract", "(Abstract not available)")
    citation_count = paper.get("citation_count")
    venue = paper.get("venue", "")
    source = paper.get("source", "unknown")
    url = paper.get("url", "")

    block = f"""
---
### Paper #{index}: {title}

**Authors:** {authors}
**Year:** {year}
**Source:** {source}{f' | {venue}' if venue else ''}
{f'**Citations:** {citation_count}' if citation_count else ''}
{f'**DOI:** {doi}' if doi else ''}
{f'**URL:** {url}' if url else ''}

**Abstract:**
{abstract[:2000]}

---
"""
    return block


def generate_batch_prompt(papers: list[dict], query: str) -> str:
    """Generate a batch summary template for AI-driven review."""
    lines = [
        f"# Literature Review: {query}",
        f"",
        f"Total papers: {len(papers)}",
        f"",
        "For each paper below, provide a concise academic summary:",
        "1. Core research question and motivation",
        "2. Key methodology / approach",
        "3. Main findings and conclusions",
        "4. Significance and limitations",
        "",
    ]

    for i, paper in enumerate(papers, 1):
        lines.append(format_paper_block(paper, i))

    lines.extend([
        "",
        "## Overall Synthesis",
        "After reviewing all papers above, provide:",
        "1. Cross-cutting themes and trends",
        "2. Consensus findings vs. controversies",
        "3. Gaps in the literature",
        "4. Directions for future research",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate literature summary blocks")
    parser.add_argument("--file", "-f", type=str, help="Input JSON file (default: stdin)")
    parser.add_argument("--format", type=str, default="batch",
                        choices=["batch", "individual"],
                        help="Output format: batch (single prompt) or individual (per-paper)")
    parser.add_argument("--output", "-o", type=str, help="Output file (default: stdout)")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    query = data.get("query", "Unknown query")
    papers = data.get("results", [])

    if args.format == "batch":
        output = generate_batch_prompt(papers, query)
    else:
        output = ""
        for i, paper in enumerate(papers, 1):
            output += format_paper_block(paper, i)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
