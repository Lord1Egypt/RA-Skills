"""
命中率统计 — 历史预测全景分析

输出：
- 总体命中率（1X2 / 大小球 / 比分）
- 按卦象分组的命中率（哪些卦最准）
- 按信心档位分组（高/中/低 信心档的实际命中率）
- 按 6 维爻位的强弱关联性
- 时间趋势（近 7 / 30 / 90 天）

用法:
    python scripts/stats.py
    python scripts/stats.py --days 30
"""
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.welcome import (NEON_CYAN, NEON_PINK, NEON_GREEN, NEON_YELLOW,
                          GOLD, WHITE, HOT_RED as RED, DIM, BOLD, RESET, GRAY)

DB = ROOT / "data" / "experience.jsonl"
SEED = ROOT / "data" / "seed_experience.jsonl"


def load_all() -> list:
    records = []
    for path in [SEED, DB]:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            records.append(json.loads(line))
                        except Exception:
                            pass
    return records


def filter_by_days(records: list, days: int) -> list:
    if days <= 0:
        return records
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    return [r for r in records if r.get("timestamp", 0) > cutoff]


def bar(rate: float, width: int = 20) -> str:
    filled = int(rate * width)
    color = NEON_GREEN if rate >= 0.6 else (NEON_YELLOW if rate >= 0.5 else RED)
    return f"{color}{'█' * filled}{DIM}{'░' * (width - filled)}{RESET}"


def show_stats(days: int = 0):
    records = load_all()
    if days > 0:
        records = filter_by_days(records, days)

    n_total = len(records)
    n_with_result = len([r for r in records if r.get("prediction_correct")])

    print(f"\n  {NEON_CYAN}╔═══ 命中率全景 {' ' * 30}═══╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  数据范围: {('近 ' + str(days) + ' 天') if days > 0 else '全部历史'}")
    print(f"  {NEON_CYAN}║{RESET}  总预测数: {BOLD}{n_total}{RESET}  已回传: {n_with_result}  待回传: {n_total - n_with_result}")
    print(f"  {NEON_CYAN}║{RESET}")

    if n_with_result == 0:
        print(f"  {NEON_CYAN}║{RESET}  {DIM}暂无回传数据。先跑: python scripts/backfill.py{RESET}")
        print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")
        return

    # === 1. 总体命中率 ===
    total_correct = defaultdict(int)
    total_count = defaultdict(int)
    for r in records:
        pc = r.get("prediction_correct")
        if not pc:
            continue
        for k in ["1x2", "total_2_5", "score", "any"]:
            if k in pc:
                total_count[k] += 1
                if pc[k]:
                    total_correct[k] += 1

    print(f"  {NEON_CYAN}║{RESET}  {BOLD}总体命中率{RESET}")
    for k in ["1x2", "total_2_5", "any"]:
        if total_count[k]:
            rate = total_correct[k] / total_count[k]
            print(f"  {NEON_CYAN}║{RESET}    {k:<10} [{bar(rate)}] {rate*100:5.1f}%  ({total_correct[k]}/{total_count[k]})")
    print(f"  {NEON_CYAN}║{RESET}")

    # === 2. 按信心档分组 ===
    by_conf = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in records:
        pc = r.get("prediction_correct")
        conf = r.get("confidence", "未知")
        if pc and "1x2" in pc:
            by_conf[conf]["total"] += 1
            if pc["1x2"]:
                by_conf[conf]["correct"] += 1

    print(f"  {NEON_CYAN}║{RESET}  {BOLD}按信心档（1X2）{RESET}")
    for conf in ["高", "中", "低"]:
        if conf in by_conf and by_conf[conf]["total"]:
            d = by_conf[conf]
            rate = d["correct"] / d["total"]
            print(f"  {NEON_CYAN}║{RESET}    {conf} 信心    [{bar(rate)}] {rate*100:5.1f}%  ({d['correct']}/{d['total']})")
    print(f"  {NEON_CYAN}║{RESET}")

    # === 3. 按卦象分组（命中率最高的 5 卦）===
    by_hex = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in records:
        pc = r.get("prediction_correct")
        if pc and "1x2" in pc:
            name = r.get("hexagram_name", "?")
            by_hex[name]["total"] += 1
            if pc["1x2"]:
                by_hex[name]["correct"] += 1

    print(f"  {NEON_CYAN}║{RESET}  {BOLD}按卦象（命中率前 5）{RESET}")
    sorted_hex = sorted(
        [(n, d) for n, d in by_hex.items() if d["total"] >= 1],
        key=lambda x: -x[1]["correct"] / x[1]["total"]
    )[:5]
    for name, d in sorted_hex:
        rate = d["correct"] / d["total"]
        print(f"  {NEON_CYAN}║{RESET}    {GOLD}{name:<4}{RESET}卦  [{bar(rate)}] {rate*100:5.1f}%  ({d['correct']}/{d['total']})")
    print(f"  {NEON_CYAN}║{RESET}")

    # === 4. 阳爻数 vs 命中率（验证「阳越多越准」假设）===
    by_yang = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in records:
        pc = r.get("prediction_correct")
        if pc and "1x2" in pc:
            yc = r.get("yang_count", -1)
            by_yang[yc]["total"] += 1
            if pc["1x2"]:
                by_yang[yc]["correct"] += 1

    print(f"  {NEON_CYAN}║{RESET}  {BOLD}阳爻数 → 命中率{RESET}")
    for yc in sorted(by_yang.keys()):
        d = by_yang[yc]
        if d["total"] == 0:
            continue
        rate = d["correct"] / d["total"]
        print(f"  {NEON_CYAN}║{RESET}    {yc} 阳    [{bar(rate)}] {rate*100:5.1f}%  ({d['correct']}/{d['total']})")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")


