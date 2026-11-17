#!/usr/bin/env python3
"""
审稿 JSON 校验脚本 — review-checker.md 的配套实现

用法：
  python3 validate_checklist.py <checklist.json>

返回码：
  0 — 通过（所有 mandatory passed）
  1 — 不通过（有 mandatory 未通过）
  2 — JSON 格式错误

输出：
  [PASS]      审稿完整性校验通过
  [FAIL]      审稿不完整，列出未通过项
  [WARN]      suggested 未完成项（不影响通过）
"""

import json
import sys
import os
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────

REQUIRED_FIELDS = [
    "meta.draft_path",
    "meta.draft_version",
    "meta.review_date",
    "meta.reviewer",
]

MANDATORY_ITEMS = [
    "cross_act_repetition",
    "source_material_verification",
    "privacy_check",
    "hard_issues_tracked",
    "topic_consistency",
    "ending_matches_core_conflict",
]

SUGGESTED_ITEMS = [
    "dialogue_rhythm",
    "cross_episode_echo",
    "anti_ai_check",
    "term_friendly",
    "ending_brevity",
]

OPTIONAL_ITEMS = [
    "multi_model_cross",
    "cross_episode_consistency",
]

# ── 辅助函数 ──────────────────────────────────────────

def get_nested(d, path, default=None):
    """通过点分隔路径访问嵌套字典"""
    keys = path.split(".")
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return default
        if d is None:
            return default
    return d


def color(text, code):
    """终端着色"""
    return f"\033[{code}m{text}\033[0m"


def red(text):
    return color(text, "31")


def green(text):
    return color(text, "32")


def yellow(text):
    return color(text, "33")


def cyan(text):
    return color(text, "36")


# ── 校验核心 ──────────────────────────────────────────

def validate(data):
    """返回 (passed, errors, warnings)"""
    errors = []
    warnings = []

    # Step 1: 检查元数据
    for field in REQUIRED_FIELDS:
        val = get_nested(data, field)
        if not val:
            errors.append(f"META_MISSING: {field}")

    # Step 2: 检查 schema 版本
    schema = data.get("schema", "")
    if not schema.startswith("openclaw.review.checklist."):
        errors.append(f"SCHEMA_MISMATCH: expected 'openclaw.review.checklist.*', got '{schema}'")

    # Step 3: 遍历 mandatory 检查项
    checks = data.get("checks", {})
    mandatory = checks.get("mandatory", {})

    for item_name in MANDATORY_ITEMS:
        item = mandatory.get(item_name, {})
        passed = item.get("passed", False)
        if not passed:
            desc = item.get("description", item_name)
            errors.append(f"MANDATORY_FAIL: {desc} ({item_name})")
            details = item.get("details", [])
            if isinstance(details, dict):
                assessment = details.get("assessment", "")
                if assessment and "❌" in assessment:
                    errors.append(f"  → 结尾评估不通过: {assessment}")
            elif isinstance(details, list):
                for d in details:
                    status = d.get("status", "")
                    if isinstance(status, str) and "待修" in status:
                        errors.append(f"  → 未修复: {d.get('location', '?')} - {d.get('issue', '?')}")

    # Step 4: 遍历 suggested 检查项
    suggested = checks.get("suggested", {})
    for item_name in SUGGESTED_ITEMS:
        item = suggested.get(item_name, {})
        passed = item.get("passed", False)
        if not passed:
            desc = item.get("description", item_name)
            warnings.append(f"SUGGESTED_FAIL: {desc} ({item_name})")
            details = item.get("details", [])
            if isinstance(details, list):
                for d in details:
                    fixed = d.get("fixed")
                    if fixed is False:
                        warnings.append(f"  → 未处理: {d.get('issue', '?')} at {d.get('location', '?')}")

    # Step 5: 遍历 optional 检查项（仅记录 info）
    optional = checks.get("optional", {})
    for item_name in OPTIONAL_ITEMS:
        item = optional.get(item_name, {})
        passed = item.get("passed", False)
        if not passed:
            desc = item.get("description", item_name)
            # optional 未通过不算 warnings 也不报错，只输出 info
            details = item.get("details", [])
            if isinstance(details, list):
                for d in details:
                    consistent = d.get("consistent")
                    if consistent is False:
                        pass  # 可选层，仅记录

    # Step 6: 统计汇总
    return (len(errors) == 0, errors, warnings)


