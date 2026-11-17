#!/usr/bin/env python3
"""skillbench — Skill 能力评测计划生成器（仅 dry-run）

安全边界声明（SECURITY BOUNDARY）：
- 本工具 **只做 dry-run**：预览/导出评测测试定义（命令、期望输出），
  **不执行任何代码**（不调用 subprocess）。
- 实际执行测试请使用仓库 tests/ 下的 pytest 套件，由开发者在本仓库环境运行。
- 评测输出只写本地文件，无网络请求、不读取凭证。

Usage:
    python skillbench.py run <skill_dir>            # dry-run：预览测试定义
    python skillbench.py run <skill_dir> --output plan.json   # 导出测试计划
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ── Test definitions per skill (pure data — never executed by this tool) ──

TESTS = {
    "iso14971-risk-matrix": [
        {
            "name": "basic_assess_s4_p2",
            "cmd": ["python", "scripts/risk_matrix.py", "assess", "-s", "4", "-p", "2"],
            "expect_in_output": ["风险评分", "8", "M"],
        },
        {
            "name": "high_risk_s5_p5",
            "cmd": ["python", "scripts/risk_matrix.py", "assess", "-s", "5", "-p", "5"],
            "expect_in_output": ["25", "H"],
        },
        {
            "name": "residual_risk_comparison",
            "cmd": ["python", "scripts/risk_matrix.py", "assess", "-s", "5", "-p", "4", "--rs", "2", "--rp", "1"],
            "expect_in_output": ["剩余风险", "L"],
        },
        {
            "name": "risk_options_hierarchy",
            "cmd": ["python", "scripts/risk_matrix.py", "options"],
            "expect_in_output": ["固有安全", "防护措施", "安全信息"],
        },
    ],
    "medxpert-termbase": [
        {
            "name": "term_lookup_biocompatibility",
            "cmd": ["python", "scripts/term_check.py", "lookup", "biocompatibility"],
            "expect_in_output": ["生物相容性"],
        },
        {
            "name": "term_lookup_chinese",
            "cmd": ["python", "scripts/term_check.py", "lookup", "风险"],
            "expect_in_output": [],
        },
        {
            "name": "stats_inventory",
            "cmd": ["python", "scripts/term_check.py", "stats"],
            "expect_in_output": ["entries"],
        },
    ],
    "reg-citation-normalizer": [
        {
            "name": "normalize_21cfr",
            "cmd": ["python", "scripts/cite_normalize.py", "normalize", "21 CFR 820.30 (a)(6)"],
            "expect_in_output": ["820.30(a)(6)"],
        },
        {
            "name": "normalize_iso",
            "cmd": ["python", "scripts/cite_normalize.py", "normalize", "ISO 13485:2016 clause 7.5.1"],
            "expect_in_output": ["ISO 13485:2016"],
        },
        {
            "name": "parse_json",
            "cmd": ["python", "scripts/cite_normalize.py", "parse", "ISO 13485:2016", "--json"],
            "expect_in_output": ["type", "iso-iec"],
        },
    ],
}


def resolve_tests(skill_dir: str) -> tuple[str, list]:
    """匹配 skill 的测试定义（纯数据，不执行任何代码）。"""
    skill_path = Path(skill_dir).resolve()
    skill_name = skill_path.name
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                for line in content[3:end].splitlines():
                    if line.startswith("name:"):
                        skill_name = line.split(":", 1)[1].strip()
                        break
    tests = TESTS.get(skill_name, [])
    if not tests:
        for key in TESTS:
            if key in skill_path.name:
                tests = TESTS[key]
                break
    return skill_name, tests


def main():
    ap = argparse.ArgumentParser(description="SkillBench — Skill 能力评测运行器")
    sub = ap.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="预览 skill 评测测试定义（dry-run，不执行任何代码）")
    run_parser.add_argument("skill_dir", help="skill 目录路径")
    run_parser.add_argument("--baseline", help="基线 JSON 文件路径")
    run_parser.add_argument("--output", help="输出测试计划 JSON 文件路径")

    args = ap.parse_args()

    if args.command == "run":
        # 固定 dry-run：只预览测试定义，不执行任何目标代码（安全边界，无 --execute）
        skill_name, tests = resolve_tests(args.skill_dir)
        print("⚠️  DRY-RUN（安全边界）：仅预览测试定义，未执行任何代码")
        print(f"   Skill: {skill_name}  匹配测试: {len(tests)}")
        for t in tests:
            print(f"   - {t['name']}: {' '.join(t['cmd'])}")
        if args.output:
            # Confined write: export plan only inside the target folder.
            _target = Path(args.skill_dir).resolve()
            _out = Path(args.output).resolve()
            try:
                _ok = _out.is_relative_to(_target)
            except (ValueError, AttributeError):
                _ok = False
            if not _ok:
                print(f"错误: 输出路径必须在目标目录内: {_target}", file=sys.stderr)
                sys.exit(2)
            if _out.is_symlink() or _out.is_junction():
                print(f"错误: 输出路径不能是符号链接/junction: {_out}", file=sys.stderr)
                sys.exit(2)
            _out.write_text(
                json.dumps({"skill": skill_name, "dry_run": True, "tests": tests}, indent=2, ensure_ascii=False),
                encoding="utf-8")
            print(f"\n测试计划已导出: {args.output}")
        print("\n   实际执行请使用仓库 tests/ 下的 pytest 套件（仅限本仓库开发环境）")
        sys.exit(0)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
