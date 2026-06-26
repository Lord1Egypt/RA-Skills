# -*- coding: utf-8 -*-
"""
skill-evolve-pro - Phase 4
skill_apply.py - Four atomic operation modules

Applies Patch (edits list) to SKILL.md.
Each step checks SLOW_UPDATE protected region and returns execution report.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# -- Constants ------------------------------------------------------------
SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"


# -- Protected region detection -------------------------------------------
def _is_in_slow_update_region(skill: str, target: str) -> bool:
    """
    Check if target is inside SLOW_UPDATE protected region.
    Returns True = in protected region, should reject operation.
    """
    if not target:
        return False
    start_idx = skill.find(SLOW_UPDATE_START)
    end_idx = skill.find(SLOW_UPDATE_END)
    if start_idx == -1 or end_idx == -1:
        return False
    target_idx = skill.find(target)
    if target_idx == -1:
        return False
    return start_idx <= target_idx < end_idx + len(SLOW_UPDATE_END)


def _get_slow_update_region_bounds(skill: str) -> tuple[int, int]:
    """Return (start_idx, end_idx) or (-1, -1) if not found"""
    start = skill.find(SLOW_UPDATE_START)
    end = skill.find(SLOW_UPDATE_END)
    return start, end


# -- Atomic operations ----------------------------------------------------

def apply_append(skill: str, content: str, slow_region: tuple) -> tuple[str, dict]:
    """
    Append content to document end or before protected region.

    Returns: (new_skill_content, report_dict)
    """
    su_start, su_end = slow_region
    report = {
        "op": "append",
        "target": "",
        "content_preview": content[:80] if content else "",
        "status": "unknown",
        "reason": "",
    }

    content = content.strip()
    if not content:
        report["status"] = "skipped_empty_content"
        report["reason"] = "content is empty, skip"
        return skill, report

    if su_start != -1:
        before = skill[:su_start].rstrip()
        report["status"] = "applied_append_before_slow_update"
        report["reason"] = "inserted before SLOW_UPDATE protected region"
        return before + "\n\n" + content + "\n\n" + skill[su_start:], report
    else:
        report["status"] = "applied_append"
        report["reason"] = "appended to document end"
        return skill.rstrip() + "\n\n" + content + "\n", report


def apply_insert_after(
    skill: str, target: str, content: str, slow_region: tuple
) -> tuple[str, dict]:
    """
    Insert new content after the target text segment.

    Returns: (new_skill_content, report_dict)
    """
    su_start, su_end = slow_region
    report = {
        "op": "insert_after",
        "target": target[:100] if target else "",
        "content_preview": content[:80] if content else "",
        "status": "unknown",
        "reason": "",
    }

    content = content.strip()
    target = target.strip()

    if not target:
        report["status"] = "applied_insert_after_fallback_append"
        report["reason"] = "target is empty, degraded to append"
        new_skill, _ = apply_append(skill, content, slow_region)
        return new_skill, report

    if _is_in_slow_update_region(skill, target):
        report["status"] = "skipped_in_slow_update_region"
        report["reason"] = "target text is in SLOW_UPDATE protected region, reject"
        return skill, report

    if target not in skill:
        report["status"] = "skipped_target_not_found"
        report["reason"] = "target not found in document, degraded to append"
        new_skill, _ = apply_append(skill, content, slow_region)
        return new_skill, report

    idx = skill.index(target) + len(target)
    newline_idx = skill.find("\n", idx)
    if newline_idx != -1:
        insert_at = newline_idx + 1
    else:
        insert_at = len(skill)

    report["status"] = "applied_insert_after"
    report["reason"] = "inserted after target"
    return skill[:insert_at] + "\n" + content + "\n" + skill[insert_at:], report


def apply_replace(
    skill: str, target: str, content: str, slow_region: tuple
) -> tuple[str, dict]:
    """
    Replace target text with new content.

    Returns: (new_skill_content, report_dict)
    """
    su_start, su_end = slow_region
    report = {
        "op": "replace",
        "target": target[:100] if target else "",
        "content_preview": content[:80] if content else "",
        "status": "unknown",
        "reason": "",
    }

    content = content.strip()
    target = target.strip()

    if not target:
        report["status"] = "skipped_empty_target"
        report["reason"] = "target is empty, cannot replace"
        return skill, report

    if _is_in_slow_update_region(skill, target):
        report["status"] = "skipped_in_slow_update_region"
        report["reason"] = "target text is in SLOW_UPDATE protected region, reject"
        return skill, report

    if target not in skill:
        report["status"] = "skipped_target_not_found"
        report["reason"] = "target not found in document, cannot replace"
        return skill, report

    report["status"] = "applied_replace"
    report["reason"] = "target text replaced"
    return skill.replace(target, content, 1), report


def apply_delete(skill: str, target: str, slow_region: tuple) -> tuple[str, dict]:
    """
    Delete target text from document.

    Returns: (new_skill_content, report_dict)
    """
    su_start, su_end = slow_region
    report = {
        "op": "delete",
        "target": target[:100] if target else "",
        "status": "unknown",
        "reason": "",
    }

    target = target.strip()

    if not target:
        report["status"] = "skipped_empty_target"
        report["reason"] = "target is empty, cannot delete"
        return skill, report

    if _is_in_slow_update_region(skill, target):
        report["status"] = "skipped_in_slow_update_region"
        report["reason"] = "target text is in SLOW_UPDATE protected region, reject"
        return skill, report

    if target not in skill:
        report["status"] = "skipped_target_not_found"
        report["reason"] = "target not found in document, cannot delete"
        return skill, report

    report["status"] = "applied_delete"
    report["reason"] = "target text deleted"
    return skill.replace(target, "", 1), report


# -- Main function -------------------------------------------------------

def apply_all_edits(
    skill: str, edits: list, slow_region: Optional[tuple] = None
) -> tuple[str, list[dict]]:
    """
    Apply all edits sequentially, return updated skill content and per-step reports.

    Parameters
    ----------
    skill : str
        Current SKILL.md content
    edits : list[dict]
        Phase 3 output edits list, each with:
        op, target, content, reason, priority, fail_count
    slow_region : tuple, optional
        (slow_start_idx, slow_end_idx), auto-detected if None

    Returns
    -------
    tuple[str, list[dict]]
        (new_skill_content, edit_reports_list)
        edit_report: {"op", "target", "content_preview", "status", "reason", "index"}
    """
    if slow_region is None:
        slow_region = _get_slow_update_region_bounds(skill)

    reports: list[dict] = []

    for idx, edit in enumerate(edits, 1):
        op = edit.get("op", "append")
        target = edit.get("target", "").strip()
        content = edit.get("content", "").strip()
        reason = edit.get("reason", "")

        base_report = {
            "index": idx,
            "op": op,
            "target": target[:100] if target else "(none)",
            "content_preview": content[:80] if content else "(none)",
            "reason": reason,
            "status": "unknown",
        }

        if op == "append":
            new_skill, report = apply_append(skill, content, slow_region)
        elif op == "insert_after":
            new_skill, report = apply_insert_after(skill, target, content, slow_region)
        elif op == "replace":
            new_skill, report = apply_replace(skill, target, content, slow_region)
        elif op == "delete":
            new_skill, report = apply_delete(skill, target, slow_region)
        else:
            report = {"status": "skipped_unknown_op", "reason": f"unknown op: {op}"}
            new_skill = skill

        full_report = {**base_report, **report}
        full_report["index"] = idx
        reports.append(full_report)
        skill = new_skill

    return skill, reports


# -- CLI test entry ------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="skill_apply.py - Phase 4 atomic operations")
    parser.add_argument("--skill", "-s", default=None, help="SKILL.md path")
    parser.add_argument("--edits", "-e", default=None, help="edits JSON path")
    parser.add_argument("--output", "-o", default=None, help="output path")
    args = parser.parse_args()

    # Load SKILL.md
    if args.skill:
        skill_path = Path(args.skill)
    else:
        try:
            from config import DEFAULT_TARGET_SKILL_DIR
            skill_path = DEFAULT_TARGET_SKILL_DIR / "SKILL.md"
        except ImportError:
            import os
            WORKSPACE = Path(os.environ.get(
                "OPENCLAW_WORKSPACE",
                os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
            ))
            skill_path = WORKSPACE / "skills" / "robot-evolve" / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8")
    print(f"[skill_apply] Read SKILL.md: {skill_path}")
    print(f"[skill_apply] SKILL.md length: {len(skill)} chars")

    # Load or build edits
    if args.edits:
        edits_path = Path(args.edits)
        data = json.loads(edits_path.read_text(encoding="utf-8"))
        edits = data.get("edits", []) if isinstance(data, dict) else data
    else:
        # Demo edits targeting robot-evolve SKILL.md - uses actual file content
        edits = [
            {
                "op": "replace",
                "target": "1. **MMX命令规范**：任何搜索必须使用 `npx mmx search` 命令，路径格式为 `npx mmx search query --q \"关键词\"`，严禁使用其他替代命令或绕路格式。",
                "content": "1. **MMX命令规范**：任何搜索必须使用 `npx mmx search` 命令，路径格式为 `npx mmx search query --q \"关键词\"`，严禁使用其他替代命令或绕路格式。\n\n2. **搜索沉心模式**：遇到错误或决断问题时，至少进行 3 次搜索内容检查，再给出回答。\n\n3. **产品参数核实**：涉及硬件规格、芯片型号等信息时，必须调用搜索获取最新官方网站数据或权威评测，禁止凭模型内部知识直接作答。",
                "reason": "Add search depth rule and product parameter verification rule",
                "priority": "high",
                "fail_count": 2,
            },
            {
                "op": "append",
                "target": "",
                "content": "\n\n---\n\n## 进化记录\n\n| 日期 | round | 轨迹统计 | 应用编辑数 | Gate通过 |\n|------|-------|---------|-----------|---------|\n| - | - | total=0 hard_success=0 hard_fail=0 | - | - |\n\n进化记录由 `skill-evolve-pro` Phase 6 自动维护。",
                "reason": "Add evolution record table for tracking history",
                "priority": "medium",
                "fail_count": 1,
            },
            {
                "op": "replace",
                "target": "1. **禁止修改安全字段**：`gateway.bind`、`gateway.auth`、`tailscale.expose`",
                "content": "1. **禁止修改安全字段**：`gateway.bind`、`gateway.auth`、`tailscale.expose`、`agent.model`",
                "reason": "Add agent.model to forbidden modification list",
                "priority": "medium",
                "fail_count": 1,
            },
            {
                "op": "insert_after",
                "target": "### L0 级别（无需告知）",
                "content": "#### L0 自我检查清单\n- [ ] 工作区文件完整（SOUL.md、AGENTS.md、MEMORY.md 存在）\n- [ ] `memory/` 目录可写\n- [ ] 无异常长度的会话状态文件",
                "reason": "Add L0 self-check checklist before executing L0 actions",
                "priority": "low",
                "fail_count": 0,
            },
        ]

    print(f"[skill_apply] Loaded {len(edits)} edits to apply")

    # Run apply
    new_skill, reports = apply_all_edits(skill, edits)

    # Output reports
    sep = "=" * 70
    print(f"\n{sep}")
    print("apply_all_edits() - Execution Report")
    print(sep)

    for r in reports:
        status_tag = "OK" if r["status"].startswith("applied") else "SKIP"
        target_display = repr(r["target"])[:60]
        try:
            print(f"\n  [{r['index']}] {status_tag} {r['op'].upper():15s}  status={r['status']}")
            print(f"       target:   {target_display}")
            if r.get("content_preview"):
                content_display = repr(r["content_preview"])[:60]
                print(f"       content:  {content_display}")
            print(f"       reason:   {r.get('reason', '')}")
        except UnicodeEncodeError:
            print(f"\n  [{r['index']}] {status_tag} {r['op'].upper():15s}  status={r['status']}")
            print(f"       target:   (unicode, skipped)")
            print(f"       reason:   {r.get('reason', '')}")

    applied = sum(1 for r in reports if r["status"].startswith("applied"))
    skipped = len(reports) - applied
    print(f"\n  Summary: {applied} applied / {skipped} skipped")

    # Output last 20 lines of SKILL.md
    new_lines = new_skill.splitlines()
    print(f"\n{sep}")
    print(f"SKILL.md after apply - last 20 lines (total {len(new_lines)} lines)")
    print(sep)
    for line in new_lines[-20:]:
        print(line)

    # Save optional output
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(new_skill, encoding="utf-8")
        print(f"\n[skill_apply] Saved to: {out_path}")

    print("\n[PASS] skill_apply.py test complete")
