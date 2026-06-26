#!/usr/bin/env python3
"""Build a compact prompt bundle for research-paper-to-ppt-v1.

This script does not call external APIs. It converts resolved paper metadata,
full-text markdown, extracted figure inventory, and outline policy into a
single JSON bundle that another agent/skill can feed into a PPTX generator.

Usage:
  python3 build_prompt_bundle.py \
    --paper-meta paper_meta.json \
    --fulltext fulltext.md \
    --figures figures.json \
    --output bundle.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

SECTION_HINTS = {
    "background": ["introduction", "background"],
    "methods": ["methods", "materials and methods", "experimental procedures"],
    "results": ["results"],
    "discussion": ["discussion"],
    "conclusion": ["conclusion", "conclusions"],
    "abstract": ["abstract"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_sections(md: str) -> Dict[str, str]:
    lines = md.splitlines()
    buckets: Dict[str, List[str]] = {k: [] for k in SECTION_HINTS}
    current = None
    for line in lines:
        stripped = line.strip()
        heading = stripped.lstrip("#").strip().lower() if stripped.startswith("#") else ""
        matched = None
        if heading:
            for key, hints in SECTION_HINTS.items():
                if any(h in heading for h in hints):
                    matched = key
                    break
            current = matched
            continue
        if current:
            buckets[current].append(line)
    return {k: normalize_ws("\n".join(v)) for k, v in buckets.items() if normalize_ws("\n".join(v))}


def build_bundle(paper_meta: Dict[str, Any], fulltext: str, figures: Any) -> Dict[str, Any]:
    sections = extract_sections(fulltext)
    return {
        "paper_meta": paper_meta,
        "fulltext_sections": sections,
        "figures": figures,
        "constraints": {
            "must_use_original_figures": True,
            "result_slides_require_original_images": True,
            "figure_explanation_required": True,
            "skip_missing_outline_sections": True,
            "fail_on_missing_fulltext": True,
            "fail_message": "检索失败，无法生成",
            "author_display_default": "first_et_al",
            "result_title_priority": "results_subtitle_first",
            "allow_repeat_same_figure_across_2_3_slides": True,
            "figure_explanation_style": "必须输出全中文图解，优先直接参照原文图注翻译并做轻度整理；需要时可补充实验目的、主要比较对象、核心观察结果和该图在全文证据链中的意义，但不要为了显得高级而过度改写。",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-meta", required=True)
    parser.add_argument("--fulltext", required=True)
    parser.add_argument("--figures", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    paper_meta = read_json(Path(args.paper_meta))
    fulltext = read_text(Path(args.fulltext))
    figures = read_json(Path(args.figures))
    bundle = build_bundle(paper_meta, fulltext, figures)
    Path(args.output).write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