def show_crystals(stale_days: int = 30, limit: int = 20):
    """晶体排行报告：按复用次数降序 + stale 监控（超过 stale_days 没被命中的晶体）"""
    from core.crystallizer import load_crystals
    now = datetime.now(timezone.utc)
    stale_cutoff = now - timedelta(days=stale_days)

    crystals = load_crystals()
    if not crystals:
        print(f"\n  {DIM}还没有晶体。先跑 python scripts/crystallize.py{RESET}\n")
        return

    # 按 recurrence_count 降序，同级按 rate 降序
    crystals.sort(
        key=lambda c: (c.get("recurrence_count", 0), c.get("stats", {}).get("rate", 0)),
        reverse=True,
    )

    def age(iso):
        if not iso:
            return "?"
        try:
            t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
            d = (now - t).days
            return f"{d}d 前" if d > 0 else "今日"
        except Exception:
            return "?"

    def is_stale(c):
        last = c.get("last_seen") or c.get("discovered_at")
        if not last:
            return False
        try:
            t = datetime.fromisoformat(last.replace("Z", "+00:00"))
            if t.tzinfo is None:
                t = t.replace(tzinfo=timezone.utc)
            return t < stale_cutoff and c.get("recurrence_count", 0) == 0
        except Exception:
            return False

    print(f"\n  {NEON_CYAN}╔═══ 晶体排行 ({len(crystals)} 个){' ' * 30}═══╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  {BOLD}ID{RESET}          "
          f"{BOLD}卦象{RESET}   {BOLD}输出{RESET}          "
          f"{BOLD}命中率{RESET}    {BOLD}复用{RESET}    {BOLD}最近{RESET}")
    for c in crystals[:limit]:
        s = c.get("stats", {})
        t = c.get("trigger", {})
        rc = c.get("recurrence_count", 0)
        rate_pct = int(s.get("rate", 0) * 100)
        stale_mark = f" {RED}[stale]{RESET}" if is_stale(c) else ""
        print(f"  {NEON_CYAN}║{RESET}  {c.get('crystal_id','?'):<12} "
              f"{t.get('hexagram','?'):<4} "
              f"{c.get('outcome','?'):<12}  "
              f"{rate_pct:>3}% ({s.get('hits',0)}/{s.get('matches',0)})  "
              f"{rc:>3}   "
              f"{age(c.get('last_seen') or c.get('discovered_at'))}"
              f"{stale_mark}")

    stale_count = sum(1 for c in crystals if is_stale(c))
    active_count = sum(1 for c in crystals if c.get("recurrence_count", 0) > 0)
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  {DIM}活跃晶体（有复用）: {active_count}  "
          f"· stale 晶体（{stale_days}d+ 未命中且 0 复用）: {stale_count}{RESET}")
    print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=0, help="只统计最近 N 天，0=全部")
    p.add_argument("--errors", type=int, nargs="?", const=10, default=0,
                   help="显示最近 N 条错误（默认 10），不跑预测统计")
    p.add_argument("--crystals", action="store_true",
                   help="晶体排行 + stale 监控，不跑预测统计")
    p.add_argument("--stale-days", type=int, default=30,
                   help="晶体 N 天未命中算 stale（默认 30）")
    args = p.parse_args()
    if args.errors:
        from scripts.error_log import summarize_recent
        print(summarize_recent(args.errors))
        return
    if args.crystals:
        show_crystals(stale_days=args.stale_days)
        return
    show_stats(days=args.days)


if __name__ == "__main__":
    main()
