# -*- coding: utf-8 -*-
"""
skill-evolve-pro · Phase 2
SESSION-STATE.md 解析器 + 失败模式检测

从 SESSION-STATE.md 提取结构化信息，生成 RolloutResult 列表
"""

from __future__ import annotations

import re
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple

from rollout_result import RolloutResult, make_rollout_result


# ---------------------------------------------------------------------------
# 解析 SESSION-STATE.md
# ---------------------------------------------------------------------------

def parse_session_state(session_state_path: str) -> dict:
    """
    解析 SESSION-STATE.md，返回结构化数据字典。

    Parameters
    ----------
    session_state_path : str
        SESSION-STATE.md 文件路径

    Returns
    -------
    dict
        结构化数据，包含字段：
        - timestamp: str           最后更新时间
        - task_type: str           当前任务类型
        - active_tasks: list[dict] 活跃任务列表
        - recent_operations: list[dict] 最近操作记录
        -，先生纠正内容: list[str] 先生刚纠正的内容
        - failures_detected: list[str] 检测到的失败模式列表
        - raw_content: str         原始内容（用于调试）
    """
    if not os.path.exists(session_state_path):
        return {
            "timestamp": "",
            "task_type": "unknown",
            "active_tasks": [],
            "recent_operations": [],
            "corrections": [],
            "failures_detected": [],
            "raw_content": "",
            "error": "file not found",
        }

    with open(session_state_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 提取 timestamp
    ts_match = re.search(r"最后更新时间[：:]\s*(.+)", content)
    timestamp = ts_match.group(1).strip() if ts_match else ""

    # 2. 提取 task_type（从 "## 当前任务" 或 Session Info 中）
    task_type = _extract_task_type(content)

    # 3. 提取活跃任务（表格行）
    active_tasks = _extract_active_tasks(content)

    # 4. 提取最近操作记录（Conversation / 操作日志）
    recent_ops = _extract_recent_operations(content)

    # 5. 提取先生刚纠正的内容（先生说的"不是"/"重来"/纠错类话）
    corrections = _extract_corrections(content)

    # 6. 检测失败模式（先生纠正 + AI执行失败 + 明确否定）
    failures_detected = _detect_failure_patterns(content)

    return {
        "timestamp": timestamp,
        "task_type": task_type,
        "active_tasks": active_tasks,
        "recent_operations": recent_ops,
        "corrections": corrections,
        "failures_detected": failures_detected,
        "raw_content": content,
    }


def _extract_task_type(content: str) -> str:
    """从 SESSION-STATE.md 提取当前任务类型"""
    # 匹配 "task_type: xxx" 或 "## 当前任务"
    match = re.search(r"task_type[：:]\s*(\w+)", content)
    if match:
        return match.group(1).strip()

    # 从 ## 当前任务 区域提取
    section = re.search(r"## 当前任务(.+?)(?=##|\Z)", content, re.DOTALL)
    if section:
        lines = section.group(1).strip().splitlines()
        for line in lines:
            if "项目" in line or "任务" in line:
                # 返回第一个非表头的任务名
                continue
            if line.strip() and not line.startswith("|") and not line.startswith("-"):
                return line.strip()[:50]

    return "unknown"


def _extract_active_tasks(content: str) -> list[dict]:
    """提取活跃任务表格"""
    tasks = []
    # 匹配 markdown 表格行（以 | 开头）
    rows = re.findall(r"^\|[^|\n]+\|[^|\n]+\|[^|\n]+\|[^|\n]+\|", content, re.MULTILINE)
    for row in rows:
        cells = [c.strip() for c in row.split("|")[1:-1]]  # 去掉首尾空cell
        if len(cells) >= 3 and cells[0].isdigit():
            tasks.append({
                "id": cells[0],
                "project": cells[1],
                "task": cells[2],
                "status": cells[3] if len(cells) > 3 else "",
            })
    return tasks


def _extract_recent_operations(content: str) -> list[dict]:
    """提取最近操作记录"""
    ops = []
    # 查找 ## Conversation 或 ## 最近操作 节
    section = re.search(
        r"(?:## Conversation|## 最近操作|## 操作记录)(.+?)(?=## |\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not section:
        return ops

    lines = section.group(1).strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # 检测先生/AI 发言行
        m_user = re.match(r"先生[：:]\s*(.+)", line)
        m_ai = re.match(r"(?:AI|双鱼座)[：:]\s*(.+)", line)
        if m_user:
            ops.append({"role": "user", "content": m_user.group(1)[:200]})
        elif m_ai:
            ops.append({"role": "ai", "content": m_ai.group(1)[:200]})
    return ops


def _extract_corrections(content: str) -> list[str]:
    """
    从 SESSION-STATE.md 提取先生刚纠正的内容。
    触发词：不是/重来/错了/路径不对/芯片型号错了 等
    """
    correction_patterns = [
        r"不是[，,\s].+",
        r"重来",
        r"错了[，,\s].+",
        r"路径不对",
        r"芯片型号错了",
        r"漏了[，,\s].+",
        r"缺少[，,\s].+",
        r"应该[是|用].+[,，]不是",
        r"你(?:又)?搞错",
        r"重新(.+)",
    ]
    corrections = []
    for pat in correction_patterns:
        matches = re.findall(pat, content)
        corrections.extend(matches)
    # 去重，保持顺序
    seen = set()
    unique = []
    for c in corrections:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def _detect_failure_patterns(content: str) -> list[str]:
    """
    检测 SESSION-STATE.md 中的失败模式。

    失败模式检测规则：
    1. 先生纠正了AI的错误
    2. AI执行失败（工具调用报错）
    3. 先生说了"不是"或"重来"
    4. 任务状态为 "❌ 失败" 或 "❌ 完成" 但有错误标记
    """
    patterns = [
        # 显式失败标记
        (r"❌\s*失败", "AI执行失败"),
        (r"❌\s*报错[：:]\s*(.+?)(?:\n|$)", "工具调用报错: \\1"),
        (r"error[：:]\s*(.+?)(?:\n|$)", "执行错误: \\1"),

        # 先生明确否定
        (r"不是[，,\s](.+?)(?:\n|$)", "先生否定: 不是 \\1"),
        (r"重来", "先生要求重来"),
        (r"路径不对", "先生纠正: 路径不对"),

        # 任务未完成标记
        (r"状态[：:]\s*.*?(失败|错误|❌)", "任务状态: 失败"),
    ]

    detected = []
    for pattern, description in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for m in matches:
            if isinstance(m, tuple):
                msg = description.replace("\\1", m[0] if m else "")
            else:
                msg = description.replace("\\1", str(m))
            if msg not in detected:
                detected.append(msg)
    return detected


# ---------------------------------------------------------------------------
# 从 SESSION-STATE.md 检测失败轨迹 → RolloutResult 列表
# ---------------------------------------------------------------------------

def detect_failures(session_state_path: str) -> List[RolloutResult]:
    """
    从 SESSION-STATE.md 检测失败模式，生成 RolloutResult 列表。

    Parameters
    ----------
    session_state_path : str
        SESSION-STATE.md 文件路径

    Returns
    -------
    List[RolloutResult]
        检测到的每条失败轨迹（可能为空列表）
    """
    parsed = parse_session_state(session_state_path)
    content = parsed["raw_content"]

    if not content:
        return []

    results: List[RolloutResult] = []

    # 从 active_tasks 中提取失败任务
    for task in parsed.get("active_tasks", []):
        status = task.get("status", "")
        # 失败状态判断
        if any(kw in status for kw in ["❌", "失败", "错误", "待改"]):
            fail_reason = _status_to_fail_reason(status)
            result = make_rollout_result(
                skill_id="unknown",
                task_type="unknown",
                task_description=task.get("task", ""),
                user_message="",
                predicted_answer="",
                hard=0.0,
                soft=0.0,
                fail_reason=fail_reason,
                feedback="",
            )
            results.append(result)

    # 从先生纠正内容中生成 RolloutResult
    corrections = parsed.get("corrections", [])
    for corr in corrections:
        if corr.strip():
            result = make_rollout_result(
                skill_id="unknown",
                task_type="persona",
                task_description=f"先生纠正: {corr[:60]}",
                user_message="",
                predicted_answer="",
                hard=0.0,
                soft=0.0,
                fail_reason=corr,
                feedback="先生直接纠正",
            )
            results.append(result)

    # 从检测到的失败模式中生成 RolloutResult
    for failure in parsed.get("failures_detected", []):
        if failure.strip():
            result = make_rollout_result(
                skill_id="unknown",
                task_type="tool_use",
                task_description=f"失败模式: {failure[:60]}",
                user_message="",
                predicted_answer="",
                hard=0.0,
                soft=0.0,
                fail_reason=failure,
                feedback="",
            )
            results.append(result)

    return results


def _status_to_fail_reason(status: str) -> str:
    """将状态字符串转换为失败原因"""
    if "❌" in status:
        return status.split("❌")[-1].strip()
    if "失败" in status:
        return status
    if "错误" in status:
        return status
    if "待改" in status:
        return f"待修改: {status}"
    return status


# ---------------------------------------------------------------------------
# CLI 测试入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    try:
        from config import DEFAULT_SESSION
        default_path = str(DEFAULT_SESSION)
    except ImportError:
        import os
        WORKSPACE = Path(os.environ.get(
            "OPENCLAW_WORKSPACE",
            os.path.join(os.path.expanduser("~"), ".jvs", "workspace")
        ))
        default_path = str(WORKSPACE / "SESSION-STATE.md")

    path = sys.argv[1] if len(sys.argv) > 1 else default_path

    print(f"[parse_session_state] 解析文件: {path}")
    parsed = parse_session_state(path)

    print(f"\n--- 解析结果摘要 ---")
    print(f"timestamp  : {parsed['timestamp']}")
    print(f"task_type  : {parsed['task_type']}")
    print(f"active_tasks ({len(parsed['active_tasks'])} 条):")
    for t in parsed["active_tasks"]:
        print(f"  [{t['id']}] {t['project']} | {t['task']} | {t['status']}")
    print(f"corrections ({len(parsed['corrections'])} 条):")
    for c in parsed["corrections"]:
        print(f"  - {c}")
    print(f"failures_detected ({len(parsed['failures_detected'])} 条):")
    for f in parsed["failures_detected"]:
        print(f"  - {f}")

    print(f"\n--- detect_failures 轨迹列表 ---")
    rollouts = detect_failures(path)
    print(f"检测到 {len(rollouts)} 条失败轨迹:")
    for r in rollouts:
        print(f"  {r.summary()}")
