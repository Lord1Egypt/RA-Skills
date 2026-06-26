#!/usr/bin/env python3
"""
诸葛亮 · AI 推演军师 — 一键启动入口

Usage:
    python start.py                      # 引导式安装+演示
    python start.py demo                 # 跳过引导直接看 demo
    python start.py predict <比赛>        # 直接预测 (需 API key, 否则走 demo)
    python start.py stats                # 历史命中率
"""
import sys
import time
import os
from pathlib import Path

# 添加 core 和 scripts 到 path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.welcome import play_welcome
from core.wizard import run_wizard


# 队名 → 联赛快速查表
LEAGUE_HINTS = {
    "bundesliga": ["leverkusen", "dortmund", "bayern", "leipzig", "frankfurt",
                   "hoffenheim", "augsburg", "wolfsburg", "stuttgart", "bremen",
                   "freiburg", "mainz", "monchengladbach", "union berlin",
                   "st pauli", "st. pauli", "köln", "koln", "heidenheim", "hamburger"],
    "premier-league": ["chelsea", "arsenal", "liverpool", "manchester", "tottenham",
                       "newcastle", "brighton", "fulham", "brentford", "leeds",
                       "bournemouth", "wolves", "wolverhampton", "city", "united"],
    "serie-a": ["napoli", "lazio", "roma", "inter", "milan", "juventus",
                "atalanta", "fiorentina", "torino", "cagliari", "sassuolo",
                "como", "udinese", "parma"],
    "la-liga": ["real madrid", "barcelona", "atletico", "sevilla", "valencia",
                "villarreal", "athletic", "betis", "osasuna", "mallorca"],
    "ligue-1": ["psg", "paris", "marseille", "lyon", "monaco", "lens",
                "lille", "rennes", "nice", "toulouse", "lorient", "angers"],
}


def _guess_league(match: str) -> str:
    """从队名猜联赛（用户没传 --league 时）"""
    m = match.lower()
    for league, teams in LEAGUE_HINTS.items():
        for t in teams:
            if t in m:
                return league
    return "serie-a"  # 兜底


def main():
    args = sys.argv[1:]

    # 跳过欢迎动画的快捷方式
    if args and args[0] in ("--no-anim", "-q", "quiet"):
        args = args[1:]
    else:
        play_welcome(skip_on_keypress=True)

    # 路由命令
    if not args:
        # 默认：跑 wizard
        run_wizard()
    elif args[0] == "demo":
        from scripts.predict import run_demo
        run_demo()
    elif args[0] == "predict":
        from scripts.predict import predict_match
        if len(args) < 2:
            print("\n用法: python start.py predict \"Napoli vs Lazio\" [--league bundesliga]")
            sys.exit(1)
        # 解析 --league 参数（如果有）
        match = args[1]
        league = "serie-a"
        if "--league" in args:
            idx = args.index("--league")
            if idx + 1 < len(args):
                league = args[idx + 1]
        # 自动猜联赛（如果用户没传 --league）
        else:
            league = _guess_league(match)
        # Friendly error if match format wrong (e.g. "Chelsea" without "vs")
        try:
            predict_match(match, league=league)
        except ValueError as e:
            print(f"\n  ⚠ {e}")
            print(f"  示例: python start.py predict \"Chelsea vs Man Utd\"\n")
            sys.exit(1)
    elif args[0] in ("stats", "history"):
        from scripts.stats import show_stats
        show_stats()
    elif args[0] in ("help", "-h", "--help"):
        print(__doc__)
    else:
        print(f"\n未知命令: {args[0]}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  再见 🌙")
        sys.exit(0)
