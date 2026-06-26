#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Style Signature Extractor

Usage:
  python3 scripts/style_signature.py "developer docs premium monochrome"
  python3 scripts/style_signature.py "commerce admin friendly operational" --json

Builds a compact style-cloning brief from local ui-craft-pro datasets.
"""

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def load_csv(name):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tokenize(text):
    return [t.strip().lower() for t in str(text).replace(",", " ").replace("/", " ").split() if t.strip()]


def score_row(query_tokens, row, fields):
    hay = " ".join(str(row.get(field, "")) for field in fields).lower()
    score = 0
    for token in query_tokens:
        if token in hay:
            score += 1
    return score


def best_match(rows, query_tokens, fields):
    ranked = sorted(rows, key=lambda row: score_row(query_tokens, row, fields), reverse=True)
    return ranked[0] if ranked and score_row(query_tokens, ranked[0], fields) > 0 else (ranked[0] if ranked else {})


def build_signature(query):
    query_tokens = tokenize(query)

    signatures = load_csv("style-signatures.csv")
    systems = load_csv("design-systems.csv")
    patterns = load_csv("patterns-shells.csv")
    anti_generic = load_csv("anti-generic-ui.csv")

    sig = best_match(signatures, query_tokens, [
        "Signature", "Inspired By", "Best For", "Core Mood", "Keywords"
    ])
    system = best_match(systems, query_tokens, [
        "System", "Company", "Product Focus", "Vibe", "Strengths", "Steal Carefully"
    ])
    pattern = best_match(patterns, query_tokens, [
        "Pattern", "Page Type", "Best For", "Structure", "Keywords"
    ])

    warnings = []
    for row in anti_generic:
        if score_row(query_tokens, row, ["Category", "Smell", "Keywords", "Fix"]) > 0:
            warnings.append({
                "smell": row.get("Smell", ""),
                "fix": row.get("Fix", "")
            })
    if not warnings:
        warnings = [
            {"smell": "Equal-weight everything", "fix": "Create clear hierarchy before adding effects."},
            {"smell": "Style copied at surface level only", "fix": "Extract spacing, type, token, and interaction rules first."}
        ]

    return {
        "query": query,
        "signature": sig.get("Signature", "Custom Signature"),
        "inspired_by": sig.get("Inspired By", system.get("System", "Mixed references")),
        "best_for": sig.get("Best For", system.get("Product Focus", "General product UI")),
        "core_mood": sig.get("Core Mood", system.get("Vibe", "Intentional, coherent, product-aware")),
        "token_dna": system.get("Token DNA", sig.get("Color DNA", "Semantic tokens with disciplined accents")),
        "spacing_dna": sig.get("Spacing DNA", system.get("Spacing Rhythm", "Consistent sectional rhythm")),
        "type_dna": sig.get("Type DNA", system.get("Typography DNA", "Clear hierarchy with readable support text")),
        "surface_dna": sig.get("Surface DNA", system.get("Surface Treatment", "Consistent borders, shadows, and surfaces")),
        "component_dna": sig.get("Component DNA", system.get("Component DNA", "Components should feel like one family")),
        "motion_dna": sig.get("Motion DNA", system.get("Motion DNA", "Subtle, state-driven motion")),
        "recommended_pattern": pattern.get("Pattern", "Standard Product Shell"),
        "pattern_structure": pattern.get("Structure", "Hero > proof > feature detail > CTA"),
        "steal_this": sig.get("Steal This", system.get("Steal Carefully", "Hierarchy, rhythm, and token discipline")),
        "watch_outs": sig.get("Do Not Copy Blindly", pattern.get("Watch Outs", "Do not copy visual quirks without structural logic")),
        "anti_generic_warnings": warnings[:3],
    }


def to_markdown(result):
    lines = []
    lines.append(f"## Style Signature — {result['signature']}")
    lines.append(f"**Query:** {result['query']}")
    lines.append(f"**Inspired by:** {result['inspired_by']}")
    lines.append(f"**Best for:** {result['best_for']}")
    lines.append("")
    lines.append("### DNA")
    lines.append(f"- **Mood:** {result['core_mood']}")
    lines.append(f"- **Tokens:** {result['token_dna']}")
    lines.append(f"- **Spacing:** {result['spacing_dna']}")
    lines.append(f"- **Type:** {result['type_dna']}")
    lines.append(f"- **Surfaces:** {result['surface_dna']}")
    lines.append(f"- **Components:** {result['component_dna']}")
    lines.append(f"- **Motion:** {result['motion_dna']}")
    lines.append("")
    lines.append("### Recommended pattern")
    lines.append(f"- **Pattern:** {result['recommended_pattern']}")
    lines.append(f"- **Structure:** {result['pattern_structure']}")
    lines.append("")
    lines.append("### Preserve")
    lines.append(f"- {result['steal_this']}")
    lines.append("")
    lines.append("### Do not copy blindly")
    lines.append(f"- {result['watch_outs']}")
    lines.append("")
    lines.append("### Anti-generic warnings")
    for warning in result['anti_generic_warnings']:
        lines.append(f"- **{warning['smell']}** → {warning['fix']}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a style signature from local ui-craft-pro datasets")
    parser.add_argument("query", help="Style or product query")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = build_signature(args.query)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(result))
