#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hook_runner.py — 流程钩子执行器
强制执行 universal-file-ops 技能的三阶段流水线（A → A.1 → B/C），
每个钩子执行后写入状态文件，下一个钩子执行前检查前置是否完成。
不依赖 LLM 自觉，状态文件即是证据。

钩子 ID 格式：H-{阶段}{序号} (H-A01, H-A11, H-B01, H-C01, ...)
状态文件：{技能数据目录}/hooks/state.json
"""

import argparse
import json
import os
import sys
import datetime

# ── 常量 ─────────────────────────────────────────────────────────────
DEFAULT_DATA_DIR_RAW = "skills/.standardization/universal-file-ops/data/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
_data_dir_abs = os.path.normpath(os.path.join(SKILL_ROOT, "..", DEFAULT_DATA_DIR_RAW))
HOOKS_DIR = os.path.join(_data_dir_abs, "hooks")
STATE_FILE = os.path.join(HOOKS_DIR, "state.json")
MAX_RETRY = 3  # 每钩子最大重试次数

# ── 钩子链定义（强制执行顺序） ─────────────────────────────────────
# 每个钩子：id, 描述, 前置钩子列表
HOOK_CHAIN = [
    # Phase A — 环境准备
    {"id": "H-A01", "name": "detect_python",      "desc": "检测系统已安装的 Python 版本", "prereqs": []},
    {"id": "H-A02", "name": "setup_venv",          "desc": "创建 Python 虚拟环境",        "prereqs": ["H-A01"]},
    {"id": "H-A03", "name": "install_deps",        "desc": "安装所需依赖包",              "prereqs": ["H-A02"]},

    # A.1 — 语义路由
    {"id": "H-A11", "name": "semantic_route",      "desc": "语义分析：走工具箱(B)还是脚本流水线(C)", "prereqs": ["H-A03"]},

    # Phase B — 工具箱（文件 CRUD）
    {"id": "H-B01", "name": "toolbox_read",        "desc": "读取源文件",                 "prereqs": ["H-A11"]},
    {"id": "H-B02", "name": "toolbox_process",     "desc": "LLM 处理/转换数据",          "prereqs": ["H-B01"]},
    {"id": "H-B03", "name": "toolbox_write",       "desc": "原子写入目标文件",           "prereqs": ["H-B02"]},
    {"id": "H-B04", "name": "toolbox_verify",      "desc": "回读验证写入是否成功",       "prereqs": ["H-B03"]},

    # Phase C — 脚本流水线
    {"id": "H-C01", "name": "preload_standards",   "desc": "前置加载 py_standards.md",   "prereqs": ["H-A11"]},
    {"id": "H-C02", "name": "create_req_table",    "desc": "创建需求一览表",            "prereqs": ["H-C01"]},
    {"id": "H-C03", "name": "generate_code",       "desc": "生成代码并写入 .py 文件",    "prereqs": ["H-C02"]},
    {"id": "H-C04", "name": "normalize",           "desc": "规范化修复格式问题",         "prereqs": ["H-C03"]},
    {"id": "H-C05", "name": "review",              "desc": "代码审查",                  "prereqs": ["H-C04"]},
    {"id": "H-C06", "name": "oo_ify",              "desc": "OO 化建议（可选）",          "prereqs": ["H-C05"]},
    {"id": "H-C07", "name": "gen_test",            "desc": "生成 pytest 测试",           "prereqs": ["H-C06"]},
    {"id": "H-C08", "name": "sandbox_test",        "desc": "沙箱执行测试",              "prereqs": ["H-C07"]},
    {"id": "H-C09", "name": "fix_loop",            "desc": "修复循环（失败时嵌套 C9.1-C9.4）", "prereqs": ["H-C08"]},
    {"id": "H-C10", "name": "output_report",       "desc": "输出结构化终版报告",         "prereqs": ["H-A11"]},
]

# 子钩子（嵌套在修复循环中）
SUB_HOOKS = {
    "H-C09": [
        {"id": "H-C09.1", "name": "analyze_failure",     "desc": "分析失败原因"},
        {"id": "H-C09.2", "name": "fix_code",            "desc": "修复代码"},
        {"id": "H-C09.3", "name": "rerun_normalize",     "desc": "重新规范化"},
        {"id": "H-C09.4", "name": "rerun_sandbox",       "desc": "重新沙箱执行"},
    ]
}

# ── 路由依赖（B 分支和 C 分支互斥） ──────────────────────────────
ROUTE_TO_B = {"H-B01", "H-B02", "H-B03", "H-B04"}
ROUTE_TO_C = {"H-C01", "H-C02", "H-C03", "H-C04", "H-C05",
               "H-C06", "H-C07", "H-C08", "H-C09", "H-C10"}


def _ensure_dirs():
    os.makedirs(HOOKS_DIR, exist_ok=True)


def _load_state() -> dict:
    """读取钩子状态文件，不存在则返回空 dict"""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state: dict):
    """原子写入状态文件"""
    import tempfile
    _ensure_dirs()
    fd, tmp = tempfile.mkstemp(dir=HOOKS_DIR, prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, STATE_FILE)
    except BaseException:
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


def cmd_check(args):
    """检查指定钩子是否可以执行（前置是否都已完成）"""
    hook_id = args.hook_id
    state = _load_state()

    # 查找钩子定义
    hook_def = None
    for h in HOOK_CHAIN:
        if h["id"] == hook_id:
            hook_def = h
            break
    if not hook_def:
        # 查找子钩子
        for parent, subs in SUB_HOOKS.items():
            for s in subs:
                if s["id"] == hook_id:
                    hook_def = s
                    break

    if not hook_def:
        result = {"hook_id": hook_id, "check": False, "error": f"未知钩子 ID: {hook_id}"}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    prereqs = hook_def.get("prereqs", [])

    # 如果是 C 分支且选了 B 分支 → 冲突
    a11_entry = state.get("H-A11", {})
    a11_route = a11_entry.get("output", {}).get("route") if isinstance(a11_entry, dict) else None
    if hook_id in ROUTE_TO_C and a11_route == "B":
        result = {"hook_id": hook_id, "check": False, "error": "路由冲突: A.1 已指向 B(工具箱), 不能执行 C(脚本流水线)"}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    if hook_id in ROUTE_TO_B and a11_route == "C":
        result = {"hook_id": hook_id, "check": False, "error": "路由冲突: A.1 已指向 C(脚本流水线), 不能执行 B(工具箱)"}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    # 检查前置
    missing = []
    for p in prereqs:
        p_entry = state.get(p, {})
        p_status = p_entry.get("status")
        # H-C10 容忍前置 failed —— 只要路由定了就能出报告
        if hook_id == "H-C10":
            if p_status not in ("done", "failed"):
                missing.append(p)
        else:
            # 非 C10 钩子：前置必须 done（已完成）。failed = 致命错误，阻断链路
            if p_status != "done":
                missing.append(p)
        # 特殊处理：H-C06 依赖 H-C05 但可以跳过
        if hook_id == "H-C06" and p == "H-C05":
            continue

    if missing:
        result = {"hook_id": hook_id, "check": False, "error": f"前置钩子未完成: {', '.join(missing)}"}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    result = {"hook_id": hook_id, "check": True, "message": "前置依赖已满足，可以执行"}
    print(json.dumps(result, ensure_ascii=False))
    return 0


def cmd_fail(args):
    """标记钩子为失败。可后续通过 done 重试覆盖。"""
    hook_id = args.hook_id
    error_data = json.loads(args.error) if args.error else {}
    state = _load_state()

    state[hook_id] = {
        "status": "failed",
        "timestamp": datetime.datetime.now().isoformat(),
        "error": error_data,
        "retry_count": state.get(hook_id, {}).get("retry_count", 0),
    }
    _save_state(state)
    result = {"hook_id": hook_id, "status": "failed", "message": "钩子已标记为失败，修复后可重新 done"}
    print(json.dumps(result, ensure_ascii=False))
    return 0


def cmd_done(args):
    """标记钩子为已完成。支持重试：允许用 done 覆盖之前的 failed 状态。"""
    hook_id = args.hook_id
    output_data = json.loads(args.output) if args.output else {}
    state = _load_state()

    # 判断是否为重试
    previous_status = state.get(hook_id, {}).get("status")
    is_retry = (previous_status == "failed")

    if not is_retry:
        # 首次执行：检查前置
        check_result = cmd_check(args)
        if check_result != 0:
            return check_result

    retry_count = state.get(hook_id, {}).get("retry_count", 0)
    if is_retry:
        if retry_count >= MAX_RETRY:
            result = {"hook_id": hook_id, "check": False,
                       "error": f"重试已达上限 {MAX_RETRY} 次，禁止继续重试。用 hook_runner.py check H-C10 输出报告"}
            print(json.dumps(result, ensure_ascii=False))
            return 1
        retry_count += 1

    state[hook_id] = {
        "status": "done",
        "timestamp": datetime.datetime.now().isoformat(),
        "output": output_data,
        "retry_count": retry_count,
    }
    _save_state(state)
    tag = "重试通过" if is_retry else "完成"
    result = {"hook_id": hook_id, "status": "done", "message": f"钩子已{tag}", "retry_count": retry_count}
    print(json.dumps(result, ensure_ascii=False))
    return 0


def cmd_status(args):
    """显示所有钩子的当前状态"""
    state = _load_state()
    rows = []
    for h in HOOK_CHAIN:
        entry = state.get(h["id"], {})
        rows.append({"hook_id": h["id"], "name": h["name"], "desc": h["desc"],
                      "status": entry.get("status", "pending"),
                      "timestamp": entry.get("timestamp", "")})

    output = {"hooks": rows, "phase_summary": {}}

    # 阶段汇总
    phases = {"A": [], "B": [], "C": []}
    for r in rows:
        prefix = r["hook_id"].split("-")[1][0]
        if prefix in phases:
            phases[prefix].append(r)

    for phase, hooks in phases.items():
        done = sum(1 for h in hooks if h["status"] == "done")
        total = len(hooks)
        output["phase_summary"][f"phase_{phase}"] = f"{done}/{total}"

    # 输出路由信息
    route_entry = state.get("H-A11", {})
    output["route"] = route_entry.get("output", {}).get("route", "unknown")

    print(json.dumps(output, ensure_ascii=False))
    return 0


def cmd_reset(args):
    """重置所有钩子状态"""
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    print(json.dumps({"status": "reset", "message": "所有钩子状态已重置"}))


def main():
    parser = argparse.ArgumentParser(description="universal-file-ops 流程钩子执行器")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="检查前置依赖是否满足")
    p_check.add_argument("hook_id", help="钩子 ID (如 H-A01)")

    p_done = sub.add_parser("done", help="标记钩子已完成")
    p_done.add_argument("hook_id", help="钩子 ID (如 H-A01)")
    p_done.add_argument("--output", default="{}", help="附加输出数据 (JSON 字符串)")

    p_fail = sub.add_parser("fail", help="标记钩子失败（不阻塞 H-C10 报告）")
    p_fail.add_argument("hook_id", help="钩子 ID (如 H-C03)")
    p_fail.add_argument("--error", default="{}", help="错误信息 (JSON 字符串)")

    p_status = sub.add_parser("status", help="显示所有钩子状态")
    p_reset = sub.add_parser("reset", help="重置所有钩子状态")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    cmd_map = {
        "check": cmd_check,
        "done": cmd_done,
        "fail": cmd_fail,
        "status": cmd_status,
        "reset": cmd_reset,
    }
    return cmd_map[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
