#!/usr/bin/env python3
"""extract.py — Convert PaperContent JSON into StrategySpec(s) JSON.

Supports multi-strategy papers: when a paper contains multiple independent
strategies, each is extracted separately into its own StrategySpec.

Usage (CLI):
    python scripts/extract.py content.json                  # default output
    python scripts/extract.py content.json -o spec.json     # custom output

Usage (agent):
    Run after parse.py; reads the _content.json artifact.

Input:  PaperContent JSON (from parse.py)
Output: ExtractionResult JSON (array of StrategySpec objects)
"""

import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from paper2spec.extractor import extract_spec
from paper2spec.models import PaperContent


def main():
    parser = argparse.ArgumentParser(
        description="Extract StrategySpec(s) from PaperContent JSON."
    )
    parser.add_argument("content_json", help="Path to PaperContent JSON (from parse.py)")
    parser.add_argument(
        "-o", "--output",
        help="Output JSON path (default: <stem>_spec.json)",
    )
    parser.add_argument(
        "--model",
        help="Override LLM model",
    )
    parser.add_argument(
        "--mode",
        choices=["multilayer", "single"],
        default="multilayer",
        help="Extraction mode: 'multilayer' (4 focused LLM calls, default) or 'single' (1 call, legacy)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    if not os.path.isfile(args.content_json):
        print(f"Error: file not found: {args.content_json}", file=sys.stderr)
        sys.exit(1)

    # Load PaperContent
    with open(args.content_json, "r", encoding="utf-8") as f:
        pc = PaperContent.from_dict(json.load(f))

    # Extract (returns ExtractionResult with list of specs)
    result = extract_spec(pc, model=args.model, mode=args.mode)

    # Output path
    if args.output:
        out_path = args.output
    else:
        stem = os.path.splitext(os.path.basename(args.content_json))[0]
        stem = stem.replace("_content", "")
        out_path = f"{stem}_spec.json"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result.to_json())

    print(f"\n✅ Wrote {out_path} ({os.path.getsize(out_path)} bytes)")
    print(f"   Paper: {result.paper_title}")
    print(f"   Strategies detected: {result.num_detected}")
    for i, spec in enumerate(result.strategies):
        print(f"\n   [{i+1}] {spec.strategy_name} ({spec.strategy_type})")
        print(f"       Indicators: {len(spec.indicators)}")
        print(f"       Logic Steps: {len(spec.logic_pipeline)}")
        print(f"       Execution Plans: {len(spec.execution_plan)}")


if __name__ == "__main__":
    main()
