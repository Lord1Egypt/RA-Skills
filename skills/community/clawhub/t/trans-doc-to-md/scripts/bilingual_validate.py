#!/usr/bin/env python3
"""Fail fast when a bilingual Markdown output deletes or summarizes source text."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from bilingual_validation_core import (
    ValidationError,
    validate_document,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("bilingual")
    parser.add_argument(
        "--profile",
        choices=("generic", "pdf-rich"),
        default="generic",
        help="校验配置；generic 适合普通文章，pdf-rich 启用严格目录与标题结构检查",
    )
    parser.add_argument("--section", help="只校验标题中包含该文字的章节")
    parser.add_argument(
        "--raw-source",
        help="可选原始 source.md；同时校验原始目录标题未在清洗阶段被截断",
    )
    parser.add_argument("--json", action="store_true", help="输出稳定 JSON 结果")
    args = parser.parse_args()

    source_path = Path(args.source)
    bilingual_path = Path(args.bilingual)
    scope = f"section={args.section}" if args.section else "full document"
    try:
        bilingual = bilingual_path.read_text(encoding="utf-8")
        source = source_path.read_text(encoding="utf-8")
        raw_source = (
            Path(args.raw_source).read_text(encoding="utf-8")
            if args.raw_source
            else None
        )
        validate_document(
            source,
            bilingual,
            profile=args.profile,
            section=args.section,
            raw_source=raw_source,
        )
    except (OSError, ValidationError) as error:
        result = {
            "error": str(error),
            "ok": False,
            "profile": args.profile,
            "scope": scope,
            "status": "fail",
        }
        print(
            json.dumps(result, ensure_ascii=False, sort_keys=True)
            if args.json
            else f"FAIL: {error}"
        )
        return 1

    result = {
        "error": None,
        "ok": True,
        "profile": args.profile,
        "scope": scope,
        "status": "pass",
    }
    print(
        json.dumps(result, ensure_ascii=False, sort_keys=True)
        if args.json
        else f"PASS: source paragraphs and local images preserved ({scope}, profile={args.profile})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
