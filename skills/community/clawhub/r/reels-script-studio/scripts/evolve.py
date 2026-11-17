#!/usr/bin/env python3
"""
reels-script-studio 进化助手 / Evolution helper.

用法 / Usage:
  python3 evolve.py record --type "产品种草型" --platform "Seedance" --note "加强第2镜子弹时间"
  python3 evolve.py feedback --text "第3镜摇移更快" --optimization "平滑→快速"
  python3 evolve.py report
  python3 evolve.py stats

功能：将使用经验写入独立的 evolution.json（不修改核心 SKILL.md）。
"""
import argparse
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
EVOLUTION_PATH = os.path.join(HERE, "..", "evolution.json")


def load():
    with open(EVOLUTION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(EVOLUTION_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def bump(data):
    # 进化版本 +0.0.1
    maj, mid, min_ = data["evolution_version"].split(".")
    data["evolution_version"] = f"{maj}.{mid}.{int(min_) + 1}"
    data["last_updated"] = date.today().isoformat()


def record(data, stype=None, platform=None, note=""):
    data["usage_stats"]["total_generations"] += 1
    if stype:
        t = data["usage_stats"]["by_type"]
        t[stype] = t.get(stype, 0) + 1
        data["user_preferences"]["most_used_type"] = max(t, key=t.get)
    if platform:
        p = data["usage_stats"]["by_platform"]
        p[platform] = p.get(platform, 0) + 1
        data["user_preferences"]["most_used_platform"] = max(p, key=p.get)
    if note:
        data["experience_log"].append({
            "timestamp": date.today().isoformat(),
            "type": "使用记录",
            "note": note,
        })
    bump(data)
    save(data)
    print("✅ 已记录使用经验，进化版本 ->", data["evolution_version"])


def feedback(data, text, optimization):
    data["experience_log"].append({
        "timestamp": date.today().isoformat(),
        "type": "用户修改反馈",
        "original": text,
        "optimization": optimization,
        "applied": True,
    })
    bump(data)
    save(data)
    print("✅ 已记录反馈优化：", optimization)


def report(data):
    s = data["usage_stats"]
    print(f"🎯 进化报告 | Skill v{data['skill_version']} | 进化 v{data['evolution_version']}")
    print(f"累计生成：{s['total_generations']} 次")
    if s["by_type"]:
        top = max(s["by_type"], key=s["by_type"].get)
        print(f"最常用类型：{top}（{s['by_type'][top]} 次）")
    if s["by_platform"]:
        top = max(s["by_platform"], key=s["by_platform"].get)
        print(f"最常用平台：{top}（{s['by_platform'][top]} 次）")
    print(f"经验日志：{len(data['experience_log'])} 条 | 已回滚：{len(data['rejected_optimizations'])} 条")


def stats(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("record"); pr.add_argument("--type"); pr.add_argument("--platform"); pr.add_argument("--note", default="")
    pf = sub.add_parser("feedback"); pf.add_argument("--text", required=True); pf.add_argument("--optimization", required=True)
    sub.add_parser("report")
    sub.add_parser("stats")
    args = p.parse_args()
    data = load()
    if args.cmd == "record":
        record(data, args.type, args.platform, args.note)
    elif args.cmd == "feedback":
        feedback(data, args.text, args.optimization)
    elif args.cmd == "report":
        report(data)
    elif args.cmd == "stats":
        stats(data)


if __name__ == "__main__":
    main()
