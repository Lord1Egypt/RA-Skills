# -*- coding: utf-8 -*-
"""检测 openclaw.json 多 agent 协作配置，输出状态报告。

用法:
    python check_config.py [--config PATH] [--json]

说明:
    - 定位 openclaw.json：--config 指定 > OPENCLAW_CONFIG_PATH 环境变量 > 默认路径
    - 检查项：
        1. agents.list 存在且含哪些 agent
        2. tools.agentToAgent.enabled
        3. tools.sessions.visibility（跨 agent 需要 "all"）
        4. tools.agentToAgent.allow（双向：发送方 + 接收方都在内）
    - 输出分级状态（[OK]/[WARN]/[FAIL]）+ 修复建议
    - 零外部依赖，Windows / macOS 双平台通用（纯 Python 标准库）
    - 只读检查，不修改任何配置

示例:
    python check_config.py                          # 默认路径检测
    python check_config.py --config openclaw.json   # 指定路径
    python check_config.py --json                   # JSON 输出（供脚本消费）
"""
import argparse
import json
import os
import sys

DEFAULT_PATHS = [
    # 原生 OpenClaw
    os.path.expanduser("~/.openclaw/openclaw.json"),
    # 小遥Claw 桌面版（Windows / macOS）
    os.path.join(os.environ.get("APPDATA", ""), "xiaoyaoclaw-desktop",
                 "runtime", "openclaw", "state", "openclaw.json"),
    os.path.expanduser("~/Library/Application Support/xiaoyaoclaw-desktop/"
                       "runtime/openclaw/state/openclaw.json"),
]


def locate_config(explicit):
    """定位 openclaw.json，返回路径或 None。"""
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    env = os.environ.get("OPENCLAW_CONFIG_PATH")
    if env and os.path.isfile(env):
        return env
    for p in DEFAULT_PATHS:
        if os.path.isfile(p):
            return p
    return None


def load_config(path):
    """加载 openclaw.json。兼容 JSON5 常见写法（剥离注释/尾逗号后解析）。"""
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read()
    # 尝试标准 JSON
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # 轻量 JSON5 兼容：剥离 // 与 /* */ 注释、尾逗号
    import re
    s = re.sub(r"//[^\n]*", "", raw)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r",\s*([}\]])", r"\1", s)
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        return {"__parse_error__": str(e), "__raw__": raw}


def check_allow(allow_raw, sender, receiver):
    """校验 agentToAgent.allow 是否能真正覆盖「发送方 → 接收方」。

    为什么不能只数条目：allow 里有两个**互不相关**的 agent，条目数照样 ≥2，
    但本次要发消息的 sender/receiver 可能一个都不在里面 —— 计数式检查会给出
    虚假的"授权通过"。这里按**实际匹配语义**逐个核对：
      - 类型校验：must be list[str]，非字符串/空串 → FAIL
      - 匹配：精确匹配 agent id；`*` 视为通配（与 OpenClaw 一致的全放开写法）
      - 未指定 sender/receiver → 报 UNVERIFIED（无法验证，不冒充 OK）
      - 重复条目 → WARN（配置卫生问题，不影响判定）
    """
    def _fail(msg):
        return "FAIL", msg

    if allow_raw is None:
        return _fail("allow 缺失 —— 需列为 [发送方, 接收方]（或 [\"*\"]）")
    if not isinstance(allow_raw, list):
        return _fail(f"allow 类型错误（{type(allow_raw).__name__}）—— 必须是字符串数组")

    bad = [x for x in allow_raw if not isinstance(x, str) or not x.strip()]
    if bad:
        return _fail(f"allow 含非法条目（{bad!r}）—— 每条都必须是非空字符串")

    entries = [x.strip() for x in allow_raw]
    dups = sorted({e for e in entries if entries.count(e) > 1})
    wildcard = "*" in entries

    def allowed(agent_id):
        return wildcard or agent_id in entries

    if not sender or not receiver:
        hint = "；".join(filter(None, [
            "缺 --sender" if not sender else "",
            "缺 --receiver" if not receiver else "",
        ]))
        return ("UNVERIFIED",
                f"已配置 {len(entries)} 条（{', '.join(entries)}）；{hint} —— "
                f"未指定两端就无法验证双向授权，请用 --sender/--receiver 指定后再判")

    missing = [a for a in (sender, receiver) if not allowed(a)]
    if missing:
        return _fail(
            f"{sender} → {receiver} 未授权：{', '.join(missing)} 不在 allow 中"
            f"（现有 {', '.join(entries) or '空'}）"
        )

    detail = f"{sender} → {receiver} 双向已授权（{'通配 *' if wildcard else '精确匹配'}）"
    if sender == receiver:
        detail += "；⚠️ 发送方与接收方相同，跨 agent 场景请确认不是笔误"
    if dups:
        return "WARN", detail + f"；⚠️ allow 有重复条目：{', '.join(dups)}"
    return "OK", detail


