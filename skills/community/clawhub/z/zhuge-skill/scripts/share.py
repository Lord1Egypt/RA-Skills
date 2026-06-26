"""
导出预测组合 — 生成可分享的 Markdown / JSON

用法:
    python scripts/share.py                    # 导出今日所有未结算预测
    python scripts/share.py --hits             # 只导出命中的（炫战绩）
    python scripts/share.py --format json      # 导出 JSON
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.welcome import (NEON_CYAN, NEON_GREEN, GOLD, DIM, BOLD, RESET)

DB = ROOT / "data" / "experience.jsonl"
SEED = ROOT / "data" / "seed_experience.jsonl"
EXPORT = ROOT / "exports"


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


def export(filter_hits=False, fmt="md"):
    records = load_records()
    if filter_hits:
        records = [r for r in records
                   if r.get("prediction_correct", {}).get("1x2") is True]

    EXPORT.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    if fmt == "json":
        out = EXPORT / f"predictions_{ts}.json"
        out.write_text(json.dumps(records, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    else:
        out = EXPORT / f"predictions_{ts}.md"
        lines = [
            "# 诸葛亮预测战报",
            f"生成时间: {datetime.now().isoformat()}",
            f"记录数: {len(records)}",
            "",
            "| 比赛 | 卦象 | 阳爻 | 1X2 | 大小球 | 信心 | 实际 | 命中 |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for r in records:
            pred = r.get("predictions", {})
            actual = r.get("actual_result")
            actual_str = f"{actual['home_goals']}-{actual['away_goals']}" if actual else "?"
            correct = r.get("prediction_correct") or {}
            mark = "✓" if correct.get("1x2") else ("✗" if correct.get("1x2") is False else "?")
            lines.append(
                f"| {r.get('match','?')} | {r.get('hexagram_name','?')} | "
                f"{r.get('yang_count','?')}/6 | {pred.get('1x2','?')} | "
                f"{pred.get('total_2_5','?')} | {r.get('confidence','?')} | "
                f"{actual_str} | {mark} |"
            )
        out.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n  {NEON_GREEN}✓{RESET} 导出完成: {out}")
    print(f"  {DIM}共 {len(records)} 条记录{RESET}\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hits", action="store_true", help="只导出命中预测")
    p.add_argument("--format", choices=["md", "json"], default="md")
    args = p.parse_args()
    export(filter_hits=args.hits, fmt=args.format)


if __name__ == "__main__":
    main()
