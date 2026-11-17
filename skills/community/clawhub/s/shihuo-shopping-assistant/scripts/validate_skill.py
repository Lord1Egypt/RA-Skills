#!/usr/bin/env python3
"""校验识货购物助手 Skill 包的结构与资源契约。

用法：
    python3 scripts/validate_skill.py <skill_dir>
    python3 scripts/validate_skill.py <skill_dir> --strict
    python3 scripts/validate_skill.py <skill_dir> --tools-list tools-list.json --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    # 允许从 scripts/ 目录直接执行。
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lib.package_contract import validate_package  # type: ignore
else:
    from .lib.package_contract import validate_package


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验 Skill 目录、工具镜像和 frontmatter")
    parser.add_argument("skill_dir", type=Path, help="Skill 根目录")
    parser.add_argument("--strict", action="store_true", help="启用发布门禁和 allowed-tools 精确校验")
    parser.add_argument("--tools-list", type=Path, help="服务端 tools/list JSON 快照")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="输出格式，默认 text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.skill_dir.resolve()
    if not root.is_dir():
        if args.format == "json":
            print(json.dumps({"ok": False, "errors": [{"code": "invalid_skill_dir", "path": str(root), "message": "Skill 根目录不存在或不是目录"}], "warnings": [], "summary": {}}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR invalid_skill_dir {root} 不是目录")
        return 2
    report = validate_package(root, strict=args.strict, tools_list=args.tools_list)
    payload = report.as_dict()
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for issue in report.warnings:
            print(f"WARN  [{issue.code}] {issue.path}: {issue.message}")
        for issue in report.errors:
            print(f"ERROR [{issue.code}] {issue.path}: {issue.message}")
        print(f"\n{root.name}: {len(report.errors)} error, {len(report.warnings)} warning")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