def main():
    ap = argparse.ArgumentParser(description="OpenClaw multi-agent config checker")
    ap.add_argument("--config", help="openclaw.json 路径（默认自动定位）")
    ap.add_argument("--sender", help="发送方 agent id（用于双向授权校验）")
    ap.add_argument("--receiver", help="接收方 agent id（用于双向授权校验）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    path = locate_config(args.config)
    if not path:
        msg = {"ok": False, "error": "openclaw.json not found",
               "hint": "use --config PATH or set OPENCLAW_CONFIG_PATH"}
        print(json.dumps(msg, ensure_ascii=False) if args.json else
              "[FAIL] openclaw.json not found (use --config PATH or set OPENCLAW_CONFIG_PATH)")
        sys.exit(1)

    cfg = load_config(path)
    if "__parse_error__" in cfg:
        msg = {"ok": False, "error": "parse failed: " + cfg["__parse_error__"]}
        print(json.dumps(msg, ensure_ascii=False) if args.json else
              "[FAIL] openclaw.json parse failed: " + cfg["__parse_error__"])
        sys.exit(1)

    agents = cfg.get("agents", {}).get("list", []) or []
    tools = cfg.get("tools", {}) or {}
    a2a = tools.get("agentToAgent", {}) or {}
    sessions = tools.get("sessions", {}) or {}

    agent_ids = [a.get("id") for a in agents if isinstance(a, dict) and a.get("id")]
    visibility = sessions.get("visibility", "tree")
    a2a_enabled = a2a.get("enabled", False)
    allow = a2a.get("allow", []) or []

    checks = []
    # 1. agents.list
    if agent_ids:
        checks.append(("agents.list", "OK", "agents: " + ", ".join(agent_ids)))
    else:
        checks.append(("agents.list", "FAIL", "empty — no agents configured"))

    # 2. agentToAgent.enabled
    if a2a_enabled:
        checks.append(("agentToAgent.enabled", "OK", "true"))
    else:
        checks.append(("agentToAgent.enabled", "FAIL", "false — set tools.agentToAgent.enabled=true"))

    # 3. sessions.visibility
    if visibility == "all":
        checks.append(("sessions.visibility", "OK", "all"))
    elif visibility in ("agent", "tree", "self"):
        checks.append(("sessions.visibility", "WARN",
                       f'"{visibility}" — cross-agent needs "all"'))
    else:
        checks.append(("sessions.visibility", "WARN", f'unknown "{visibility}" — cross-agent needs "all"'))

    # 4. allow 双向（按实际匹配语义校验，不是数条目）
    if a2a_enabled:
        allow_status, allow_detail = check_allow(a2a.get("allow"), args.sender, args.receiver)
        checks.append(("agentToAgent.allow", allow_status, allow_detail))
    else:
        checks.append(("agentToAgent.allow", "SKIP", "agentToAgent not enabled"))

    hard_fail = any(c[1] == "FAIL" for c in checks)
    soft = any(c[1] in ("WARN", "UNVERIFIED") for c in checks)
    overall = "FAIL" if hard_fail else ("WARN" if soft else "OK")

    if args.json:
        print(json.dumps({
            "config": path, "overall": overall,
            "agents": agent_ids, "visibility": visibility,
            "agentToAgentEnabled": a2a_enabled, "allow": allow,
            "sender": args.sender, "receiver": args.receiver,
            "checks": [{"name": n, "status": s, "detail": d} for n, s, d in checks],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"config: {path}")
        print(f"overall: [{overall}]")
        for name, status, detail in checks:
            print(f"  [{status:4s}] {name}: {detail}")

    sys.exit(0 if overall == "OK" else 2 if overall == "FAIL" else 1)


if __name__ == "__main__":
    main()
