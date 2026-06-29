#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MBA Thesis Workflow - Orchestrator 自动推进引擎

功能：
1. 读取状态文件 + 决策下一步动作
2. Phase 完成后自动校验（loop_self_check）
3. HIL 节点暂停/恢复逻辑
4. 审核 Loop 的 P0 计数与重试判断

使用方式：
  # 决策
  python3 orchestrator.py <状态文件路径>
  
  # 校验 Phase 输出
  python3 orchestrator.py --validate <状态文件路径>

与 cron 配合：
  cron job 每5分钟触发 → 调用 orchestrator.py → 返回决策
  → agent 根据决策执行 next action → 更新状态文件 → cron 下次再查
"""

import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Tuple


# ==================== 动作定义 ====================

class Action(Enum):
    """Orchestrator 决策输出类型"""
    ENTER_PHASE_2 = "enter_phase_2"               # 进入 Phase 2 起草
    ENTER_PHASE_3 = "enter_phase_3"               # 进入 Phase 3 审核
    ENTER_PHASE_35 = "enter_phase_35"             # 进入 Phase 3.5 深度评审
    ENTER_PHASE_4 = "enter_phase_4"               # 进入 Phase 4 整合
    ENTER_PHASE_4_REVISION = "enter_phase_4_revision"  # 进入修订
    ENTER_PHASE_5 = "enter_phase_5"               # 进入 Phase 5 终审
    ENTER_PHASE_52 = "enter_phase_52"             # 进入 Phase 5.2 Word 输出
    HIL_WAIT = "hil_wait"                         # 暂停等用户确认
    RETRY = "retry"                               # 打回当前 Phase 重做
    DONE = "done"                                 # 全部完成


# ==================== 辅助函数 ====================

def _find_latest_report(workspace: str, paper: str = "") -> Optional[str]:
    """找到最新的审核报告"""
    candidates = []
    if paper:
        candidates = sorted(
            glob.glob(os.path.join(workspace, f"*{paper}*审核报告*.md")),
            key=os.path.getmtime, reverse=True
        )
    if not candidates:
        candidates = sorted(
            glob.glob(os.path.join(workspace, "*审核报告*.md")),
            key=os.path.getmtime, reverse=True
        )
    if not candidates:
        candidates = sorted(
            glob.glob(os.path.join(workspace, "*_审核*.md")),
            key=os.path.getmtime, reverse=True
        )
    return candidates[0] if candidates else None


def _find_latest_thesis_md(workspace: str) -> Optional[str]:
    """找到最新的论文 md 文件"""
    patterns = ["论文*.md", "*thesis*.md", "*Thesis*.md",
                "*开题*.md", "*报告*.md", "*dissertation*.md"]
    candidates = []
    for pat in patterns:
        candidates.extend(glob.glob(os.path.join(workspace, pat)))
    if not candidates:
        return None
    return sorted(candidates, key=os.path.getmtime, reverse=True)[0]


def count_p0_from_reports(workspace: str, paper: str = "") -> int:
    """从审核报告解析 P0 问题数量"""
    report = _find_latest_report(workspace, paper)
    if not report:
        return 0
    with open(report, 'r', encoding='utf-8') as f:
        content = f.read()
    # 计数策略：结构化 P0 标记 / 🔴 标记
    p0_matches = re.findall(r'🔴|P0', content)
    return len(p0_matches)


def all_chapters_exist_simple(state: Dict[str, Any]) -> bool:
    """检查所有计划章节是否已完成"""
    chapters = state.get("chapters", {})
    planned = state.get("planned_chapters", [])
    if not planned:
        return False
    return all(
        chapters.get(ch, {}).get("status") == "completed"
        for ch in planned
    )


def get_phase_number(phase_name: str) -> int:
    """从 Phase 名称提取序号（Phase 3.5 → 35）"""
    m = re.search(r'(\d+(?:\.\d+)?)', phase_name)
    return int(float(m.group(1)) * 10) if m else 0


# ==================== 核心决策树 ====================

def decide_next_action(state: Dict[str, Any], workspace: str = ".") -> Tuple[Action, Dict]:
    """
    读取状态文件，决定下一步动作。
    注意：更长的前缀必须排在更短的前面，避免子串误匹配。
    """
    phase = state.get("phase", "")
    paper = state.get("paper", "")

    # ---------- Phase 1 （无子串冲突，在最前面）----------
    if "Phase 1" in phase and ("完成" in phase or "已确认" in phase):
        if state.get("company_mapping") and state.get("outline_confirmed"):
            return Action.ENTER_PHASE_2, {}
        return Action.HIL_WAIT, {
            "hil_msg": "Phase 1 完成，请确认公司映射表和大纲后再继续"
        }

    # ---------- Phase 2.5 （比 Phase 2 长，先判断）----------
    if "Phase 2.5" in phase and ("确认" in phase or "完成" in phase):
        return Action.ENTER_PHASE_3, {}

    # ---------- Phase 2 ----------
    if "Phase 2" in phase and "完成" in phase:
        if all_chapters_exist_simple(state):
            return Action.HIL_WAIT, {
                "hil_msg": "Phase 2 章节初稿已完成，请确认内容是否符合预期"
            }
        md_file = _find_latest_thesis_md(workspace)
        return Action.RETRY, {
            "retry_reason": "章节文件不完整，请补写缺失章节",
            "md_file": str(md_file) if md_file else ""
        }

    # ---------- Phase 3.5 （比 Phase 3 长，先判断）----------
    if "Phase 3.5" in phase and "完成" in phase:
        p0_count = count_p0_from_reports(workspace, paper)
        review_round = state.get("review_loop", {}).get("current_round", 0)
        max_rounds = state.get("review_loop", {}).get("max_rounds", 3)
        if p0_count == 0:
            if review_round >= 2:
                return Action.ENTER_PHASE_4, {}
            return Action.ENTER_PHASE_4, {"note": f"P0已修复（第{review_round}轮），进入整合"}
        if review_round >= max_rounds:
            return Action.HIL_WAIT, {
                "hil_msg": f"审核已重试 {review_round}/{max_rounds} 轮仍有 {p0_count} 个 P0，请判断是否接受当前版本"
            }
        return Action.ENTER_PHASE_4_REVISION, {
            "p0_count": p0_count,
            "review_round": review_round
        }

    # ---------- Phase 3 ----------
    if "Phase 3" in phase and "完成" in phase:
        return Action.ENTER_PHASE_35, {}

    # ---------- Phase 4 修订（含 修订 的最长前缀）----------
    if "Phase 4 修订" in phase and "完成" in phase:
        return Action.ENTER_PHASE_35, {"mode": "recheck"}

    # ---------- Phase 4 整合 ----------
    if "Phase 4" in phase and ("整合" in phase or "完成" in phase):
        return Action.HIL_WAIT, {
            "hil_msg": "整合方案已完成，请确认是否进入终审"
        }

    # ---------- Phase 5.2 （比 Phase 5 长，先判断）----------
    if "Phase 5.2" in phase and ("完成" in phase or "done" in phase.lower()):
        return Action.DONE, {}

    # ---------- Phase 5 ----------
    if "Phase 5" in phase and "完成" in phase:
        return Action.ENTER_PHASE_52, {}

    # ---------- 其他 → HIL ----------
    return Action.HIL_WAIT, {
        "hil_msg": f"当前阶段: {phase}，请确认下一步操作"
    }


# ==================== 校验函数 ====================

def validate_phase_output(state: Dict[str, Any], workspace: str = ".") -> Optional[Dict]:
    """Phase 完成后自动校验"""
    phase = state.get("phase", "")
    # 只在 Phase 2/4 完成后自动校验
    if "Phase 2" not in phase and "Phase 4" not in phase:
        return None
    md_file = _find_latest_thesis_md(workspace)
    if not md_file:
        return {"error": "未找到论文文件"}
    try:
        result = subprocess.run(
            ["python3", "scripts/loop_self_check.py",
             "--file", md_file, "--json"],
            capture_output=True, text=True, timeout=30
        )
        output = json.loads(result.stdout) if result.stdout else {}
        output["md_file"] = os.path.basename(md_file)
        return output
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        return {"error": str(e), "md_file": os.path.basename(md_file)}


# ==================== 输出格式化 ====================

ACTION_LABELS = {
    Action.ENTER_PHASE_2: "进入 Phase 2：双版本起草",
    Action.ENTER_PHASE_3: "进入 Phase 3：双版本审核",
    Action.ENTER_PHASE_35: "进入 Phase 3.5：深度学术评审",
    Action.ENTER_PHASE_4: "进入 Phase 4：整合",
    Action.ENTER_PHASE_4_REVISION: "进入 Phase 4：修订（审核 Loop）",
    Action.ENTER_PHASE_5: "进入 Phase 5：终审",
    Action.ENTER_PHASE_52: "进入 Phase 5.2：Word 输出",
    Action.HIL_WAIT: "⏸ 暂停等待用户确认",
    Action.RETRY: "🔄 打回重做",
    Action.DONE: "✅ 全部完成",
}


def format_decision(action: Action, params: Dict) -> str:
    """生成人类可读的决策摘要"""
    label = ACTION_LABELS.get(action, str(action))
    msg = f"[决策] {label}"
    if action == Action.ENTER_PHASE_4_REVISION:
        msg += f" | P0={params.get('p0_count', '?')}"
    if action in (Action.HIL_WAIT, Action.RETRY):
        msg += f" | {params.get('hil_msg') or params.get('retry_reason', '')}"
    return msg


# ==================== CLI 入口 ====================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <状态文件路径> [--validate]", file=sys.stderr)
        sys.exit(1)

    state_path = sys.argv[1]
    do_validate = "--validate" in sys.argv

    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    workspace = os.path.dirname(state_path) or "."
    action, params = decide_next_action(state, workspace)

    output = {
        "action": action.value,
        "params": params,
        "label": ACTION_LABELS.get(action, str(action)),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "current_phase": state.get("phase", ""),
    }

    # Phase 完成后自动校验
    validation = validate_phase_output(state, workspace)
    if validation:
        output["validation"] = validation

    # 人类可读摘要
    output["summary"] = format_decision(action, params)

    print(json.dumps(output, ensure_ascii=False, indent=2))
