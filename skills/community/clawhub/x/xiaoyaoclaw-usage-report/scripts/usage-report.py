#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
usage-report.py — OpenClaw 性能用量查询工具（零依赖，纯标准库）

数据源：OpenClaw session JSONL（state/agents/*/sessions/*.jsonl）
能力：
  - 按 agent / 模型 / 日期 聚合 token（input+output）+ 平均耗时
  - 按工具聚合：调用次数 / 平均耗时 / 失败率 / 总耗时
  - 按任务(session)聚合：起止时间、模型序列、总 token、总耗时
  - skills 使用统计（从 read 工具参数推断 SKILL.md）
  - 支持 --today / --week / --all / --agent / --by-model / --by-tool / --skills / --json

语言：文案默认中文，可按需替换为任意语言（本工具不对使用者语言/地区设限）。
输出范围：只输出聚合统计——不含会话内容原文、不含 session 标识；
          session 级明细（session id / 起止时间）必须显式 --include-sessions 才输出。
成本：本脚本不读取、不计算、不输出任何 cost 字段（token 为通用主指标）。
路径：数据目录默认脱敏显示（仅末两级），完整本机路径需显式 --include-paths。
时间窗：窗口是**硬边界**——选定时间窗（--today / --week，或默认「今天」）后，
        所有维度（agent/模型、工具、技能、每日趋势、任务）都只统计窗口内的事件，
        窗口外的历史数据**不参与任何聚合**；全历史必须显式 --all。

统计口径（重要）：
  - 真实 token 消耗 = input + output（totalTokens 含 cacheRead 会在每轮重复计数，禁用）
  - 工具耗时 = toolResult.timestamp - 对应 toolCall 所在 assistant message.timestamp
  - 任务耗时 = session 内最后一条消息.timestamp - 第一条用户消息.timestamp
"""

import argparse
import glob
import io
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 数据目录解析顺序（与 --state 帮助、SKILL.md、README 口径一致）：
#   1) --state <路径>   2) OPENCLAW_STATE 环境变量   3) 桌面版（小遥Claw）标准路径（下行兜底值）
# 实际使用的目录会打印在报告首部，便于用户核对（不做隐式猜测）。
DEFAULT_STATE = r"C:\Users\Administrator\AppData\Roaming\xiaoyaoclaw-desktop\runtime\openclaw\state"


def parse_ts(ts):
    """解析 ISO 时间戳 -> epoch ms"""
    if isinstance(ts, (int, float)):
        return int(ts)
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except ValueError:
            return None
    return None


def find_session_files(state_dir):
    """扫描所有 agent 的 session jsonl"""
    files = []
    for agent_dir in glob.glob(os.path.join(state_dir, "agents", "*")):
        if not os.path.isdir(agent_dir):
            continue
        agent = os.path.basename(agent_dir)
        for f in glob.glob(os.path.join(agent_dir, "sessions", "*.jsonl")):
            files.append((agent, f))
    return files


def iter_events(agent, path):
    """逐行解析 jsonl，产出 (event, agent)"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                    ev["_agent"] = agent
                    yield ev
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def extract_tool_calls(msg):
    """从 assistant message content 提取 toolCall 列表"""
    calls = []
    content = msg.get("content") or []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "toolCall":
                calls.append(block)
    return calls


def is_skill_read(tool_name, args):
    """判断 read 工具是否读取了技能文件，返回技能名或 None"""
    if tool_name != "read":
        return None
    fp = ""
    if isinstance(args, dict):
        fp = str(args.get("file_path") or args.get("path") or "")
    elif isinstance(args, str):
        fp = args
    norm = fp.replace("\\", "/").lower()
    if "/skills/" in norm and norm.endswith(".md"):
        # 提取 skills/<name>/SKILL.md 或 skills/<name>.md
        parts = norm.split("/skills/")[-1].split("/")
        if parts:
            name = parts[0]
            if name.endswith(".md"):
                name = name[:-3]
            return name
    return None


def analyze(state_dir, args):
    """主分析：返回结构化结果。**所有维度都按时间窗收敛**（窗口即边界）"""
    agents = defaultdict(lambda: defaultdict(lambda: {"tokens_in": 0, "tokens_out": 0,
                                                      "cache_read": 0, "cache_write": 0,
                                                      "calls": 0,
                                                      "total_ms": 0, "max_ms": 0}))
    tools = defaultdict(lambda: {"count": 0, "errors": 0, "total_ms": 0,
                                 "max_ms": 0, "min_ms": None, "agents": set(),
                                 # per_agent：按 agent 拆分的计数，供 --agent 过滤时重新计算，
                                 # 避免把「别的 agent 也在用」的工具/技能的合并计数暴露出去
                                 "per_agent": defaultdict(lambda: {"count": 0, "errors": 0,
                                                                 "total_ms": 0, "max_ms": 0})})
    skills = defaultdict(lambda: {"count": 0, "agents": set(),
                                  "per_agent": defaultdict(lambda: {"count": 0})})
    sessions = []  # (agent, session_id, start, end, models, tokens, tools, msgs)
    daily = defaultdict(lambda: {"tokens_in": 0, "tokens_out": 0, "calls": 0,
                                 "agents": defaultdict(lambda: {"tokens_in": 0, "tokens_out": 0,
                                                                "calls": 0})})

    files = find_session_files(state_dir)
    if not files:
        # 告警里也只给脱敏路径，避免在可分享的输出里泄露本机绝对路径
        print(f"[WARN] 未找到 session 文件: {redact_path(state_dir)}")
        return None

    # 时间窗过滤器：窗口外的事件不进入任何聚合（agent/模型、工具、技能、每日趋势、任务）
    in_scope, _bounds = make_window_filter(args)

    for agent, path in files:
        # 先收集当前 session 的所有事件
        raw_events = list(iter_events(agent, path))
        if not raw_events:
            continue
        # session id 属元数据（不参与统计），从全部事件里取，不受窗口影响
        session_id = None
        for _ev in raw_events:
            if _ev.get("type") == "session":
                session_id = _ev.get("id")
                break
        # 硬边界：先按窗口裁掉窗口外事件，后续所有统计只基于窗口内事件
        events = [ev for ev in raw_events if in_scope(parse_ts(ev.get("timestamp")))]
        if not events:
            continue
        pend_calls = {}  # toolCallId -> (toolName, ts)
        s_start = None
        s_end = None
        s_models = set()
        s_tokens = {"in": 0, "out": 0}
        s_model_ms = 0
        s_tools = set()
        s_msgs = 0
        # 活跃耗时：相邻事件间隔 < 5min 的累计（排除用户思考间隔）
        ev_ts_list = []
        for ev in events:
            t = parse_ts(ev.get("timestamp"))
            if t:
                ev_ts_list.append((t, ev.get("type")))
        active_ms = 0
        for i in range(1, len(ev_ts_list)):
            gap = ev_ts_list[i][0] - ev_ts_list[i - 1][0]
            if 0 < gap < 300000:
                active_ms += gap

        prev_ev_ts = None
        for ev in events:
            etype = ev.get("type")
            ts = parse_ts(ev.get("timestamp"))
            if etype == "session":
                session_id = ev.get("id")
            elif etype == "message":
                msg = ev.get("message") or {}
                role = msg.get("role")
                # 时间基准只用**事件 ts**（已按窗口裁剪）：message.timestamp 可能是批量写入时间，
                # 落在窗口外，会让每日趋势 / 任务耗时越出所选时间窗
                mts = ts or parse_ts(msg.get("timestamp"))
                if mts:
                    if s_start is None or mts < s_start:
                        s_start = mts
                    if s_end is None or mts > s_end:
                        s_end = mts
                s_msgs += 1

                usage = msg.get("usage") or {}
                tin = usage.get("input") or 0
                tout = usage.get("output") or 0
                cr = usage.get("cacheRead") or 0
                cw = usage.get("cacheWrite") or 0

                model = msg.get("model") or "unknown"
                provider = msg.get("provider") or "unknown"

                if role == "assistant":
                    # 模型调用记录（usage 有值才算一次真实调用）
                    if usage:
                        mkey = f"{provider}/{model}"
                        agents[agent][mkey]["tokens_in"] += tin
                        agents[agent][mkey]["tokens_out"] += tout
                        agents[agent][mkey]["cache_read"] += cr
                        agents[agent][mkey]["cache_write"] += cw
                        agents[agent][mkey]["calls"] += 1
                        # 模型耗时估算：本事件 ts − 前一条事件 ts（0 < gap < 10min）。
                        # ⚠️ 不能用 message.timestamp（批量写入时间戳，非推理耗时）。
                        # 语义：assistant 的前一条事件是 user 或 toolResult → 间隔 ≈ 模型接收上下文+生成回复。
                        if prev_ev_ts and ts:
                            llm_dur = ts - prev_ev_ts
                            if 0 < llm_dur < 600000:
                                agents[agent][mkey]["total_ms"] += llm_dur
                                agents[agent][mkey]["max_ms"] = max(agents[agent][mkey]["max_ms"], llm_dur)
                                s_model_ms += llm_dur
                        s_tokens["in"] += tin
                        s_tokens["out"] += tout
                        s_models.add(mkey)
                        daily_key = datetime.fromtimestamp(mts / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
                        daily[daily_key]["tokens_in"] += tin
                        daily[daily_key]["tokens_out"] += tout
                        daily[daily_key]["calls"] += 1
                        daily[daily_key]["agents"][agent]["tokens_in"] += tin
                        daily[daily_key]["agents"][agent]["tokens_out"] += tout
                        daily[daily_key]["agents"][agent]["calls"] += 1

                    # 工具调用发起
                    for tc in extract_tool_calls(msg):
                        tid = tc.get("id")
                        tname = tc.get("name") or "?"
                        pend_calls[tid] = (tname, mts)
                        s_tools.add(tname)

                elif role == "toolResult":
                    tid = ev.get("toolCallId") or msg.get("toolCallId")
                    tname = msg.get("toolName") or "?"
                    is_err = bool(msg.get("isError"))
                    rts = ts or mts   # 同上：只用窗口内的事件时间，避免跨窗耗时
                    s_tools.add(tname)
                    if tid in pend_calls:
                        pname, pts = pend_calls.pop(tid)
                        dur = (rts - pts) if (rts and pts) else 0
                        tools[pname]["count"] += 1
                        tools[pname]["total_ms"] += dur
                        tools[pname]["max_ms"] = max(tools[pname]["max_ms"], dur)
                        tools[pname]["min_ms"] = dur if tools[pname]["min_ms"] is None else min(tools[pname]["min_ms"], dur)
                        tools[pname]["agents"].add(agent)
                        pa = tools[pname]["per_agent"][agent]
                        pa["count"] += 1
                        pa["total_ms"] += dur
                        pa["max_ms"] = max(pa["max_ms"], dur)
                        if is_err:
                            tools[pname]["errors"] += 1
                            pa["errors"] += 1
                    else:
                        # 无配对（如截断）也计数
                        tools[tname]["count"] += 1
                        tools[tname]["agents"].add(agent)
                        pa = tools[tname]["per_agent"][agent]
                        pa["count"] += 1
                        if is_err:
                            tools[tname]["errors"] += 1
                            pa["errors"] += 1

                # 任务耗时窗口：只要 session 有消息就累计
            elif etype == "custom" and ev.get("customType") == "model-snapshot":
                pass
            # 事件顶层 ts 作为序列基准（真实处理时序）
            if ts:
                prev_ev_ts = ts

        # 从 assistant toolCall 补 skills 推断（参数在 arguments 里）
        for ev in events:
            if ev.get("type") == "message":
                msg = ev.get("message") or {}
                if msg.get("role") == "assistant":
                    for tc in extract_tool_calls(msg):
                        sk = is_skill_read(tc.get("name"), tc.get("arguments"))
                        if sk:
                            skills[sk]["count"] += 1
                            skills[sk]["agents"].add(agent)
                            skills[sk]["per_agent"][agent] += 1

        if session_id and s_msgs > 0:
            # 起止时间为**窗口内**首末消息（跨窗口长会话按窗口截断），
            # 保证「任务」维度也不超出所选时间窗
            sessions.append({
                "agent": agent,
                "id": session_id,
                "start": s_start,
                "end": s_end,
                "duration_ms": (s_end - s_start) if (s_start and s_end) else 0,
                "active_ms": active_ms,
                "model_ms": s_model_ms,
                "models": sorted(s_models),
                "tokens": s_tokens["in"] + s_tokens["out"],
                "tools": sorted(s_tools),
                "msgs": s_msgs,
            })

    return {
        "agents": agents,
        "tools": tools,
        "skills": skills,
        "sessions": sessions,
        "daily": daily,
    }


def fmt_ms(ms):
    if ms is None:
        return "-"
    if ms < 1000:
        return f"{ms:.0f}ms"
    if ms < 60000:
        return f"{ms/1000:.1f}s"
    return f"{ms/60000:.1f}m"


def apply_agent_filter(r, agent_name):
    """按 agent 过滤所有维度（agents/tools/skills/sessions/daily）。
    必须在窗口过滤之前、输出之前调用，保证 --agent 对每个维度都生效。

    工具 / 技能维度是**跨 agent 合并**的计数。只把「别的 agent 也在用」的行删掉是不够的
    ——那仍会把别人的次数、耗时和名字一起暴露出去。因此这里按 per_agent 明细
    **重新计算**该 agent 自己的数值，并把 agents 集合收敛为该 agent。"""
    if not agent_name:
        return r
    r = dict(r)
    r["agents"] = {a: mm for a, mm in r["agents"].items() if a == agent_name}

    tools = {}
    for t, d in r["tools"].items():
        pa = (d.get("per_agent") or {}).get(agent_name)
        if not pa:
            continue
        tools[t] = {"count": pa["count"], "errors": pa["errors"],
                    "total_ms": pa["total_ms"], "max_ms": pa["max_ms"],
                    "min_ms": None, "agents": {agent_name}}
    r["tools"] = tools

    skills = {}
    for s, d in r["skills"].items():
        c = (d.get("per_agent") or {}).get(agent_name)
        if not c:
            continue
        skills[s] = {"count": c, "agents": {agent_name}}
    r["skills"] = skills

    r["sessions"] = [s for s in r["sessions"] if s["agent"] == agent_name]
    # daily：只保留该 agent 的每日数据（无数据的天剔除）
    r["daily"] = {k: v for k, v in r["daily"].items() if agent_name in v["agents"]}
    for v in r["daily"].values():
        v["tokens_in"] = v["agents"][agent_name]["tokens_in"]
        v["tokens_out"] = v["agents"][agent_name]["tokens_out"]
        v["calls"] = v["agents"][agent_name]["calls"]
        v["agents"] = {agent_name: v["agents"][agent_name]}
    return r


def window_label(args):
    """时间窗的中文标签（报告首部 / JSON meta 共用）"""
    if getattr(args, "all", False):
        return "全部历史（显式 --all）"
    if getattr(args, "week", False):
        return "近7天"
    return "今天"


def window_bounds(args, now=None):
    """时间窗边界 -> (lo_ms, hi_ms)；--all 返回 None（无边界）。

    窗口是**硬边界**：调用方必须用它过滤每一个维度的数据，
    不能只过滤其中一部分（否则会暴露窗口之外的历史元数据）。
    不传 --today/--week/--all 时默认为「今天」，与 SKILL.md / README 口径一致。
    """
    if getattr(args, "all", False):
        return None
    now = now or datetime.now(timezone.utc)
    hi = int(now.timestamp() * 1000) + 1
    if getattr(args, "week", False):
        return int((now - timedelta(days=7)).timestamp() * 1000), hi
    start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    return int(start.timestamp() * 1000), hi


def make_window_filter(args):
    """返回 (is_in_window, bounds)。--all 时无边界，is_in_window 恒 True。"""
    bounds = window_bounds(args)
    if bounds is None:
        return (lambda ts: True), None
    lo, hi = bounds

    def _ok(ts):
        return bool(ts) and lo <= ts < hi

    return _ok, bounds


def redact_path(p):
    """路径脱敏：默认只保留末两级目录，避免在可分享的输出里暴露本机完整路径。"""
    if not p:
        return "(未指定)"
    parts = [x for x in re.split(r"[\\/]+", str(p).strip()) if x]
    tail = parts[-2:] if len(parts) >= 2 else parts
    return "…/" + "/".join(tail)


def report(r, args):
    out = []

    # 数据在 analyze() 阶段就已按时间窗收敛（窗口 = 硬边界），这里直接使用
    sess = r["sessions"]
    daily = r["daily"]

    out.append("=" * 60)
    out.append("OpenClaw 用量报告")
    out.append(f"时间范围: {window_label(args)} | "
               f"agent 过滤: {args.agent or '全部'} | 会话数(仅计数): {len(sess)}")
    out.append("统计边界: 所有维度（agent/模型、工具、技能、每日趋势、任务）只统计该时间窗内的"
               "事件；窗口外的历史数据不参与任何聚合、不出现在输出中（跨窗口长会话按窗口内部分截断）"
               "。默认时间窗 = 今天；全历史需显式 --all")
    shown = args.state if args.include_paths else redact_path(args.state)
    out.append(f"数据源: {shown} （只读解析 agents/*/sessions/*.jsonl）"
               + ("" if args.include_paths else "；完整路径用 --include-paths"))
    out.append("输出范围: 仅聚合统计（次数/耗时/token/工具/模型/技能名）"
               "——不含会话内容原文、不含 session id；逐会话明细需显式 --include-sessions")
    out.append("=" * 60)

    # 1. 汇总（**事件级聚合**：直接从 agent/模型维度汇总，不用 session 对象，
    #    保证默认输出里不出现任何「按会话」口径的指标）
    tot_in = sum(d["tokens_in"] for mm in r["agents"].values() for d in mm.values())
    tot_out = sum(d["tokens_out"] for mm in r["agents"].values() for d in mm.values())
    tot_calls = sum(d["calls"] for mm in r["agents"].values() for d in mm.values())
    out.append(f"\n📊 总览: {tot_calls:,} 次模型调用 | 总 token(input+output): {tot_in + tot_out:,}"
               f"（输入 {tot_in:,} / 输出 {tot_out:,}）")
    out.append(f"  会话数: {len(sess)}（仅计数；逐会话耗时/token/模型明细需显式 --include-sessions）")
    out.append("  (本技能不做成本估算——脚本不读取、不计算、不输出任何 cost 字段，token 为通用主指标)")

    # 2. 按 agent + 模型
    out.append("\n📦 按 agent / 模型（token=input+output 真实消耗；模型耗时≈本消息ts−前事件ts，cap 10min）:")
    out.append(f"  {'Agent':<10}{'模型':<28}{'调用':>6}{'输入tok':>12}{'输出tok':>12}{'模型总耗时':>12}{'平均':>10}")
    for agent in sorted(r["agents"]):
        for mkey in sorted(r["agents"][agent]):
            d = r["agents"][agent][mkey]
            if mkey.endswith("/delivery-mirror"):
                continue  # 虚拟投递模型，跳过
            avg = d["total_ms"] / d["calls"] if d["calls"] else 0
            out.append(f"  {agent:<10}{mkey:<28}{d['calls']:>6}{d['tokens_in']:>12,}"
                       f"{d['tokens_out']:>12,}{fmt_ms(d['total_ms']):>12}{fmt_ms(avg):>10}")

    # 3. 按工具
    if args.by_tool:
        out.append("\n🔧 按工具（耗时 = toolResult - toolCall）:")
        out.append(f"  {'工具':<22}{'次数':>6}{'失败':>6}{'总耗时':>10}{'平均':>10}{'最慢':>10}")
        for t in sorted(r["tools"], key=lambda x: -r["tools"][x]["total_ms"]):
            d = r["tools"][t]
            avg = d["total_ms"] / d["count"] if d["count"] else 0
            out.append(f"  {t:<22}{d['count']:>6}{d['errors']:>6}{fmt_ms(d['total_ms']):>10}"
                       f"{fmt_ms(avg):>10}{fmt_ms(d['max_ms']):>10}")

    # 4. skills
    if args.skills:
        out.append("\n📚 Skills 使用（从 read 调用推断）:")
        out.append(f"  {'技能':<30}{'读取次数':>8}{'使用 agent':>20}")
        for sk in sorted(r["skills"], key=lambda x: -r["skills"][x]["count"]):
            d = r["skills"][sk]
            out.append(f"  {sk:<30}{d['count']:>8}{','.join(sorted(d['agents'])):>20}")

    # 5. 任务排行（按耗时）
    if args.by_session:
        out.append("\n⏱️ 任务排行（活跃=相邻事件间隔<5min 累计，排除用户思考；模型耗时=事件ts间隔近似，cap 10min）:")
        out.append(f"  {'Agent':<10}{'活跃耗时':>10}{'窗口耗时':>10}{'模型耗时':>10}{'token':>12}{'消息':>6}  模型")
        key = (lambda x: -x["model_ms"]) if args.by_model_time else (lambda x: -x["active_ms"])
        for s in sorted(sess, key=key)[:20]:
            out.append(f"  {s['agent']:<10}{fmt_ms(s['active_ms']):>10}{fmt_ms(s['duration_ms']):>10}"
                       f"{fmt_ms(s['model_ms']):>10}{s['tokens']:>12,}{s['msgs']:>6}  {','.join(s['models'])[:60]}")

    # 6. 每日趋势
    if args.daily:
        out.append("\n📅 每日趋势:")
        out.append(f"  {'日期':<12}{'输入tok':>12}{'输出tok':>12}{'调用':>8}")
        for day in sorted(daily):
            d = daily[day]
            out.append(f"  {day:<12}{d['tokens_in']:>12,}{d['tokens_out']:>12,}{d['calls']:>8}")

    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description="OpenClaw 用量/性能查询（只读、零依赖、纯本地；不做成本估算）",
        epilog="数据目录解析顺序：--state 参数 → OPENCLAW_STATE 环境变量 → 桌面版（小遥Claw）默认路径；"
               "实际使用的目录会脱敏打印在报告首部（完整路径需 --include-paths）。"
               "输出仅聚合统计（不含会话内容原文、默认不含 session id）。"
               "文案默认中文，可按需替换为任意语言。",
    )
    ap.add_argument("--state", default=os.environ.get("OPENCLAW_STATE", DEFAULT_STATE),
                    help="OpenClaw state 目录。解析顺序：本参数 → OPENCLAW_STATE 环境变量 → "
                         "桌面版（小遥Claw）默认路径；未显式指定时使用兜底默认值，"
                         "并在报告首部打印实际使用的目录")
    ap.add_argument("--today", action="store_true",
                    help="仅今天（默认：不给 --today/--week/--all 时即按今天统计）")
    ap.add_argument("--week", action="store_true", help="近 7 天")
    ap.add_argument("--all", action="store_true",
                    help="全部历史（须显式开启；会扫描全部 session 文件并汇总）")
    ap.add_argument("--agent", default=None, help="按 agent 过滤")
    ap.add_argument("--by-tool", action="store_true", help="工具耗时明细")
    ap.add_argument("--skills", action="store_true", help="skills 使用统计")
    # 任务级明细（每条任务的 agent / 耗时 / token / 模型）只有一个开关：--include-sessions。
    # 曾经存在的 --by-session 会被它绕过隐私门，已移除——任务明细 = session 级元数据，
    # 必须由 --include-sessions 显式开启。
    ap.add_argument("--by-model-time", action="store_true", help="任务排行按模型耗时排序")
    ap.add_argument("--daily", action="store_true", help="每日趋势")
    ap.add_argument("--json", action="store_true", help="JSON 输出（默认仅聚合统计）")
    ap.add_argument("--include-paths", action="store_true",
                    help="显示数据目录的完整本机路径（默认脱敏为末两级目录）。"
                         "⚠️ 属本地环境元数据，请勿公开分享")
    ap.add_argument("--include-sessions", action="store_true",
                    help="JSON 中追加 session 级明细（session id / 起止时间 / 模型序列 / 工具集合）。"
                         "⚠️ 属敏感运维元数据，请勿公开分享；默认关闭")
    args = ap.parse_args()

    # 时间窗互斥校验：窗口是硬边界，不允许同时指定多个（避免口径歧义）
    if sum([bool(args.today), bool(args.week), bool(args.all)]) > 1:
        ap.error("--today / --week / --all 只能选一个：时间窗是硬边界，不接受叠加")

    if args.include_paths:
        sys.stderr.write("[WARN] --include-paths：输出将包含本机绝对路径（本地环境元数据），"
                         "请勿公开分享。\n")

    r = analyze(args.state, args)
    if r is None:
        sys.exit(1)

    # 统一按 agent 过滤（对所有维度生效，report 与 JSON 共用）
    r = apply_agent_filter(r, args.agent)

    if args.json:
        # 输出最小化：默认只出聚合统计。session 级明细（session id / 起止时间 / 模型序列）
        # 必须显式 --include-sessions 才输出——该类元数据属敏感运维信息，开启时给出警告。
        bounds = window_bounds(args)
        slim = {
            "meta": {
                "scope": "aggregated+session-level" if args.include_sessions else "aggregated",
                "window": window_label(args),
                "window_scoped": True,
                "window_start": (datetime.fromtimestamp(bounds[0] / 1000, tz=timezone.utc).isoformat()
                                 if bounds else None),
                "window_end": (datetime.fromtimestamp(bounds[1] / 1000, tz=timezone.utc).isoformat()
                               if bounds else None),
                "state_dir": args.state if args.include_paths else redact_path(args.state),
                "paths_included": bool(args.include_paths),
                "sessions_included": bool(args.include_sessions),
                "session_fields": (["agent", "id", "start", "end", "duration_ms", "active_ms",
                                    "model_ms", "models", "tokens", "tools", "msgs"]
                                   if args.include_sessions else []),
                "note": "所有维度只统计所选时间窗内的事件，窗口外的历史数据不参与聚合；"
                        "不含会话内容原文；默认不含 session id / per-session 时间戳，"
                        "也不含本机绝对路径",
            },
            "agents": {a: {m: d for m, d in mm.items()} for a, mm in r["agents"].items()},
            # 逐字段输出：per_agent 明细不对外（会让 --agent 之外的使用者看到别人的分项）
            "tools": {t: {"count": d["count"], "errors": d["errors"],
                          "total_ms": d["total_ms"], "max_ms": d["max_ms"],
                          "min_ms": d.get("min_ms"), "agents": sorted(d["agents"])}
                      for t, d in r["tools"].items()},
            "skills": {k: {"count": v["count"], "agents": sorted(v["agents"])}
                       for k, v in r["skills"].items()},
            "daily": r["daily"],
        }
        if args.include_sessions:
            sys.stderr.write("[WARN] --include-sessions：本次输出包含 session 级标识与时间戳，"
                             "属敏感运维元数据，请勿公开分享。\n")
            slim["sessions"] = r["sessions"]
        print(json.dumps(slim, ensure_ascii=False, indent=1))
    else:
        # 默认全开（含工具明细）
        args.by_tool = args.by_tool or True
        args.skills = args.skills or True
        # 任务级明细（每条任务的 agent / 耗时 / token / 模型）属 session 级元数据，
        # 与 JSON 路径口径一致：**唯一开关是 --include-sessions**，没有旁路
        args.by_session = bool(args.include_sessions)
        args.daily = args.daily or True
        if args.by_session:
            sys.stderr.write("[WARN] --include-sessions：本次输出包含任务级明细"
                             "（agent / 耗时 / token / 模型），属敏感运维元数据，请勿公开分享。\n")
        print(report(r, args))


if __name__ == "__main__":
    main()
