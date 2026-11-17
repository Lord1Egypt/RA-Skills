#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chain_gate.py - Chain Gate v1.0.0
调用链门禁系统 — 与 novel-weaver pipeline_gate 同构。
每个规划步骤有前置门禁检查（gate.check）和后置门禁标记（gate.set/gate.block）。
门禁不通过 → HOOK-BLOCK 输出 + exit(1)，不给 AI 选择跳过。

零外部依赖，仅使用 Python 标准库。
跨平台支持 Windows/Linux/macOS。
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DATA_DIR = (Path.home() / ".workbuddy" / "skills" / ".standardization"
            / "skill-sub" / "data")
GATE_FILE = DATA_DIR / "gate_state.json"

# ============================================================
# 门禁定义表
# ============================================================

# 所有门禁及其依赖（前置门禁）
GATE_REGISTRY = {
    # 链规划门禁
    "blueprint_verified": {
        "description": "蓝皮书指纹验证通过",
        "depends_on": [],
        "severity": "HARD",
    },
    "intent_decomposed": {
        "description": "意图拆解完成（至少2个子意图）",
        "depends_on": ["blueprint_verified"],
        "severity": "HARD",
    },
    "steps_searched": {
        "description": "每个子意图至少1个候选步骤",
        "depends_on": ["intent_decomposed"],
        "severity": "HARD",
    },
    "steps_selected": {
        "description": "LLM 从候选中选择并排序步骤",
        "depends_on": ["steps_searched"],
        "severity": "HARD",
    },
    "io_validated": {
        "description": "相邻步骤 I/O 衔接校验完成",
        "depends_on": ["steps_selected"],
        "severity": "HARD",
    },
    "chain_connected": {
        "description": "全链 DAG 连通性验证通过（gap 数 ≤ 步数/2）",
        "depends_on": ["io_validated"],
        "severity": "HARD",
    },
    "chain_saved": {
        "description": "调用链已保存到磁盘",
        "depends_on": ["chain_connected"],
        "severity": "HARD",
    },
    "llm_chain_verified": {
        "description": "LLM 链逻辑验证通过（步骤满足用户意图）",
        "depends_on": ["steps_selected"],
        "severity": "HARD",
    },
    "milestones_set": {
        "description": "LLM 里程碑判断完成",
        "depends_on": ["llm_chain_verified"],
        "severity": "HARD",
    },
    "adhesion_resolved": {
        "description": "所有衔接缺口已补充粘连点方案",
        "depends_on": ["milestones_set"],
        "severity": "HARD",
    },
    # 链执行门禁
    "chain_loaded": {
        "description": "调用链已加载",
        "depends_on": ["chain_saved"],
        "severity": "HARD",
    },
    "execution_planned": {
        "description": "执行计划已生成",
        "depends_on": ["chain_loaded"],
        "severity": "HARD",
    },
    "execution_completed": {
        "description": "所有步骤执行完成",
        "depends_on": ["execution_planned"],
        "severity": "HARD",
    },
}


def _default_state():
    """返回默认门禁状态（全部为 blocked）"""
    now = datetime.now().isoformat()
    gates = {}
    for name, info in GATE_REGISTRY.items():
        gates[name] = {
            "status": "blocked",
            "blocked_at": now,
            "reason": f"门禁 {name} 未启动 ({info['description']})",
            "severity": info["severity"],
        }
    return {
        "version": "1.0",
        "chain_name": "",
        "updated_at": now,
        "gates": gates,
    }


