#!/usr/bin/env python3
"""Guard validation script for IR text before HTML generation.

Usage:
    python scripts/guard_validate.py <ir_file.report.md>

Output:
    JSON validation report to stdout

Exit codes:
    0 — all valid
    1 — some blocks invalid (auto_downgrade_target available)
    2 — fatal error (missing title)

Contract (v4 guardrails):
    - Guard accepts ir_text: str, not file path
    - report_class resolved using existing --generate path (SKILL.md Step 1.5)
    - Calls contract_checks validators, no cloning
    - Zero contract change
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evals.contract_checks import (
    parse_frontmatter,
    iter_blocks,
    validate_block,
)


def resolve_report_class(ir_text: str, explicit_class: str | None = None) -> str:
    """
    Resolve report_class using the same path as --generate (SKILL.md Step 1.5).

    Resolution order:
    1. Explicit parameter (from frontmatter parsing)
    2. Content nature detection (numeric density)
    3. Default to "mixed" (per SKILL.md spec)

    This function does NOT introduce a new default.
    It replicates the existing --generate resolution path.
    """
    if explicit_class:
        return explicit_class

    frontmatter, body = parse_frontmatter(ir_text)
    if "report_class" in frontmatter:
        return frontmatter["report_class"]

    # Compute numeric density (from SKILL.md Step 1.5)
    # Numeric token: words/phrases containing digits with quantitative meaning
    # Density = numeric token count / total word count

    # Simplified density detection for guard (replicate Step 1.5 logic)
    # This is NOT a new validator — just existing resolution logic
    numeric_pattern = re.compile(r"\d+[%¥$€]|[+-]?\d+[xX%]|[+-]\d+[%]|[¥$€]\d+")
    numeric_matches = numeric_pattern.findall(body)

    # Count words (Chinese: character segments; English: whitespace-split)
    # Simplified: just count whitespace-split words for now
    words = body.split()
    word_count = len(words) if words else 1

    density = len(numeric_matches) / word_count if word_count > 0 else 0

    # Classify (from SKILL.md Step 1.5)
    if density < 0.05:
        return "narrative"
    elif density > 0.20:
        return "data"
    else:
        return "mixed"


def validate_ir_text(ir_text: str, report_class: str | None = None) -> dict:
    """
    Validate IR text against contract_checks.py validators.

    Args:
        ir_text: Full IR content (frontmatter + body)
        report_class: Optional explicit report_class from frontmatter.
                      If None, the guard calls the same resolver as --generate.

    Returns:
        Validation report with status and invalid blocks.
    """
    frontmatter, body = parse_frontmatter(ir_text)

    # Check title (fatal)
    if "title" not in frontmatter:
        return {
            "status": "fatal",
            "error": "title is required in frontmatter",
            "exit_code": 2
        }

    # Resolve report_class (using existing path)
    resolved_class = resolve_report_class(ir_text, report_class)

    # Parse blocks
    blocks = iter_blocks(ir_text)

    # Validate each block (call existing validators)
    block_results = []
    for block in blocks:
        # Call contract_checks validator, no cloning
        result = validate_block(block, report_class=resolved_class)
        block_results.append({
            "tag": block.tag,
            "params": block.params,
            "status": result["status"],
            "auto_downgrade_target": result.get("auto_downgrade_target")
        })

    # Count blocks
    total_blocks = len(blocks)

    # Report
    invalid_blocks = [b for b in block_results if b["status"] != "valid"]
    if invalid_blocks:
        return {
            "status": "invalid_blocks",
            "invalid_count": len(invalid_blocks),
            "resolved_report_class": resolved_class,
            "blocks": block_results,
            "total_blocks": total_blocks,
            "exit_code": 1
        }
    else:
        return {
            "status": "valid",
            "resolved_report_class": resolved_class,
            "blocks": block_results,
            "total_blocks": total_blocks,
            "exit_code": 0
        }


def main():
    parser = argparse.ArgumentParser(description="Guard validation for IR text")
    parser.add_argument("ir_path", help="Path to IR file (adapter layer)")
    args = parser.parse_args()

    # Read IR text (adapter layer — file read happens here, not in guard)
    ir_text = Path(args.ir_path).read_text(encoding="utf-8")

    # Call guard with ir_text (not path)
    report = validate_ir_text(ir_text)

    # Output JSON report
    print(json.dumps(report, indent=2))
    sys.exit(report["exit_code"])


if __name__ == "__main__":
    main()