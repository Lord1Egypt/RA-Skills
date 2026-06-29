#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MBA Thesis Workflow - State Manager
v1.7.2 新增：状态文件自动生成与维护

管理 `{论文名}_任务状态.json` 的读写和更新。
"""

import json
import os
import re
from datetime import datetime
from typing import Optional, Dict, Any


STATE_SCHEMA = {
    "paper": "",
    "version": "",
    "phase": "",
    "started_at": "",
    "last_updated": "",
    "chapters": {},
    "planned_chapters": [],
    "next_action": "",
    "review_loop": {
        "current_round": 0,
        "max_rounds": 3,
        "p0_fixed": [],
        "p0_pending": [],
    },
}


def _find_state_files(workspace: str = ".") -> list:
    """查找工作目录下的所有状态文件"""
    files = []
    for f in os.listdir(workspace):
        if f.endswith("_任务状态.json"):
            files.append(os.path.join(workspace, f))
    return sorted(files)


def resolve_paper_name(md_path: str) -> Optional[str]:
    """从 md 文件名推断论文名称"""
    bn = os.path.basename(md_path)
    bn = re.sub(r'\.md$', '', bn)
    # 去掉版本号：v1.0, v2.0, v2 等
    bn = re.sub(r'_v[\d.]+', '', bn)
    # 去掉版本后缀：_v2_final, _v1_final 等
    bn = re.sub(r'_v\d+', '', bn)
    # 去掉章节后缀：_chapter1_2_7, _H_chapter3_4, 整合版, 终稿, 润色后 等
    bn = re.sub(r'_(?:H|O|chapter|整合版|终稿|润色后|integrated).*$', '', bn)
    # 去掉审核报告后缀
    bn = re.sub(r'_审核报告.*$', '', bn)
    return bn if bn else None


def state_path_for(paper_name: str, workspace: str = ".") -> str:
    """生成状态文件路径"""
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', paper_name)
    return os.path.join(workspace, f"{safe_name}_任务状态.json")


def load_state(paper_name: str, workspace: str = ".") -> Optional[Dict[str, Any]]:
    """加载状态文件，不存在返回 None"""
    path = state_path_for(paper_name, workspace)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(state: Dict[str, Any], workspace: str = ".") -> str:
    """保存状态文件，返回文件路径"""
    paper_name = state.get("paper", "unknown")
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    path = state_path_for(paper_name, workspace)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return path


def create_state(
    paper_name: str,
    version: str = "v1.0",
    planned_chapters: Optional[list] = None,
    workspace: str = ".",
) -> Dict[str, Any]:
    """创建初始状态文件"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    state = {
        "paper": paper_name,
        "version": version,
        "phase": "Phase 1",
        "started_at": now,
        "last_updated": now,
        "chapters": {},
        "planned_chapters": planned_chapters or [],
        "next_action": "开始 Phase 1：确认论文基本信息",
        "review_loop": {
            "current_round": 0,
            "max_rounds": 3,
            "p0_fixed": [],
            "p0_pending": [],
        },
    }
    save_state(state, workspace)
    return state


def update_phase(state: Dict[str, Any], phase_name: str) -> Dict[str, Any]:
    """更新当前 Phase"""
    state["phase"] = phase_name
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return state


def update_chapter(
    state: Dict[str, Any],
    chapter_key: str,
    status: str = "completed",
    file_path: Optional[str] = None,
    lines: int = 0,
) -> Dict[str, Any]:
    """更新特定章节的状态"""
    state["chapters"][chapter_key] = {
        "status": status,
        "file": file_path,
        "lines": lines,
    }
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return state


def increment_retry(state: Dict[str, Any], loop_type: str = "review_loop") -> int:
    """增加 Loop 重试计数，返回当前轮次"""
    if loop_type not in state:
        state[loop_type] = {"current_round": 0, "max_rounds": 3}
    state[loop_type]["current_round"] = (
        state[loop_type].get("current_round", 0) + 1
    )
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return state[loop_type]["current_round"]


