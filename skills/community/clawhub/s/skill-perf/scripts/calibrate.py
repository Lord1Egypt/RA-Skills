#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrate.py
------------
管理本机的底噪标定值。每台机器/账号需要独立标定。

用法:
    # 保存标定结果
    python3 calibrate.py save --total 18927

    # 查看当前标定值
    python3 calibrate.py show

    # 计算某个 skill 的底噪估算值
    python3 calibrate.py noise --skill-md ~/.openclaw/skills/html-extractor/SKILL.md
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

SKILL_PERF_DIR       = Path(__file__).parent.parent
CONFIG_FILE          = SKILL_PERF_DIR / "calibration.json"
CALIBRATION_SKILL_MD = SKILL_PERF_DIR.parent / "skill-calibration" / "SKILL.md"
CALIBRATION_MD_TOKENS = 338  # skill-calibration SKILL.md 的 token 数（tiktoken cl100k_base）


def load_config() -> dict:
    """加载完整 calibration.json（包含所有 agent 的标定数据）"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_agent_config(agent: str = "main") -> dict:
    """加载指定 agent 的标定数据，兼容旧版（无 agents 字段）"""
    config = load_config()
    agents = config.get("agents", {})
    if agent in agents:
        return agents[agent]
    # 兼容旧版：main agent 的数据直接存在根层
    if agent == "main" and "calibration_noise" in config:
        return config
    return {}


def save_config(data: dict):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_noise(agent: str = "main") -> int:
    """返回指定 agent 的底噪值，未标定则返回默认值 18000"""
    agent_config = load_agent_config(agent)
    return agent_config.get("calibration_noise", 18000)


def count_tokens(path: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        text = Path(path).read_text(encoding="utf-8")
        return len(enc.encode(text))
    except Exception as e:
        print(f"  警告: 无法计算 token 数（{e}），使用字符数估算")
        text = Path(path).read_text(encoding="utf-8")
        return len(text) // 4


def cmd_save(total_tokens: int, runs: int = 1, agent: str = "main"):
    """保存标定结果（支持 per-agent）"""
    config = load_config()
    noise = total_tokens - CALIBRATION_MD_TOKENS - 6

    # 加载该 agent 的现有数据
    agents = config.get("agents", {})
    # 兼容旧版：main agent 的数据在根层，迁移到 agents.main
    if agent == "main" and "calibration_noise" in config and "main" not in agents:
        agents["main"] = {
            k: v for k, v in config.items()
            if k not in ("agents",)
        }

    agent_data = agents.get(agent, {})
    history = agent_data.get("history", [])
    history.append({
        "total_tokens": total_tokens,
        "noise": noise,
        "calibrated_at": datetime.now().isoformat(),
    })
    # 使用本次标定值作为底噪，历史仅作参考

    agent_data.update({
        "calibration_noise": noise,
        "last_total_tokens": total_tokens,
        "last_noise": noise,
        "calibrated_at": datetime.now().isoformat(),
        "calibration_skill_md_tokens": CALIBRATION_MD_TOKENS,
        "runs_averaged": 1,
        "history": history,
    })
    agents[agent] = agent_data

    # 同时保留顶层字段供旧版兼容（仅 main agent）
    if agent == "main":
        config.update(agent_data)
    config["agents"] = agents
    save_config(config)

    print(f"\n✅ 标定结果已保存 [{agent}]")
    print(f"   本次 totalTokens: {total_tokens:,}")
    print(f"   本次底噪:         {noise:,}")
    print(f"   本次底噪（用于计算）: {noise:,}  ← 将用于 snapshot.py")
    if len(history) > 1:
        recent = history[-5:]
        avg_hist = round(sum(r['noise'] for r in recent) / len(recent))
        print(f"   历史均值（近{len(recent)}次，仅参考）: {avg_hist:,}")
    print(f"   保存位置: {CONFIG_FILE}")


def cmd_show(agent: str = None):
    """显示当前标定值（可指定 agent，不指定则显示所有）"""
    config = load_config()

    def _show_one(name: str, data: dict):
        if not data:
            print(f"\n  [{name}] ⚠️  尚未标定（使用默认底噪 18,000）")
            return
        print(f"\n  [{name}] 📐 标定信息")
        print(f"   底噪（本次）:  {data.get('calibration_noise', '未知'):>8,} tokens")
        print(f"   最近一次:      {data.get('last_total_tokens', '?'):>8,} totalTokens → 底噪 {data.get('last_noise', '?'):,}")
        print(f"   标定时间:      {data.get('calibrated_at', '未知')}")
        print(f"   平均次数:      {data.get('runs_averaged', 1)} 次")
        print(f"   历史记录:")
        for r in data.get("history", [])[-5:]:
            print(f"     {r['calibrated_at'][:16]}  totalTokens={r['total_tokens']:,}  noise={r['noise']:,}")

    if agent:
        _show_one(agent, load_agent_config(agent))
    else:
        # 显示所有已标定的 agent
        agents_data = config.get("agents", {})
        # 兼容旧版：main agent 的数据在根层
        main_data = agents_data.get("main") or (config if "calibration_noise" in config else {})
        if main_data:
            _show_one("main", main_data)
        for name, data in agents_data.items():
            if name != "main":
                _show_one(name, data)


def cmd_noise(skill_md_path: str, agent: str = "main"):
    """计算某个 skill 的底噪估算"""
    base_noise = get_noise(agent)

    skill_tokens = count_tokens(skill_md_path)
    extra = skill_tokens - CALIBRATION_MD_TOKENS
    estimated_noise = base_noise + extra

    print(f"\n📊 底噪估算: {Path(skill_md_path).parent.name}")
    print(f"   skill SKILL.md:     {skill_tokens:>8,} tokens")
    print(f"   calibration SKILL.md:{CALIBRATION_MD_TOKENS:>7,} tokens")
    print(f"   差值:               {extra:>+8,} tokens")
    print(f"   基准底噪（本机）:   {base_noise:>8,} tokens")
    print(f"   ───────────────────────────────────")
    print(f"   估算底噪:           {estimated_noise:>8,} tokens")
    print(f"\n   净消耗 = totalTokens(实测) - {estimated_noise:,}")


def cmd_check(threshold_pct: float = 5.0, max_extra_runs: int = 2, agent: str = "main") -> int:
    """
    自适应标定检查：
    1. 从 sessions.json 读取最新一次 perf-calibration 运行结果
    2. 与历史均值对比，如果偏差 > threshold_pct%，输出警告并返回退出码 2（提示需要重新多标定几次）
    3. 如果在误差范围内，保存并返回 0

    返回值：
      0  正常，底噪已更新
      1  未找到新的标定 session
      2  偏差过大，需要重新标定（调用方可据此决定是否再次触发标定 job）
    """
    # isolated cron jobs 始终写入 main agent 的 sessions.json，所以搜索所有 sessions 文件
    # 用 job id pattern 来匹配：perf-calibration-<agent>-* 或 perf-calibration-test-* (main)
    all_sessions_files = list((SKILL_PERF_DIR.parent.parent / "agents").rglob("sessions.json"))
    # 构建此 agent 的 calibration job 匹配模式
    if agent == "main":
        cal_pattern = "perf-calibration-test-"
    else:
        cal_pattern = f"perf-calibration-{agent}-"

    cal_sessions = []
    for sessions_file in all_sessions_files:
        if not sessions_file.exists():
            continue
        try:
            with open(sessions_file, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        for key, val in data.items():
            if not isinstance(val, dict) or "totalTokens" not in val:
                continue
            if cal_pattern in key and val.get("totalTokens", 0) > 0:
                cal_sessions.append({
                    "key": key,
                    "totalTokens": val["totalTokens"],
                    "updatedAt": val.get("updatedAt", 0),
                })

    if not cal_sessions:
        print("❌ 未找到 perf-calibration session，请先运行标定 Cron job")
        return 1

    cal_sessions.sort(key=lambda x: x["updatedAt"], reverse=True)
    latest = cal_sessions[0]
    new_total = latest["totalTokens"]
    new_noise = new_total - CALIBRATION_MD_TOKENS - 6
    ts = datetime.fromtimestamp(latest["updatedAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S") if latest["updatedAt"] else "?"

    agent_config = load_agent_config(agent)
    history = agent_config.get("history", [])
    avg_noise = agent_config.get("calibration_noise", 0)

    print(f"\n🔍 本次标定结果 [{agent}]")
    print(f"   session:     {latest['key']}")
    print(f"   时间:        {ts}")
    print(f"   totalTokens: {new_total:,}")
    print(f"   底噪:        {new_noise:,}")

    # 如果有历史均值，做偏差检测
    if avg_noise > 0 and history:
        diff = abs(new_noise - avg_noise)
        diff_pct = diff / avg_noise * 100
        print(f"\n📊 偏差分析")
        print(f"   历史均值底噪（近{len(history[-5:])}次）: {avg_noise:,} tokens")
        print(f"   本次底噪:                         {new_noise:,} tokens")
        print(f"   偏差:                             {diff:+,} tokens ({diff_pct:+.1f}%)")
        print(f"   阈值:                             ±{threshold_pct:.0f}%")

        if diff_pct > threshold_pct:
            print(f"\n⚠️  偏差超过阈值 {threshold_pct:.0f}%，底噪可能不稳定！")
            print(f"   建议：再额外运行 {max_extra_runs} 次标定取均值后再测试")
            print(f"   操作：触发 perf-calibration-test-001 再运行 {max_extra_runs} 次")
            # 仍然保存本次结果（会滚入均值计算）
            # 先检查是否重复
            if history and history[-1].get("total_tokens") == new_total:
                print(f"   （本次结果已在历史中，无需重复保存）")
            else:
                cmd_save(new_total, agent=agent)
            return 2  # 偏差过大信号
        else:
            print(f"\n✅ 偏差在阈值内，底噪稳定")
    else:
        print(f"\n📝 首次标定，无历史数据对比")

    # 检查是否重复保存
    if history and history[-1].get("total_tokens") == new_total:
        print(f"⚠️  本次 totalTokens={new_total:,} 与上次相同，已跳过保存（无新运行）")
        return 1

    cmd_save(new_total, agent=agent)
    return 0


def cmd_auto(agent: str = "main"):
    """自动从 sessions.json 读取标定 session 的 totalTokens 并保存"""
    # isolated jobs 始终写入 main sessions.json，统一搜索所有 sessions 文件
    all_sessions_files = list((SKILL_PERF_DIR.parent.parent / "agents").rglob("sessions.json"))
    if agent == "main":
        cal_pattern = "perf-calibration-test-"
    else:
        cal_pattern = f"perf-calibration-{agent}-"

    calibration_sessions = []
    for sessions_file in all_sessions_files:
        if not sessions_file.exists():
            continue
        try:
            with open(sessions_file, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        for key, val in data.items():
            if not isinstance(val, dict) or "totalTokens" not in val:
                continue
            if cal_pattern in key:
                calibration_sessions.append({
                    "key": key,
                    "totalTokens": val.get("totalTokens", 0),
                    "updatedAt": val.get("updatedAt", 0),
                })

    if not calibration_sessions:
        print("❌ 未找到 perf-calibration session，请先运行标定 Cron job")
        return

    # 按 updatedAt 排序，取最新的
    calibration_sessions.sort(key=lambda x: x["updatedAt"], reverse=True)
    latest = calibration_sessions[0]

    agent_config = load_agent_config(agent)
    history = agent_config.get("history", [])

    # 检查是否已经保存过这个值（避免重复）
    if history and history[-1].get("total_tokens") == latest["totalTokens"]:
        ts = datetime.fromtimestamp(latest["updatedAt"] / 1000).strftime("%H:%M:%S")
        print(f"\n⚠️  最新标定 session（{ts}, totalTokens={latest['totalTokens']:,}）已保存，无需重复保存")
        cmd_show(agent)
        return

    ts = datetime.fromtimestamp(latest["updatedAt"] / 1000).strftime("%H:%M:%S")
    print(f"\n🔍 找到标定 session [{agent}]:")
    print(f"   key:         {latest['key']}")
    print(f"   totalTokens: {latest['totalTokens']:,}")
    print(f"   updatedAt:   {ts}")

    cmd_save(latest["totalTokens"], agent=agent)


def main():
    parser = argparse.ArgumentParser(description="管理本机底噪标定值")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # 通用 --agent 参数（所有子命令共享）
    for name in ["save", "show", "noise", "auto", "check"]:
        pass  # 在各子命令里单独添加

    p_save = sub.add_parser("save", help="保存标定结果")
    p_save.add_argument("--total", type=int, required=True,
                        help="Cron isolated session 实测的 totalTokens")
    p_save.add_argument("--agent", default="main", help="Agent 名称（默认 main）")

    p_show = sub.add_parser("show", help="查看当前标定值")
    p_show.add_argument("--agent", default=None, help="Agent 名称（不指定则显示所有）")

    p_noise = sub.add_parser("noise", help="估算某个 skill 的底噪")
    p_noise.add_argument("--skill-md", required=True, help="被测 skill 的 SKILL.md 路径")
    p_noise.add_argument("--agent", default="main", help="Agent 名称（默认 main）")

    p_auto = sub.add_parser("auto", help="自动从 sessions.json 读取标定 session 数据并保存")
    p_auto.add_argument("--agent", default="main", help="Agent 名称（默认 main）")

    p_check = sub.add_parser("check", help="自适应标定检查：读取最新标定结果，偏差过大时返回退出码 2")
    p_check.add_argument("--threshold", type=float, default=5.0, help="偏差阈值（百分比，默认 5）")
    p_check.add_argument("--max-extra-runs", type=int, default=2, help="偏差过大时建议补充的标定次数（默认 2）")
    p_check.add_argument("--agent", default="main", help="Agent 名称（默认 main）")

    args = parser.parse_args()

    if args.cmd == "save":
        cmd_save(args.total, agent=args.agent)
    elif args.cmd == "show":
        cmd_show(getattr(args, 'agent', None))
    elif args.cmd == "noise":
        cmd_noise(args.skill_md, agent=args.agent)
    elif args.cmd == "auto":
        cmd_auto(agent=args.agent)
    elif args.cmd == "check":
        import sys
        sys.exit(cmd_check(args.threshold, args.max_extra_runs, agent=args.agent))


if __name__ == "__main__":
    main()
