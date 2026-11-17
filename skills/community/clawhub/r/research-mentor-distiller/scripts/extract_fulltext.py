#!/usr/bin/env python3
"""Extract full text from PDFs and generate distillation signal cards.

Use this after collect_publications.py has downloaded open PDFs, or point it at
any folder of PDFs the user is allowed to provide. The script creates markdown
full texts, per-paper signal cards, and a workbench for cross-direction method
synthesis. It uses pdfplumber when available and falls back to pypdf.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SECTION_PATTERNS = {
    "abstract": r"abstract",
    "introduction": r"introduction",
    "related_work": r"related work|background|prior work",
    "method": r"method|methods|approach|framework|model|architecture",
    "data": r"data|dataset|benchmark|pretraining data|annotation",
    "experiments": r"experiment|experimental setup|implementation details|evaluation",
    "results": r"result|analysis|ablation|comparison",
    "discussion": r"discussion",
    "limitations": r"limitation|limitations|failure|future work",
    "conclusion": r"conclusion|conclusions",
    "appendix": r"appendix|supplementary|supplemental",
}

SIGNAL_PATTERNS = {
    "problem_framing": [
        r"\bchallenge\b",
        r"\bproblem\b",
        r"\bgap\b",
        r"\blimit(?:ation|ed|s)?\b",
        r"\bhowever\b",
        r"\bwe address\b",
        r"\bwe study\b",
        r"\bwe investigate\b",
        r"\bwe aim\b",
    ],
    "contribution": [
        r"\bwe propose\b",
        r"\bwe introduce\b",
        r"\bwe present\b",
        r"\bwe develop\b",
        r"\bwe construct\b",
        r"\bwe release\b",
        r"\bcontribution\b",
    ],
    "data_supervision": [
        r"\bdataset\b",
        r"\bbenchmark\b",
        r"\bannotation\b",
        r"\blabel\b",
        r"\bpseudo-label\b",
        r"\bself-supervised\b",
        r"\bweakly supervised\b",
        r"\breport\b",
        r"\bontology\b",
        r"\bretrieval\b",
    ],
    "method": [
        r"\bframework\b",
        r"\bmodel\b",
        r"\barchitecture\b",
        r"\btraining\b",
        r"\bpretrain",
        r"\bfine-tun",
        r"\breasoning\b",
        r"\bverification\b",
        r"\bmemory\b",
        r"\bagent\b",
    ],
    "evaluation": [
        r"\bevaluate\b",
        r"\bmetric\b",
        r"\bbaseline\b",
        r"\bablation\b",
        r"\boutperform\b",
        r"\bstate-of-the-art\b",
        r"\bgeneralization\b",
        r"\brobust\b",
    ],
    "limits": [
        r"\blimitations?\b",
        r"\bfailure\b",
        r"\bfuture work\b",
        r"\bnot address\b",
        r"\bremain(?:s)?\b",
    ],
}

METHOD_TAGS = {
    "data-engine-or-benchmark": [
        "dataset",
        "benchmark",
        "corpus",
        "annotation",
        "large-scale",
        "curated",
    ],
    "self-or-weak-supervision": [
        "self-supervised",
        "weakly supervised",
        "contrastive",
        "predictive",
        "pretext",
        "pseudo-label",
    ],
    "multimodal-alignment": [
        "vision-language",
        "audio-visual",
        "audiovisual",
        "multimodal",
        "image-text",
        "video-language",
        "text",
    ],
    "knowledge-reasoning-verification": [
        "knowledge",
        "ontology",
        "retrieval",
        "rag",
        "reasoning",
        "verification",
        "traceable",
    ],
    "foundation-model-training": [
        "foundation model",
        "pre-training",
        "pretraining",
        "large language model",
        "mllm",
        "generalist",
    ],
    "evaluation-and-ablation": [
        "evaluation",
        "metric",
        "baseline",
        "ablation",
        "generalization",
        "robustness",
    ],
    "domain-translation": [
        "clinical",
        "diagnosis",
        "pathology",
        "radiology",
        "biology",
        "drug",
        "cell",
        "science",
    ],
    "temporal-spatial-perception": [
        "video",
        "motion",
        "temporal",
        "spatial",
        "3d",
        "tracking",
        "scene",
    ],
    "agentic-system": [
        "agent",
        "agentic",
        "system",
        "workflow",
        "environment",
        "tool",
    ],
}

DIRECTION_RULES = [
    (
        "ai4science-and-medicine",
        [
            "clinical",
            "diagnosis",
            "medical",
            "medicine",
            "radiology",
            "pathology",
            "cancer",
            "drug",
            "cell",
            "ehr",
            "disease",
            "biology",
        ],
    ),
    (
        "self-supervised-visual-representation",
        [
            "self-supervised",
            "representation learning",
            "predictive coding",
            "correspondence",
            "pretext",
            "contrastive",
        ],
    ),
    (
        "multimodal-audio-visual-language",
        [
            "audio",
            "speech",
            "sound",
            "lip",
            "vision-language",
            "video-language",
            "multimodal",
            "text retrieval",
        ],
    ),
    (
        "vision-spatial-video-and-3d",
        [
            "tracking",
            "spatial",
            "3d",
            "video",
            "scene",
            "soccer",
            "flow",
            "image generation",
        ],
    ),
]


@dataclass
class PdfRecord:
    pdf_path: Path
    title: str
    year: int | None = None
    venue: str = ""
    direction: str = ""
    url: str = ""
    source_id: str = ""


@dataclass
class ExtractedPaper:
    record: PdfRecord
    method: str
    page_count: int
    text: str
    sections: dict[str, str]
    direction: str
    method_tags: Counter
    warnings: list[str]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def slugify(value: str, max_len: int = 96) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return (value[:max_len].strip("-") or "untitled")


def md_escape(value: Any) -> str:
    return normalize_ws(str(value or "")).replace("|", "\\|")


def load_pdf_records(args: argparse.Namespace) -> list[PdfRecord]:
    records: list[PdfRecord] = []
    seen: set[Path] = set()
    if args.publication_index:
        data = json.loads(args.publication_index.read_text(encoding="utf-8"))
        base = args.publication_index.parent
        for pub in data.get("publications", []):
            local_pdf = pub.get("local_pdf") or ""
            if not local_pdf:
                continue
            path = Path(local_pdf)
            if not path.is_absolute():
                path = (base / path).resolve()
            if path.exists() and path.suffix.lower() == ".pdf":
                records.append(
                    PdfRecord(
                        pdf_path=path,
                        title=pub.get("title") or path.stem,
                        year=pub.get("year"),
                        venue=pub.get("venue") or "",
                        direction=pub.get("direction") or "",
                        url=pub.get("url") or pub.get("pdf_url") or "",
                        source_id=pub.get("id") or "",
                    )
                )
                seen.add(path.resolve())
    if args.pdf_dir:
        for path in sorted(args.pdf_dir.rglob("*.pdf")):
            resolved = path.resolve()
            if resolved in seen:
                continue
            records.append(PdfRecord(pdf_path=resolved, title=path.stem))
            seen.add(resolved)
    if args.max_papers:
        records = records[: args.max_papers]
    return records


def extract_pdf_text(path: Path, max_pages: int | None) -> tuple[str, str, int]:
    pdfplumber_error = None
    try:
        import pdfplumber  # type: ignore

        pages = []
        with pdfplumber.open(path) as pdf:
            page_limit = min(len(pdf.pages), max_pages) if max_pages else len(pdf.pages)
            for idx, page in enumerate(pdf.pages[:page_limit], start=1):
                page_text = page.extract_text(x_tolerance=1.5, y_tolerance=3) or ""
                pages.append(f"\n\n<!-- page: {idx} -->\n\n{page_text}")
            return normalize_text("\n".join(pages)), "pdfplumber", len(pdf.pages)
    except Exception as exc:  # noqa: BLE001
        pdfplumber_error = exc

    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        page_count = len(reader.pages)
        page_limit = min(page_count, max_pages) if max_pages else page_count
        pages = []
        for idx in range(page_limit):
            page_text = reader.pages[idx].extract_text() or ""
            pages.append(f"\n\n<!-- page: {idx + 1} -->\n\n{page_text}")
        return normalize_text("\n".join(pages)), "pypdf", page_count
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Could not extract text from {path}. pdfplumber error: {pdfplumber_error}; pypdf error: {exc}"
        ) from exc


def is_heading(line: str) -> str | None:
    line = normalize_ws(line)
    if not line or len(line) > 90:
        return None
    line = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", line)
    line = line.strip(" :-")
    low = line.lower()
    for key, pattern in SECTION_PATTERNS.items():
        if re.fullmatch(pattern, low, flags=re.IGNORECASE):
            return key
    return None


def split_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    sections: dict[str, list[str]] = defaultdict(list)
    current = "front_matter"
    for line in lines:
        marker = re.match(r"<!-- page: \d+ -->", line.strip())
        heading = None if marker else is_heading(line)
        if heading:
            current = heading
            continue
        sections[current].append(line)
    cleaned = {key: normalize_text("\n".join(value)) for key, value in sections.items() if normalize_ws("\n".join(value))}
    if "abstract" not in cleaned:
        abstract = infer_abstract(text)
        if abstract:
            cleaned["abstract"] = abstract
    return cleaned


def infer_abstract(text: str) -> str:
    match = re.search(
        r"(?is)\babstract\b\s*[:.-]?\s*(.*?)(?:\n\s*(?:1\.?\s*)?introduction\b|\n\s*keywords?\b|\n\s*index terms\b)",
        text[:12000],
    )
    if match:
        return normalize_text(match.group(1))
    paragraphs = [normalize_ws(p) for p in re.split(r"\n\s*\n", text[:8000]) if len(normalize_ws(p)) > 120]
    return paragraphs[0] if paragraphs else ""


def sentence_split(text: str) -> list[str]:
    text = normalize_ws(text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
    return [p.strip() for p in parts if 50 <= len(p.strip()) <= 450]


def pick_sentences(text: str, patterns: list[str], limit: int = 5) -> list[str]:
    picked = []
    combined = re.compile("|".join(patterns), flags=re.IGNORECASE)
    for sentence in sentence_split(text):
        if combined.search(sentence):
            picked.append(sentence)
        if len(picked) >= limit:
            break
    return picked


def count_method_tags(text: str) -> Counter:
    low = text.lower()
    counts = Counter()
    for tag, terms in METHOD_TAGS.items():
        total = 0
        for term in terms:
            total += len(re.findall(re.escape(term.lower()), low))
        if total:
            counts[tag] = total
    return counts


def infer_direction(record: PdfRecord, text: str) -> str:
    if record.direction:
        return slugify(record.direction, 80)
    search_space = f"{record.title}\n{text[:12000]}".lower()
    scores = []
    for direction, terms in DIRECTION_RULES:
        score = sum(search_space.count(term) for term in terms)
        if score:
            scores.append((score, direction))
    if scores:
        return sorted(scores, reverse=True)[0][1]
    return "general"


def render_fulltext_md(paper: ExtractedPaper, max_chars: int) -> str:
    record = paper.record
    lines = [
        f"# {record.title}",
        "",
        "## Metadata",
        "",
        f"- Source PDF: `{record.pdf_path}`",
        f"- URL: {record.url or 'unknown'}",
        f"- Year: {record.year or 'unknown'}",
        f"- Venue: {record.venue or 'unknown'}",
        f"- Direction: {paper.direction}",
        f"- Extraction method: {paper.method}",
        f"- Pages in PDF: {paper.page_count}",
        "",
        "## Detected Sections",
        "",
    ]
    for key in SECTION_PATTERNS:
        if key in paper.sections:
            lines.append(f"- {key}: {len(paper.sections[key])} characters")
    lines.extend(["", "## Section Text", ""])
    for key, content in paper.sections.items():
        if key == "front_matter" and "abstract" in paper.sections:
            continue
        lines.extend([f"### {key.replace('_', ' ').title()}", "", content[:max_chars], ""])
    if len(paper.text) > max_chars:
        lines.extend(
            [
                "## Raw Full Text",
                "",
                paper.text[:max_chars],
                "",
                f"[Truncated at {max_chars} characters for markdown size. Re-run with --max-fulltext-chars to adjust.]",
                "",
            ]
        )
    return "\n".join(lines)


def render_signal_card(paper: ExtractedPaper) -> str:
    record = paper.record
    abstract_intro = "\n".join(
        [
            paper.sections.get("abstract", ""),
            paper.sections.get("introduction", ""),
            paper.sections.get("front_matter", "")[:3000],
        ]
    )
    method_text = "\n".join([paper.sections.get("method", ""), paper.sections.get("data", "")])
    eval_text = "\n".join([paper.sections.get("experiments", ""), paper.sections.get("results", "")])
    all_text = paper.text
    signal_sources = {
        "problem_framing": abstract_intro,
        "contribution": abstract_intro,
        "data_supervision": "\n".join([abstract_intro, method_text]),
        "method": method_text or all_text[:12000],
        "evaluation": eval_text or all_text[:16000],
        "limits": "\n".join([paper.sections.get("limitations", ""), paper.sections.get("discussion", ""), paper.sections.get("conclusion", "")]),
    }
    lines = [
        f"# Paper Signal Card: {record.title}",
        "",
        "## Metadata",
        "",
        f"- Source PDF: `{record.pdf_path}`",
        f"- Year: {record.year or 'unknown'}",
        f"- Venue: {record.venue or 'unknown'}",
        f"- Direction hypothesis: {paper.direction}",
        f"- URL: {record.url or 'unknown'}",
        f"- Extraction method: {paper.method}",
        f"- Page count: {paper.page_count}",
        "",
        "## Method Tags",
        "",
    ]
    if paper.method_tags:
        for tag, count in paper.method_tags.most_common():
            lines.append(f"- {tag}: {count}")
    else:
        lines.append("- none detected")
    lines.extend(["", "## Section Coverage", ""])
    for key in SECTION_PATTERNS:
        status = "present" if key in paper.sections else "missing"
        lines.append(f"- {key}: {status}")
    lines.extend(["", "## Distillation Signals", ""])
    for signal, source_text in signal_sources.items():
        lines.extend([f"### {signal.replace('_', ' ').title()}", ""])
        picks = pick_sentences(source_text, SIGNAL_PATTERNS[signal], limit=5)
        if picks:
            for sentence in picks:
                lines.append(f"- {sentence}")
        else:
            lines.append("- No high-confidence sentence found automatically. Agent should inspect the full text manually.")
        lines.append("")
    lines.extend(
        [
            "## Agent Notes To Fill",
            "",
            "- Problem framing:",
            "- Contribution type:",
            "- Data and supervision pattern:",
            "- Methodological move:",
            "- Evaluation taste:",
            "- Boundary or anti-pattern signal:",
            "- Confidence: direct evidence / strong inference / speculative extension",
            "",
        ]
    )
    return "\n".join(lines)


def render_workbench(papers: list[ExtractedPaper], generated_at: str) -> str:
    direction_groups: dict[str, list[ExtractedPaper]] = defaultdict(list)
    total_tags = Counter()
    tag_paper_presence = Counter()
    for paper in papers:
        direction_groups[paper.direction].append(paper)
        total_tags.update(paper.method_tags)
        for tag in paper.method_tags:
            tag_paper_presence[tag] += 1
    lines = [
        "# Full-Text Distillation Workbench",
        "",
        f"- Generated: {generated_at}",
        f"- Papers extracted: {len(papers)}",
        "",
        "## Cross-Direction Methodology Seeds",
        "",
        "Treat these as leads, not conclusions. Promote a pattern into the mentor skill only after checking the paper signal cards and full-text evidence.",
        "",
    ]
    recurring = [(tag, count) for tag, count in tag_paper_presence.most_common() if count >= 2]
    if recurring:
        for tag, count in recurring:
            lines.append(f"- {tag}: appears in {count} papers; total mentions {total_tags[tag]}")
    else:
        lines.append("- No recurring tag appears in at least two extracted papers.")
    lines.extend(["", "## Direction-Specific Methodology Seeds", ""])
    for direction, items in sorted(direction_groups.items()):
        local_tags = Counter()
        for paper in items:
            local_tags.update(paper.method_tags)
        lines.extend([f"### {direction}", ""])
        lines.append(f"- Papers: {len(items)}")
        if local_tags:
            lines.append("- Top method tags: " + ", ".join(f"{tag} ({count})" for tag, count in local_tags.most_common(8)))
        else:
            lines.append("- Top method tags: none detected")
        lines.append("- Representative papers:")
        for paper in items[:12]:
            lines.append(f"  - {paper.record.year or 'unknown'}: {paper.record.title}")
        lines.append("")
    lines.extend(
        [
            "## Agent Synthesis Checklist",
            "",
            "- Core methodology across directions: identify moves recurring across at least two directions or three papers.",
            "- Direction methodology: separate AI4Science/medicine, self-supervised representation, multimodal audio-visual-language, and spatial/video/3D vision when evidence supports the split.",
            "- Evidence recurrence: cite at least two papers for a strong inference; otherwise label it speculative.",
            "- Full-text priority: prefer introduction/method/experiment/limitation evidence over title-only or abstract-only signals.",
            "- Boundary: do not infer private beliefs, current unpublished opinions, or exact review decisions.",
            "",
        ]
    )
    return "\n".join(lines)


def render_report(papers: list[ExtractedPaper], failures: list[str], generated_at: str) -> str:
    lines = [
        "# Full-Text Extraction Report",
        "",
        f"- Generated: {generated_at}",
        f"- Extracted papers: {len(papers)}",
        f"- Failures: {len(failures)}",
        "",
        "## Extracted Papers",
        "",
        "| Title | Direction | Pages | Method | Text Chars | Warnings |",
        "|---|---|---:|---|---:|---|",
    ]
    for paper in papers:
        lines.append(
            "| {title} | {direction} | {pages} | {method} | {chars} | {warnings} |".format(
                title=md_escape(paper.record.title),
                direction=md_escape(paper.direction),
                pages=paper.page_count,
                method=paper.method,
                chars=len(paper.text),
                warnings=md_escape("; ".join(paper.warnings)),
            )
        )
    lines.extend(["", "## Failures", ""])
    if failures:
        lines.extend(f"- {failure}" for failure in failures)
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def write_json_index(papers: list[ExtractedPaper], output_dir: Path, generated_at: str) -> None:
    payload = {
        "generated_at": generated_at,
        "papers": [
            {
                "title": paper.record.title,
                "year": paper.record.year,
                "venue": paper.record.venue,
                "direction": paper.direction,
                "source_pdf": str(paper.record.pdf_path),
                "method": paper.method,
                "page_count": paper.page_count,
                "text_chars": len(paper.text),
                "sections": {key: len(value) for key, value in paper.sections.items()},
                "method_tags": dict(paper.method_tags),
                "warnings": paper.warnings,
            }
            for paper in papers
        ],
    }
    (output_dir / "fulltext-index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publication-index", type=Path, help="publication-index.json from collect_publications.py")
    parser.add_argument("--pdf-dir", type=Path, help="Folder containing PDF files")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output folder for full texts and signal cards")
    parser.add_argument("--max-papers", type=int, default=50, help="Maximum PDFs to process")
    parser.add_argument("--max-pages", type=int, help="Maximum pages per PDF to extract")
    parser.add_argument("--max-fulltext-chars", type=int, default=120000, help="Maximum chars included per fulltext markdown section dump")
    parser.add_argument("--min-text-chars", type=int, default=2500, help="Warn when extracted text is shorter than this")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing markdown outputs")
    args = parser.parse_args()
    if not args.publication_index and not args.pdf_dir:
        parser.error("provide --publication-index or --pdf-dir")
    if args.publication_index:
        args.publication_index = args.publication_index.resolve()
    if args.pdf_dir:
        args.pdf_dir = args.pdf_dir.resolve()
    args.output_dir = args.output_dir.resolve()
    return args


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir
    fulltext_dir = output_dir / "fulltext"
    cards_dir = output_dir / "paper-signal-cards"
    fulltext_dir.mkdir(parents=True, exist_ok=True)
    cards_dir.mkdir(parents=True, exist_ok=True)

    records = load_pdf_records(args)
    failures: list[str] = []
    extracted: list[ExtractedPaper] = []
    if not records:
        failures.append("No PDF records found. Run collect_publications.py with --download-pdfs or provide --pdf-dir.")

    for record in records:
        try:
            text, method, page_count = extract_pdf_text(record.pdf_path, args.max_pages)
            sections = split_sections(text)
            direction = infer_direction(record, text)
            tags = count_method_tags(text)
            warnings = []
            if len(text) < args.min_text_chars:
                warnings.append(f"short extracted text: {len(text)} chars")
            if "abstract" not in sections:
                warnings.append("abstract not detected")
            if "method" not in sections:
                warnings.append("method section not detected")
            if "experiments" not in sections and "results" not in sections:
                warnings.append("experiment/results section not detected")
            paper = ExtractedPaper(
                record=record,
                method=method,
                page_count=page_count,
                text=text,
                sections=sections,
                direction=direction,
                method_tags=tags,
                warnings=warnings,
            )
            extracted.append(paper)

            base_name = f"{record.year or 'unknown'}-{slugify(record.title)}"
            fulltext_path = fulltext_dir / f"{base_name}.md"
            card_path = cards_dir / f"{base_name}.md"
            if args.overwrite or not fulltext_path.exists():
                fulltext_path.write_text(render_fulltext_md(paper, args.max_fulltext_chars), encoding="utf-8")
            if args.overwrite or not card_path.exists():
                card_path.write_text(render_signal_card(paper), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{record.pdf_path}: {exc}")
            print(f"[warn] {record.pdf_path}: {exc}", file=sys.stderr)

    generated_at = now_iso()
    (output_dir / "distillation-workbench.md").write_text(render_workbench(extracted, generated_at), encoding="utf-8")
    (output_dir / "extraction-report.md").write_text(render_report(extracted, failures, generated_at), encoding="utf-8")
    write_json_index(extracted, output_dir, generated_at)
    print(f"Extracted {len(extracted)} papers into {output_dir}")
    if failures and not extracted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
