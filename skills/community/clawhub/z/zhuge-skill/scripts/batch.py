"""
批量预测 — 一次性处理多场比赛

用法:
    python scripts/batch.py "Napoli vs Lazio" "Inter vs Cagliari" "Roma vs Atalanta"
    python scripts/batch.py --league premier-league "Chelsea vs Manchester United" "Tottenham vs Brighton"
"""
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.predict import predict_match
from core.welcome import NEON_CYAN, NEON_GREEN, NEON_PINK, BOLD, DIM, RESET


def main():
    p = argparse.ArgumentParser()
    p.add_argument("matches", nargs="+", help="比赛列表 'Home vs Away'")
    p.add_argument("--league", default="serie-a")
    args = p.parse_args()

    print(f"\n  {BOLD}{NEON_CYAN}批量推演 {len(args.matches)} 场{RESET}\n")

    results = []
    for i, m in enumerate(args.matches, 1):
        print(f"  {NEON_PINK}━━━ [{i}/{len(args.matches)}] {m} ━━━{RESET}")
        try:
            r = predict_match(m, league=args.league)
            results.append((m, "OK"))
        except Exception as e:
            results.append((m, f"ERR: {e}"))
            print(f"  {DIM}失败: {e}{RESET}")

    print(f"\n  {BOLD}批量推演完成{RESET}")
    for m, s in results:
        print(f"  - {m:50} {s}")
    print()


if __name__ == "__main__":
    main()
