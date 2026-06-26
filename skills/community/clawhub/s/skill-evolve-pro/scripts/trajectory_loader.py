# -*- coding: utf-8 -*-
"""
skill-evolve-pro · Phase 1+2
轨迹加载器

Phase 1: 从 temp/ 目录读取失败轨迹 JSON 文件
Phase 2: 从 SESSION-STATE.md 解析失败轨迹 + 保存 RolloutResult

格式要求（Phase 1 JSON）：
  - id: str           唯一标识
  - task_description / question: str   任务描述
  - fail_reason: str  失败原因
  - predicted_answer: str  预测答案
  - reference_text: str   参考答案（可选）
"""

from __future__ import annotations

import json
import os
import glob
from pathlib import Path
from typing import Any, List, Optional

# Phase 2 模块
from rollout_result import RolloutResult, make_rollout_result
from session_state_parser import parse_session_state, detect_failures


# ---------------------------------------------------------------------------
# Phase 1: load_failed_trajectories（原有逻辑）
# ---------------------------------------------------------------------------

def load_failed_trajectories(
    temp_dir: str = "temp",
    pattern: str = "failed_trajectory_*.json",
) -> list[dict[str, Any]]:
    """
    从 temp_dir 加载所有匹配 pattern 的失败轨迹 JSON 文件。

    Parameters
    ----------
    temp_dir : str
        轨迹文件所在目录。
    pattern : str
        文件名匹配模式（默认: failed_trajectory_*.json）。

    Returns
    -------
    list[dict]
        RolloutResult 格式的 dict 列表，按文件名排序。
        单条轨迹缺少必需字段时打印警告并跳过。

    轨迹 JSON 格式示例::

        {
            "id": "task_001",
            "task_description": "帮先生写一封商务邮件",
            "question": "帮先生写一封商务邮件",
            "fail_reason": "邮件格式不符合商务规范",
            "predicted_answer": "Dear Sir, Hello...",
            "reference_text": "Dear Mr. Chen, I am writing to...",
            "hard": 0,
            "soft": 0.3
        }

    注意：即使 JSON 内 hard/soft 字段存在，loader 也仅做透传；
    质量评估由外部 rollout 评测系统负责。
    """
    # 兼容相对路径（相对于 workspace 根目录）
    workspace_root = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "..", ".."
    )
    # 如果 temp_dir 不是绝对路径，尝试相对于 workspace
    if not os.path.isabs(temp_dir):
        candidate = os.path.join(workspace_root, temp_dir)
        if os.path.isdir(candidate):
            temp_dir = candidate

    glob_path = os.path.join(temp_dir, pattern)
    files = sorted(glob.glob(glob_path))

    # 备选：直接扫描目录内所有 .json
    if not files:
        all_json = sorted(glob.glob(os.path.join(temp_dir, "*.json")))
        if all_json:
            files = all_json
            print(f"[trajectory_loader] 未找到 '{pattern}'，改为加载所有 .json 文件 ({len(files)} 个)")

    trajectories: list[dict[str, Any]] = []
    loaded = 0
    skipped = 0

    REQUIRED_FIELDS = ["fail_reason"]

    for fpath in files:
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            print(f"[trajectory_loader] 读取失败 {fpath}: {exc}")
            skipped += 1
            continue

        # 支持单条 dict 或多条 list
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = [data]
        else:
            print(f"[trajectory_loader] 跳过非法格式文件: {fpath}")
            skipped += 1
            continue

        for item in items:
            missing = [f for f in REQUIRED_FIELDS if f not in item or not item[f]]
            if missing:
                print(f"[trajectory_loader] 轨迹 {item.get('id', '?')} 缺少字段 {missing}，已跳过")
                skipped += 1
                continue

            # 标准化字段名：question → task_description
            if "question" in item and "task_description" not in item:
                item["task_description"] = item["question"]
            if "id" not in item or not item["id"]:
                item["id"] = os.path.splitext(os.path.basename(fpath))[0]

            trajectories.append(item)
            loaded += 1

    print(f"[trajectory_loader] 加载完成: {loaded} 条轨迹, {skipped} 条跳过, 来自 {len(files)} 个文件")
    return trajectories


