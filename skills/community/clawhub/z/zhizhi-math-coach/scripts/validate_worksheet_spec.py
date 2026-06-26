#!/usr/bin/env python3
"""Validate a worksheet spec without writing worksheet outputs."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_worksheet.py"
REVIEWED_STATUSES = {"model_reviewed", "human_review_needed", "approved"}
COMPLEX_TYPES = {
    "multi_step_word_problem",
    "condition_filtering_problem",
    "compare_after_intermediate_problem",
    "geometry_problem",
}
SUPPORTED_GEOMETRY = {"rectangle", "composite_rect"}


def load_generator():
    spec = importlib.util.spec_from_file_location("worksheet_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load generator from {GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_items(spec: dict):
    for section_index, section in enumerate(spec.get("sections", []), start=1):
        for item_index, item in enumerate(section.get("items", []), start=1):
            yield section_index, item_index, item


def validate_semantics(spec: dict, allow_draft: bool = False) -> None:
    if not spec.get("title"):
        raise ValueError("spec missing title")
    if not spec.get("sections"):
        raise ValueError("spec must contain at least one section")

    for section_index, item_index, item in iter_items(spec):
        item_type = item.get("type")
        location = f"section {section_index} item {item_index}"

        if item_type in COMPLEX_TYPES and not allow_draft:
            status = item.get("review_status") or spec.get("review_status")
            if status not in REVIEWED_STATUSES:
                raise ValueError(
                    f"{location}: {item_type} requires review_status in "
                    f"{sorted(REVIEWED_STATUSES)} before printing"
                )

        if item_type == "geometry_problem":
            geometry_spec = item.get("geometry_spec", {})
            geometry_type = geometry_spec.get("type")
            if geometry_type not in SUPPORTED_GEOMETRY:
                raise ValueError(
                    f"{location}: unsupported geometry_spec type {geometry_type!r}; "
                    f"supported: {sorted(SUPPORTED_GEOMETRY)}"
                )
            if "answer_detail" in geometry_spec:
                raise ValueError(f"{location}: geometry_spec must not contain answer_detail")

        answer_detail = item.get("answer_detail")
        if item_type in COMPLEX_TYPES and (not answer_detail or len(str(answer_detail).strip()) < 8):
            raise ValueError(f"{location}: complex item requires a useful answer_detail")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a zhizhi worksheet spec without writing output files.")
    parser.add_argument("spec", type=Path, help="Path to worksheet-spec.json")
    parser.add_argument("--allow-draft", action="store_true", help="Allow draft complex/geometry items.")
    args = parser.parse_args()

    generator = load_generator()
    spec_path = args.spec.resolve()
    spec = generator.load_json(spec_path)
    registry = generator.load_json(generator.TYPE_REGISTRY)

    generator.validate_spec(spec, registry)
    validate_semantics(spec, allow_draft=args.allow_draft)

    item_count = sum(1 for _ in iter_items(spec))
    print(f"ok: {spec_path} ({item_count} item(s))")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
