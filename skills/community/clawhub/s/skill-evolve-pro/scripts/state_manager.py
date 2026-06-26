# -*- coding: utf-8 -*-
"""
Phase 1: state_manager.py
skill-evolve-pro 状态管理模块
管理 evolve_state.json 的读写与状态更新
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

STATE_DIR = Path(__file__).parent.parent / "state"


@dataclass
class EvolveState:
    skill_id: str
    version: str
    epoch: int = 1
    round: int = 0
    edit_budget: int = 8
    last_update: Optional[str] = None
    trajectory_stats: dict = None
    edit_history: list = None
    slow_update_region: Optional[str] = None

    def __post_init__(self):
        if self.trajectory_stats is None:
            self.trajectory_stats = {
                "total": 0,
                "hard_success": 0,
                "hard_fail": 0,
                "soft_fail": 0
            }
        if self.edit_history is None:
            self.edit_history = []


def get_state_path(skill_id: str) -> Path:
    """返回 state/<skill_id>.json 路径"""
    return STATE_DIR / f"{skill_id}.json"


def load_state(skill_id: str) -> Optional[EvolveState]:
    """加载指定技能的状态，如果不存在则返回 None"""
    path = get_state_path(skill_id)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return EvolveState(**data)


def save_state(state: EvolveState) -> None:
    """保存状态到 state/<skill_id>.json"""
    STATE_DIR.mkdir(exist_ok=True)
    state.last_update = datetime.now().isoformat()
    path = get_state_path(state.skill_id)
    path.write_text(
        json.dumps(asdict(state), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def init_state(skill_id: str, skill_version: str, edit_budget: int = 8) -> EvolveState:
    """初始化新技能的状态"""
    state = EvolveState(
        skill_id=skill_id,
        version=skill_version,
        epoch=1,
        round=0,
        edit_budget=edit_budget,
        last_update=datetime.now().isoformat(),
        trajectory_stats={
            "total": 0,
            "hard_success": 0,
            "hard_fail": 0,
            "soft_fail": 0
        },
        edit_history=[],
        slow_update_region=None
    )
    save_state(state)
    return state


def bump_round(skill_id: str) -> EvolveState:
    """当前 round +1，返回更新后的状态"""
    state = load_state(skill_id)
    if state is None:
        raise ValueError(f"State for {skill_id} not found")
    state.round += 1
    save_state(state)
    return state


def record_edits(skill_id: str, applied: int, rejected: int, edits: list) -> EvolveState:
    """记录一轮编辑结果"""
    state = load_state(skill_id)
    state.edit_history.append({
        "round": state.round,
        "applied": applied,
        "rejected": rejected,
        "edits": edits,
        "timestamp": datetime.now().isoformat()
    })
    save_state(state)
    return state


def update_trajectory_stats(
    skill_id: str,
    hard_success: int = 0,
    hard_fail: int = 0,
    soft_fail: int = 0
) -> EvolveState:
    """更新轨迹统计"""
    state = load_state(skill_id)
    stats = state.trajectory_stats
    stats["total"] += hard_success + hard_fail + soft_fail
    stats["hard_success"] += hard_success
    stats["hard_fail"] += hard_fail
    stats["soft_fail"] += soft_fail
    save_state(state)
    return state
