#!/usr/bin/env python3
"""
gatekeeper_integration.py — Orchestrator 与 Gatekeeper 协作层

通过状态文件通信，零直接函数调用：
  _gk_pending_action.json   ← Orchestrator 写入，Gatekeeper 读取
  _gk_user_decision.json    ← Gatekeeper 写入，Orchestrator 读取

用法：
  from gatekeeper_integration import (
      notify_gatekeeper,          # 通知 Gatekeeper 有新事件
      wait_for_gatekeeper,        # 等待用户决策
      gk_available,               # 检查 Gatekeeper 是否启用
  )
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

WORKSPACE = Path(os.environ.get(
    "THESIS_WORKSPACE",
    os.path.expanduser("~/.openclaw/workspace")
))


# ============================================================
# 路径工具
# ============================================================

def _paper_dir(paper_name: str) -> Path:
    return WORKSPACE / paper_name


def _pending_action_path(paper_name: str) -> Path:
    return _paper_dir(paper_name) / "_gk_pending_action.json"


def _user_decision_path(paper_name: str) -> Path:
    return _paper_dir(paper_name) / "_gk_user_decision.json"


# ============================================================
# Gatekeeper 可用性检查
# ============================================================

def gk_enabled(paper_name: str) -> bool:
    """检查 Gatekeeper 是否启用（state 中有 gk_enabled=true）"""
    state_path = _paper_dir(paper_name) / "_orchestrate_state.json"
    if not state_path.exists():
        return False
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state.get("gk_enabled", False)
    except Exception:
        return False


# ============================================================
# 通知 Gatekeeper（Orchestrator → Gatekeeper）
# ============================================================

def notify_gatekeeper(
    paper_name: str,
    event: str,
    phase: str,
    node_id: str = "",
    details: Dict = None,
    blocking: bool = False,
) -> Dict[str, Any]:
    """
    通知 Gatekeeper 有新事件发生。

    参数：
      paper_name: 论文名
      event:      事件类型（见下）
      phase:      当前 Phase
      node_id:    节点 ID（可选）
      details:    额外详情
      blocking:   是否阻塞等待用户决策

    事件类型：
      "phase_start"        — Phase 开始
      "phase_complete"    — Phase 完成
      "node_write_complete"— 节点写作完成
      "quality_check"      — 触发质量检查
      "hils_blocked"      — HIL 阻断
      "export_ready"       — 准备导出 Word

    返回：
      {"ok": True,  "decision": None}           — 无需等待，继续
      {"ok": True,  "decision": "proceed"}      — 用户选择继续
      {"ok": True,  "decision": "skip"}          — 用户选择跳过
      {"ok": True,  "decision": "fix"}           — 用户选择修复
      {"ok": False, "blocked": True, ...}       — 需要等待
    """
    details = details or {}

    # 写 pending action
    action = {
        "event": event,
        "phase": phase,
        "node_id": node_id,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "details": details,
        "blocking": blocking,
        "handled": False,
    }
    pending_path = _pending_action_path(paper_name)
    pending_path.parent.mkdir(parents=True, exist_ok=True)
    with open(pending_path, "w", encoding="utf-8") as f:
        json.dump(action, f, ensure_ascii=False, indent=2)

    if not blocking:
        return {"ok": True, "decision": None, "event": event}

    # 阻塞等待用户决策（最多等 30 分钟）
    deadline = time.time() + 1800
    while time.time() < deadline:
        decision_path = _user_decision_path(paper_name)
        if decision_path.exists():
            try:
                with open(decision_path, "r", encoding="utf-8") as f:
                    decision = json.load(f)
                if decision.get("handled"):
                    # 清理决策文件
                    decision_path.unlink()
                    _pending_action_path(paper_name).unlink(missing_ok=True)
                    return {
                        "ok": True,
                        "decision": decision.get("decision"),
                        "reason": decision.get("reason", ""),
                    }
            except Exception:
                pass
        time.sleep(2)

    return {
        "ok": False,
        "blocked": True,
        "reason": "用户决策超时（30分钟）",
    }


# ============================================================
# Gatekeeper 事件分发（Gatekeeper → Orchestrator）
# ============================================================

def clear_pending(paper_name: str) -> None:
    """清除 pending action 文件"""
    _pending_action_path(paper_name).unlink(missing_ok=True)
    _user_decision_path(paper_name).unlink(missing_ok=True)


def write_user_decision(
    paper_name: str,
    decision: str,  # "proceed" | "skip" | "fix" | "manual"
    reason: str = "",
) -> None:
    """
    写入用户决策（供 Orchestrator 读取）。

    通常由 OpenClaw agent 调用（在收到 Gatekeeper 飞书通知后）。
    """
    decision_path = _user_decision_path(paper_name)
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    with open(decision_path, "w", encoding="utf-8") as f:
        json.dump({
            "decision": decision,
            "reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "handled": True,
        }, f, ensure_ascii=False, indent=2)