def is_retry_exceeded(state: Dict[str, Any], loop_type: str = "review_loop") -> bool:
    """检查是否超过最大重试次数"""
    loop = state.get(loop_type, {})
    current = loop.get("current_round", 0)
    max_r = loop.get("max_rounds", 3)
    return current >= max_r


def all_chapters_exist(state: Dict[str, Any]) -> bool:
    """检查所有计划章节是否已完成"""
    planned = state.get("planned_chapters", [])
    if not planned:
        return False
    for ch in planned:
        ch_state = state.get("chapters", {}).get(ch, {})
        if ch_state.get("status") != "completed":
            return False
    return True


def delete_state(paper_name: str, workspace: str = ".") -> bool:
    """删除状态文件"""
    path = state_path_for(paper_name, workspace)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def format_state_summary(state: Dict[str, Any]) -> str:
    """生成状态摘要字符串（用于发送给用户的简短同步）"""
    phase = state.get("phase", "未知")
    chapters = state.get("chapters", {})
    done = sum(1 for c in chapters.values() if c.get("status") == "completed")
    total = len(state.get("planned_chapters", []))
    review = state.get("review_loop", {})
    rnd = review.get("current_round", 0)
    p0 = len(review.get("p0_pending", []))
    return (
        f"[状态] Phase: {phase} | 章节: {done}/{total} | "
        f"审核轮次: {rnd} | P0待修复: {p0} | "
        f"下一步: {state.get('next_action', '待定')}"
    )


def parse_p0_from_report(report_path: str) -> int:
    """从审核报告文件解析 P0 问题数量"""
    import re
    if not os.path.exists(report_path):
        return 0
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 计数 🔴 和 P0 标记
    marks = re.findall(r'🔴|P0', content)
    return len(marks)


def get_phase_number(phase_name: str) -> int:
    """从 Phase 名称提取数值序号（Phase 3.5 → 35）"""
    import re
    m = re.search(r'(\d+(?:\.\d+)?)', phase_name)
    if m:
        return int(float(m.group(1)) * 10)
    return 0


def next_phase_name(current_phase: str) -> str:
    """根据当前 Phase 返回下一个 Phase 的推荐名称"""
    sequence = [
        ("Phase 1", "Phase 1 完成"),
        ("Phase 2", "Phase 2 完成"),
        ("Phase 2.5", "Phase 2.5 确认"),
        ("Phase 3", "Phase 3 完成"),
        ("Phase 3.5", "Phase 3.5 完成"),
        ("Phase 4 修订", "Phase 4 修订 完成"),
        ("Phase 4 整合", "Phase 4 整合 完成"),
        ("Phase 5", "Phase 5 完成"),
        ("Phase 5.2", "Phase 5.2 完成"),
    ]
    for i, (name, done_name) in enumerate(sequence):
        if current_phase == name or current_phase == done_name:
            next_idx = min(i + 1, len(sequence) - 1)
            return sequence[next_idx][0]
    return current_phase


def set_hil_pause(state: Dict[str, Any], message: str) -> Dict[str, Any]:
    """标记状态文件为 HIL 暂停状态"""
    state["hil_paused"] = True
    state["hil_message"] = message
    state["hil_paused_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    state["next_action"] = f"⏸ 等待用户确认: {message}"
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return state


def clear_hil_pause(state: Dict[str, Any]) -> Dict[str, Any]:
    """清除 HIL 暂停状态"""
    state["hil_paused"] = False
    state["hil_message"] = ""
    state["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return state


if __name__ == "__main__":
    # 简单测试
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        state = create_state(
            "测试论文",
            version="v1.0",
            planned_chapters=["chapter1", "chapter2", "chapter3"],
            workspace="/tmp",
        )
        print(f"✨ 已创建: {state_path_for('测试论文', '/tmp')}")
        print(format_state_summary(state))
        delete_state("测试论文", "/tmp")
        print("🧹 已清理")
