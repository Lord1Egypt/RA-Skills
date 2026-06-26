#!/usr/bin/env python3
"""Assemble the final related works report from intermediate artifacts.

Usage:
  python3 build_final_related_works_report.py \
    step1_extracted_related_works_and_citations.md \
    step2_deduplicated_paper_list.md \
    abstract_batches_dir \
    final_related_works_report.md \
    [step1_normalized_related_works.md]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def parse_step1(text: str) -> list[dict[str, str]]:
    pattern = re.compile(
        r"^##\s+\d+\.\s+(?P<title>.+?)\n\n"
        r"Source file:\s+`(?P<source>[^`]+)`\n\n"
        r"### Related Works Original Text\n\n```text\n(?P<body>.*?)\n```\n",
        re.S | re.M,
    )
    return [
        {
            "title": m.group("title").strip(),
            "source": m.group("source").strip(),
            "body": m.group("body").rstrip(),
        }
        for m in pattern.finditer(text)
    ]


def parse_step2(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| P"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        items.append(
            {
                "dedup_id": parts[0],
                "year": parts[1],
                "title": parts[2],
                "authors": parts[3],
                "source_occurrences": parts[4],
            }
        )
    return items


def parse_batch_results(text: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    current_id = ""
    current_title = ""
    current_url = ""
    current_abstract = ""

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("### "):
            if current_id:
                out[current_id] = {
                    "title": current_title,
                    "arxiv_url": current_url,
                    "abstract": current_abstract,
                }
            match = re.match(r"###\s+(P\d+)[\.:]\s+(.*)$", stripped)
            if match:
                current_id = match.group(1)
                current_title = match.group(2).strip()
                current_url = ""
                current_abstract = ""
        elif stripped.startswith("- arXiv URL:"):
            current_url = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Abstract:"):
            current_abstract = stripped.split(":", 1)[1].strip()

    if current_id:
        out[current_id] = {
            "title": current_title,
            "arxiv_url": current_url,
            "abstract": current_abstract,
        }
    return out


def bib_escape(value: str) -> str:
    value = value.replace("\\", "\\\\")
    value = value.replace("{", "\\{").replace("}", "\\}")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def build_bibtex_entry(item: dict[str, str], abstract_data: dict[str, str] | None) -> str:
    abstract_data = abstract_data or {}
    fields = [
        f"  title = {{{bib_escape(item['title'])}}}",
        f"  author = {{{bib_escape(item['authors'])}}}",
    ]
    if item["year"]:
        fields.append(f"  year = {{{bib_escape(item['year'])}}}")
    if abstract_data.get("arxiv_url"):
        fields.append(f"  url = {{{bib_escape(abstract_data['arxiv_url'])}}}")
    if abstract_data.get("abstract"):
        fields.append(f"  abstract = {{{bib_escape(abstract_data['abstract'])}}}")
        fields.append("  retrieval_status = {matched}")
    else:
        fields.append("  retrieval_status = {no_reliable_arxiv_abstract}")
    fields.append(f"  source_occurrences = {{{bib_escape(item['source_occurrences'])}}}")
    return "@misc{" + item["dedup_id"] + ",\n" + ",\n".join(fields) + "\n}"


def main(argv: list[str]) -> int:
    if len(argv) not in {4, 5}:
        print(
            "Usage: python3 build_final_related_works_report.py <step1.md> <step2.md> <abstract_batches_dir> <output.md> [normalized.md]",
            file=sys.stderr,
        )
        return 1

    step1_path = Path(argv[0])
    step2_path = Path(argv[1])
    batches_dir = Path(argv[2])
    output_path = Path(argv[3])
    normalized_path = Path(argv[4]) if len(argv) == 5 else None

    step1_sections = parse_step1(step1_path.read_text(encoding="utf-8"))
    step2_items = parse_step2(step2_path.read_text(encoding="utf-8"))

    abstract_map: dict[str, dict[str, str]] = {}
    for batch_file in sorted(batches_dir.glob("batch_*_results.md")):
        abstract_map.update(parse_batch_results(batch_file.read_text(encoding="utf-8")))

    matched_count = sum(1 for v in abstract_map.values() if v.get("arxiv_url"))
    lines: list[str] = []
    lines.append("# Final Related Works Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Source papers: {len(step1_sections)}")
    lines.append(f"- Deduplicated cited papers: {len(step2_items)}")
    lines.append(f"- Papers with reliable arXiv abstract: {matched_count}")
    lines.append("")
    lines.append("## Part 1. Related Works Original Text")
    lines.append("")

    for idx, sec in enumerate(step1_sections, 1):
        lines.append(f"### {idx}. {sec['title']}")
        lines.append(f"- Source file: `{sec['source']}`")
        lines.append("")
        lines.append("```text")
        lines.append(sec["body"])
        lines.append("```")
        lines.append("")

    if normalized_path and normalized_path.exists():
        lines.append("## Part 1B. Related Works with Normalized Citations")
        lines.append("")
        lines.append(normalized_path.read_text(encoding="utf-8").rstrip())
        lines.append("")

    lines.append("## Part 2. BibTeX with Abstracts")
    lines.append("")
    for item in step2_items:
        lines.append("```bibtex")
        lines.append(build_bibtex_entry(item, abstract_map.get(item["dedup_id"])))
        lines.append("```")
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
