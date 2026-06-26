#!/usr/bin/env python3
"""Enforce conditional figure requirements for PPT generation.

Fail when:
- the paper has original figures, but result/mechanism slides that should use them do not
- a slide uses an original figure but lacks explanation / explanation is too weak

Allow when:
- the full paper genuinely has no extractable original figures, in which case text-only slides are allowed

Input bundle shape is flexible but expects a slides[] array.
Output JSON: {ok, message, reasons}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FAIL = "检索失败，无法生成"
RESULT_TYPES = {"result"}
STRICT_VISUAL_TYPES = {"mechanism"}


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides-json", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    data = read_json(args.slides_json)
    slides = data.get("slides", []) if isinstance(data, dict) else []
    reasons: List[str] = []
    if not slides:
        reasons.append("缺少幻灯片结构")

    has_any_original_figures = False
    for slide in slides:
        if slide.get("figure_refs") or slide.get("image_paths_or_urls"):
            has_any_original_figures = True
            break

    for idx, slide in enumerate(slides, start=1):
        st = str(slide.get("slide_type", "")).lower()
        images = slide.get("image_paths_or_urls") or []
        fig_refs = slide.get("figure_refs") or []
        explanations = slide.get("figure_explanations") or []
        uses_figure = bool(images or fig_refs)
        figure_required = bool(slide.get("figure_required", False))

        if st in RESULT_TYPES and has_any_original_figures:
            if not images or not fig_refs:
                reasons.append(f"第{idx}页结果页缺少原文图片")

        if st in STRICT_VISUAL_TYPES and figure_required:
            if not images or not fig_refs:
                reasons.append(f"第{idx}页机制页被标记为必须配原图，但未嵌入原文图片")

        if uses_figure:
            if not explanations:
                reasons.append(f"第{idx}页使用原文图片但缺少图片解释")
            else:
                weak = []
                for e in explanations:
                    text = str((e or {}).get("explanation", "")).strip()
                    if len(text) < 24:
                        weak.append(text)
                if weak:
                    reasons.append(f"第{idx}页图片解释过短，无法支撑讲解")

    result = {
        "ok": not reasons,
        "message": "OK" if not reasons else FAIL,
        "reasons": reasons,
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
