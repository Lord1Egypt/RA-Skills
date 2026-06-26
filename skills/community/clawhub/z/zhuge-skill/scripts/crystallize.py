"""
经验结晶 — 入口脚本

调用 core/crystallizer.py 把历史回传记录提炼成晶体。

用法:
    python scripts/crystallize.py            # 结晶
    python scripts/crystallize.py --share    # 结晶 + 推到共享池
"""
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.crystallizer import crystallize
from core.welcome import NEON_CYAN, NEON_GREEN, GOLD, DIM, BOLD, RESET


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="只预览计算结果，不写入 crystals_local.jsonl")
    args = p.parse_args()

    banner = "经验结晶引擎 启动（DRY-RUN）" if args.dry_run else "经验结晶引擎 启动"
    pad = max(50 - len(banner) * 2, 0)
    print(f"\n  {NEON_CYAN}╔═══ {banner} {' ' * pad}═══╗{RESET}")
    print(f"  {NEON_CYAN}║{RESET}")
    crystals = crystallize(verbose=True, write=not args.dry_run)
    if args.dry_run and crystals:
        print(f"\n  {DIM}（以上为预览；如要写入，去掉 --dry-run 重新运行）{RESET}")
    print(f"  {NEON_CYAN}╚{'═' * 50}╝{RESET}\n")


if __name__ == "__main__":
    main()
