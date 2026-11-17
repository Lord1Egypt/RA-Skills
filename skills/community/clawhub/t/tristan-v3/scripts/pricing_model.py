#!/usr/bin/env python3
"""
pricing_model.py — Stage 3 pricing calculator for Tristan RFQ Overseer.

Reads an RFQ note (Obsidian markdown with a "Line Items" table), computes
subtotal / overhead / margin / total, and either prints the result as JSON
or writes the updated figures back into the note's "## Pricing" section.

Usage:
    python pricing_model.py <path/to/RFQ-note.md> [--margin 0.18] [--overhead 0.05] [--write]

Config:
    Default margin and overhead can be overridden with CLI flags, or by
    placing a `pricing.config.json` file next to this script:
        { "margin": 0.18, "overhead": 0.05 }
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_MARGIN = 0.18
DEFAULT_OVERHEAD = 0.05

LINE_ITEM_ROW_RE = re.compile(
    r"^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|"
    r"\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$"
)


def load_config(script_dir: Path) -> dict:
    config_path = script_dir / "pricing.config.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"Warning: could not parse {config_path}, using defaults.", file=sys.stderr)
    return {}


def parse_line_items(note_text: str):
    """Extract rows from the '## Line Items' markdown table."""
    lines = note_text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().startswith("## Line Items"))
    except StopIteration:
        return []

    items = []
    in_table = False
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        if set(stripped.replace("|", "").strip()) <= {"-", " "}:
            in_table = True
            continue
        match = LINE_ITEM_ROW_RE.match(stripped)
        if not match:
            continue
        item, qty_raw, unit, cost_raw, notes = match.groups()
        row = {"item": item, "qty": qty_raw, "unit": unit, "cost": cost_raw, "notes": notes}
        if row["item"].lower() == "item":
            continue  # header row
        try:
            qty = float(row["qty"]) if row["qty"] else 0.0
            cost = float(re.sub(r"[^0-9.\-]", "", row["cost"])) if row["cost"] else 0.0
        except ValueError:
            continue
        if not row["item"] or qty == 0:
            continue
        items.append({
            "item": row["item"],
            "qty": qty,
            "unit": row["unit"],
            "unit_cost": cost,
            "notes": row["notes"],
            "line_total": round(qty * cost, 2),
        })
    return items


def compute_pricing(items, margin: float, overhead: float):
    subtotal = round(sum(i["line_total"] for i in items), 2)
    overhead_amount = round(subtotal * overhead, 2)
    cost_base = round(subtotal + overhead_amount, 2)
    margin_amount = round(cost_base * margin, 2)
    total = round(cost_base + margin_amount, 2)
    return {
        "subtotal": subtotal,
        "overhead_rate": overhead,
        "overhead_amount": overhead_amount,
        "margin_rate": margin,
        "margin_amount": margin_amount,
        "total": total,
    }


def render_pricing_section(pricing: dict) -> str:
    return (
        "## Pricing\n"
        "_Populated by `scripts/pricing_model.py`._\n\n"
        f"- Subtotal: {pricing['subtotal']:.2f}\n"
        f"- Overhead ({pricing['overhead_rate']*100:.1f}%): {pricing['overhead_amount']:.2f}\n"
        f"- Margin applied ({pricing['margin_rate']*100:.1f}%): {pricing['margin_amount']:.2f}\n"
        f"- Total quote value: {pricing['total']:.2f}\n"
    )


def write_back(note_path: Path, note_text: str, pricing: dict) -> None:
    section_re = re.compile(r"## Pricing\n.*?(?=\n## |$)", re.DOTALL)
    new_section = render_pricing_section(pricing)
    if section_re.search(note_text):
        updated = section_re.sub(new_section.rstrip("\n") + "\n", note_text, count=1)
    else:
        updated = note_text.rstrip("\n") + "\n\n" + new_section
    note_path.write_text(updated, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compute pricing for an RFQ note.")
    parser.add_argument("note", type=Path, help="Path to the RFQ note markdown file")
    parser.add_argument("--margin", type=float, default=None, help="Margin rate, e.g. 0.18 for 18%")
    parser.add_argument("--overhead", type=float, default=None, help="Overhead rate, e.g. 0.05 for 5%")
    parser.add_argument("--write", action="store_true", help="Write results back into the note's Pricing section")
    args = parser.parse_args()

    if not args.note.exists():
        print(f"Error: note not found at {args.note}", file=sys.stderr)
        sys.exit(1)

    config = load_config(Path(__file__).parent)
    margin = args.margin if args.margin is not None else config.get("margin", DEFAULT_MARGIN)
    overhead = args.overhead if args.overhead is not None else config.get("overhead", DEFAULT_OVERHEAD)

    note_text = args.note.read_text(encoding="utf-8")
    items = parse_line_items(note_text)

    if not items:
        print("No valid line items found — fill in the Line Items table before pricing.", file=sys.stderr)
        sys.exit(1)

    pricing = compute_pricing(items, margin, overhead)
    result = {"rfq_note": str(args.note), "items": items, "pricing": pricing}

    print(json.dumps(result, indent=2))

    if args.write:
        write_back(args.note, note_text, pricing)
        print(f"\nUpdated Pricing section written to {args.note}", file=sys.stderr)


if __name__ == "__main__":
    main()
