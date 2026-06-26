#!/usr/bin/env python3
"""Validate minimal inputs for research-paper-to-ppt-v1.

Checks whether the resolved paper identity, full text availability, and figure
inventory satisfy the hard failure conditions described in SKILL.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

FAIL = "检索失败，无法生成"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(meta: Dict[str, Any], fulltext: str, figures: Any) -> Dict[str, Any]:
    reasons = []
    identity_keys = ("doi", "pmid", "source_id", "title_en", "title")
    if not any(meta.get(k) for k in identity_keys):
        reasons.append("缺少可唯一定位文献的标识")

    text = (fulltext or "").strip()
    if len(text) < 2000:
        reasons.append("全文正文过短，无法支持PPT生成")
    low = text.lower()
    if low and not any(h in low for h in ["abstract", "introduction", "methods", "results", "discussion", "conclusion", "背景", "方法", "结果", "讨论", "结论"]):
        reasons.append("全文缺少可识别章节，疑似只有摘要或残缺正文")

    has_figures = False
    if isinstance(figures, dict):
        has_figures = len(figures) > 0
    elif isinstance(figures, list):
        has_figures = len(figures) > 0

    # 图片不再是“必须有”的全局前置条件。
    # 新规则：如果全文确实有原图，则后续页面必须优先使用原图；
    # 如果全文没有可提取图片，则允许继续生成无图版 PPT。
    if has_figures:
        # Best-effort source traceability check.
        bad = []
        items = figures.values() if isinstance(figures, dict) else figures
        for item in items:
            if isinstance(item, dict):
                url = str(item.get("url") or item.get("image_url") or item.get("path") or "")
                if url and not (url.startswith("http://") or url.startswith("https://") or url.startswith("/") or url.startswith("./")):
                    bad.append(url)
        if bad:
            reasons.append("图片来源不可追溯")
    return {
        "ok": not reasons,
        "message": "OK" if not reasons else FAIL,
        "reasons": reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-meta", required=True)
    parser.add_argument("--fulltext", required=True)
    parser.add_argument("--figures", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = validate(
        read_json(Path(args.paper_meta)),
        read_text(Path(args.fulltext)),
        read_json(Path(args.figures)),
    )
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