def load_state():
    """加载门禁状态"""
    if not GATE_FILE.exists():
        return _default_state()
    try:
        with open(GATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return _default_state()


def save_state(state):
    """保存门禁状态"""
    state["updated_at"] = datetime.now().isoformat()
    GATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ============================================================
# 核心 API
# ============================================================

def check(gate_name, state=None):
    """检查指定门禁是否可通过。

    规则：
    1. 门禁本身必须是 open 状态
    2. 所有依赖门禁必须是 open 状态
    3. 不通过 → 打印 HOOK-BLOCK 信息并 exit(1)

    返回: True（通过）或不返回（exit）
    """
    if state is None:
        state = load_state()

    if gate_name not in GATE_REGISTRY:
        print(f"[GATE-ERROR] 未知门禁: {gate_name}")
        sys.exit(1)

    gate_info = GATE_REGISTRY[gate_name]
    gate = state["gates"].get(gate_name, {})

    # 检查依赖门禁
    for dep in gate_info["depends_on"]:
        dep_gate = state["gates"].get(dep, {})
        if dep_gate.get("status") != "open":
            reason = dep_gate.get("reason", f"门禁 {dep} 未通过")
            blocked_at = dep_gate.get("blocked_at", "?")
            severity = dep_gate.get("severity", "HARD")
            print(f"HOOK-BLOCK [{severity}]: 门禁 [{gate_name}] 依赖 [{dep}] 未通过")
            print(f"  原因: {reason}")
            print(f"  阻断时间: {blocked_at}")
            print(f"  修复后重试: chain_gate.py set --name {dep} --status open")
            sys.exit(1)

    # 检查门禁自身
    if gate.get("status") != "open":
        reason = gate.get("reason", f"门禁 {gate_name} 未通过")
        blocked_at = gate.get("blocked_at", "?")
        severity = gate.get("severity", "HARD")
        print(f"HOOK-BLOCK [{severity}]: 门禁 [{gate_name}] 未通过")
        print(f"  原因: {reason}")
        print(f"  阻断时间: {blocked_at}")
        print(f"  修复: 请先通过前置步骤并设置: chain_gate.py set --name {gate_name} --status open")
        sys.exit(1)

    return True


def set_gate(gate_name, status="open", reason=None, state=None):
    """设置门禁状态（open 或 blocked）"""
    if state is None:
        state = load_state()

    if gate_name not in GATE_REGISTRY:
        print(f"[GATE-ERROR] 未知门禁: {gate_name}")
        sys.exit(1)

    gate = state["gates"].get(gate_name, {})
    gate_info = GATE_REGISTRY[gate_name]
    gate["status"] = status
    gate["severity"] = gate_info["severity"]

    if status == "blocked":
        gate["blocked_at"] = datetime.now().isoformat()
        gate["reason"] = reason or f"门禁 {gate_name} 被阻断"
    else:
        gate["blocked_at"] = None
        gate["reason"] = None

    state["gates"][gate_name] = gate
    save_state(state)


def block(gate_name, reason, state=None):
    """阻断门禁并退出（快捷方式）"""
    if state is None:
        state = load_state()
    severity = GATE_REGISTRY.get(gate_name, {}).get("severity", "HARD")
    set_gate(gate_name, "blocked", reason, state)
    print(f"HOOK-BLOCK [{severity}]: 门禁 [{gate_name}] 被阻断")
    print(f"  原因: {reason}")
    sys.exit(1)


def reset(state=None):
    """重置所有门禁为 blocked"""
    new_state = _default_state()
    save_state(new_state)
    return new_state


# ============================================================
# CLI
# ============================================================

def cmd_check(args):
    """检查门禁状态"""
    gate_name = args.name
    try:
        check(gate_name)
        print(f"✅ 门禁 [{gate_name}] 通过")
        return 0
    except SystemExit:
        return 1


def cmd_set(args):
    """设置门禁"""
    state = load_state()
    set_gate(args.name, args.status, args.reason, state)
    print(f"✅ 门禁 [{args.name}] → {args.status}")
    return 0


def cmd_status(args):
    """查看全部门禁状态"""
    state = load_state()
    print(f"📋 门禁状态 ({state.get('chain_name', '未命名')})")
    print(f"{'='*55}")
    for name, info in GATE_REGISTRY.items():
        gate = state["gates"].get(name, {})
        status = gate.get("status", "blocked")
        icon = "✅" if status == "open" else "🔴"
        desc = info["description"]
        severity = info["severity"]
        print(f"  {icon} [{severity}] {name:25s} {status:8s} — {desc}")
        if status == "blocked" and gate.get("reason"):
            print(f"      原因: {gate['reason'][:60]}")
    return 0


def cmd_reset(args):
    """重置门禁"""
    reset()
    print("🔄 门禁已重置（全部 blocked）")
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(
        description="Chain Gate v1.0 - 调用链门禁系统",
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")

    p_check = subparsers.add_parser("check", help="检查门禁（不通过则 exit(1)）")
    p_check.add_argument("--name", required=True, help="门禁名称")

    p_set = subparsers.add_parser("set", help="设置门禁状态")
    p_set.add_argument("--name", required=True, help="门禁名称")
    p_set.add_argument("--status", default="open", choices=["open", "blocked"])
    p_set.add_argument("--reason", default=None, help="阻断原因（status=blocked 时必填）")

    subparsers.add_parser("status", help="查看全部门禁状态")
    subparsers.add_parser("reset", help="重置所有门禁")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "check": cmd_check,
        "set": cmd_set,
        "status": cmd_status,
        "reset": cmd_reset,
    }
    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
