#!/usr/bin/env python3
"""analyze.py — One-shot document → all outputs (content + spec + markdown).

Runs the full paper2spec pipeline:
  1. Parse document (PDF/MD/DOCX/TXT) → PaperContent JSON + Markdown
  2. Extract PaperContent → ExtractionResult JSON + Markdown

All outputs are written to the specified output directory.

Usage:
    python scripts/analyze.py paper.pdf                     # PDF input
    python scripts/analyze.py strategy.md                   # Markdown input
    python scripts/analyze.py report.docx                   # DOCX input
    python scripts/analyze.py paper.pdf -o library/paper/    # custom output dir
    python scripts/analyze.py paper.pdf --parser-mode agent  # Mode B (FAISS)
"""

import argparse
import json
import logging
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from paper2spec.extractor import extract_spec
from paper2spec.config import get_library_path
from paper2spec.models import PaperContent
from paper2spec.parser import parse_document
from paper2spec.render import content_to_markdown, spec_to_markdown


def _slugify(text: str) -> str:
    """Convert a title to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "_", text)
    return text[:80].rstrip("_") or "paper"


def main():
    parser = argparse.ArgumentParser(
        description="Full pipeline: Document (PDF/MD/DOCX/TXT) → PaperContent + StrategySpec (JSON + Markdown)."
    )
    parser.add_argument("input", help="Path to document file (PDF, .md, .docx, or .txt)")
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory (default: <PAPER2SPEC_LIBRARY_PATH>/<slugified_title>/)",
    )
    parser.add_argument(
        "--parser-mode",
        choices=["builtin", "agent"],
        default="builtin",
        help="Parser mode: 'builtin' (fast, no embeddings) or 'agent' (FAISS, better for long papers)",
    )
    parser.add_argument(
        "--extractor-mode",
        choices=["multilayer", "single"],
        default="multilayer",
        help="Extractor mode: 'multilayer' (recommended) or 'single' (legacy)",
    )
    parser.add_argument("--model", help="Override LLM model for both stages")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    if not os.path.isfile(args.input):
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # ── Stage 1: Parse ──
    print(f"📄 Parsing {args.input}...")
    pc = parse_document(args.input, mode=args.parser_mode, model=args.model)
    print(f"   Title: {pc.title}")

    # Determine output directory
    if args.output_dir:
        out_dir = args.output_dir
    else:
        base_library = get_library_path()
        slug = _slugify(pc.title or os.path.splitext(os.path.basename(args.input))[0])
        out_dir = os.path.join(base_library, slug)
    os.makedirs(out_dir, exist_ok=True)

    # Write PaperContent JSON
    content_json_path = os.path.join(out_dir, "content.json")
    with open(content_json_path, "w", encoding="utf-8") as f:
        f.write(pc.to_json())

    # Write PaperContent Markdown
    content_md_path = os.path.join(out_dir, "content.md")
    with open(content_md_path, "w", encoding="utf-8") as f:
        f.write(content_to_markdown(pc))

    print(f"   → {content_json_path} ({os.path.getsize(content_json_path):,} bytes)")
    print(f"   → {content_md_path}")

    # ── Stage 2: Extract ──
    print(f"\n🔬 Extracting strategies...")
    result = extract_spec(pc, model=args.model, mode=args.extractor_mode)

    # Write ExtractionResult JSON
    spec_json_path = os.path.join(out_dir, "spec.json")
    with open(spec_json_path, "w", encoding="utf-8") as f:
        f.write(result.to_json())

    # Write ExtractionResult Markdown
    spec_md_path = os.path.join(out_dir, "spec.md")
    with open(spec_md_path, "w", encoding="utf-8") as f:
        f.write(spec_to_markdown(result))

    print(f"   → {spec_json_path} ({os.path.getsize(spec_json_path):,} bytes)")
    print(f"   → {spec_md_path}")

    # Copy original source file into output directory for self-contained library
    src_basename = os.path.basename(args.input)
    src_dest = os.path.join(out_dir, src_basename)
    if os.path.abspath(args.input) != os.path.abspath(src_dest):
        shutil.copy2(args.input, src_dest)
        print(f"   → {src_dest} (original source)")

    # Write metadata
    metadata = {
        "source_file": os.path.abspath(args.input),
        "source_filename": src_basename,
        "source_format": os.path.splitext(src_basename)[1].lower(),
        "paper_title": pc.title,
        "paper_title": pc.title,
        "parser_mode": args.parser_mode,
        "extractor_mode": args.extractor_mode,
        "model": args.model or os.environ.get("PAPER2SPEC_MODEL", ""),
        "num_strategies": result.num_detected,
        "strategies": [s.strategy_name for s in result.strategies],
        "version": "0.3.0",
    }
    meta_path = os.path.join(out_dir, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # ── Summary ──
    print(f"\n✅ Analysis complete → {out_dir}/")
    print(f"   Strategies: {result.num_detected}")
    for i, spec in enumerate(result.strategies):
        print(f"   [{i+1}] {spec.strategy_name} ({spec.strategy_type})")
        print(f"       {len(spec.indicators)} indicators, {len(spec.logic_pipeline)} logic steps")

    print(f"\n   Files:")
    print(f"     {src_basename:<16s} — Original document")
    print(f"     content.json   — PaperContent (machine-readable)")
    print(f"     content.md     — PaperContent (human-readable)")
    print(f"     spec.json      — StrategySpec (machine-readable)")
    print(f"     spec.md        — StrategySpec (human-readable)")
    print(f"     metadata.json  — Analysis metadata")


if __name__ == "__main__":
    main()
