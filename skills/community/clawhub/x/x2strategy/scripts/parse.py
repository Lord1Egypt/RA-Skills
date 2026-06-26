#!/usr/bin/env python3
"""parse.py — Extract structured content from a quantitative finance paper PDF.

Usage (CLI):
    python scripts/parse.py paper.pdf                    # Mode A (builtin)
    python scripts/parse.py paper.pdf --mode agent       # Mode B (FAISS)
    python scripts/parse.py paper.pdf -o content.json    # custom output path
    # default output if -o omitted: <PAPER2SPEC_LIBRARY_PATH>/<pdf_stem>/content.json

Usage (agent):
    The agent reads SKILL.md, then runs this script on the user's PDF.

Output: JSON file with PaperContent (title, abstract, methodology, data_description, signal_logic, …)
"""

import argparse
import json
import logging
import os
import sys

# Allow running from repo root or scripts/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from paper2spec.parser import parse_pdf
from paper2spec.config import get_library_path


def main():
    parser = argparse.ArgumentParser(
        description="Parse a quantitative finance paper PDF into structured JSON."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "-o", "--output",
        help="Output JSON path (default: <PAPER2SPEC_LIBRARY_PATH>/<pdf_stem>/content.json)",
    )
    parser.add_argument(
        "--mode",
        choices=["builtin", "agent"],
        default="builtin",
        help="Extraction mode: 'builtin' (direct LLM, no embeddings) or 'agent' (FAISS semantic search)",
    )
    parser.add_argument(
        "--model",
        help="Override LLM model (e.g. openai/gpt-4o, anthropic/claude-sonnet-4-20250514)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    if not os.path.isfile(args.pdf):
        print(f"Error: file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    # Parse
    paper_content = parse_pdf(args.pdf, mode=args.mode, model=args.model)

    # Output path
    if args.output:
        out_path = args.output
    else:
        stem = os.path.splitext(os.path.basename(args.pdf))[0]
        base_library = get_library_path()
        paper_dir = os.path.join(base_library, stem)
        out_path = os.path.join(paper_dir, "content.json")

    out_parent = os.path.dirname(out_path)
    if out_parent:
        os.makedirs(out_parent, exist_ok=True)

    # Write
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(paper_content.to_json())

    print(f"✅ Wrote {out_path} ({os.path.getsize(out_path)} bytes)")
    print(f"   Title: {paper_content.title}")
    print(f"   Methodology: {len(paper_content.methodology)} chars")
    print(f"   Signal Logic: {len(paper_content.signal_logic)} chars")
    print(f"   Data Description: {len(paper_content.data_description)} chars")


if __name__ == "__main__":
    main()