def trajectories_to_rollout_results(trajectories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    将轨迹列表转换为 RolloutResult 兼容格式。

    确保每条记录包含: id, hard, soft, fail_reason, task_description,
    predicted_answer, reference_text。
    """
    results = []
    for t in trajectories:
        results.append({
            "id": str(t.get("id", "")),
            "hard": int(t.get("hard", 0)),
            "soft": float(t.get("soft", 0.0)),
            "fail_reason": str(t.get("fail_reason", "")),
            "task_description": str(t.get("task_description", t.get("question", ""))),
            "predicted_answer": str(t.get("predicted_answer", "")),
            "reference_text": str(t.get("reference_text", "")),
            "question": str(t.get("question", "")),
        })
    return results


# ---------------------------------------------------------------------------
# Phase 2: SESSION-STATE 解析 + RolloutResult 保存
# ---------------------------------------------------------------------------

def load_from_session_state(session_state_path: str) -> List[RolloutResult]:
    """
    从 SESSION-STATE.md 解析失败轨迹，生成 RolloutResult 列表。

    Parameters
    ----------
    session_state_path : str
        SESSION-STATE.md 文件路径

    Returns
    -------
    List[RolloutResult]
        失败轨迹列表（可能为空）
    """
    rollouts = detect_failures(session_state_path)
    print(f"[trajectory_loader] 从 SESSION-STATE 解析到 {len(rollouts)} 条失败轨迹")
    return rollouts


def load_rollout_from_json(json_path: str) -> List[RolloutResult]:
    """
    从 JSON 文件加载 RolloutResult（Phase 2 标准化格式）。

    Parameters
    ----------
    json_path : str
        JSON 文件路径

    Returns
    -------
    List[RolloutResult]
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data if isinstance(data, list) else [data]
    results = []
    for item in items:
        try:
            r = RolloutResult.from_dict(item)
            results.append(r)
        except Exception as exc:
            print(f"[trajectory_loader] RolloutResult 解析失败 {json_path}: {exc}")
    return results


def save_rollout_result(
    result: RolloutResult,
    output_dir: str = "temp/rollouts",
) -> str:
    """
    保存单条 RolloutResult 到 JSON 文件。

    Parameters
    ----------
    result : RolloutResult
        要保存的轨迹记录
    output_dir : str
        输出目录（默认: temp/rollouts，相对于 workspace）

    Returns
    -------
    str
        保存的文件路径
    """
    # 解析 workspace root
    workspace_root = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "..", ".."
    )
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(workspace_root, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    # 文件名格式: rollout_<skill_id>_<timestamp>.json
    skill_id = result.skill_id or "unknown"
    timestamp = result.timestamp.replace(":", "-").replace("T", "_")[:19]
    filename = f"rollout_{skill_id}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)

    print(f"[trajectory_loader] 已保存 RolloutResult → {filepath}")
    return filepath


def save_rollout_results(
    results: List[RolloutResult],
    output_dir: str = "temp/rollouts",
) -> List[str]:
    """
    批量保存 RolloutResult 列表到 JSON 文件。

    Parameters
    ----------
    results : List[RolloutResult]
    output_dir : str

    Returns
    -------
    List[str]
        保存的文件路径列表
    """
    return [save_rollout_result(r, output_dir) for r in results]


# ---------------------------------------------------------------------------
# 统一入口：load_all_rollouts
# ---------------------------------------------------------------------------

def load_all_rollouts(
    session_state_path: Optional[str] = None,
    json_dir: Optional[str] = None,
    json_pattern: str = "rollout_*.json",
) -> List[RolloutResult]:
    """
    统一加载入口：同时支持 SESSION-STATE.md 和 JSON 文件。

    Parameters
    ----------
    session_state_path : Optional[str]
        SESSION-STATE.md 路径（Phase 2）
    json_dir : Optional[str]
        JSON 文件目录（Phase 2 标准化格式）
    json_pattern : str
        JSON 文件匹配模式

    Returns
    -------
    List[RolloutResult]
        所有加载到的轨迹列表
    """
    all_results: List[RolloutResult] = []

    # 从 SESSION-STATE.md 解析
    if session_state_path and os.path.exists(session_state_path):
        all_results.extend(load_from_session_state(session_state_path))

    # 从 JSON 文件加载
    if json_dir:
        workspace_root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "..", ".."
        )
        if not os.path.isabs(json_dir):
            json_dir = os.path.join(workspace_root, json_dir)

        if os.path.isdir(json_dir):
            files = sorted(glob.glob(os.path.join(json_dir, json_pattern)))
            for fpath in files:
                all_results.extend(load_rollout_from_json(fpath))

    return all_results


# ---------------------------------------------------------------------------
# CLI 测试入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    # 默认 workspace
    workspace = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "..", ".."
    )
    default_session = os.path.join(workspace, "SESSION-STATE.md")

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.endswith(".md"):
            # 按文件路径测试
            path = arg
            print(f"[CLI] 解析文件: {path}")
            parsed = parse_session_state(path)
            print(f"  timestamp : {parsed['timestamp']}")
            print(f"  task_type : {parsed['task_type']}")
            print(f"  tasks     : {len(parsed['active_tasks'])} 条")
            print(f"  corrections: {len(parsed['corrections'])} 条")
            rollouts = detect_failures(path)
            print(f"\n检测到 {len(rollouts)} 条失败轨迹:")
            for r in rollouts:
                print(f"  {r.summary()}")
        else:
            # JSON 目录模式
            trajs = load_failed_trajectories(arg)
            print(f"\n共加载 {len(trajs)} 条轨迹:")
            for t in trajs:
                print(f"  [{t['id']}] fail_reason={t['fail_reason'][:60]!r}")
    else:
        # 默认测试 SESSION-STATE.md
        if os.path.exists(default_session):
            print(f"[CLI] 默认测试 SESSION-STATE.md")
            parsed = parse_session_state(default_session)
            print(f"  timestamp : {parsed['timestamp']}")
            print(f"  task_type : {parsed['task_type']}")
            print(f"  tasks     : {len(parsed['active_tasks'])} 条")
            print(f"  corrections: {len(parsed['corrections'])} 条")
            rollouts = load_from_session_state(default_session)
            print(f"\n检测到 {len(rollouts)} 条失败轨迹:")
            for r in rollouts:
                print(f"  {r.summary()}")
        else:
            print(f"[CLI] SESSION-STATE.md 不存在: {default_session}")
