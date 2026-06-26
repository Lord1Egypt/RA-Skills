# -*- coding: utf-8 -*-
"""
skill_evolve_state_manager.py
命令行测试入口：验证 state_manager.py 所有函数

用法：
    python skill_evolve_state_manager.py init   <skill_id> [version] [edit_budget]
    python skill_evolve_state_manager.py show   <skill_id>
    python skill_evolve_state_manager.py bump   <skill_id>
    python skill_evolve_state_manager.py record <skill_id> <applied> <rejected>
    python skill_evolve_state_manager.py stats  <skill_id> [hard_success] [hard_fail] [soft_fail]
    python skill_evolve_state_manager.py load   <skill_id>
"""

import sys
import json
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from state_manager import (
    load_state,
    save_state,
    init_state,
    bump_round,
    record_edits,
    update_trajectory_stats,
    STATE_DIR,
    EvolveState,
)


def cmd_init(skill_id: str, version: str = "1.0.0", edit_budget: int = 8):
    """初始化状态"""
    print(f"[INIT] skill_id={skill_id}, version={version}, edit_budget={edit_budget}")
    state = init_state(skill_id, version, edit_budget)
    print(f"[INIT] ✓ 状态已创建")
    print(json.dumps({"skill_id": state.skill_id, "version": state.version, "epoch": state.epoch, "round": state.round}, indent=2))
    return state


def cmd_show(skill_id: str):
    """显示状态"""
    state = load_state(skill_id)
    if state is None:
        print(f"[SHOW] 状态文件 state/{skill_id}.json 不存在")
        return None
    print(f"[SHOW] ✓ 找到状态文件 state/{skill_id}.json")
    # 直接读取原始 JSON 显示
    path = STATE_DIR / f"{skill_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return state


def cmd_bump(skill_id: str):
    """round +1"""
    print(f"[BUMP] skill_id={skill_id}")
    state = bump_round(skill_id)
    print(f"[BUMP] ✓ round: 0 -> {state.round}")
    return state


def cmd_record(skill_id: str, applied: int, rejected: int):
    """记录编辑结果"""
    print(f"[RECORD] skill_id={skill_id}, applied={applied}, rejected={rejected}")
    # 模拟 edits 列表
    edits = [f"edit_{i+1}" for i in range(applied)]
    state = record_edits(skill_id, applied, rejected, edits)
    print(f"[RECORD] ✓ 已追加到 edit_history (共 {len(state.edit_history)} 条记录)")
    return state


def cmd_stats(skill_id: str, hard_success: int = 0, hard_fail: int = 0, soft_fail: int = 0):
    """更新轨迹统计"""
    print(f"[STATS] skill_id={skill_id}, hard_success={hard_success}, hard_fail={hard_fail}, soft_fail={soft_fail}")
    state = update_trajectory_stats(skill_id, hard_success, hard_fail, soft_fail)
    print(f"[STATS] ✓ trajectory_stats: {state.trajectory_stats}")
    return state


def cmd_load(skill_id: str):
    """加载状态（程序化验证）"""
    print(f"[LOAD] skill_id={skill_id}")
    state = load_state(skill_id)
    if state is None:
        print(f"[LOAD] ✗ 状态不存在")
        return None
    print(f"[LOAD] ✓ 加载成功")
    print(f"  skill_id: {state.skill_id}")
    print(f"  version: {state.version}")
    print(f"  epoch: {state.epoch}")
    print(f"  round: {state.round}")
    print(f"  edit_budget: {state.edit_budget}")
    print(f"  last_update: {state.last_update}")
    print(f"  trajectory_stats: {state.trajectory_stats}")
    print(f"  edit_history: {len(state.edit_history)} 条")
    print(f"  slow_update_region: {state.slow_update_region}")
    return state


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("示例：")
        print("  python skill_evolve_state_manager.py init   robot-evolve 3.0.3 8")
        print("  python skill_evolve_state_manager.py show   robot-evolve")
        print("  python skill_evolve_state_manager.py bump   robot-evolve")
        print("  python skill_evolve_state_manager.py record robot-evolve 3 1")
        print("  python skill_evolve_state_manager.py stats  robot-evolve 1 0 0")
        print("  python skill_evolve_state_manager.py load   robot-evolve")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    skill_id = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "init":
        version = sys.argv[3] if len(sys.argv) > 3 else "1.0.0"
        edit_budget = int(sys.argv[4]) if len(sys.argv) > 4 else 8
        cmd_init(skill_id or "robot-evolve", version, edit_budget)

    elif cmd == "show":
        if not skill_id:
            print("[ERROR] 请提供 skill_id"); sys.exit(1)
        cmd_show(skill_id)

    elif cmd == "bump":
        if not skill_id:
            print("[ERROR] 请提供 skill_id"); sys.exit(1)
        cmd_bump(skill_id)

    elif cmd == "record":
        if not skill_id:
            print("[ERROR] 请提供 skill_id"); sys.exit(1)
        applied = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        rejected = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        cmd_record(skill_id, applied, rejected)

    elif cmd == "stats":
        if not skill_id:
            print("[ERROR] 请提供 skill_id"); sys.exit(1)
        hard_success = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        hard_fail = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        soft_fail = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        cmd_stats(skill_id, hard_success, hard_fail, soft_fail)

    elif cmd == "load":
        if not skill_id:
            print("[ERROR] 请提供 skill_id"); sys.exit(1)
        cmd_load(skill_id)

    else:
        print(f"[ERROR] 未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