def analyze(data):
    """返回统计信息"""
    checks = data.get("checks", {})
    
    def count_items(section):
        items = checks.get(section, {})
        total = len(items)
        passed = sum(1 for v in items.values() if v.get("passed", False))
        failed = total - passed
        return total, passed, failed

    m_total, m_passed, m_failed = count_items("mandatory")
    s_total, s_passed, s_failed = count_items("suggested")
    o_total, o_passed, o_failed = count_items("optional")

    # 统计 detail 记录数
    detail_count = 0
    leaf_count = 0
    for section in ["mandatory", "suggested", "optional"]:
        for item in checks.get(section, {}).values():
            details = item.get("details", [])
            if isinstance(details, list):
                detail_count += len(details)
                for d in details:
                    leaf_count += len(d)
            elif isinstance(details, dict):
                detail_count += 1
                leaf_count += len(details)

    return {
        "mandatory": {"total": m_total, "passed": m_passed, "failed": m_failed},
        "suggested": {"total": s_total, "passed": s_passed, "failed": s_failed},
        "optional": {"total": o_total, "passed": o_passed, "failed": o_failed},
        "detail_records": detail_count,
        "leaf_fields": leaf_count,
    }


# ── 主入口 ──────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(red(f"用法: python3 {sys.argv[0]} <checklist.json>"))
        print(f"     支持通配符: python3 {sys.argv[0]} 'docs/reviews/*/checklist*.json'")
        sys.exit(2)

    input_path = sys.argv[1]
    files = sorted(Path(".").glob(input_path)) if ("*" in input_path or "?" in input_path) else [Path(input_path)]

    if not files:
        print(red(f"未找到文件: {input_path}"))
        sys.exit(2)

    all_passed = True
    for filepath in files:
        if not filepath.exists():
            print(red(f"文件不存在: {filepath}"))
            all_passed = False
            continue

        try:
            data = json.loads(filepath.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(red(f"[JSON_ERROR] {filepath}: {e}"))
            sys.exit(2)

        # ── 输出头部 ──
        meta = data.get("meta", {})
        print(f"\n{'='*60}")
        print(f"📋 {filepath}")
        print(f"   草稿: {meta.get('draft_path', '?')}")
        print(f"   版本: {meta.get('draft_version', '?')}")
        print(f"   日期: {meta.get('review_date', '?')}")
        print(f"   审稿: {meta.get('reviewer', '?')}")
        print(f"{'='*60}")

        # ── 校验 ──
        passed, errors, warnings = validate(data)

        # ── 统计 ──
        stats = analyze(data)

        # ── 汇总表 ──
        print(f"\n  {'层级':<12} {'总数':>5} {'通过':>5} {'未通过':>5}")
        print(f"  {'-'*30}")
        for level in ["mandatory", "suggested", "optional"]:
            s = stats[level]
            label = {"mandatory": "🔴 必须", "suggested": "🟡 建议", "optional": "🔧 可选"}[level]
            print(f"  {label:<12} {s['total']:>5} {s['passed']:>5} {s['failed']:>5}")
        print(f"\n  detail 记录: {stats['detail_records']}")
        print(f"  叶子字段:  {stats['leaf_fields']}")
        print(f"  检查点:    {stats['mandatory']['total'] + stats['suggested']['total'] + stats['optional']['total']}")

        # ── 结果 ──
        if errors:
            print(f"\n  {red('[FAIL] 审稿不完整')}")
            for err in errors:
                print(f"    {red('✗')} {err}")
            all_passed = False
        elif warnings:
            print(f"\n  {yellow('[PASS_WARN] 审稿通过但有提醒')}")
            for warn in warnings:
                print(f"    {yellow('⚠')} {warn}")
        else:
            print(f"\n  {green('[PASS] 审稿完整性校验通过')}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
