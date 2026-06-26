"""
周报/月报 — 自然语言总结

可选 LLM 生成「孔明月报」古风总结，否则用模板。

用法:
    python scripts/report.py            # 周报（近 7 天）
    python scripts/report.py --days 30  # 月报
    python scripts/report.py --llm      # 用 LLM 生成自然语言总结
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.welcome import (NEON_CYAN, NEON_PINK, NEON_GREEN, GOLD,
                          DIM, BOLD, RESET, NEON_PURPLE)
from core.llm import LLMClient

DB = ROOT / "data" / "experience.jsonl"
SEED = ROOT / "data" / "seed_experience.jsonl"


def load_records():
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


def gen_report(days=7, use_llm=False):
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    records = [r for r in load_records() if r.get("timestamp", 0) > cutoff]
    finished = [r for r in records if r.get("prediction_correct")]

    # 数据汇总
    n_total = len(records)
    n_finished = len(finished)
    correct_1x2 = sum(1 for r in finished if r["prediction_correct"].get("1x2"))
    correct_total = sum(1 for r in finished if r["prediction_correct"].get("total_2_5"))

    # 卦象分布
    hex_count = Counter(r.get("hexagram_name", "?") for r in records)

    # 最准的卦
    by_hex = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in finished:
        n = r.get("hexagram_name", "?")
        by_hex[n]["total"] += 1
        if r["prediction_correct"].get("1x2"):
            by_hex[n]["correct"] += 1
    top_hex = sorted(
        [(n, d) for n, d in by_hex.items() if d["total"] >= 2],
        key=lambda x: -x[1]["correct"] / x[1]["total"]
    )[:3]

    # === 输出 ===
    print(f"\n  {NEON_CYAN}╔═══ 诸葛亮 · 近 {days} 天战报 {' ' * 20}═══╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")
    print(f"  {NEON_CYAN}║{RESET}  期间预测: {BOLD}{n_total}{RESET} 场  (已回传 {n_finished})")
    if n_finished:
        print(f"  {NEON_CYAN}║{RESET}  1X2 命中: {NEON_GREEN}{correct_1x2}/{n_finished}{RESET} ({100*correct_1x2/n_finished:.0f}%)")
        print(f"  {NEON_CYAN}║{RESET}  大小球命中: {NEON_GREEN}{correct_total}/{n_finished}{RESET} ({100*correct_total/n_finished:.0f}%)")
    print(f"  {NEON_CYAN}║{RESET}")

    if hex_count:
        print(f"  {NEON_CYAN}║{RESET}  {BOLD}卦象分布（top 5）{RESET}")
        for name, c in hex_count.most_common(5):
            print(f"  {NEON_CYAN}║{RESET}    {GOLD}{name:<4}{RESET}卦 × {c}")
        print(f"  {NEON_CYAN}║{RESET}")

    if top_hex:
        print(f"  {NEON_CYAN}║{RESET}  {BOLD}本期最准的卦{RESET}")
        for name, d in top_hex:
            rate = d["correct"] / d["total"]
            print(f"  {NEON_CYAN}║{RESET}    {GOLD}{name:<4}{RESET}卦  {NEON_GREEN}{rate*100:.0f}%{RESET}  ({d['correct']}/{d['total']})")

    print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")

    # LLM 自然语言总结（可选）
    if use_llm:
        client = LLMClient()
        if not client.enabled:
            print(f"  {DIM}（LLM 未配置，跳过自然语言总结）{RESET}\n")
            return
        print(f"  {NEON_PURPLE}{BOLD}孔明月报（{client.provider}/{client.model}）{RESET}\n")
        prompt = f"""请扮演诸葛亮，用古风文言（《出师表》风格但允许少量现代词）
为这份近 {days} 天的足球预测战报写一段 150-250 字的总结。
要包含：(1) 表彰胜势 (2) 反思败因 (3) 下阶段策略

数据：
- 预测 {n_total} 场，已结算 {n_finished} 场
- 1X2 命中 {correct_1x2}/{n_finished}
- 卦象分布: {dict(hex_count.most_common(5))}
- 最准卦象: {[(n, d['correct'], d['total']) for n, d in top_hex]}

请直接输出战报正文，不要其他说明。"""
        text = client.chat(prompt, max_tokens=400)
        if text:
            print(f"  {text}\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--llm", action="store_true", help="用 LLM 生成自然语言战报")
    args = p.parse_args()
    gen_report(days=args.days, use_llm=args.llm)


if __name__ == "__main__":
    main()
