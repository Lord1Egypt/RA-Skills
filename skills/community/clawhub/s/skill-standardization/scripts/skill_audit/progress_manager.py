#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
progress_manager.py v1.0.0
过程管理：读写 .progress.md，追踪 skill-standardization 三模式执行进度。

文件位置：skills/.standardization/<skill-name>/.progress.md
仅在审计结束后一次性更新，不逐条写入。
"""

import os
import re
from datetime import datetime
from pathlib import Path

# ── 常量定义 ──────────────────────────────────────────────────────────────────

RULES_ORDER = [f"R-{i:02d}" for i in range(1, 25)]  # R-01 ~ R-24

RULES_NAMES = {
    "R-01": "Frontmatter 存在性",
    "R-02": "name 字段",
    "R-03": "version 字段（SemVer）",
    "R-04": "description 字段",
    "R-05": "tags 字段",
    "R-06": "H1 标题存在",
    "R-07": "触发条件章节",
    "R-08": "核心能力章节",
    "R-09": "主要流程章节",
    "R-10": "name 与目录名一致",
    "R-11": "产出物路径合规",
    "R-12": "外部数据目录声明",
    "R-13": "敏感信息访问声明",
    "R-14": "关键位置写入声明",
    "R-15": "高权限操作风险说明",
    "R-16": "权限权重说明",
    "R-17": "渐进加载引用",
    "R-18": "反模式具体性",
    "R-19": "FAQ 有意义性",
    "R-20": "写作规范",
    "R-21": "渐进式加载显式说明",
    "R-22": "数据目录规范检查",
    "R-23": "文档-代码一致性检查",
    "R-24": "更新日志渐进加载",
}


# ── 公共接口 ────────────────────────────────────────────────────────────────────

def create_progress(skill_dir: str, mode: str) -> str:
    """
    创建/重置 .progress.md。

    Args:
        skill_dir: skill 数据目录（skills/.standardization/<skill-name>/）
        mode: 操作模式（create / update / refactor）

    Returns:
        str: .progress.md 文件路径
    """
    skill_dir = Path(skill_dir).resolve()
    progress_file = skill_dir / ".progress.md"

    operator = "AI"  # 默认操作者，可后续更新

    lines = []
    lines.append(f"# 标准化过程记录 — {skill_dir.name}")
    lines.append("")
    lines.append(f"- **操作**：{mode}")
    lines.append(f"- **开始时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **操作者**：{operator}")
    lines.append("")
    lines.append("## 进度")
    lines.append("")

    for rule_id in RULES_ORDER:
        name = RULES_NAMES.get(rule_id, rule_id)
        lines.append(f"- [ ] {rule_id}  {name}")

    lines.append("")
    lines.append("## 自动修正记录")
    lines.append("")
    lines.append("## 待手动处理")
    lines.append("")
    lines.append("## 结果")
    lines.append("")
    lines.append("_（审计完成后自动填写）_")
    lines.append("")

    progress_file.write_text("\n".join(lines), encoding="utf-8")
    return str(progress_file)


def update_progress_from_audit(skill_dir: str, audit_result: dict) -> None:
    """
    根据审计结果一次性更新 .progress.md。

    Args:
        skill_dir: skill 数据目录
        audit_result: audit_skill() 的返回结果字典
    """
    skill_dir = Path(skill_dir).resolve()
    progress_file = skill_dir / ".progress.md"
    if not progress_file.is_file():
        return  # 进度文件不存在，跳过

    content = progress_file.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 构建 rule_id → result 映射
    result_map = {}
    for res in audit_result.get("results", []):
        rid = res.get("rule_id", "")
        result_map[rid] = res

    # 更新进度章节
    new_lines = []
    in_progress = False
    in_auto_fix = False
    in_manual_fix = False
    auto_fix_items = []
    manual_fix_items = []

    for line in lines:
        stripped = line.strip()

        if stripped == "## 进度":
            in_progress = True
            new_lines.append(line)
            continue
        if stripped.startswith("## ") and in_progress:
            in_progress = False
        if stripped == "## 自动修正记录":
            in_auto_fix = True
            new_lines.append(line)
            continue
        if stripped.startswith("## ") and in_auto_fix:
            in_auto_fix = False
        if stripped == "## 待手动处理":
            in_manual_fix = True
            new_lines.append(line)
            continue
        if stripped.startswith("## ") and in_manual_fix:
            in_manual_fix = False

        # 更新进度行
        if in_progress:
            m = re.match(r"- \[( |x|X)\] (R-\d{2})\s", stripped)
            if m:
                rule_id = m.group(2)
                res = result_map.get(rule_id)
                if res:
                    passed = res.get("passed", False)
                    detail = res.get("detail", "")
                    name = RULES_NAMES.get(rule_id, rule_id)
                    new_line = f"- [{'x' if passed else ' '}] {rule_id}  {name}"
                    if detail and not passed:
                        new_line += f" — {detail[:60]}"
                    new_lines.append(new_line)
                    continue  # 跳过原行

        new_lines.append(line)

    # 收集自动修正和待手动处理项
    for res in audit_result.get("results", []):
        if res.get("passed"):
            continue
        rule_id = res.get("rule_id", "")
        fix = res.get("fix")
        if fix:
            # 判断是自动修正还是手动处理
            auto_keys = {"name", "version", "description", "tags",
                         "sensitive_access", "critical_write", "permission_weight"}
            if fix.get("key") in auto_keys:
                auto_fix_items.append(
                    f"  - `{rule_id}`: {fix.get('operation', '')}"
                )
            else:
                manual_fix_items.append(
                    f"  - `{rule_id}`: {fix.get('operation', '')} "
                    f"（位置：{fix.get('location', '未知')}）"
                )

    # 插入自动修正记录
    if auto_fix_items:
        inserted = False
        final_lines = []
        for line in new_lines:
            final_lines.append(line)
            if line.strip() == "## 自动修正记录":
                final_lines.extend(auto_fix_items)
                final_lines.append("")  # 空行
                inserted = True
        if inserted:
            new_lines = final_lines

    # 插入待手动处理项
    if manual_fix_items:
        inserted = False
        final_lines = []
        for line in new_lines:
            final_lines.append(line)
            if line.strip() == "## 待手动处理":
                final_lines.extend(manual_fix_items)
                final_lines.append("")  # 空行
                inserted = True
        if inserted:
            new_lines = final_lines

    progress_file.write_text("\n".join(new_lines), encoding="utf-8")


def finalize_progress(skill_dir: str, audit_result: dict) -> None:
    """
    写入最终结果（判定、统计、完成时间）。

    Args:
        skill_dir: skill 数据目录
        audit_result: audit_skill() 的返回结果字典
    """
    skill_dir = Path(skill_dir).resolve()
    progress_file = skill_dir / ".progress.md"
    if not progress_file.is_file():
        return

    content = progress_file.read_text(encoding="utf-8")
    lines = content.split("\n")

    verdict = audit_result.get("verdict", "?")
    summary = audit_result.get("summary", {})

    new_lines = []
    in_result = False
    result_written = False

    for line in lines:
        stripped = line.strip()

        if stripped == "## 结果":
            new_lines.append(line)
            in_result = True
            continue

        if in_result and not result_written:
            if stripped.startswith("## ") or stripped.startswith("# "):
                in_result = False

        if in_result and not result_written:
            # 覆盖旧的结果章节内容，写入新结果
            new_lines.append(f"- **最终判定**：{verdict}")
            new_lines.append(f"- **总计**：{summary.get('total', '?')} 条")
            new_lines.append(f"- **通过**：{summary.get('pass', '?')} 条")
            new_lines.append(f"- **失败**：{summary.get('fail', '?')} 条")
            new_lines.append(f"- **跳过**：{summary.get('skip', '?')} 条")
            new_lines.append(
                f"- **完成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            new_lines.append("")
            result_written = True
            in_result = False
            continue  # 跳过原结果章节的剩余行

        new_lines.append(line)

    # 如果结果章节是空的（只有 "_（审计完成后自动填写）_"），直接替换
    if not result_written:
        # 没找到结果章节，追加到文件末尾
        new_lines.append("## 结果")
        new_lines.append("")
        new_lines.append(f"- **最终判定**：{verdict}")
        new_lines.append(f"- **总计**：{summary.get('total', '?')} 条")
        new_lines.append(f"- **通过**：{summary.get('pass', '?')} 条")
        new_lines.append(f"- **失败**：{summary.get('fail', '?')} 条")
        new_lines.append(f"- **跳过**：{summary.get('skip', '?')} 条")
        new_lines.append(
            f"- **完成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        new_lines.append("")

    progress_file.write_text("\n".join(new_lines), encoding="utf-8")


def load_progress(skill_dir: str) -> dict:
    """
    读取当前进度（用于断点续传）。

    Args:
        skill_dir: skill 数据目录

    Returns:
        dict: {rule_id: {"passed": bool, "detail": str}, ...}
    """
    skill_dir = Path(skill_dir).resolve()
    progress_file = skill_dir / ".progress.md"
    if not progress_file.is_file():
        return {}

    content = progress_file.read_text(encoding="utf-8")
    progress = {}

    for line in content.split("\n"):
        stripped = line.strip()
        m = re.match(r"- \[([ xX])\] (R-\d{2})\s", stripped)
        if m:
            mark = m.group(1).strip()
            rule_id = m.group(2)
            detail = stripped[m.end():].strip(" —")
            progress[rule_id] = {
                "passed": mark == "x",
                "detail": detail,
            }

    return progress


def format_progress_markdown(skill_dir: str) -> str:
    """
    返回格式化的进度 Markdown（用于显示在报告中）。

    Args:
        skill_dir: skill 数据目录

    Returns:
        str: Markdown 格式进度条
    """
    progress = load_progress(skill_dir)
    if not progress:
        return "_（无进度记录）_"

    total = len(RULES_ORDER)
    passed = sum(1 for r in progress.values() if r["passed"])
    failed = sum(1 for r in progress.values() if not r["passed"])

    bar_len = 20
    filled = int(bar_len * passed / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)

    lines = []
    lines.append(f"**进度**：`{bar}` {passed}/{total} 通过（{failed} 失败）")
    return "\n".join(lines)
