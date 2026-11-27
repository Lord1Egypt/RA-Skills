#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit an Agent Skill directory against the six-step standard.

Usage:
    python audit_skill.py <skill_dir>
    python audit_skill.py --selftest

Exit code: 0 = pass (warnings allowed), 1 = hard failure.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

REQUIRED_FRONTMATTER = [
    "name", "description", "user-invocable", "version", "last_updated",
]
REQUIRED_SECTIONS = [
    "边界清单", "路由元信息", "工作流", "依赖与资源",
    "异常与兜底", "状态与权限", "评测", "迭代",
]
HEADING_ABSTRACT = {
    "输出", "标准", "格式", "规范", "目标", "流程", "边界", "评测", "迭代",
    "资源", "权限", "状态", "依赖", "异常", "兜底", "配置", "管理", "设计",
    "实现", "机制", "方案", "模块", "系统", "能力", "工作流", "验收", "呈现",
    "内容", "形式",
}


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("#"):
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def headings(text: str) -> list:
    return [h.strip() for h in re.findall(r"^##\s+(.+)$", text, flags=re.M)]


def heading_collisions(items: list) -> list:
    hits = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a == b:
                hits.append((a, b, {"重复标题"}))
                continue
            shared = {w for w in HEADING_ABSTRACT if w in a and w in b}
            if shared:
                hits.append((a, b, shared))
    return hits


def audit(skill_dir: Path):
    errors, warnings = [], []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return ["缺少 SKILL.md"], []

    text = md.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)

    for key in REQUIRED_FRONTMATTER:
        if not fm.get(key):
            errors.append(f"frontmatter 缺少或为空：{key}")

    desc = fm.get("description", "")
    if "触发" not in desc:
        errors.append("description 缺少触发词")
    if "不适用" not in desc and "禁用" not in desc:
        errors.append("description 缺少“不适用于/禁用场景”")

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}", text, flags=re.M):
            errors.append(f"缺少章节：{section}")

    cases = skill_dir / "eval" / "cases.md"
    failures = skill_dir / "eval" / "failures.md"
    if not cases.exists():
        errors.append("缺少 eval/cases.md")
    else:
        c = cases.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"正向|正例", c):
            warnings.append("eval/cases.md 未发现正向用例")
        if not re.search(r"反向|反例|异常", c):
            warnings.append("eval/cases.md 未发现反向/异常用例")
    if not failures.exists():
        errors.append("缺少 eval/failures.md")

    if not any((skill_dir / d).exists() for d in ("assets", "references", "scripts")):
        warnings.append("没有 assets/references/scripts，确认是否只需要指令")

    for a, b, shared in heading_collisions(headings(text)):
        warnings.append(
            f"标题撞词：「{a}」与「{b}」共享 {'/'.join(sorted(shared))}；"
            f"请加限定词（内容/呈现/验收/执行）或写清边界")

    return errors, warnings


def report(label: str, errors: list, warnings: list) -> int:
    print(f"== audit: {label} ==")
    for w in warnings:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[FAIL] {e}")
    if errors:
        print(f"RESULT: FAIL ({len(errors)} errors, {len(warnings)} warnings)\n")
        return 1
    print(f"RESULT: PASS ({len(warnings)} warnings)\n")
    return 0


def write_fixture(root: Path, name: str, body: str) -> Path:
    d = root / name
    (d / "eval").mkdir(parents=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")
    (d / "eval" / "cases.md").write_text(
        "# cases\n\n## 一、正向用例\n\n- ok\n\n## 二、反向用例\n\n- no\n",
        encoding="utf-8")
    (d / "eval" / "failures.md").write_text("# failures\n", encoding="utf-8")
    return d


def selftest() -> int:
    good = """---
name: demo
description: demo. 触发词：demo。不适用于：none。
user-invocable: true
version: "0.1.0"
last_updated: "2026-10-26"
---
# demo
## 边界清单
## 路由元信息
## 工作流
## 依赖与资源
## 异常与兜底
## 状态与权限
## 评测
## 迭代
"""
    bad = """---
name: bad
description: no triggers here
user-invocable: true
---
# bad
## 工作流
"""
    collide = good + "\n## 输出标准\n\n## 输出格式\n"

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        g = write_fixture(root, "good", good)
        b = write_fixture(root, "bad", bad)
        c = write_fixture(root, "collide", collide)

        g_err, g_warn = audit(g)
        b_err, _ = audit(b)
        c_err, c_warn = audit(c)

        checks = [
            ("good skill passes", not g_err),
            ("bad skill fails", bool(b_err)),
            ("collision warns", any("标题撞词" in w for w in c_warn)),
            ("collision has no hard error", not c_err),
        ]
        failed = 0
        for name, ok in checks:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}")
            failed += 0 if ok else 1
        print(f"\nselftest: {len(checks) - failed}/{len(checks)} passed")
        return 0 if failed == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.skill_dir:
        ap.print_help()
        return 2

    skill = Path(args.skill_dir)
    errors, warnings = audit(skill)
    return report(str(skill), errors, warnings)


if __name__ == "__main__":
    sys.exit(main())
